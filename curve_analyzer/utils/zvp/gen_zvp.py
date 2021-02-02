import operator

from sage.all import ZZ, Integer, PolynomialRing, QuotientRing, EllipticCurve, GF, next_prime

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "**": operator.pow,
    "^": operator.pow
}


def eval_binary_function(f, x, y):
    return [fi(x, y) for fi in f]


class ZVPFinder:
    R = PolynomialRing(ZZ, ('a', 'b', 'x1', 'x2', 'y1', 'y2'), order='invlex')
    a, b, x1, x2, y1, y2 = R.gens()
    Q = QuotientRing(R, R.ideal(y1 ** 2 - x1 ** 3 - a * x1 - b, y2 ** 2 - x2 ** 3 - a * x2 - b),
                     ('aa', 'bb', 'x_1', 'x_2', 'y_1', 'y_2'))
    aa, bb, x_1, x_2, y_1, y_2 = Q.gens()
    E = EllipticCurve(R, [a, b])

    def __init__(self, formula_file, multiple, verbose=False, one_point_dependent=False):
        self.formula_file = formula_file
        self.multiple = multiple
        self.register = {"X1": self.Q(self.x1), "Y1": self.Q(self.y1), "X2": self.Q(self.x2), "Y2": self.Q(self.y2), "Z1": self.Q(1), "Z2": self.Q(1), "a": self.Q(self.a),
                         "b": self.Q(self.b)}
        self.zvp_set = set()
        self.zvp_set = self.fill_register()
        self.zvp_lifted = [x.lift() for x in self.zvp_set if not one_point_dependent
                           or (one_point_dependent and self.depends_on_one_point(x))]
        self.zvp_sorted = sorted(self.zvp_lifted, key=lambda x: len(str(x)))
        self.mult = self.E.multiplication_by_m(multiple)
        self.x2_subst, self.y2_subst = eval_binary_function(self.mult, self.x1, self.y1)
        self.zvp_substited = [x(x2=self.x2_subst, y2=self.y2_subst) for x in self.zvp_sorted]
        self.zvp_numerators = [self.Q(x.numerator()).lift() for x in self.zvp_substited]
        self.zvp_reduced = set()
        for numerator in self.zvp_numerators:
            for f, m in numerator.factor():
                self.add_atomic(f, self.zvp_reduced)
        self.zvp_reduced_lifted = [x.lift() for x in self.zvp_reduced]
        self.zvp_reduced_sorted = sorted(self.zvp_reduced_lifted, key=lambda x: len(str(x)))
        self.zvp_univariate = self.make_conditions_univariate()
        if verbose:
            self.print_zvp_conditions()

    def interpret_symbol(self, symbol):
        if symbol.isdigit():
            return self.Q(symbol)
        else:
            return self.register[symbol]

    def eval_reg_binary(self, expression):
        """Expects a binary operation (or avalue defined earlier)."""
        for op in ops.keys():
            symbols = expression.split(op)
            if len(symbols) == 2:
                symbol1, symbol2 = symbols
                value1 = self.interpret_symbol(symbol1)
                value2 = self.interpret_symbol(symbol2)
                self.add_to_zvp(op, value1, value2)
                if op in ['**', '^'] and not isinstance(value2, int):
                    value2 = int(value2.lift())
                return ops[op](value1, value2)
        # if there was no binary operation
        return self.register[expression]

    def add_atomic(self, value, zvp_set):
        try:
            rad = value.lift().radical()
        except (TypeError, AttributeError):
            try:
                rad = value.radical()
            except AttributeError:
                rad = Integer(value).radical()
        if not isinstance(rad, Integer):
            for f, m in rad.factor():
                if not isinstance(f, Integer) and not isinstance(f, int) and not self.Q(-f) in zvp_set:
                    if self.Q(f) == self.y_1:
                        zvp_set.add(self.Q(self.y1 ** 2))
                    else:
                        zvp_set.add(self.Q(f))

    def add_to_zvp(self, op, value1, value2):
        if op == '*':
            for value in [value1, value2]:
                if not isinstance(value, int):
                    self.add_atomic(value, self.zvp_set)
        elif op in ['**', '^']:
            if not isinstance(value1, int):
                self.add_atomic(value1, self.zvp_set)
        else:
            self.add_atomic(ops[op](value1, value2), self.zvp_set)

    def fill_register(self):
        with open(self.formula_file) as f:
            lines = f.readlines()
            for line in lines:
                formula = line.strip().replace(" ", "")
                lhs, rhs = formula.split('=')
                self.register[lhs] = self.eval_reg_binary(rhs)
        return self.zvp_set

    def print_zvp_conditions(self):
        print("ZVP conditions for general affine points on E: y^2 = x^3 + ax + b:")
        for p in self.zvp_sorted:
            print(p.polynomial(self.x1))

        print("\nBy setting (x2,y2) =", self.multiple, "* (x1,y1), we get:")
        print("x2 =", self.x2_subst)
        print("y2 =", self.y2_subst, "\n")

        print("Thus the ZVP conditions become (after eliminating linear occurences of y1):")
        for p in self.zvp_univariate:
            print(p.polynomial(self.x1))

    def __str__(self):
        return '{self.zvp_reduced_sorted}'.format(self=self)

    def depends_on_one_point(self, p):
        vs = p.variables()
        return (self.x1 not in vs and self.y1 not in vs or self.x2 not in vs and self.y2 not in vs) \
               and (self.x1 in vs or self.x2 in vs or self.y1 in vs or self.y2 in vs)

    def make_conditions_univariate(self):
        """Eliminate y1 from the conditions and return univariate conditions instead (though they are still not
        recognized as univariate until a,b values are substitued in). """
        zvp_univariate = []
        for p in self.zvp_reduced_sorted:
            if self.y1 in p.variables():
                # since the polynomial is at most linear in y1, we can solve for y1 and use the curve equation
                p_wrt_y = p.polynomial(self.y1)
                roots_wrt_y = p_wrt_y.roots(p_wrt_y.base_ring().fraction_field())
                assert len(roots_wrt_y) == 1
                r, _ = roots_wrt_y[0]
                # use the curve equation as a rational function and substitute for y1
                curve_function = (self.y1 ** 2 - self.x1 ** 3 - self.a * self.x1 - self.b) / 1
                p_univariate = self.R(curve_function(y1=r).numerator())
            else:
                p_univariate = p
            zvp_univariate.append(p_univariate)
        return zvp_univariate

    def evaluate_univariate_conditions(self, a, b, q):
        """Evaluates the univariate conditions at a,b and returns a list of those that remain nonconstant or are zero
        (as polynomials over GF(q)). """
        zvp_evaluated_nonconst = []
        for p in self.zvp_univariate:
            p_eval = p(a=a, b=b).univariate_polynomial()
            if not p_eval.is_constant():
                zvp_evaluated_nonconst.append(p_eval)
            elif GF(q)(p_eval) == 0:
                zvp_evaluated_nonconst.append(GF(q)(p_eval))
        return sorted(zvp_evaluated_nonconst)

    def find_points(self, a, b, q, verbose=False):
        """Solves ZVP conditions and finds corresponding curve points. Only works properly for nonzero univariate
        conditions (i.e., y1 should not be present if x1 is). """
        if verbose:
            print("\nFinding ZVPs over finite field with", q, "elements for a =", a, "and b =", b, ":")
        E = EllipticCurve(GF(q), [a, b])
        zero_value_points = []
        zvp_evaluated_nonconst = self.evaluate_univariate_conditions(a, b, q)
        for p in zvp_evaluated_nonconst:
            if p == 0:
                zero_value_points.append("Any point, since a,b already satisfy a ZVP condition")
            else:
                roots_with_multiplicity = p.roots(GF(q))
                if verbose:
                    print("Polynomial:", p, "\nRoots:", roots_with_multiplicity)
                for root, m in roots_with_multiplicity:
                    if E.is_x_coord(root) and E.lift_x(root) not in zero_value_points:
                        zero_value_points.append(E.lift_x(root))
                        if verbose:
                            print("Corresponding curve point:", E.lift_x(root))
        return zero_value_points


def main():
    from curve_analyzer.definitions import EFD_PATH
    from pathlib import Path
    formula_file = Path(EFD_PATH, 'shortw', 'projective', 'addition', 'add-2016-rcb.op3')
    ZVP = ZVPFinder(formula_file, multiple=2, verbose=True)
    q = next_prime(2 ** 256)
    a = 1
    b = 2
    points = ZVP.find_points(a, b, q, verbose=True)
    print(points)


if __name__ == '__main__':
    main()

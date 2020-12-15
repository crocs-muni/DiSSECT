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

    def __init__(self, formula_file, multiple):
        self.formula_file = formula_file
        self.multiple = multiple
        self.register = {"X1": self.x1, "Y1": self.y1, "X2": self.x2, "Y2": self.y2, "Z1": 1, "Z2": 1}
        self.zvp_set = set()
        self.zvp_set = self.fill_register()
        self.zvp_lifted = [x.lift() for x in self.zvp_set]
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

    def interpret_symbol(self, symbol):
        if symbol.isdigit():
            return self.Q(symbol)
        else:
            return self.register[symbol]

    def eval_reg_binary(self, expression):
        """Assumes a binary operation."""
        for op in ops.keys():
            symbols = expression.split(op)
            if len(symbols) == 2:
                symbol1, symbol2 = symbols
                value1 = self.interpret_symbol(symbol1)
                value2 = self.interpret_symbol(symbol2)
                self.add_to_zvp(op, value1, value2)
                return ops[op](value1, value2)

    def add_atomic(self, value, zvp_set):
        try:
            rad = value.lift().radical()
        except (TypeError, AttributeError):
            rad = value.radical()
        if not isinstance(rad, Integer):
            for f, m in rad.factor():
                if not self.Q(-f) in zvp_set:
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

    def print_zero_conditions(self):
        print("ZVP conditions for general affine points on E: y^2 = x^3 + ax + b:")
        for n in self.zvp_sorted:
            print(n)

        print("\nBy setting (x2,y2) =", self.multiple, "* (x1,y1), we get:")
        print("x2 =", self.x2_subst)
        print("y2 =", self.y2_subst, "\n")

        print("Thus the ZVP conditions become:")
        for n in self.zvp_reduced_sorted:
            print(n)

    def __str__(self):
        return '{self.zvp_reduced_sorted}'.format(self=self)

    def find_zvp_roots(self, a, b, q, verbose=False):
        zvp_roots = set()
        for p in self.zvp_reduced_sorted:
            roots_with_multiplicity = p(a=a, b=b).univariate_polynomial().roots(GF(q))
            if verbose:
                print(roots_with_multiplicity)
            for root, m in roots_with_multiplicity:
                zvp_roots.add(root)
        return list(zvp_roots)


def main():
    ZVP = ZVPFinder('addition_formula_1.txt', multiple=3)
    ZVP.print_zero_conditions()
    q = next_prime(2 ** 256)
    a = 1
    b = 2
    print("\nFinding ZVP roots over finite field with", q, "elements for a =", a, "and b =", b, ":")
    roots = ZVP.find_zvp_roots(a, b, q, verbose=True)
    print("\nAll roots found:")
    print(roots)


if __name__ == '__main__':
    main()

import operator

from sage.all import ZZ, Integer, PolynomialRing, QuotientRing, EllipticCurve

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "**": operator.pow,
    "^": operator.pow
}


class ZVPFinder:
    R = PolynomialRing(ZZ, ('a', 'b', 'x1', 'y1', 'x2', 'y2'), order='invlex(4), lex(2)')
    a, b, x1, y1, x2, y2 = R.gens()
    Q = QuotientRing(R, R.ideal(y1 ** 2 - x1 ** 3 - a * x1 - b, y2 ** 2 - x2 ** 3 - a * x2 - b),
                     ('a', 'b', 'x_1', 'y_1', 'x_2', 'y_2'))
    E = EllipticCurve(R, [a, b])

    def __init__(self, formula_file, multiple):
        self.formula_file = formula_file
        self.register = {"X1": self.x1, "Y1": self.y1, "X2": self.x2, "Y2": self.y2, "Z1": 1, "Z2": 1}
        self.zvp_set = set()
        self.zvp_set = self.fill_register()
        self.mult = self.E.multiplication_by_m(multiple)
        self.eval_mult = lambda f, x, y: [fi(x, y) for fi in f]

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

    def add_atomic(self, value):
        try:
            rad = value.lift().radical()
        except (TypeError, AttributeError):
            rad = value.radical()
        if not isinstance(rad, Integer):
            for f, m in rad.factor():
                if not self.Q(-f) in self.zvp_set:
                    self.zvp_set.add(self.Q(f))

    def add_to_zvp(self, op, value1, value2):
        if op == '*':
            for value in [value1, value2]:
                if not isinstance(value, int):
                    self.add_atomic(value)
        elif op in ['**', '^']:
            self.add_atomic(value1)
        else:
            self.add_atomic(ops[op](value1, value2))

    def fill_register(self):
        with open(self.formula_file) as f:
            lines = f.readlines()
            for line in lines:
                formula = line.strip().replace(" ", "")
                lhs, rhs = formula.split('=')
                self.register[lhs] = self.eval_reg_binary(rhs)
        return self.zvp_set

    def print_ZVP_conditions(self):
        zvp_lifted = [x.lift() for x in self.zvp_set]
        zvp_sorted = sorted(zvp_lifted, key=lambda x: len(str(x)))
        print("ZVP conditions for general affine points on E: y^2 = x^3 + ax + b:")
        print(zvp_sorted, "\n")

        x2_subst, y2_subst = self.eval_mult(self.mult, self.x1, self.y1)
        print("By setting (x2,y2) = c*(x1,y1), we get:")
        print("x2 =", x2_subst)
        print("y2 =", y2_subst, "\n")

        print("Thus the ZVP conditions become:")
        zvp_substited = [x(x2=x2_subst, y2=y2_subst) for x in zvp_sorted]
        zvp_numerators = [self.Q(x.numerator()).lift().factor() for x in zvp_substited]
        zvp_reduced = set()
        for factorization in zvp_numerators:
            for f, m in factorization:
                zvp_reduced.add(f)
        for n in zvp_numerators:
            print(n)

        print("")
        for n in zvp_reduced:
            print(n)

    def __str__(self):
        # return 'Intermediate register values:\n{self.register}'.format(self=self)
        return 'ZVP conditions for general points:\n{self.zvp_set}'.format(self=self)


def main():
    ZVP = ZVPFinder('addition_formula_1.txt', 3)
    ZVP.print_ZVP_conditions()


if __name__ == '__main__':
    main()

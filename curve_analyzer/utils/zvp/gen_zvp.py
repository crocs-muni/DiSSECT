import operator

from sage.all import Integer, ZZ, PolynomialRing, QuotientRing

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "**": operator.pow,
    "^": operator.pow
}


def interpret_symbol(register, symbol):
    if symbol.isdigit():
        return Integer(symbol)
    else:
        return register[symbol]

def eval_reg_binary(register, expression, quotient_ring=ZZ):
    """Assumes a binary operation."""
    for op in ops.keys():
        symbols = expression.split(op)
        if len(symbols) == 2:
            symbol1, symbol2 = symbols
            value1 = interpret_symbol(register, symbol1)
            value2 = interpret_symbol(register, symbol2)
            return quotient_ring(ops[op](value1, value2))


def fill_register(register, formula_file, quotient_ring=ZZ):
    with open(formula_file) as f:
        lines = f.readlines()
        for line in lines:
            formula = line.strip().replace(" ", "")
            lhs, rhs = formula.split('=')
            register[lhs] = eval_reg_binary(register, rhs, quotient_ring)


def main():
    R = PolynomialRing(ZZ, ('x1', 'y1', 'x2', 'y2'))
    x1, y1, x2, y2 = R.gens()
    Q = QuotientRing(R, R.ideal(y1 ** 2 - x1 ** 3, y2 ** 2 - x2 ** 3), ('x_1', 'y_1', 'x_2', 'y_2'))
    register = {"X1": x1, "Y1": y1, "X2": x2, "Y2": y2, "Z1": 1, "Z2": 1}
    fill_register(register, formula_file='addition_formula_1.txt', quotient_ring=Q)

    print(register)
    for value in set(register.values()):
        if not isinstance(value, int):
            print(value)


if __name__ == '__main__':
    main()

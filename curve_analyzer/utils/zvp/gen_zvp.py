import operator

from sage.all import ZZ, Integer, PolynomialRing, QuotientRing

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "**": operator.pow,
    "^": operator.pow
}


def interpret_symbol(register, symbol, quotient_ring=ZZ):
    if symbol.isdigit():
        return quotient_ring(symbol)
    else:
        return register[symbol]


def eval_reg_binary(register, expression, zvp_set, quotient_ring=ZZ):
    """Assumes a binary operation."""
    for op in ops.keys():
        symbols = expression.split(op)
        if len(symbols) == 2:
            symbol1, symbol2 = symbols
            value1 = interpret_symbol(register, symbol1, quotient_ring)
            value2 = interpret_symbol(register, symbol2, quotient_ring)
            add_to_zvp(zvp_set, op, value1, value2, quotient_ring)
            return ops[op](value1, value2)


def add_atomic(zvp_set, value, quotient_ring):
    try:
        rad = value.lift().radical()
    except (TypeError, AttributeError):
        rad = value.radical()
    if not isinstance(rad, Integer):
        for f, m in rad.factor():
            zvp_set.add(quotient_ring(f))


def add_to_zvp(zvp_set, op, value1, value2, quotient_ring):
    if op == '*':
        for value in [value1, value2]:
            if not isinstance(value, int):
                add_atomic(zvp_set, value, quotient_ring)
    elif op in ['**', '^']:
        add_atomic(zvp_set, value1, quotient_ring)
    else:
        add_atomic(zvp_set, ops[op](value1, value2), quotient_ring)


def fill_register(register, formula_file, quotient_ring=ZZ):
    zvp_set = set()
    with open(formula_file) as f:
        lines = f.readlines()
        for line in lines:
            formula = line.strip().replace(" ", "")
            lhs, rhs = formula.split('=')
            register[lhs] = eval_reg_binary(register, rhs, zvp_set, quotient_ring)
    return zvp_set


def main():
    R = PolynomialRing(ZZ, ('x1', 'y1', 'x2', 'y2', 'a', 'b'))
    x1, y1, x2, y2, a, b = R.gens()
    Q = QuotientRing(R, R.ideal(y1 ** 2 - x1 ** 3 - a * x1 - b, y2 ** 2 - x2 ** 3 - a * x2 - b),
                     ('x_1', 'y_1', 'x_2', 'y_2', 'a', 'b'))
    register = {"X1": x1, "Y1": y1, "X2": x2, "Y2": y2, "Z1": 1, "Z2": 1}
    zvp_set = fill_register(register, formula_file='addition_formula_1.txt', quotient_ring=Q)
    print("Intermediate values:")
    print(register)
    print("ZVP conditions:")
    zvp_lifted = [x.lift() for x in zvp_set]
    print(sorted(zvp_lifted, key=lambda x: len(str(x))))


if __name__ == '__main__':
    main()

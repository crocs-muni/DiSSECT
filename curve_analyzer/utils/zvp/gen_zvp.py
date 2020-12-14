import operator

from sage.all import ZZ, Integer, PolynomialRing, QuotientRing, EllipticCurve

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
            if not quotient_ring(-f) in zvp_set:
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
    R = PolynomialRing(ZZ, ('a', 'b', 'x1', 'y1', 'x2', 'y2'), order='invlex(4), lex(2)')
    a, b, x1, y1, x2, y2, = R.gens()
    Q = QuotientRing(R, R.ideal(y1 ** 2 - x1 ** 3 - a * x1 - b, y2 ** 2 - x2 ** 3 - a * x2 - b),
                     ('a', 'b', 'x_1', 'y_1', 'x_2', 'y_2'))
    register = {"X1": x1, "Y1": y1, "X2": x2, "Y2": y2, "Z1": 1, "Z2": 1}
    zvp_set = fill_register(register, formula_file='addition_formula_1.txt', quotient_ring=Q)
    print("Intermediate values:")
    print(register)
    print("ZVP conditions for general points:")
    zvp_lifted = [x.lift() for x in zvp_set]
    zvp_sorted = sorted(zvp_lifted, key=lambda x: len(str(x)))
    print(zvp_sorted)

    E = EllipticCurve(R, [a, b])
    mult = E.multiplication_by_m(3)
    eval_mult = lambda f, x, y: [fi(x, y) for fi in f]
    x2_subst, y2_subst = eval_mult(mult, x1, y1)
    # print(x2_subst, y2_subst)
    print("ZVP conditions for (x2,y2) = c*(x1,y1):")
    zvp_substited = [x(x2=x2_subst, y2=y2_subst) for x in zvp_sorted]
    zvp_numerators_lifted = [Q(x.numerator()).lift().factor() for x in zvp_substited]
    # for f in zvp_substited:
    #     print(f)
    #
    # print("nums")
    # for f in zvp_numerators_lifted:
    #     print(f)

    for x in zvp_sorted:
        print(x)
        print(x(x2=x2_subst, y2=y2_subst))
        print(Q(x(x2=x2_subst, y2=y2_subst).numerator()).lift().factor())
        print("")

if __name__ == '__main__':
    main()

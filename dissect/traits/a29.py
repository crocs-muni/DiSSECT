from sage.all import ZZ, QQ, EllipticCurve

from dissect.utils.custom_curve import CustomCurve
from dissect.traits import Trait


class A29(Trait):
    NAME = "a29"
    DESCRIPTION = "Torsion order of the lift of $E$ to $Q$."
    INPUT = {}
    OUTPUT = {
        "Q_torsion": (int, "Q torsion")
    }
    DEFAULT_PARAMS = {}

    def compute(curve: CustomCurve, params):
        """
        Computation of the torsion order of E' where E' is the lift of the given
        curve to Q. By lift, we mean lift of coefficients to ZZ
        """
        try:
            a, b = ZZ(curve.a()), ZZ(curve.b())
        except TypeError:
            a, b = ZZ(curve.params()['a']['raw']), ZZ(curve.params()['b']['raw'])
        except ValueError:
            return {'Q_torsion': None}
        ec = EllipticCurve(QQ, [a, b])
        return {'Q_torsion': ec.torsion_order()}

from .trait import Trait
from .cofactor import CofactorTrait
from .discriminant import DiscriminantTrait
from .twist_order import TwistOrderTrait
from .kn_factorization import KNFactorizationTrait
from .torsion_extension import TorsionExtensionTrait
from .conductor import ConductorTrait
from .embedding import EmbeddingTrait
from .class_number import ClassNumberTrait
from .small_prime_order import SmallPrimeOrderTrait
from .division_polynomials import DivisionPolynomialsTrait
from .volcano import VolcanoTrait
from .isogeny_extension import IsogenyExtensionTrait
from .trace_factorization import TraceFactorizationTrait
from .isogeny_neighbors import IsogenyNeighborsTrait
from .q_torsion import QTorsionTrait
from .hamming_x import HammingXTrait
from .square_4p1 import Square4P1Trait
from .pow_distance import PowDistanceTrait
from .multiples_x import MultiplesXTrait
from .x962_invariant import X962InvariantTrait
from .brainpool_overlap import BrainpoolOverlapTrait
from .weierstrass import WeierstrassTrait

TRAITS = dict(
    map(
        lambda x: (x.NAME, x()),
        [
            CofactorTrait,
            DiscriminantTrait,
            TwistOrderTrait,
            KNFactorizationTrait,
            TorsionExtensionTrait,
            ConductorTrait,
            EmbeddingTrait,
            ClassNumberTrait,
            SmallPrimeOrderTrait,
            DivisionPolynomialsTrait,
            VolcanoTrait,
            IsogenyExtensionTrait,
            TraceFactorizationTrait,
            IsogenyNeighborsTrait,
            QTorsionTrait,
            HammingXTrait,
            Square4P1Trait,
            PowDistanceTrait,
            MultiplesXTrait,
            X962InvariantTrait,
            BrainpoolOverlapTrait,
            WeierstrassTrait,
        ],
    )
)

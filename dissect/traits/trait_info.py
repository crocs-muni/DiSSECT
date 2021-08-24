from typing import List
import pathlib
import json
import itertools
from dissect.definitions import TRAIT_PATH

from sage.all import sage_eval


TRAIT_INFO = {}

TRAIT_INFO["a01"] = {
    "description": "The Smith normal form of the group in an extension field, i.e. $(n_1,n_2)$ where $n_1$ divides $n_2$.",
    "motivation": "The group structure is not an isogeny invariant.",
    "input": {
        "r": (int, "Integer $r$")
    },
    "output": {
        "ord1": (int, "Order 1"),
        "ord2": (int, "Order 2")
    }
}

TRAIT_INFO["a02"] = {
    "description": "Factorization of the discriminant of the Frobenius polynomial, i.e. factorization of  $t^2-4p=v^2d_K$, where $t$ is the trace of Frobenius, $v$ is the maximal conductor and $d_K$ is the CM discriminant.",
    "motivation": "A large conductor has interesting implications.",
    "input": {},
    "output": {
        "cm_disc": (int, "CM discriminant"),
        "factorization": (List[int], "Factorization of $D = t^2-4p$"),
        "max_conductor": (int, "Maximal conductor $v$")
    }
}

TRAIT_INFO["a03"] = {
    "description": "Factorization of the quadratic twist cardinality in an extension, i.e. $\\#E(\\mathbb{F}_{p^d})$.",
    "motivation": "Smooth cardinality of a quadratic twist might allow attacks on some implementations.",
    "input": {
        "deg": (int, "Degree of extension")
    },
    "output": {
        "twist_cardinality": (int, "Twist cardinality"),
        "factorization": (List[int], "Factorization of the cardinality")
    }
}

TRAIT_INFO["a04"] = {
    "description": "Factorization of $kn \\pm 1$ where $n$ is the cardinality of the curve.",
    "motivation": "Scalar multiplication by $kn \\pm 1$ is the identity or negation, respectively; it can be seen as a generalization of [https://link.springer.com/content/pdf/10.1007%2F11761679_1.pdf](https://link.springer.com/content/pdf/10.1007%2F11761679_1.pdf).",
    "input": {
        "k": (int, "Integer")
    },
    "output": {
        "(+)factorization": (List[int], "Factorization of $kn + 1$"),
        "(+)largest_factor_bitlen": (int, "Largest factor of $kn + 1$"),
        "(-)factorization": (List[int], "Factorization of $kn - 1$"),
        "(-)largest_factor_bitlen": (int, "Largest factor of $kn - 1$")
    }
}

TRAIT_INFO["a05"] = {
    "description": "Degrees of field extensions containing the least nontrivial $l$-torsion, the full $l$-torsion and their relative degree of extension.",
    "motivation": "Low $k_1, k_2$ might lead to computable pairings.",
    "input": {
        "l": (int, "$l$-torsion")
    },
    "output": {
        "least": (int, "Least"),
        "full": (int, "Full"),
        "relative": (int, "Relative"),
    }
}

TRAIT_INFO["a06"] = {
    "description": "Factorization of ratio of the maximal conductors of CM-field over an extension and over a basefield.",
    "motivation": "The prime factors of the ratio determine for which $l$ does the $l$-crater of the curve grows in the given extension.",
    "input": {
        "deg": (int, "Integer")
    },
    "output": {
        "factorization": (List[int], "Factorization"),
        "ratio_sqrt": (int, "Ratio sqrt"),
    }
}

TRAIT_INFO["a07"] = {
    "description": "The complement of the embedding degree, i.e. $(n-1)/e$ where $n$ is the prime-subgroup order and $e$ is the embedding degree.",
    "motivation": "Low embedding degrees might allow the MOV attack.",
    "input": {},
    "output": {
        "embedding_degree_complement": (int, "Embedding degree complement"),
        "complement_bit_length": (int, "Complement bit length")
    }
}

TRAIT_INFO["a08"] = {
    "description": "Upper and lower bound for the class number of the CM-field.",
    "motivation": "The class number is a classical invariant.",
    "input": {},
    "output": {
        "upper": (int, "Upper"),
        "lower": (int, "Lower")
    }
}

TRAIT_INFO["a12"] = {
    "description": "Multiplicative orders of small primes modulo the prime-subgroup order.",
    "motivation": "Small orders might have implications for scalar multiplication.",
    "input": {
        "l": (int, "Small prime")
    },
    "output": {
        "order": (int, "Order"),
        "complement_bit_length": (int, "Complement bit length")
    }
}

TRAIT_INFO["a22"] = {
    "description": "Factorizations of small division polynomials.",
    "motivation": "This is partially relevant to a05.",
    "input": {
        "l": (int, "Prime")
    },
    "output": {
        "factorization": (List[List[int]], "Factorization of $l$-th division polynomial"),
        "len": (int, "Length")
    }
}

TRAIT_INFO["a23"] = {
    "description": "Volcano depth and crater degree of the $l$-isogeny graph.",
    "motivation": "The volcano structure might be relevant for cryptanalysis.",
    "input": {
        "l": (int, "Prime")
    },
    "output": {
        "crater_degree": (int, "Crater degree"),
        "depth": (int, "Depth")
    }
}

TRAIT_INFO["a24"] = {
    "description": "The least field extensions containing a nontrivial number and full number of $l$-isogenies and their relative ratio.",
    "motivation": "This is loosely related to a05 and a06.",
    "input": {
        "l": (int, "Prime")
    },
    "output": {
        "least": (int, "Least"),
        "full": (int, "Full"),
        "relative": (int, "Relative")
    }
}

TRAIT_INFO["a25"] = {
    "description": "Factorization of trace in field extensions.",
    "motivation": "Loosely speaking, this somehow measures the \"extent of supersingularity\" (if we regard it as a spectrum).",
    "input": {
        "deg": (int, "Integer")
    },
    "output": {
        "trace": (int, "Trace"),
        "trace_factorization": (List[int], "Factorization of trace"),
        "number_of_factors": (int, "Number of factors")
    }
}

TRAIT_INFO["i04"] = {
    "description": "Number of points with low Hamming weight of the $x$-coordinate and the expected weight.",
    "motivation": "Might be relevant for faulty RNG.",
    "input": {
        "weight": (int, "Integer")
    },
    "output": {
        "x_coord_count": (int, "X coordinate weight"),
        "expected": (int, "Expected"),
        "ratio": (float, "Ratio")
    }
}

TRAIT_INFO["i06"] = {
    "description": "Square parts of $4q \\pm 1$ and $4n \\pm 1$.",
    "motivation": "Inspired by the [4p-1 paper](https://crocs.fi.muni.cz/public/papers/Secrypt2019).",
    "input": {},
    "output": {
        "p": (int, "p"),
        "order": (int, "Order")
    }
}

TRAIT_INFO["i07"] = {
    "description": "Distance of $n$ from the nearest power of two and multiple of 32/64.",
    "motivation": "The first part is related to scalar multiplication bias when not using rejection sampling, the second is inspired by the paper [Big Numbers - Big Troubles](https://www.usenix.org/conference/usenixsecurity20/presentation/weiser).",
    "input": {},
    "output": {
        "distance": (int, "Distance"),
        "ratio": (float, "Order"),
        "distance 32": (int, "Distance 32"),
        "distance 64": (int, "Distance 64")
    }
}

TRAIT_INFO["i08"] = {
    "description": "Bitlength of the $x$-coordinate of small inverted generator scalar multiples, i.e. $x$-coordinate of $P$ where $kP=G$. The difference and ratio to the bitlength of the whole group is also considered.",
    "motivation": "The strange behaviour of secp224k1 and secp256k1 for the scalar $k=2$.",
    "input": {
        "k": (int, "Integer")
    },
    "output": {
        "Hx": (int, "x-coordinate"),
        "bits": (int, "Bitlength of x"),
        "difference": (int, "Difference"),
        "ratio": (float, "Ratio")
    }
}



TRAIT_INFO["i13"] = {
    "description": "Computation of $a^3/b^2$.",
    "motivation": "Value used in several standards.",
    "input": {},
    "output": {
        "r": (int, "Integer r")
    }
}

TRAIT_INFO["a28"] = {
    "description": "Number of $j$-invariants adjacent to the curve by $l$-isogeny. This is the degree of the point in the $l$-isogeny graph.",
    "motivation": "The volcano structure might be relevant for cryptanalysis.",
    "input": {
        "l": (int, "Small prime")
    },
    "output": {
        "len": (int, "Number of adjacent curves")
    }
}

TRAIT_INFO["a29"] = {
    "description": "Torsion order of the lift of $E$ to $Q$.",
    "motivation": "Inspired by the lifting of ECDLP to curve over $\\mathbb{Q}$.",
    "input": {},
    "output": {
        "Q_torsion": (int, "Q torsion")
    }
}

TRAIT_INFO["i14"] = {
    "description": "Bit overlaps in curve coefficients",
    "motivation": "Brainpool construction causes significant overlap",
    "input": {},
    "output": {
        "o": (int, "overlap")
    }
}

def params_iter(trait_name):
    with open(pathlib.Path(TRAIT_PATH, trait_name, trait_name + ".params"), "r") as params_file:
        params = json.load(params_file)

    params_names = params["params_local_names"]
    params_ranges = {}
    for key in params["params_global"].keys():
        params_ranges[key] = sage_eval(params["params_global"][key])

    for params_values in itertools.product(*params_ranges.values()):
        yield dict(zip(params_names, params_values))


def numeric_outputs(trait_name):
    outputs = []

    for output, info in TRAIT_INFO[trait_name]["output"].items():
        if info[0] == int or info[0] == float:
            outputs.append(output)

    return outputs


def nonnumeric_outputs(trait_name):
    outputs = []

    for output, info in TRAIT_INFO[trait_name]["output"].items():
        if not (info[0] == int or info[0] == float):
            outputs.append(output)

    return outputs

def outputs(trait_name):
    return list(TRAIT_INFO[trait_name]["output"].keys())

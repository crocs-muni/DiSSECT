from typing import List

TRAIT_INFO = {}

TRAIT_INFO["a01"] = {
    "description": "Group structure of the curve in field extensions",
    "motivation": "The group structure is not an isogeny invariant",
    "input": {
        "r": (int, "Integer $r$")
    },
    "output": {
        "ord1": (int, "Order 1"),
        "ord2": (int, "Order 2")
    }
}

TRAIT_INFO["a02"] = {
    "description": "Factorization of the CM discriminant",
    "motivation": "A large square factor of D has interesting implications",
    "input": {},
    "output": {
        "cm_disc": (int, "Discriminant"),
        "factorization": (List[int], "Factorization of $D = t^2-4p = v^2d_K$, where $t$ is the trace of Frobenius of E and $d_K$ is the discriminant of the endomorphism algebra of $E$"),
        "max_conductor": (int, "Max conductor")
    }
}

TRAIT_INFO["a03"] = {
    "description": "Factorization of the quadratic twist cardinality",
    "motivation": "Smooth cardinality of a quadratic twist might allow attacks on some implementations",
    "input": {
        "deg": (int, "Integer")
    },
    "output": {
        "twist_cardinality": (int, "Twist Cardinality"),
        "factorization": (List[int], "The factorization of the cardinality of the quadratic twist of $E(\mathbb{F}_{p^r})$")
    }
}

TRAIT_INFO["a04"] = {
    "description": "Factorization of $kn \pm 1$ where $n$ is the order of $E/F_p$",
    "motivation": "Scalar multiplication by $kn \pm 1$ is the identity or negation, respectively; it can be seen as a generalization of https://link.springer.com/content/pdf/10.1007%2F11761679_1.pdf",
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
    "description": "Field extensions containing nontrivial/full l-torsion",
    "motivation": "Low $k_1, k_2$ might lead to computable pairings",
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
    "description": "Factorization of ratios of CM discriminants in extension fields and base fields",
    "motivation": "The prime factors of $D_r/D_1$ determine for which $l$ does the $l$-crater of E grow in the $r$-th extension",
    "input": {
        "deg": (int, "Integer")
    },
    "output": {
        "factorization": (List[int], "Factorization"),
        "ratio_sqrt": (int, "Ratio sqrt"),
    }
}

TRAIT_INFO["a07"] = {
    "description": "Embedding degree",
    "motivation": "Low embedding degrees might allow the MOV attack",
    "input": {},
    "output": {
        "embedding_degree_complement": (int, "Embedding degree complement"),
        "complement_bit_length": (int, "Complement bit length")
    }
}

TRAIT_INFO["a08"] = {
    "description": "Upper and lower bound for the class number of the endomorphism algebra",
    "motivation": "The class number is a classical invariant",
    "input": {},
    "output": {
        "upper": (int, "Upper"),
        "lower": (int, "Lower")
    }
}

TRAIT_INFO["a12"] = {
    "description": "Multiplicative orders of small primes modulo $n$",
    "motivation": "Small $m$ might have implications for scalar multiplication",
    "input": {
        "l": (int, "Small prime")
    },
    "output": {
        "order": (int, "Order"),
        "complement_bit_length": (int, "Complement bit length")
    }
}

TRAIT_INFO["a22"] = {
    "description": "Factorizations of small division polynomials",
    "motivation": "This is partially relevant to a05",
    "input": {
        "l": (int, "Prime")
    },
    "output": {
        "factorization": (List[List[int]], "Factorization of $l$-th division polynomial"),
        "len": (int, "Length")
    }
}

TRAIT_INFO["a23"] = {
    "description": "Volcano depth and crater degree in the l-isogeny graph",
    "motivation": "The volcano structure might be relevant for cryptanalysis",
    "input": {
        "l": (int, "Prime")
    },
    "output": {
        "crater_degree": (int, "Crater degree"),
        "depth": (int, "Depth")
    }
}

TRAIT_INFO["a24"] = {
    "description": "Field extensions containing nontrivial/full number of l-isogenies",
    "motivation": "This is loosely related to a05 and a06",
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
    "description": "Trace in field extensions and its factorization",
    "motivation": "Loosely speaking, this somehow measures the \"extent of supersingularity\" (if we regard it as a spectrum)",
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
    "description": "Number of points with low Hamming weight",
    "motivation": "Might be relevant for faulty RNG",
    "input": {
        "weight": (int, "Integer")
    },
    "output": {
        "x_coord_count": (int, "X coordinate count"),
        "expected": (int, "Expected"),
        "ratio": (float, "Ratio")
    }
}

TRAIT_INFO["i06"] = {
    "description": "Square parts of $4q \pm 1$ and $4n \pm 1$",
    "motivation": "Inspired by the [4p-1 paper](https://crocs.fi.muni.cz/public/papers/Secrypt2019)",
    "input": {},
    "output": {
        "p": (int, "p"),
        "order": (int, "Order")
    }
}

TRAIT_INFO["i07"] = {
    "description": "Distance of $n$ from the nearest power of two and multiple of 32/64",
    "motivation": "The first part is related to scalar multiplication bias when not using rejection sampling, the second is inspired by the paper [Big Numbers - Big Troubles](https://www.usenix.org/conference/usenixsecurity20/presentation/weiser)",
    "input": {},
    "output": {
        "distance": (int, "Distance"),
        "ratio": (float, "Order"),
        "distance 32": (int, "Distance 32"),
        "distance 64": (int, "Distance 64")
    }
}

TRAIT_INFO["i08"] = {
    "description": "Bit length of small inverted generator multiples",
    "motivation": "The strange behaviour of secp224k1 and secp256k1 for k=2",
    "input": {
        "k": (int, "Integer")
    },
    "output": {
        "Hx": (int, "X"),
        "bits": (int, "Bits"),
        "difference": (int, "Difference"),
        "ratio": (float, "Ratio")
    }
}

TRAIT_INFO["i10"] = {
    "description": "Points satisfying ZVP conditions",
    "motivation": "Might allow nontrivial ZVP attacks",
    "input": {
        "multiple": (int, "Integer"),
        "formula_file": (str, "Path to formula file"),
    },
    "output": {
        "points": (List[List[int]], "Points"),
        "len": (int, "Length")
    }
}

TRAIT_INFO["i11"] = {
    "description": "Points satisfying ZVP independently of the multiple",
    "motivation": "Might allow trivial ZVP/RPA attacks",
    "input": {
        "formula_file": (str, "Path to formula file")
    },
    "output": {
        "points": (List[List[int]], "Points"),
        "len": (int, "Length")
    }
}

TRAIT_INFO["i12"] = {
    "description": "Exceptional points with respect to given formulas",
    "motivation": "Might allow exceptional point attacks",
    "input": {
        "formula_file": (str, "Path to formula file")
    },
    "output": {
        "ideal": (str, "Ideal"),
        "dimension": (int, "Dimension"),
        "variety": (None, "Variety")
    }
}

TRAIT_INFO["s01"] = {
    "description": "TODO",
    "motivation": "TODO",
    "input": {},
    "output": {
        "histogram": (List[int], "Histogram"),
        "value": (str, "Value"),
    }
}

TRAIT_INFO["a28"] = {
    "description": "Number of $j$-invariants adjacent to the curve by $l$-isogeny",
    "motivation": "These roots correspond to $l$-isogenous curves",
    "input": {
        "l": (int, "Small prime")
    },
    "output": {
        "len": (int, "Length")
    }
}

TRAIT_INFO["a29"] = {
    "description": "Torsion order of the lift of E to Q",
    "motivation": "Inspired by the lifting of ECDLP to curve over $\mathbb{Q}$.",
    "input": {},
    "output": {
        "Q_torsion": (int, "Q torsion")
    }
}

from dissect.utils.custom_curve import CustomCurve

# noinspection SpellCheckingInspection
curve_brain = CustomCurve({
    "name": "brainpoolP160r1",
    "category": "brainpool",
    "desc": "",
    "oid": "1.3.36.3.3.2.8.1.1.1",
    "field": {
        "type": "Prime",
        "p": "0xe95e4a5f737059dc60dfc7ad95b3d8139515620f",
        "bits": 160
    },
    "form": "Weierstrass",
    "params": {
        "a": {
            "raw": "0x340e7be2a280eb74e2be61bada745d97e8f7c300"
        },
        "b": {
            "raw": "0x1e589a8595423412134faa2dbdec95c8d8675e58"
        }
    },
    "generator": {
        "x": {
            "raw": "0xbed5af16ea3f6a4f62938c4631eb5af7bdbcdbc3"
        },
        "y": {
            "raw": "0x1667cb477a1a8ec338f94741669c976316da6321"
        }
    },
    "order": "0xe95e4a5f737059dc60df5991d45029409e60fc09",
    "cofactor": "0x1",
    "characteristics": {
        "discriminant": "845365293605815390445478703156256339281515926196",
        "j_invariant": "387367055434500543477184371239969891945180101787",
        "trace_of_frobenius": "519972310379544251229703",
        "embedding_degree": "444099199480014958275695012943393788070980856152",
        "anomalous": False,
        "supersingular": False,
        "cm_disc": "592132265973353277700926857248628510609391551437",
        "conductor": "3",
        "torsion_degrees": [
            {
                "r": 2,
                "least": 3,
                "full": 3
            },
            {
                "r": 3,
                "least": 2,
                "full": 6
            },
            {
                "r": 5,
                "least": 12,
                "full": 12
            },
            {
                "r": 7,
                "least": 8,
                "full": 8
            },
            {
                "r": 11,
                "least": 5,
                "full": 55
            }
        ]
    }
})

curve_bn = CustomCurve({
    "name": "bn158",
    "category": "bn",
    "desc": "",
    "field": {
        "type": "Prime",
        "p": "0x24240D8241D5445106C8442084001384E0000013",
        "bits": 158
    },
    "form": "Weierstrass",
    "params": {
        "a": {
            "raw": "0x0000000000000000000000000000000000000000"
        },
        "b": {
            "raw": "0x0000000000000000000000000000000000000011"
        }
    },
    "generator": {
        "x": {
            "raw": "0x24240D8241D5445106C8442084001384E0000012"
        },
        "y": {
            "raw": "0x0000000000000000000000000000000000000004"
        }
    },
    "order": "0x24240D8241D5445106C7E3F07E0010842000000D",
    "cofactor": "0x01",
    "characteristics": {
        "discriminant": "206327671360737302491015800744139033450590902371",
        "j_invariant": "0",
        "trace_of_frobenius": "454233058419889982668807",
        "embedding_degree": "12",
        "anomalous": False,
        "supersingular": False,
        "cm_disc": "825310685442949209964062748743497713912381440069",
        "conductor": "1",
        "torsion_degrees": [
            {
                "r": 2,
                "least": 3,
                "full": 3
            },
            {
                "r": 3,
                "least": 2,
                "full": 6
            },
            {
                "r": 5,
                "least": 12,
                "full": 12
            },
            {
                "r": 7,
                "least": 6,
                "full": 6
            }
        ]
    }
})

curve_sec = CustomCurve({
    "name": "secp112r2",
    "category": "secg",
    "desc": "A randomly generated curve. [SEC2v1](https://www.secg.org/SEC2-Ver-1.0.pdf) states 'E was chosen "
            "verifiably at random as specified in ANSI X9.62 [1] from the seed'.",
    "oid": "1.3.132.0.7",
    "field": {
        "type": "Prime",
        "p": "0xdb7c2abf62e35e668076bead208b",
        "bits": 112
    },
    "form": "Weierstrass",
    "params": {
        "a": {
            "raw": "0x6127c24c05f38a0aaaf65c0ef02c"
        },
        "b": {
            "raw": "0x51def1815db5ed74fcc34c85d709"
        }
    },
    "generator": {
        "x": {
            "raw": "0x4ba30ab5e892b4e1649dd0928643"
        },
        "y": {
            "raw": "0xadcd46f5882e3747def36e956e97"
        }
    },
    "order": "0x36df0aafd8b8d7597ca10520d04b",
    "cofactor": "0x04",
    "characteristics": {
        "seed": "002757A1114D696E6768756151755316C05E0BD4",
        "discriminant": "3350974381310990100142288157262754",
        "j_invariant": "1815128745141690948653052996943564",
        "trace_of_frobenius": "72213667414400864",
        "embedding_degree": "370973768757809558322577571595630",
        "anomalous": False,
        "supersingular": False,
        "cm_disc": "494631691677079417114575713327579",
        "conductor": "6",
        "torsion_degrees": [
            {
                "r": 2,
                "least": 1,
                "full": 1
            },
            {
                "r": 3,
                "least": 8,
                "full": 8
            },
            {
                "r": 5,
                "least": 24,
                "full": 24
            },
            {
                "r": 7,
                "least": 3,
                "full": 6
            },
            {
                "r": 11,
                "least": 5,
                "full": 10
            },
            {
                "r": 13,
                "least": 3,
                "full": 12
            },
            {
                "r": 17,
                "least": 288,
                "full": 288
            },
            {
                "r": 19,
                "least": 360,
                "full": 360
            }
        ]
    }
})

curves = [curve_sec, curve_bn, curve_brain]
curve_names = {"secp112r2": curve_sec, "bn158": curve_bn, "brainpoolP160r1": curve_brain}

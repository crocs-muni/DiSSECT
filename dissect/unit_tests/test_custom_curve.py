import unittest
from dissect.utils.custom_curve import CustomCurve
from sage.all import EllipticCurve, EllipticCurve_from_j, GF, ZZ
from dissect.utils.utils import customize_curve

BINARY = CustomCurve(
    {
        "name": "sect163k1",
        "category": "secg",
        "desc": "",
        "oid": "1.3.132.0.1",
        "field": {
            "type": "Binary",
            "poly": [
                {"power": 163, "coeff": "0x01"},
                {"power": 7, "coeff": "0x01"},
                {"power": 6, "coeff": "0x01"},
                {"power": 3, "coeff": "0x01"},
                {"power": 0, "coeff": "0x01"},
            ],
            "bits": 163,
            "degree": 163,
        },
        "form": "Weierstrass",
        "params": {
            "a": {"raw": "0x000000000000000000000000000000000000000001"},
            "b": {"raw": "0x000000000000000000000000000000000000000001"},
        },
        "generator": {
            "x": {"raw": "0x02fe13c0537bbc11acaa07d793de4e6d5e5c94eee8"},
            "y": {"raw": "0x0289070fb05d38ff58321f2e800536d538ccdaa3d9"},
        },
        "order": "0x04000000000000000000020108a2e0cc0d99f8a5ef",
        "cofactor": "0x2",
        "aliases": ["nist/K-163"],
        "characteristics": {
            "discriminant": "1",
            "j_invariant": "1",
            "trace_of_frobenius": "-4845466632539410776804317",
            "anomalous": False,
            "supersingular": False,
            "cm_disc": "46768052394588893382517919492387689168400618179549",
            "conductor": "1",
        },
    }
)

MONTGOMERY = CustomCurve({
    "name": "M-221",
    "category": "other",
    "desc": "Curve from https://eprint.iacr.org/2013/647.pdf",
    "field": {
        "type": "Prime",
        "p": "0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD",
        "bits": 221
    },
    "form": "Montgomery",
    "params": {
        "a": {
            "raw": "0x01c93a"
        },
        "b": {
            "raw": "0x01"
        }
    },
    "generator": {
        "x": {
            "raw": "0x04"
        },
        "y": {
            "raw": "0x0f7acdd2a4939571d1cef14eca37c228e61dbff10707dc6c08c5056d"
        }
    },
    "order": "0x040000000000000000000000000015A08ED730E8A2F77F005042605B",
    "cofactor": "0x8"
})

WEIERSTRASS = CustomCurve({
    "name": "x962_sim_256_seed_diff_302361",
    "category": "x962_sim_256",
    "form": "Weierstrass",
    "field": {
        "type": "Prime",
        "p": "0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff",
        "bits": 256
    },
    "params": {
        "a": {
            "raw": "-0x3"
        },
        "b": {
            "raw": "0x226c4993ea4df0010cfc11dbb66cbbfedb0ace35bf1f3020473c4bd94a2e339a"
        }
    },
    "order": "0x333333330000000033333333333333334ae9ac61625e7d64f1938eea1e41a96f",
    "cofactor": "0x5",
    "simulation": {
        "seed": "0xc49d360886e704936a6678e1139d26b7819ae177"
    },
    "properties": {
        "j_invariant": "0x1e4c0d9bbd81cdf4ba3ce44a8842ad0a6af882d2c59cd05a88aa2029a511528e",
        "trace": "-0x76905de5ebd872f8b7e1ca9297484f2b",
        "embedding_degree": "0x19999999800000001999999999999999a574d630b12f3eb278c9c7750f20d4b7",
        "cm_discriminant": "-0x3c9169802457a46aa509f7a93178aed253fa77232a89157b657997522a5546ec3"
    }
})

EXTENSION = CustomCurve({
    "name": "Fp254n2BNa",
    "category": "other",
    "desc": "Curve used in: https://eprint.iacr.org/2010/354.pdf",
    "field": {
        "type": "Extension",
        "base": "0x2370fb049d410fbe4e761a9886e502417d023f40180000017e80600000000001",
        "bits": 508,
        "degree": 2,
        "poly": [
            {
                "power": 2,
                "coeff": "0x01"
            },
            {
                "power": 0,
                "coeff": "0x05"
            }
        ]
    },
    "form": "Weierstrass",
    "params": {
        "a": {
            "poly": [
                {
                    "power": 0,
                    "coeff": "0x00"
                }
            ]
        },
        "b": {
            "poly": [
                {
                    "power": 1,
                    "coeff": "0x2370fb049d410fbe4e761a9886e502417d023f40180000017e80600000000000"
                }
            ]
        }
    },
    "generator": {
        "x": {
            "poly": [
                {
                    "power": 1,
                    "coeff": "0xa1cf585585a61c6e9880b1f2a5c539f7d906fff238fa6341e1de1a2e45c3f72"
                },
                {
                    "power": 0,
                    "coeff": "0x19b0bea4afe4c330da93cc3533da38a9f430b471c6f8a536e81962ed967909b5"
                }
            ]
        },
        "y": {
            "poly": [
                {
                    "power": 1,
                    "coeff": "0x0ee97d6de9902a27d00e952232a78700863bc9aa9be960C32f5bf9fd0a32d345"
                },
                {
                    "power": 0,
                    "coeff": "0x17abd366ebbd65333e49c711a80a0cf6d24adf1b9b3990eedcc91731384d2627"
                }
            ]
        }
    },
    "order": "0x2370fb049d410fbe4e761a9886e502411dc1af70120000017e80600000000001",
    "cofactor": "0x2370fb049d410fbe4e761a9886e50241dc42cf101e0000017e80600000000001"
})


class TestCustomCurve(unittest.TestCase):

    def test_BINARY(self):
        self.assertEqual(BINARY.cofactor(), 2)
        self.assertEqual(BINARY.a(), 1)
        self.assertEqual(BINARY.b(), 1)
        self.assertEqual(BINARY.order(), 0x04000000000000000000020108A2E0CC0D99F8A5EF)
        self.assertEqual(BINARY.generator()[0].integer_representation(), 0x02FE13C0537BBC11ACAA07D793DE4E6D5E5C94EEE8)
        self.assertEqual(BINARY.generator()[1].integer_representation(), 0x0289070FB05D38FF58321F2E800536D538CCDAA3D9)
        self.assertEqual(BINARY.j_invariant(), 1)
        self.assertEqual(BINARY.trace(), -4845466632539410776804317)
        self.assertEqual(BINARY.cm_discriminant(), -7)
        self.assertEqual(BINARY.nbits(), 163)
        self.assertFalse(BINARY.is_over_extension())
        self.assertFalse(BINARY.is_over_prime())
        self.assertTrue(BINARY.is_over_binary())
        self.assertEqual(BINARY.embedding_degree(),17932535427373041941149514581590332356837787037)

    def test_MONTGOMERY(self):
        self.assertEqual(MONTGOMERY.cofactor(), 8)
        self.assertEqual(MONTGOMERY.order(), 421249166674228746791672110734682167926895081980396304944335052891)
        self.assertEqual(MONTGOMERY.j_invariant(), 2198635150322943370581460256665771755915443349493942401782889387523)
        self.assertEqual(MONTGOMERY.trace(), -3509210517603025598879416729141978)
        self.assertEqual(MONTGOMERY.cm_discriminant(), -0x2c43ddd54943526ae6d55085b3a85fd81970f09e26691124ae6f794)
        self.assertEqual(MONTGOMERY.nbits(), 219)
        self.assertEqual(MONTGOMERY.embedding_degree(),0x2000000000000000000000000000ad0476b9874517bbf802821302d)

    def test_WEIERSTRASS(self):
        self.assertEqual(WEIERSTRASS.name(), "x962_sim_256_seed_diff_302361")
        self.assertEqual(WEIERSTRASS.order(), 0x333333330000000033333333333333334ae9ac61625e7d64f1938eea1e41a96f)
        self.assertEqual(WEIERSTRASS.category(), "x962_sim_256")
        self.assertEqual(WEIERSTRASS.params(), {"a": {"raw": "-0x3"}, "b": {
            "raw": "0x226c4993ea4df0010cfc11dbb66cbbfedb0ace35bf1f3020473c4bd94a2e339a"}})
        self.assertEqual(WEIERSTRASS.cofactor(), 5)
        self.assertEqual(WEIERSTRASS.cardinality(), 0xffffffff00000001000000000000000076905de6ebd872f8b7e1ca9297484f2b)
        self.assertEqual(WEIERSTRASS.nbits(), 254)
        p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
        self.assertEqual(WEIERSTRASS.field().order(), p)
        self.assertEqual(WEIERSTRASS.field_type(), "Prime")
        self.assertEqual(WEIERSTRASS.q(), p)
        self.assertEqual(WEIERSTRASS.form().form(), "weierstrass")
        self.assertEqual(WEIERSTRASS.description(), None)
        self.assertEqual(WEIERSTRASS.seed(), "0xc49d360886e704936a6678e1139d26b7819ae177")
        self.assertFalse(WEIERSTRASS.is_over_binary())
        self.assertEqual(WEIERSTRASS.a(), -3)
        self.assertEqual(WEIERSTRASS.b(), 0x226c4993ea4df0010cfc11dbb66cbbfedb0ace35bf1f3020473c4bd94a2e339a)
        self.assertEqual(WEIERSTRASS.generator(), None)
        self.assertFalse(WEIERSTRASS.is_over_extension())
        self.assertTrue(WEIERSTRASS.is_over_prime())
        self.assertEqual(WEIERSTRASS.trace(), -157598498730582091775914883381658668843)
        self.assertEqual(WEIERSTRASS.cm_discriminant(),
                         -0x3c9169802457a46aa509f7a93178aed253fa77232a89157b657997522a5546ec3)
        self.assertEqual(WEIERSTRASS.j_invariant(),
                         13703759755872812151735812950849952450951590630043982456996394172744381584014)
        self.assertEqual(WEIERSTRASS.embedding_degree(),
                         11579208921035624876269744694940757353024374191402089628730954619224875652279)

    def test_EXTENSION(self):
        self.assertEqual(EXTENSION.cofactor(), 0x2370fb049d410fbe4e761a9886e50241dc42cf101e0000017e80600000000001)
        self.assertEqual(EXTENSION.a().lift(), 0)
        self.assertEqual(EXTENSION.b().matrix()[1][0],
                         0x2370fb049d410fbe4e761a9886e502417d023f40180000017e80600000000000)
        self.assertEqual(EXTENSION.order(), 0x2370fb049d410fbe4e761a9886e502411dc1af70120000017e80600000000001)
        self.assertEqual(EXTENSION.generator()[0].norm(),
                         11281539936611307808114476023359139338266750998829135672729497725604682084229)
        self.assertEqual(EXTENSION.generator()[1].norm(),
                         12123625036987721582261441339415773604879084932378194785387869031552991984941)
        self.assertEqual(EXTENSION.j_invariant(), 0)
        self.assertEqual(EXTENSION.trace(), 0x2370fb049d410fbdc02400000000000000000000000000000000000000000001)
        self.assertEqual(EXTENSION.nbits(), 254)
        self.assertTrue(EXTENSION.is_over_extension())
        self.assertFalse(EXTENSION.is_over_prime())
        self.assertFalse(EXTENSION.is_over_binary())

    def test_extensions(self):
        p = 101
        ec = EllipticCurve_from_j(GF(p)(1))
        bin_size = 2**10
        bin_ec = EllipticCurve(GF(bin_size), [1, 1, 0, 0, 1])
        deg = 3
        custom_ec = CustomCurve(customize_curve(ec))
        custom_bin_ec = CustomCurve(customize_curve(bin_ec))
        self.assertEqual(1073731736, custom_bin_ec.extended_cardinality(deg))
        self.assertEqual(1029924, custom_ec.extended_cardinality(deg))
        self.assertEqual(10089, custom_bin_ec.extended_trace(deg))
        self.assertEqual(378, custom_ec.extended_trace(deg))
        self.assertEqual(-4193179375, custom_bin_ec.extended_frobenius_disc(deg))
        self.assertEqual(-3978320, custom_ec.extended_frobenius_disc(deg))
        ext = custom_bin_ec.extended_ec(deg)
        self.assertEqual([ZZ(i) for i in bin_ec.a_invariants()], [ZZ(i) for i in ext.a_invariants()])
        self.assertEqual(bin_size**deg, ext.base_field().order())
        ext = custom_ec.extended_ec(deg)
        self.assertEqual(101 ** deg, ext.base_field().order())
        self.assertEqual(ec.change_ring(ext.base_field()), ext)

    def test_is_torsion_cyclic(self):
        field = GF(101)
        ec = EllipticCurve_from_j(field(10))
        custom_ec = CustomCurve(customize_curve(ec))
        self.assertTrue(custom_ec.is_torsion_cyclic(prime=5, deg=1))
        ec = EllipticCurve_from_j(field(4))
        custom_ec = CustomCurve(customize_curve(ec))
        self.assertTrue(custom_ec.is_torsion_cyclic(prime=5, deg=1))
        ec = EllipticCurve_from_j(field(11))
        custom_ec = CustomCurve(customize_curve(ec))
        self.assertFalse(custom_ec.is_torsion_cyclic(prime=5, deg=1))


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")

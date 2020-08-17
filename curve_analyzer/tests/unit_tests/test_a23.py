import unittest
from curve_analyzer.tests.a23.a23 import a23_curve_function
from curve_analyzer.utils.custom_curve import CustomCurve

degree_0_depth_0_3 = CustomCurve({'name': 'secp112r1',
                                  'category': 'secg',
                                  'desc': '',
                                  'oid': '1.3.132.0.6',
                                  'field': {'type': 'Prime',
                                            'p': '0xdb7c2abf62e35e668076bead208b',
                                            'bits': 112},
                                  'form': 'Weierstrass',
                                  'params': {'a': {"raw": '0xdb7c2abf62e35e668076bead2088'},
                                             'b': {"raw": '0x659ef8ba043916eede8911702b22'}},
                                  'generator': {'x': {"raw": '0x09487239995a5ee76b55f9c2f098'},
                                                'y': {"raw": '0xa89ce5af8724c0a23e0e0ff77500'}},
                                  'order': '0xdb7c2abf62e35e7628dfac6561c5',
                                  'cofactor': '0x1',
                                  'characteristics': {'discriminant': '431641039663814096123514803737201',
                                                      'j_invariant': '3522606870331875081851146801233610',
                                                      'trace_of_frobenius': '-4407293269000505',
                                                      'embedding_degree': '4451685225093714776491891542548932',
                                                      'anomalous': False,
                                                      'supersingular': False,
                                                      'cm_disc': '17806740900374859092745686363194213',
                                                      'conductor': '1',
                                                      'torsion_degrees': [{'r': 2, 'least': 3, 'full': 3},
                                                                          {'r': 3, 'least': 8, 'full': 8},
                                                                          {'r': 5, 'least': 8, 'full': 8},
                                                                          {'r': 7, 'least': 3, 'full': 6},
                                                                          {'r': 11, 'least': 120, 'full': 120},
                                                                          {'r': 13, 'least': 24, 'full': 24},
                                                                          {'r': 17, 'least': 8, 'full': 16},
                                                                          {'r': 19, 'least': 360, 'full': 360}]}})

degree_1_depth_1_3 = CustomCurve(
    {'name': 'secp224r1',
     'category': 'secg',
     'desc': '',
     'oid': '1.3.132.0.33',
     'field': {'type': 'Prime',
               'p': '0xffffffffffffffffffffffffffffffff000000000000000000000001',
               'bits': 224},
     'form': 'Weierstrass',
     'params': {'a': {"raw": '0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe'},
                'b': {"raw": '0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4'}},
     'generator': {'x': {"raw": '0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21'},
                   'y': {"raw": '0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34'}},
     'order': '0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d',
     'cofactor': '0x1',
     'aliases': ['nist/P-224'],
     'characteristics': {'discriminant': '8133954887115844930654026312464158747844254983800706208418026371607',
                         'j_invariant': '20781977079628996477063007379734849057519732242287194936686605794677',
                         'trace_of_frobenius': '4733100108545601916421827343930821',
                         'embedding_degree': '8986648889050213264889005029006541980152602571474797240560907456020',
                         'anomalous': False,
                         'supersingular': False,
                         'cm_disc': '107839786668602559178668060348078517961131556494503316152212921264703',
                         'conductor': '1',
                         'torsion_degrees': [{'r': 2, 'least': 3, 'full': 3},
                                             {'r': 3, 'least': 2, 'full': 2},
                                             {'r': 5, 'least': 6, 'full': 6}]}})

degree_2_depth_0_3 = CustomCurve({'name': 'x962_sim_112_rel_seed_-15',
                                  'category': 'x962_sim_112',
                                  'desc': '',
                                  'field': {'type': 'Prime',
                                            'p': '0xdb7c2abf62e35e668076bead208b',
                                            'bits': 112},
                                  'form': 'Weierstrass',
                                  'params': {'a': {"raw": '-0x3'}, 'b': {"raw": '0x40bbf13932634ed8a28e4bf5940b'}},
                                  'generator': None,
                                  'order': 9698660621119204226245963124771,
                                  'cofactor': 459,
                                  'characteristics': None,
                                  'seed': '00F50B028E4D696E676875615175290472783FA2'})

degree_0_depth_0_2 = degree_0_depth_0_3

degree_1_depth_0_2 = CustomCurve({'name': 'x962_sim_112_rel_seed_-190',
                                  'category': 'x962_sim_112',
                                  'desc': '',
                                  'field': {'type': 'Prime',
                                            'p': '0xdb7c2abf62e35e668076bead208b',
                                            'bits': 112},
                                  'form': 'Weierstrass',
                                  'params': {'a': {"raw": '-0x3'}, 'b': {"raw": '0x51a203f1fcea5c488e3c764a4a8b'}},
                                  'generator': None,
                                  'order': 28175222943631106725417688148217,
                                  'cofactor': 158,
                                  'characteristics': None,
                                  'seed': '00F50B028E4D696E676875615175290472783EF3'})

degree_2_depth_0_2 = CustomCurve({'name': 'sect163k1',
                                  'category': 'secg',
                                  'desc': '',
                                  'oid': '1.3.132.0.1',
                                  "field": {
                                      "type": "Binary",
                                      "poly": [
                                          {
                                              "power": 163,
                                              "coeff": "0x01"
                                          },
                                          {
                                              "power": 7,
                                              "coeff": "0x01"
                                          },
                                          {
                                              "power": 6,
                                              "coeff": "0x01"
                                          },
                                          {
                                              "power": 3,
                                              "coeff": "0x01"
                                          },
                                          {
                                              "power": 0,
                                              "coeff": "0x01"
                                          }
                                      ],
                                      "bits": 163,
                                      "degree": 163
                                  },
                                  'form': 'Weierstrass',
                                  'params': {'a': {"raw": '0x000000000000000000000000000000000000000001'},
                                             'b': {"raw": '0x000000000000000000000000000000000000000001'}},
                                  'generator': {'x': {"raw": '0x02fe13c0537bbc11acaa07d793de4e6d5e5c94eee8'},
                                                'y': {"raw": '0x0289070fb05d38ff58321f2e800536d538ccdaa3d9'}},
                                  'order': '0x04000000000000000000020108a2e0cc0d99f8a5ef',
                                  'cofactor': '0x2',
                                  'aliases': ['nist/K-163'],
                                  'characteristics': {'discriminant': '1',
                                                      'j_invariant': '1',
                                                      'trace_of_frobenius': '-4845466632539410776804317',
                                                      'anomalous': False,
                                                      'supersingular': False,
                                                      'cm_disc': '46768052394588893382517919492387689168400618179549',
                                                      'conductor': '1'}})

degree_0_depth_1_2 = CustomCurve({'name': 'secp112r2',
                                  'category': 'secg',
                                  'desc': '',
                                  'oid': '1.3.132.0.7',
                                  'field': {'type': 'Prime',
                                            'p': '0xdb7c2abf62e35e668076bead208b',
                                            'bits': 112},
                                  'form': 'Weierstrass',
                                  'params': {'a': {"raw": '0x6127c24c05f38a0aaaf65c0ef02c'},
                                             'b': {"raw": '0x51def1815db5ed74fcc34c85d709'}},
                                  'generator': {'x': {"raw": '0x4ba30ab5e892b4e1649dd0928643'},
                                                'y': {"raw": '0xadcd46f5882e3747def36e956e97'}},
                                  'order': '0x36df0aafd8b8d7597ca10520d04b',
                                  'cofactor': '0x4',
                                  'characteristics': {'discriminant': '3350974381310990100142288157262754',
                                                      'j_invariant': '1815128745141690948653052996943564',
                                                      'trace_of_frobenius': '72213667414400864',
                                                      'embedding_degree': '370973768757809558322577571595630',
                                                      'anomalous': False,
                                                      'supersingular': False,
                                                      'cm_disc': '494631691677079417114575713327579',
                                                      'conductor': '6',
                                                      'torsion_degrees': [{'r': 2, 'least': 1, 'full': 1},
                                                                          {'r': 3, 'least': 8, 'full': 8},
                                                                          {'r': 5, 'least': 24, 'full': 24},
                                                                          {'r': 7, 'least': 3, 'full': 6},
                                                                          {'r': 11, 'least': 5, 'full': 10},
                                                                          {'r': 13, 'least': 3, 'full': 12},
                                                                          {'r': 17, 'least': 288, 'full': 288},
                                                                          {'r': 19, 'least': 360, 'full': 360}]}})


class Test_a23(unittest.TestCase):

    def test_prime_2(self):
        result = a23_curve_function(degree_0_depth_0_3, 3)
        self.assertEqual(result['crater_degree'], 0, "Should be 0")
        self.assertEqual(result['depth'], 0, "Should be 0")

        result = a23_curve_function(degree_1_depth_1_3, 3)
        self.assertEqual(result['crater_degree'], 1, "Should be 1")
        self.assertEqual(result['depth'], 1, "Should be 1")

        result = a23_curve_function(degree_2_depth_0_3, 3)
        self.assertEqual(result['crater_degree'], 2, "Should be 2")
        self.assertEqual(result['depth'], 0, "Should be 0")

    def test_prime_3(self):
        result = a23_curve_function(degree_0_depth_0_2, 2)
        self.assertEqual(result['crater_degree'], 0, "Should be 0")
        self.assertEqual(result['depth'], 0, "Should be 0")

        result = a23_curve_function(degree_1_depth_0_2, 2)
        self.assertEqual(result['crater_degree'], 1, "Should be 1")
        self.assertEqual(result['depth'], 0, "Should be 0")

        result = a23_curve_function(degree_2_depth_0_2, 2)
        self.assertEqual(result['crater_degree'], 2, "Should be 2")
        self.assertEqual(result['depth'], 0, "Should be 0")

        result = a23_curve_function(degree_0_depth_1_2, 2)
        self.assertEqual(result['crater_degree'], 0, "Should be 0")
        self.assertEqual(result['depth'], 1, "Should be 1")


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")

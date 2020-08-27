import unittest

from curve_analyzer.tests.a25.a25 import a25_curve_function
from curve_analyzer.utils.custom_curve import CustomCurve

E1 = CustomCurve({'name': 'secp112r1',
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

number_of_trace_factors = 5
trace_factorization = [[5, 1], [13, 1], [367, 1], [653, 1], [282930227, 1]]

class Test_a25(unittest.TestCase):

    def test_1(self):
        result = a25_curve_function(E1)
        self.assertEqual(result['trace'], number_of_trace_factors, "Should be " + str(number_of_trace_factors))
        self.assertEqual(result['trace_factorization'], trace_factorization, "Should be " + str(trace_factorization))


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")

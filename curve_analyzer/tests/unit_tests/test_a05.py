import unittest
from curve_analyzer.tests.a05.a05 import a05_curve_function
from curve_analyzer.utils.custom_curve import CustomCurve

E1 = CustomCurve({'name': 'secp192k1',
                  'category': 'secg',
                  'desc': '',
                  'oid': '1.3.132.0.31',
                  'field': {'type': 'Prime',
                            'p': '0xfffffffffffffffffffffffffffffffffffffffeffffee37',
                            'bits': 192},
                  'form': 'Weierstrass',
                  'params': {'a': {"raw": '0x000000000000000000000000000000000000000000000000'},
                             'b': {"raw": '0x000000000000000000000000000000000000000000000003'}},
                  'generator': {'x': {"raw": '0xdb4ff10ec057e9ae26b07d0280b7f4341da5d1b1eae06c7d'},
                                'y': {"raw": '0x9b2f2f6d9c5628a7844163d015be86344082aa88d95e2f9d'}},
                  'order': '0xfffffffffffffffffffffffe26f2fc170f69466a74defd8d',
                  'cofactor': '0x1',
                  'characteristics': {'discriminant': '6277101735386680763835789423207666416102355444459739537159',
                                      'j_invariant': '0',
                                      'trace_of_frobenius': '146402144145231529258894028971',
                                      'embedding_degree': '3138550867693340381917894711530632135978561957600422756038',
                                      'anomalous': False,
                                      'supersingular': False,
                                      'cm_disc': '25108406941546723055343157692684263520264190248580064135217',
                                      'conductor': '1',
                                      'torsion_degrees': [{'r': 2, 'least': 3, 'full': 3},
                                                          {'r': 3, 'least': 2, 'full': 6},
                                                          {'r': 5, 'least': 24, 'full': 24},
                                                          {'r': 7, 'least': 3, 'full': 3},
                                                          {'r': 11, 'least': 4, 'full': 4},
                                                          {'r': 13, 'least': 3, 'full': 12}]}})

K2 = {'least': 3, 'full': 3, 'relative': 1}
K3 = {'least': 2, 'full': 6, 'relative': 3}
K5 = {'least': 24, 'full': 24, 'relative': 1}


class Test_a05(unittest.TestCase):

    def test_2(self):
        result = a05_curve_function(E1, 2)
        self.assertEqual(result['least'], K2['least'], "Should be " + str(K2['least']))
        self.assertEqual(result['full'], K2['full'], "Should be " + str(K2['full']))
        self.assertEqual(result['relative'], K2['relative'], "Should be " + str(K2['relative']))

    def test_3(self):
        result = a05_curve_function(E1, 3)
        self.assertEqual(result['least'], K3['least'], "Should be " + str(K3['least']))
        self.assertEqual(result['full'], K3['full'], "Should be " + str(K3['full']))
        self.assertEqual(result['relative'], K3['relative'], "Should be " + str(K3['relative']))

    def test_5(self):
        result = a05_curve_function(E1, 5)
        self.assertEqual(result['least'], K5['least'], "Should be " + str(K5['least']))
        self.assertEqual(result['full'], K5['full'], "Should be " + str(K5['full']))
        self.assertEqual(result['relative'], K5['relative'], "Should be " + str(K5['relative']))


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")

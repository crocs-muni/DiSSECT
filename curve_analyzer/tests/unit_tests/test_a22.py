import unittest
from sage.all_cmdline import *
from curve_analyzer.tests.a22.a22 import a22_curve_function
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

x = PolynomialRing(GF(E1.q), 'x').gen()
div_3 = {'factorization': [(x, 1), (x ** 3 + 12, 1)], 'degs_list': [1, 3], 'len': 2}
div_7 = {'factorization': [(x ** 3 + 467353055321752719589468804695657373614662829753922604176,
                            1),
                           (x ** 3 + 1461524858479648087495516199521419332331176135129164141372, 1),
                           (x ** 3 + 1678405026624114921665503827994582034929485137593983145081, 1),
                           (x ** 3 + 3011947769412597320163742530617319489590564667928336237472, 1),
                           (x ** 3 + 3022119238225123886672904817055485250599077753770649816517, 1),
                           (x ** 3 + 4034898747917209133012034203818445112621129953206786739997, 1),
                           (x ** 3 + 4156169612397413243446860118155590636770470819671980177967, 1),
                           (x ** 3 + 5482530994486954953629758784341404600780752925224209720140, 1)],
         'degs_list': [3, 3, 3, 3, 3, 3, 3, 3],
         'len': 8}


class Test_a22(unittest.TestCase):

    def test_3(self):
        result = a22_curve_function(E1, 3)
        self.assertEqual(result['factorization'], div_3['factorization'], "Should be " + str(div_3['factorization']))
        self.assertEqual(result['degs_list'], div_3['degs_list'], "Should be " + str(div_3['degs_list']))
        self.assertEqual(result['len'], div_3['len'], "Should be " + str(div_3['len']))

    def test_7(self):
        result = a22_curve_function(E1, 7)
        self.assertEqual(result['factorization'], div_7['factorization'], "Should be " + str(div_7['factorization']))
        self.assertEqual(result['degs_list'], div_7['degs_list'], "Should be " + str(div_7['degs_list']))
        self.assertEqual(result['len'], div_7['len'], "Should be " + str(div_7['len']))


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")

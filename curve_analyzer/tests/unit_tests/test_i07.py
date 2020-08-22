import unittest

from curve_analyzer.tests.i07.i07 import i07_curve_function
from curve_analyzer.utils.custom_curve import CustomCurve

E1 = CustomCurve({'name': 'secp112r2',
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

dist1 = {'distance': 740611633441112928659565470072532}


class Test_i07(unittest.TestCase):

    def test_1(self):
        result = i07_curve_function(E1)
        self.assertEqual(result['distance'], dist1['distance'],
                         "Should be " + str(dist1['distance']))


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")

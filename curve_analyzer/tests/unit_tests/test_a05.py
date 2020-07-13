import unittest
from curve_analyzer.tests.a05.a05_torsion_extensions import a5_curve_function
from curve_analyzer.utils.custom_curve import CustomCurve



E1 = CustomCurve({'name': 'secp192k1',
 'category': 'secg',
 'desc': '',
 'oid': '1.3.132.0.31',
 'field': {'type': 'Prime',
  'p': '0xfffffffffffffffffffffffffffffffffffffffeffffee37',
  'bits': 192},
 'form': 'Weierstrass',
 'params': {'a': '0x000000000000000000000000000000000000000000000000',
  'b': '0x000000000000000000000000000000000000000000000003'},
 'generator': {'x': '0xdb4ff10ec057e9ae26b07d0280b7f4341da5d1b1eae06c7d',
  'y': '0x9b2f2f6d9c5628a7844163d015be86344082aa88d95e2f9d'},
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

K1 = {'least': [3, 2, 24], 'full': [3, 6, 24], 'relative': [1, 3, 1]}

class Test_a05(unittest.TestCase):
    
    def test_up_to_5(self):
        result = a5_curve_function(E1,6)
        self.assertEqual(result['least'], K1['least'], "Should be "+str(K1['least']))
        self.assertEqual(result['full'], K1['full'], "Should be "+str(K1['full']))
        self.assertEqual(result['relative'], K1['relative'], "Should be "+str(K1['relative']))
       

        
if __name__ == '__main__':
    unittest.main()
    print("Everything passed")
    
    



import unittest
from curve_analyzer.tests.a24_isogeny_extensions import a24_curve_function
from curve_analyzer.tests.curve_handler import CustomCurve


E1 = CustomCurve({'name': 'gost512',
 'category': 'gost',
 'desc': '',
 'field': {'type': 'Prime',
  'p': '0x4531acd1fe0023c7550d267b6b2fee80922b14b2ffb90f04d4eb7c09b5d2d15df1d852741af4704a0458047e80e4546d35b8336fac224dd81664bbf528be6373',
  'bits': 512},
 'form': 'Weierstrass',
 'params': {'a': '0x7',
  'b': '0x1cff0806a31116da29d8cfa54e57eb748bc5f377e49400fdd788b649eca1ac4361834013b2ad7322480a89ca58e0cf74bc9e540c2add6897fad0a3084f302adc'},
 'generator': {'x': '0x24d19cc64572ee30f396bf6ebbfd7a6c5213b3b3d7057cc825f91093a68cd762fd60611262cd838dc6b60aa7eee804e28bc849977fac33b4b530f1b120248a9a',
  'y': '0x2bb312a43bd2ce6e0d020613c857acddcfbf061e91e5f2c3f32447c259f39b2c83ab156d77f1496bf7eb3351e1ee4e43dc1a18b91b24640b6dbb92cb1add371e'},
 'order': '0x4531acd1fe0023c7550d267b6b2fee80922b14b2ffb90f04d4eb7c09b5d2d15da82f2d7ecb1dbac719905c5eecc423f1d86e25edbe23c595d644aaf187e6e6df',
 'cofactor': '0x1',
 'characteristics': {'discriminant': '2354030499938796080455685465248118319217198068927486418321815690157012200907763643687518461996694967111330756661917773558875004226725808279081784408642042',
  'j_invariant': '610900649669533983695054775734306011088557592049408816983490905302782604532556561056354879375964032515423415363590524121501491460792551618405795037507769',
  'trace_of_frobenius': '33317690176989408428354063686744165122149707869071609401230178415964786752661'}})

I1 = {'least': [3, 2, 1], 'full': [3, 2, 4], 'relative': [1, 1, 4]}


class Test_a24(unittest.TestCase):
    
    def test_up_to_5(self):
        result = a24_curve_function(E1,6)
        self.assertEqual(result['least'], I1['least'], "Should be "+str(I1['least']))
        self.assertEqual(result['full'], I1['full'], "Should be "+str(I1['full']))
        self.assertEqual(result['relative'], I1['relative'], "Should be "+str(I1['relative']))
       

        
if __name__ == '__main__':
    unittest.main()
    print("Everything passed")
    
    



import ast, sys, os, optparse, json
from curve_analyzer.utils.json_handler import save_into_json, load_from_json
from curve_analyzer.definitions import TEST_PATH, TEST_MODULE_PATH, TEST_prefixes
from curve_analyzer.tests.testing_curves import curves

def parse(text):
    try:
        value = int(text)
    except:
        try:
            value = json.loads(text)
        except:
            pass
    if isinstance(text, list):
        value = [parse(i) for i in text]
    return value



def create_structure_file(name):
    f = open(TEST_PATH+"/"+name+"/"+name+".params","r")
    params = ast.literal_eval(f.read())
    f.close()
    local_params = params["params_local_names"]
    if local_params:
        print("Input parameters: ")
    params = []
    for param_name in local_params:
        param_value = parse(input(param_name+": "))
        params.append(param_value)
    module_name = TEST_MODULE_PATH+'.'+name + '.' + name
    __import__(module_name)
    curve_function = getattr(sys.modules[module_name], name+"_curve_function")
    params_local = str(dict(zip(local_params, params)))
    result = {}
    for curve in curves:
        print("Curve "+curve.name+": ")
        result[curve.name] = {}
        computed_result = curve_function(curve, *params)
        for key in computed_result.keys():
            key_result = parse(input("Result for "+key+": "))
            if computed_result[key]!=key_result and str(computed_result[key])!=key_result:
                print("Wrong result, should be: " + str(computed_result[key]))
                return False
        result[curve.name][params_local] = computed_result
    json_file = TEST_PATH+"/"+ name+"/" +name +'_structure.json'
    save_into_json(result, json_file, mode='w')
    return True

def create_unittest(name):
    results = load_from_json(TEST_PATH+"/"+name+"/"+name+"_structure.json")
    if os.path.exists(TEST_PATH+"/unit_tests/test_"+name+".py"):
        answer = input("Unittest for "+name+" already exists, overwrite? [Y/n]")
        if answer in "[n,N]":
            return
    f = open(TEST_PATH+"/unit_tests/test_"+name+".py","w")
    f.write("import unittest, ast\n")
    f.write("from curve_analyzer.tests."+name+"."+name+" import "+name+"_curve_function\n")
    f.write("from curve_analyzer.tests.testing_curves import curves, curve_names\n")
    f.write("results="+str(results)+"\n")
    f.write("\nclass Test_"+name+"(unittest.TestCase):\n \n")
    for curve in results.keys():
        f.write("    # This test has been auto-generated by gen_unittest\n")
        f.write("    def test_auto_generated_"+str(curve)+"(self):\n")
        f.write("        params = ast.literal_eval(list(results[\""+str(curve)+"\"].keys())[0]).values()\n")
        f.write("        computed_result = "+name+"_curve_function(curve_names[\""+str(curve)+"\"],*params)\n")
        f.write("        self.assertEqual(computed_result,list(results[\""+str(curve)+"\"].values())[0])\n\n")
    f.write("\nif __name__ == '__main__':\n")
    f.write("   unittest.main()\n")
    f.write("   print(\"Everything passed\")\n")
    f.close()

tests_to_skip = ['a08']

def all_tests(structure, unittest):
    directory = TEST_PATH
    for filename in os.listdir(directory):
        if filename in tests_to_skip:
            continue
        if not filename[0] in TEST_prefixes:
            continue
        try:
            int(filename[1:], 10)
        except:
            continue
        if structure:
            create_structure_file(filename)
        if unittest:
            create_unittest(filename)




def main():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--unittest',
                      action="store", dest="unittest",
                      help="list of names for unittest seperated by comma or \'all\'", default="_")

    parser.add_option('-s', '--structure',
                      action="store", dest="structure",
                      help="list of names for structure files seperated by comma or \'all\'", default="_")
    parser.add_option('-b', '--both',
                      action="store", dest="both",
                      help="list of names for unittest and structure files seperated by comma or \'all\'", default="_")

    options, args = parser.parse_args()
    if options.both!="_":
        if options.both.strip()=="all":
            all_tests(True,True)
        else:
            tests = options.both.split(",")
            for name in tests:
                create_structure_file(name.strip())
                create_unittest(name.strip())

    elif options.unittest!="_":
        if options.unittest.strip()=="all":
            all_tests(False,True)
        else:
            tests = options.unittest.split(",")
            for name in tests:
                create_unittest(name.strip())

    elif options.structure!="_":
        if options.structure.strip()=="all":
            all_tests(True,False)
        else:
            tests = options.structure.split(",")
            for name in tests:
                create_structure_file(name.strip())
    else:
        print("Something's wrong")






main()




import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
CURVE_PATH = ROOT_DIR + '/curves_json'
CURVE_PATH_SIM = ROOT_DIR + '/curves_json_sim'
TEST_PATH = ROOT_DIR + '/tests'
PARALLEL_RESULTS_PATH = ROOT_DIR + '/utils/parallel/results'
X962_PATH = ROOT_DIR + '/utils/parallel/x962'
TEST_MODULE_PATH = 'curve_analyzer.tests'
TEST_prefixes = ['a','i']

from pathlib import Path

ROOT_DIR = Path(__file__).parent   # This is your Project Root
CURVE_PATH = Path(ROOT_DIR, 'curves_json')
CURVE_PATH_SIM = Path(ROOT_DIR, 'curves_json_sim')
TEST_PATH = Path(ROOT_DIR, 'tests')
PARALLEL_RESULTS_PATH = Path(ROOT_DIR, 'utils/parallel/results')
X962_PATH = Path(ROOT_DIR, 'utils/parallel/x962')
TEST_MODULE_PATH = 'curve_analyzer.tests'
TEST_prefixes = ['a','i','s']
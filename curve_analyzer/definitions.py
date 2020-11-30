from pathlib import Path

ROOT_DIR = Path(__file__).parent  # This is your Project Root
CURVE_PATH = Path(ROOT_DIR, 'curves_json')
CURVE_PATH_SIM = Path(ROOT_DIR, 'curves_json_sim')
TEST_PATH = Path(ROOT_DIR, 'tests')
PARALLEL_RESULTS_PATH = Path(ROOT_DIR, 'utils/parallel/results')
X962_PATH = Path(ROOT_DIR, 'utils/parallel/x962')
TEST_MODULE_PATH = 'curve_analyzer.tests'
TEST_PREFIXES = ['a', 'i', 's']
TEST_NAMES = [f.name for f in TEST_PATH.iterdir() if f.is_dir() and f.name[0] in TEST_PREFIXES and int(f.name[1:], 10)]

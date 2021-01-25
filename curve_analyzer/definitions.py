import re
from pathlib import Path

ROOT_DIR = Path(__file__).parent  # This is your Project Root
CURVE_PATH = Path(ROOT_DIR, 'curves_json')
CURVE_PATH_SIM = Path(ROOT_DIR, 'curves_json_sim')
TRAIT_PATH = Path(ROOT_DIR, 'traits')
PARALLEL_RESULTS_PATH = Path(ROOT_DIR, 'utils', 'parallel', 'results')
ZVP_PATH = Path(ROOT_DIR, 'utils', 'zvp')
EFD_PATH = Path(ROOT_DIR, 'utils', 'efd')
EFD_SHORTW_PROJECTIVE_ADDITION_PATH = Path(EFD_PATH, 'shortw', 'projective', 'addition')
EFD_SHORTW_PROJECTIVE_ADDITION_FORMULAS = [f for f in EFD_SHORTW_PROJECTIVE_ADDITION_PATH.iterdir() if
                                           f.suffix == '.op3']
EFD_SHORTW_PROJECTIVE_MINUS3_ADDITION_PATH = Path(EFD_PATH, 'shortw', 'projective-3', 'addition')
EFD_SHORTW_PROJECTIVE_MINUS3_ADDITION_FORMULAS = [f for f in EFD_SHORTW_PROJECTIVE_MINUS3_ADDITION_PATH.iterdir() if
                                                  f.suffix == '.op3']
X962_PATH = Path(ROOT_DIR, 'utils', 'parallel', 'x962')
TRAIT_MODULE_PATH = 'curve_analyzer.traits'
TRAIT_NAME_CONDITION = r'[ais][0-9][0-9]'
TRAIT_NAMES = [f.name for f in TRAIT_PATH.iterdir() if f.is_dir() and re.search(TRAIT_NAME_CONDITION, f.name)]
STD_SOURCES = [f.name for f in CURVE_PATH.iterdir() if f.is_dir() and not "." in f.name]

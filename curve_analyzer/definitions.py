import re
from pathlib import Path

from sage.all import ZZ

from curve_analyzer.utils.json_handler import load_from_json

ROOT_DIR = Path(__file__).parent  # This is the project root
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
STD_BITLENGTHS = set()
STD_COFACTORS = set()
STD_CURVE_NAMES = []
STD_CURVE_DICT = {}
for source in STD_SOURCES:
    STD_CURVE_DICT[source] = []
    curves = load_from_json(Path(CURVE_PATH, source, "curves.json"))["curves"]
    for curve in curves:
        STD_CURVE_DICT[source].append(curve["name"])
        STD_CURVE_NAMES.append(curve["name"])
        STD_BITLENGTHS.add(curve["field"]["bits"])
        STD_COFACTORS.add(ZZ(curve["cofactor"]))
STD_CURVE_COUNT = len(STD_CURVE_NAMES)
STD_COFACTORS = sorted(STD_COFACTORS)
STD_BITLENGTHS = sorted(STD_BITLENGTHS)

# SIM_BITLENGTHS = list(map(ZZ, [d.name for d in Path(CURVE_PATH_SIM, "x962_sim").iterdir() if d.is_dir()]))
# SIM_COFACTORS = set()
# for d in Path(CURVE_PATH_SIM, "x962_sim").iterdir():
#     if d.is_dir():
#         for f in d.iterdir():
#             curves = load_from_json(f)["curves"]
#             for curve in curves:
#                 SIM_COFACTORS.add(ZZ(curve["cofactor"]))
# SIM_COFACTORS = sorted(SIM_COFACTORS)
SIM_BITLENGTHS = [128, 160, 192, 224, 256]
SIM_COFACTORS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31]
ALL_COFACTORS = sorted(set(STD_COFACTORS + SIM_COFACTORS))

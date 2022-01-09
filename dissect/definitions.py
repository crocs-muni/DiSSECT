import re
from pathlib import Path
from typing import List, Set, Any, Union

from sage.all import ZZ

from dissect.utils.json_handler import load_from_json

ROOT_DIR: Union[Path, Any] = Path(__file__).parent  # This is the project root
CURVE_PATH_SIM = Path(ROOT_DIR, "curves_json_sim")
TRAIT_PATH = Path(ROOT_DIR, "traits")
KOHEL_PATH = Path(ROOT_DIR, "utils", "kohel")
TRAIT_MODULE_PATH: str = "dissect.traits"
TRAIT_NAME_CONDITION = r"[ais][0-9][0-9]"
TRAIT_NAMES: List[str] = sorted([
    f.name
    for f in TRAIT_PATH.iterdir()
    if f.is_dir() and re.search(TRAIT_NAME_CONDITION, f.name)
])

STD_BITLENGTHS = set()
STD_COFACTORS: Set[ZZ] = set()
STD_CURVE_NAMES = []
STD_CURVE_DICT = {}
STD_CURVE_COUNT = len(STD_CURVE_NAMES)
STD_COFACTORS = sorted(STD_COFACTORS)
STD_SOURCES = ["anssi","bls","bn","brainpool","gost","mnt","nist","nums","oakley","oscaa","other","secg","wtls","x962","x963"]
STD_BITLENGTHS = sorted(STD_BITLENGTHS)

ALL_CURVE_COUNT = 217396
SIM_CURVE_COUNT = ALL_CURVE_COUNT - STD_CURVE_COUNT
SIM_BITLENGTHS = [128, 160, 192, 224, 256]
ALL_BITLENGTHS = sorted(set(STD_BITLENGTHS + SIM_BITLENGTHS))
SIM_COFACTORS = list(range(1, 9))
ALL_COFACTORS = sorted(set(STD_COFACTORS + SIM_COFACTORS))

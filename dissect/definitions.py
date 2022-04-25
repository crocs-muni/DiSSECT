import re
from pathlib import Path
from typing import List, Set, Any, Union

ROOT_DIR: Union[Path, Any] = Path(__file__).parent  # This is the project root
TRAIT_PATH = Path(ROOT_DIR, "traits")
KOHEL_PATH = Path(ROOT_DIR, "utils", "kohel")
TRAIT_MODULE_PATH: str = "dissect.traits"
TRAIT_NAME_CONDITION = r"[ais][0-9][0-9]"
TRAIT_NAMES: List[str] = sorted([
    f.name
    for f in TRAIT_PATH.iterdir()
    if f.is_dir() and re.search(TRAIT_NAME_CONDITION, f.name)
])

from pathlib import Path
from typing import Any, Union

ROOT_DIR: Union[Path, Any] = Path(__file__).parent  # This is the project root
KOHEL_PATH = Path(ROOT_DIR, "utils", "kohel")

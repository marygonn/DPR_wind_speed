from pathlib import Path
from typing import NamedTuple


class DprGmiFilePair(NamedTuple):
    dpr_fpath: Path
    gmi_fpath: Path


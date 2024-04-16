import os
from pathlib import Path

from back.src.constantes import PICKLE_NAME

ROOT_DIR = Path(__file__).parent
PICKEL_PATH = os.path.join(ROOT_DIR, "src", "dump_data", PICKLE_NAME)  # noqa: PTH118

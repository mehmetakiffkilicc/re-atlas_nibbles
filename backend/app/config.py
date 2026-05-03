import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() == "true"
DATA_DIR: Path = Path(__file__).parent.parent / "data"
CACHE_DIR: Path = DATA_DIR / "cache"
CONTRACTS_DIR: Path = Path(__file__).parent.parent.parent / "contracts"

import sys
from pathlib import Path

# Add src to the path to resolve imports correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from wms.main import app

# Vercel needs a variable named 'app'

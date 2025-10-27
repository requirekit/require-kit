# Test imports fix
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "installer/global/commands"))

from lib.complexity_models import ImplementationPlan
from lib.pager_display import PagerDisplay
from lib.change_tracker import ChangeTracker
from lib.modification_session import ModificationSession

print("All imports successful!")

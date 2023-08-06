# This file is required to import Visual COMeT as a package
import inspect
import sys
import visual_comet

module_path = inspect.getfile(visual_comet).replace("__init__.py", "")
sys.path.append(module_path)

from models import *
from dataloaders import *
from visualcomet import VisualCOMET
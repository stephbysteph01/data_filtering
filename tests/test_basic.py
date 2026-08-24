import sys
import os
import importlib

# Ensure src/ is on sys.path so package is importable without installation
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)


def test_importable():
    mod = importlib.import_module('czrm_analysis')
    assert hasattr(mod, '__version__')

# Make project root importable as a package for tests.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
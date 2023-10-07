import os.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.backend.command import entrypoint

if __name__ == "__main__":
    entrypoint()

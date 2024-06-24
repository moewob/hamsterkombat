import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import print_banner, main

if __name__ == "__main__":
    try:
        print_banner()
        main()
    except KeyboardInterrupt:
        sys.exit()

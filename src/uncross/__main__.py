"""module entrypoint"""

import sys

if __name__ == "__main__":
    from uncross.cli import uncross

    sys.exit(uncross())

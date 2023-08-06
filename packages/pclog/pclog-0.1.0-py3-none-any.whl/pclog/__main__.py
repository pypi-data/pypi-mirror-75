"""
CLI
"""

import sys
import argparse
from . import example


def main() -> int:
    """Execute CLI."""
    parser = argparse.ArgumentParser(
        prog='pclog',
        description='Pretty Color Log'
    )
    parser.add_argument('-e', '--example', action='store_true',
                        help='print example')

    args = parser.parse_args()

    if args.example:
        example.main()
    parser.print_help(sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())

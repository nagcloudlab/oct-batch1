"""Makes the package runnable: python -m payments_tools data/payments.csv --account 4201"""
import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())

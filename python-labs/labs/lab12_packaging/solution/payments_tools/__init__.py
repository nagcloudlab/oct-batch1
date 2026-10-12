"""payments_tools: load and summarize payment data.

The package's public API is what this file exposes, so users write
    from payments_tools import load_payments, summarize
without knowing which module each function lives in.
"""
from .loader import load_payments
from .stats import summarize, summarize_file

__version__ = "0.1.0"
__all__ = ["load_payments", "summarize", "summarize_file"]

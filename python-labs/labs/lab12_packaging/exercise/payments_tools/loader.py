"""Reading payment data (given, complete)."""
import csv


def load_payments(path) -> list[dict]:
    """Read a payments CSV into dicts with int ids and float amounts."""
    with open(path, newline="") as f:
        return [
            {**row,
             "payment_id": int(row["payment_id"]),
             "account_id": int(row["account_id"]),
             "amount": float(row["amount"])}
            for row in csv.DictReader(f)
        ]

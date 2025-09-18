#!/usr/bin/env python3
"""
Calibrate sensors by computing a linear fit from a CSV with columns:
raw,true

Usage:
    python3 scripts/calibrate_sensor.py calibration.csv
"""
import argparse
import csv
import numpy as np


def linear_fit(raw_vals, true_vals):
    """Compute linear fit parameters a,b for true = a*raw + b."""
    a, b = np.polyfit(raw_vals, true_vals, 1)
    return a, b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csvfile")
    args = parser.parse_args()

    raw = []
    true = []
    with open(args.csvfile) as f:
        reader = csv.DictReader(f)
        for r in reader:
            raw.append(float(r["raw"]))
            true.append(float(r["true"]))

    a, b = linear_fit(raw, true)
    print(f"Calibration: value = {a:.6f}*raw + {b:.6f}")


if __name__ == "__main__":
    main()

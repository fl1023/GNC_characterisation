#!/usr/bin/env python3
"""
Plot serial log data and calculate actual sampling frequency.
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path
import sys

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    raise SystemExit(
        "Missing dependencies: install matplotlib and numpy with "
        "'pip install matplotlib numpy'."
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot serial log CSV and analyze sampling frequency."
    )
    parser.add_argument(
        "--input",
        default="serial_log.csv",
        help="CSV input file name (default: serial_log.csv).",
    )
    return parser.parse_args()


def parse_csv(csv_path):
    """
    Read the CSV file and extract timestamps and data.
    Returns lists of timestamps, raw values, voltages, and angles.
    """
    timestamps = []
    raw_values = []
    voltages = []
    angles = []

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header row

            for row in reader:
                if len(row) < 2:
                    continue

                try:
                    ts_str = row[0]
                    line = row[1]

                    # Parse timestamp
                    ts = datetime.fromisoformat(ts_str)
                    timestamps.append(ts)

                    # Parse the serial line: "ADC pin X raw = Y  voltage = Z V  angle = W deg"
                    # Handle lines that might be missing "ADC pin X raw =" at the start
                    if "raw =" in line:
                        parts = line.split()
                        # Find the index of "raw"
                        try:
                            raw_idx = parts.index("raw")
                            voltage_idx = parts.index("voltage")
                            angle_idx = parts.index("angle")
                            
                            raw = int(parts[raw_idx + 2])
                            voltage = float(parts[voltage_idx + 2])
                            angle = float(parts[angle_idx + 2])

                            raw_values.append(raw)
                            voltages.append(voltage)
                            angles.append(angle)
                        except (ValueError, IndexError):
                            # Skip malformed lines
                            pass
                except (ValueError, IndexError):
                    # Skip malformed lines
                    continue

    except FileNotFoundError:
        raise SystemExit(f"File not found: {csv_path}")

    return timestamps, raw_values, voltages, angles


def calculate_frequency(timestamps):
    """
    Calculate the sampling frequency from timestamps.
    Returns frequency in Hz and statistics.
    """
    if len(timestamps) < 2:
        return None, None, None

    # Calculate time deltas in seconds
    deltas = []
    for i in range(1, len(timestamps)):
        dt = (timestamps[i] - timestamps[i - 1]).total_seconds()
        if dt > 0:
            deltas.append(dt)

    if not deltas:
        return None, None, None

    # Calculate frequencies (1 / dt)
    frequencies = [1.0 / dt for dt in deltas]

    mean_freq = np.mean(frequencies)
    std_freq = np.std(frequencies)
    min_freq = np.min(frequencies)
    max_freq = np.max(frequencies)

    return mean_freq, std_freq, (min_freq, max_freq)


def main():
    args = parse_args()
    input_path = Path(args.input)

    print(f"Reading {input_path}...")
    timestamps, raw_values, voltages, angles = parse_csv(input_path)

    if not timestamps:
        raise SystemExit("No valid data found in CSV file.")

    print(f"Loaded {len(timestamps)} timestamps, {len(raw_values)} complete samples")

    # Trim timestamps to match parsed data
    timestamps = timestamps[:len(raw_values)]

    # Calculate frequency
    mean_freq, std_freq, freq_range = calculate_frequency(timestamps)

    if mean_freq is not None:
        print(f"\n--- Frequency Analysis ---")
        print(f"Mean frequency:     {mean_freq:.2f} Hz")
        print(f"Std deviation:      {std_freq:.2f} Hz")
        print(f"Min frequency:      {freq_range[0]:.2f} Hz")
        print(f"Max frequency:      {freq_range[1]:.2f} Hz")
        print(f"Total duration:     {(timestamps[-1] - timestamps[0]).total_seconds():.2f} seconds")
    else:
        print("Could not calculate frequency from timestamps.")

    # Create figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # Convert timestamps to seconds relative to start
    t_start = timestamps[0]
    t_seconds = [(ts - t_start).total_seconds() for ts in timestamps]

    # Plot 1: Raw ADC values
    axes[0].plot(t_seconds, raw_values, "b-", linewidth=1, label="Raw ADC")
    axes[0].set_ylabel("Raw ADC Value")
    axes[0].set_title("Serial Log Data")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    # Plot 2: Voltage
    axes[1].plot(t_seconds, voltages, "g-", linewidth=1, label="Voltage")
    axes[1].set_ylabel("Voltage (V)")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # Plot 3: Angle
    axes[2].plot(t_seconds, angles, "r-", linewidth=1, label="Angle")
    axes[2].set_ylabel("Angle (deg)")
    axes[2].set_xlabel("Time (seconds)")
    axes[2].grid(True, alpha=0.3)
    axes[2].legend()

    plt.tight_layout()
    plt.savefig("serial_log_plot.png", dpi=150)
    print(f"\nPlot saved to serial_log_plot.png")
    plt.show()


if __name__ == "__main__":
    main()

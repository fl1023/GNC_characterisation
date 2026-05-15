import argparse
import csv
import re
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

LINE_RE = re.compile(
    r"ADC pin \d+ raw = (?P<raw>\d+)\s+voltage = (?P<voltage>[0-9.]+) V\s+angle = (?P<angle>[0-9.]+) deg"
)


def parse_row(timestamp_str: str, line: str):
    ts = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    match = LINE_RE.search(line)
    if not match:
        return None
    return {
        "timestamp": ts,
        "raw": int(match.group("raw")),
        "voltage": float(match.group("voltage")),
        "angle": float(match.group("angle")),
    }


def load_data(csv_path: Path):
    timestamps = []
    raw = []
    voltage = []
    angle = []

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 2:
                continue
            parsed = parse_row(row[0], row[1])
            if parsed is None:
                continue
            timestamps.append(parsed["timestamp"])
            raw.append(parsed["raw"])
            voltage.append(parsed["voltage"])
            angle.append(parsed["angle"])

    return timestamps, np.array(raw), np.array(voltage), np.array(angle)


def compute_sample_frequency(timestamps):
    if len(timestamps) < 2:
        return None
    dt = np.diff([ts.timestamp() for ts in timestamps])
    avg_dt = float(np.mean(dt))
    return 1.0 / avg_dt if avg_dt > 0 else None


def plot_data(timestamps, raw, voltage, angle, output_image: Path):
    times = np.array([(ts - timestamps[0]).total_seconds() for ts in timestamps])

    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    ax[0].plot(times, raw, "-o", markersize=2)
    ax[0].set_ylabel("Raw ADC")
    ax[0].grid(True)

    ax[1].plot(times, voltage, "-o", markersize=2)
    ax[1].set_ylabel("Voltage (V)")
    ax[1].grid(True)

    ax[2].plot(times, angle, "-o", markersize=2)
    ax[2].set_ylabel("Angle (deg)")
    ax[2].set_xlabel("Time (s)")
    ax[2].grid(True)

    fig.suptitle("Serial Log Data")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    output_image.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_image, dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Plot serial_log.csv and compute sample frequency.")
    parser.add_argument("csvfile", nargs="?", default="serial_log.csv", help="CSV file to plot.")
    parser.add_argument("--out", default="serial_plot.png", help="Output plot image.")
    args = parser.parse_args()

    csv_path = Path(args.csvfile)
    output_image = Path(args.out)

    timestamps, raw, voltage, angle = load_data(csv_path)
    if not timestamps:
        raise SystemExit(f"No valid data parsed from {csv_path}")

    freq = compute_sample_frequency(timestamps)
    print(f"Estimated sample frequency: {freq:.2f} Hz")
    plot_data(timestamps, raw, voltage, angle, output_image)
    print(f"Saved plot to {output_image}")


if __name__ == "__main__":
    main()
import argparse
import csv
from datetime import datetime
from pathlib import Path


try:
    import serial
except ImportError:
    raise SystemExit("Missing dependency: install pyserial with 'pip install pyserial'.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read serial lines, add timestamps, and save to CSV."
    )
    parser.add_argument(
        "--port",
        required=True,
        help="Serial port name, e.g. COM3 on Windows or /dev/ttyUSB0 on Linux.",
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        default=230400,
        help="Serial baud rate (default: 115200).",
    )
    parser.add_argument(
        "--output",
        default="serial_log.csv",
        help="CSV output file name (default: serial_log.csv).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Read timeout in seconds (default: 1.0).",
    )
    parser.add_argument(
        "--flush-every",
        type=int,
        default=50,
        help="Flush CSV file every N lines (default: 50).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_path = Path(args.output)

    try:
        ser = serial.Serial(args.port, args.baudrate, timeout=args.timeout)
    except serial.SerialException as exc:
        raise SystemExit(f"Unable to open serial port {args.port}: {exc}")

    print(f"Listening on {args.port} at {args.baudrate} baud. Logging to {output_path}")

    write_header = not output_path.exists()
    with output_path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        if write_header:
            writer.writerow(["timestamp", "serial_line"])
            csv_file.flush()

        try:
            line_count = 0
            while True:
                raw_bytes = ser.readline()
                if not raw_bytes:
                    continue

                line = raw_bytes.decode("utf-8", errors="replace").strip()
                timestamp = datetime.now().isoformat(sep=" ", timespec="milliseconds")
                writer.writerow([timestamp, line])
                line_count += 1
                if args.flush_every > 0 and line_count % args.flush_every == 0:
                    csv_file.flush()
                print(f"[{timestamp}] {line}")
        except KeyboardInterrupt:
            print("\nSerial logger stopped by user.")
        finally:
            ser.close()


if __name__ == "__main__":
    main()

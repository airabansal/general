import math
import re

# Base SI Unit Conversion Factors relative to standard base units
# Base units: meter (m), kilogram (kg), second (s), liter (L), kelvin (K)
UNIT_CONVERSIONS = {
    # Length -> Base: meters (m)
    "mm": ("m", 0.001),
    "cm": ("m", 0.01),
    "m": ("m", 1.0),
    "km": ("m", 1000.0),
    "in": ("m", 0.0254),
    "ft": ("m", 0.3048),
    # Mass -> Base: kilograms (kg)
    "mg": ("kg", 0.000001),
    "g": ("kg", 0.001),
    "kg": ("kg", 1.0),
    "lb": ("kg", 0.453592),
    "lbs": ("kg", 0.453592),
    # Volume -> Base: liters (L)
    "ml": ("L", 0.001),
    "l": ("L", 1.0),
    # Time -> Base: seconds (s)
    "ms": ("s", 0.001),
    "s": ("s", 1.0),
    "sec": ("s", 1.0),
    "min": ("s", 60.0),
    "hr": ("s", 3600.0),
}


def convert_temperature(value, unit):
    """Handles non-linear temperature conversions to Kelvin."""
    unit = unit.upper()
    if unit in ["C", "°C", "CELSIUS"]:
        return value + 273.15, "K"
    elif unit in ["F", "°F", "FAHRENHEIT"]:
        return (value - 32) * 5 / 9 + 273.15, "K"
    elif unit in ["K", "KELVIN"]:
        return value, "K"
    return None, None


def parse_measurement(raw_str):
    """Parses a messy input string (e.g., '250.5 mL', '1.2kg') into value and unit."""
    cleaned = raw_str.strip().lower()

    # Regex matches: leading sign/digits/decimal followed by optional space and unit string
    match = re.match(r"^([+-]?\d*\.?\d+)\s*([a-zA-Z°]+)?$", cleaned)
    if not match:
        return None, None, "Invalid Format"

    val_str, unit_str = match.groups()
    val = float(val_str)
    unit_str = unit_str if unit_str else ""

    # Check for temperature
    if unit_str in ["c", "f", "k", "°c", "°f"]:
        converted_val, base_unit = convert_temperature(val, unit_str)
        return converted_val, base_unit, "Success"

    # Check standard SI units
    if unit_str in UNIT_CONVERSIONS:
        base_unit, factor = UNIT_CONVERSIONS[unit_str]
        return val * factor, base_unit, "Success"

    return val, unit_str if unit_str else "Unknown", "Unrecognized Unit"


def detect_outliers_iqr(records):
    """Flags values exceeding 1.5 * IQR as statistical outliers."""
    # Group values by unit type
    by_unit = {}
    for r in records:
        if r["status"] == "Success":
            by_unit.setdefault(r["base_unit"], []).append(r["base_val"])

    outliers = set()
    for unit, vals in by_unit.items():
        if len(vals) < 4:
            continue  # Need at least 4 data points for a meaningful IQR
        sorted_v = sorted(vals)
        n = len(sorted_v)
        q1 = sorted_v[n // 4]
        q3 = sorted_v[(3 * n) // 4]
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        for r in records:
            if (
                r["base_unit"] == unit
                and not (lower_bound <= r["base_val"] <= upper_bound)
            ):
                outliers.add(r["id"])

    return outliers


class ScienceLabCleaner:

    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.raw_data = []

    def load_data(self, data_list):
        """Ingests raw measurement strings."""
        self.raw_data = data_list

    def process(self):
        """Cleans, normalizes, and flags outliers in the dataset."""
        processed = []
        for idx, raw in enumerate(self.raw_data, 1):
            val, unit, status = parse_measurement(raw)
            processed.append(
                {
                    "id": idx,
                    "raw": raw,
                    "base_val": val,
                    "base_unit": unit,
                    "status": status,
                    "is_outlier": False,
                }
            )

        # Flag outliers
        outlier_ids = detect_outliers_iqr(processed)
        for r in processed:
            if r["id"] in outlier_ids:
                r["is_outlier"] = True

        return processed

    def print_report(self, results):
        """Displays formatted table output."""
        print("=" * 72)
        print(f"       LAB DATA CLEANING REPORT: {self.experiment_name.upper()}")
        print("=" * 72)
        print(
            f"  {'ID':<4} | {'Raw Input':<14} | {'Cleaned Value':<16} | {'Unit':<6} | {'Status'}"
        )
        print("  " + "-" * 66)

        for r in results:
            if r["status"] == "Success":
                val_str = f"{r['base_val']:>10.4f}"
                unit_str = r["base_unit"]
                flag = "⚠️ OUTLIER" if r["is_outlier"] else "✅ OK"
            else:
                val_str = "        N/A"
                unit_str = r["base_unit"]
                flag = f"❌ {r['status']}"

            print(
                f"  {r['id']:<4} | {r['raw']:<14} | {val_str:<16} | {unit_str:<6} | {flag}"
            )

        print("=" * 72 + "\n")


# --- Example Execution ---
if __name__ == "__main__":
    # Simulated messy Chemistry/Physics lab observations (Titration / Mass trial)
    messy_lab_trials = [
        "250 ml",
        "0.26 L",
        "245 mL",
        "252 ml",
        "1250 mL",  # Outlier / Measurement error
        "1.2 kg",
        "1150 g",
        "1200g",
        "25.5 C",
        "78.0 °F",
        "bad_data_12",  # Malformed input
        "15.2 cm",
        "0.153 m",
    ]

    cleaner = ScienceLabCleaner("Titration & Mass Measurements")
    cleaner.load_data(messy_lab_trials)
    results = cleaner.process()
    cleaner.print_report(results)

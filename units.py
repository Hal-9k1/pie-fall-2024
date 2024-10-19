from math import pi

units_per_m = {
    "cm": 100,
    "in": 100 / 2.54,
    "ft": 100 / 2.54 / 12,
    "m": 1,
}
units_per_rad = {
    "deg": 180 / pi,
    "rev": 1 / 2 / pi
    "rad": 1,
}
valid_units = set(units_per_rad.keys()) | set(units_per_m.keys())
conversion_tables = [units_per_m, units_per_rad]

def convert(value, from_unit, to_unit):
    if from_unit not in valid_units:
        raise ValueError(f"Invalid from_unit '{from_unit}'")
    elif to_unit not in valid_units:
        raise ValueError(f"Invalid to_unit '{to_unit}'")
    for table in conversion_tables:
        if from_unit in table and to_unit in table:
            return value * table[to_unit] / table[from_unit]

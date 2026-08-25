#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###########################
# Electric bike speed/power/mileage calculator
#
# Vibecoded in Gemini 3.1 Pro by s0me0ne-25
# Non-Copyright: AI Work
# If the above is not applicable:
# - Licensed under Creative Commons CC0
###########################

import sys

# --- CONSTANTS ---
# Usable battery capacity factor (85% depth of discharge for cycle life preservation)
BATTERY_USABLE_FACTOR = 0.85

# Calibration table: Speed (km/h) -> Power (W)
#
# Third-party empirical measurement data is used
# Credits: https://e4bike.ru/page/speed-and-mileage
CALIBRATION_DATA = {
    20: 150,
    25: 250,
    30: 350,
    35: 500,
    40: 750,
    45: 1000,
    50: 1500,
    60: 2000,
    70: 2500,
    80: 4500
}

# Sort the data for interpolation to ensure order
SPEEDS = sorted(CALIBRATION_DATA.keys())
POWERS = [CALIBRATION_DATA[v] for v in SPEEDS]


def interpolate(x, x_values, y_values):
    """Simple linear interpolation function."""
    if x <= x_values[0]:
        return y_values[0]
    if x >= x_values[-1]:
        return y_values[-1]
    
    for i in range(len(x_values) - 1):
        x1, x2 = x_values[i], x_values[i+1]
        if x1 <= x <= x2:
            y1, y2 = y_values[i], y_values[i+1]
            # Linear interpolation formula
            return y1 + (y2 - y1) * ((x - x1) / (x2 - x1))
    return 0


def get_power_for_speed(speed):
    """Returns required power (W) for a given speed (km/h)."""
    return interpolate(speed, SPEEDS, POWERS)


def parse_capacity(input_str):
    """
    Parses capacity input. 
    Accepts direct Wh (e.g., '500') or Voltage * Ah (e.g., '48*15').
    """
    try:
        # Remove spaces to easily handle inputs like '48 * 15'
        input_str = input_str.strip().replace(' ', '')
        if '*' in input_str:
            parts = input_str.split('*')
            if len(parts) == 2:
                return float(parts[0]) * float(parts[1])
        return float(input_str)
    except ValueError:
        return None


def calc_range():
    print("\n--- Calculate Range ---")
    speed_str = input("Enter speed (km/h): ")
    cap_str = input("Enter battery capacity (Wh or V*Ah, e.g. 500 or 48*15): ")
    
    try:
        speed = float(speed_str)
        nominal_capacity = parse_capacity(cap_str)
        
        if nominal_capacity is None:
            print("Error: Invalid capacity input format.")
            return
        
        power = get_power_for_speed(speed)
        usable_capacity = nominal_capacity * BATTERY_USABLE_FACTOR
        
        # time = usable_capacity / power
        # distance = speed * time
        estimated_range = speed * (usable_capacity / power)
        
        print(f"\nResult:")
        print(f"- Speed: {speed:.1f} km/h (requires ~{power:.1f} W)")
        print(f"- Nominal Capacity: {nominal_capacity:.1f} Wh")
        print(f"- Usable Capacity ({BATTERY_USABLE_FACTOR*100:.0f}% limit): {usable_capacity:.1f} Wh")
        print(f"- Estimated Range: {estimated_range:.1f} km")
        
    except ValueError:
        print("Error: Invalid numerical input.")


def calc_capacity():
    print("\n--- Calculate Required Capacity ---")
    speed_str = input("Enter speed (km/h): ")
    range_str = input("Enter target range (km): ")
    
    try:
        speed = float(speed_str)
        target_range = float(range_str)
        
        power = get_power_for_speed(speed)
        
        # range = speed * (usable_capacity / power)
        # usable_capacity = (target_range * power) / speed
        usable_capacity = (target_range * power) / speed
        nominal_capacity = usable_capacity / BATTERY_USABLE_FACTOR
        
        print(f"\nResult:")
        print(f"- Speed: {speed:.1f} km/h (requires ~{power:.1f} W)")
        print(f"- Target Range: {target_range:.1f} km")
        print(f"- Required Usable Capacity: {usable_capacity:.1f} Wh")
        print(f"- Required Nominal Capacity (with {BATTERY_USABLE_FACTOR*100:.0f}% limit): {nominal_capacity:.1f} Wh")
        
    except ValueError:
        print("Error: Invalid numerical input.")


def calc_speed():
    print("\n--- Calculate Average Speed ---")
    cap_str = input("Enter battery capacity (Wh or V*Ah, e.g. 500 or 48*15): ")
    range_str = input("Enter target range (km): ")
    
    try:
        nominal_capacity = parse_capacity(cap_str)
        target_range = float(range_str)
        
        if nominal_capacity is None:
            print("Error: Invalid capacity input format.")
            return
            
        usable_capacity = nominal_capacity * BATTERY_USABLE_FACTOR
        
        # Mathematical relation: range = v * (usable_capacity / P(v))
        # Therefore: v / P(v) = target_range / usable_capacity
        target_ratio = target_range / usable_capacity
        
        # Calculate the ratio (speed/power) for each known point
        ratios = [v / get_power_for_speed(v) for v in SPEEDS]
        
        # The ratio (v / P(v)) decreases as speed increases, 
        # so we reverse the lists to make the x_values strictly increasing for interpolation.
        rev_ratios = ratios[::-1]
        rev_speeds = SPEEDS[::-1]
        
        if target_ratio > ratios[0]:  # ratios[0] corresponds to 20 km/h (most efficient)
            print(f"\nResult: Target range is easily achievable at speeds lower than {SPEEDS[0]} km/h.")
            print(f"(Not enough calibration data to calculate exact speed below {SPEEDS[0]} km/h)")
            return
        elif target_ratio < ratios[-1]:  # ratios[-1] corresponds to 80 km/h (least efficient)
            print(f"\nResult: Insufficient capacity. Cannot achieve this range even at {SPEEDS[-1]} km/h.")
            return
        
        # Interpolate the required speed based on the target ratio
        estimated_speed = interpolate(target_ratio, rev_ratios, rev_speeds)
        required_power = get_power_for_speed(estimated_speed)
        
        print(f"\nResult:")
        print(f"- Target Range: {target_range:.1f} km")
        print(f"- Usable Capacity: {usable_capacity:.1f} Wh")
        print(f"- Estimated Average Speed: {estimated_speed:.1f} km/h")
        print(f"- Average Power Draw: ~{required_power:.1f} W")
        
    except ValueError:
        print("Error: Invalid numerical input.")


def main_menu():
    while True:
        print("\n" + "="*35)
        print("       E-Bike Power Calculator")
        print("="*35)
        print("1. Calculate range (km) by speed & capacity")
        print("2. Calculate required capacity by speed & range")
        print("3. Calculate average speed by capacity & range")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            calc_range()
        elif choice == '2':
            calc_capacity()
        elif choice == '3':
            calc_speed()
        elif choice == '4':
            print("Exiting calculator. Ride safe!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting calculator. Ride safe!")
        sys.exit(0)

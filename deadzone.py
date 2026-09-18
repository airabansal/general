def apply_deadzone(value: float, threshold: float = 0.08) -> float:
    """Returns 0.0 if the input value falls within the deadzone threshold."""
    if abs(value) < threshold:
        return 0.0
    return value

# Example Usage:
x_raw, y_raw = 0.04, -0.03  # Slight joystick drift
x = apply_deadzone(x_raw, threshold=0.08)  # Returns 0.0
y = apply_deadzone(y_raw, threshold=0.08)  # Returns 0.0

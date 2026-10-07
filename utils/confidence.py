"""Confidence and grounding utilities."""

def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    return max(min_val, min(max_val, value))

def format_percentage(value: float) -> str:
    return f"{value * 100:.0f}%"

def confidence_color(score: float) -> str:
    if score >= 0.85:
        return "#28a745"  # green
    elif score >= 0.65:
        return "#ffc107"  # yellow
    elif score >= 0.4:
        return "#fd7e14"  # orange
    else:
        return "#dc3545"  # red

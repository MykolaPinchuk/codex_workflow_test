from __future__ import annotations


def parse_param_string(value: str) -> dict[str, float]:
    if not value:
        return {}
    params: dict[str, float] = {}
    items = [item.strip() for item in value.split(",") if item.strip()]
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid param '{item}'. Expected key=value.")
        key, raw_value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"Invalid param '{item}'. Empty key.")
        try:
            params[key] = float(raw_value)
        except ValueError as exc:
            raise ValueError(f"Invalid value for '{key}': '{raw_value}'. Expected float.") from exc
    return params

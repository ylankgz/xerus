def parse_kwargs(raw_kwargs):
    """Parse key=value arguments into a dictionary"""
    parsed = {}
    for arg in raw_kwargs:
        if "=" not in arg:
            raise ValueError(f"Invalid argument format: {arg}")
        key, value = arg.split("=", 1)
        parsed[key] = value
    return parsed 
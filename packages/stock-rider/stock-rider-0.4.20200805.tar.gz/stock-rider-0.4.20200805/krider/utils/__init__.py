def str_to_bool(bool_str):
    if type(bool_str) is bool:
        return bool_str
    if not bool_str:
        return False
    return bool_str.lower() in ("yes", "true", "t", "1")

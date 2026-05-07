def verify_result(result):
    return isinstance(result, dict) and "error" not in result
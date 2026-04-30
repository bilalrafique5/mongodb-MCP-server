def verify_result(result):
    if not result:
        return False

    if isinstance(result, dict) and "error" in result:
        return False

    return True
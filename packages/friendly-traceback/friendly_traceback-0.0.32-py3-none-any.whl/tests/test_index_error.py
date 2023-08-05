import friendly_traceback


def test_index_error1():
    a = (1, 2, 3)
    b = [1, 2, 3]
    try:
        print(a[3], b[2])
    except Exception:
        friendly_traceback.explain(redirect="capture")
    result = friendly_traceback.get_output()
    assert "IndexError" in result
    return result


def test_index_error2():
    a = list(range(40))
    b = tuple(range(50))
    try:
        print(a[50], b[0])
    except Exception:
        friendly_traceback.explain(redirect="capture")
    result = friendly_traceback.get_output()
    assert "IndexError" in result
    return result


if __name__ == "__main__":
    print(test_index_error1())
    print(test_index_error2())

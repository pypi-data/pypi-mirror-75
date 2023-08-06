from ..executable import hello_world


def test_no_name():
    args = {"repeat": 1}

    # Nominode API calls your engine makes are logged
    # and returned with your function result, so you can
    # see what your engine did
    api_calls, results = hello_world(**args)
    assert results == (args["repeat"], f"Hello World")


def test_with_name():
    args = {"repeat": 3, "myname": "joe"}
    api_calls, results = hello_world(**args)
    assert results == (args["repeat"], f"Hello joe")

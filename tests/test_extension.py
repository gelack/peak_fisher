
def test_hello():
    import emzed.ext
    reload(emzed.ext)
    assert emzed.ext.peak_fisher.hello().startswith("hello")
    
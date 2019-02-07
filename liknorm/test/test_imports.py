import liknorm


def _get_import_names():
    import types

    names = []
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            names.append(val.__name__)
    return names


def _clean_up_import_names(names):
    to_ignore = set(["builtins", "types", "_pytest", "__builtin__"])
    return [n for n in names if n.split(".")[0] not in to_ignore]


# Make sure `import liknorm` does not import other packages indirectly.
def test_import_names():
    # Prevent the `unused name` warning
    assert hasattr(liknorm, "__version__")
    names = _get_import_names()
    names = set(_clean_up_import_names(names))
    assert names == set(["liknorm"])

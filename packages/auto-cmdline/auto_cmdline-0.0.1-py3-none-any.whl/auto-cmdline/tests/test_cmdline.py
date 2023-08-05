import cmdline


def test_project_defines_author_and_version():
    assert hasattr(cmdline, '__author__')
    assert hasattr(cmdline, '__version__')

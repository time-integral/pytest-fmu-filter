def test_invalid_fmu_filter_key(pytester):
    pytester.makepyfile("""
        import pytest

        @pytest.mark.fmu_filter(dummy=True)
        def test_invalid_fmu_filter_key(fmu):
            pass
    """)

    result = pytester.runpytest("--fmus=tests/data/hello_world.fmu", "-v")
    assert result.ret == 2

    result = pytester.runpytest("-v")
    assert result.ret == 1


def test_fmu_filter_undefined(pytester):
    """Test that no fmu_filter marker results in no FMU being loaded."""
    pytester.makepyfile("""
        import pytest

        def test_fmu_filter_undefined(fmu):
            assert fmu is not None
    """)

    result = pytester.runpytest(
        "--fmus", "tests/data/hello_world.fmu", "-v"
    )
    assert result.ret == 1

    result = pytester.runpytest(
        "--fmus", "tests/data/hello_world.fmu", "tests/data/hello_world2.fmu", "-v"
    )
    assert result.ret == 1

    result = pytester.runpytest("-v")
    assert result.ret == 1


def test_fmu_unrelated(pytester):
    """Test that no fmu_filter marker results in no FMU being loaded."""
    pytester.makepyfile("""
        import pytest

        def test_fmu_unrelated():
            assert True
    """)

    result = pytester.runpytest(
        "--fmus", "tests/data/hello_world.fmu", "-v"
    )
    assert result.ret == 0
    result = pytester.runpytest(
        "--fmus", "tests/data/hello_world.fmu", "tests/data/hello_world2.fmu", "-v"
    )
    assert result.ret == 0
    result = pytester.runpytest("-v")
    assert result.ret == 0
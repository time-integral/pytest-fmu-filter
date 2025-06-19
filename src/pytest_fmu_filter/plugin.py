import pytest
import pathlib

VALID_FMU_FILTER_KEYS = [
    "is_ME",
    "is_CS",
    "is_ME_and_CS",
    "with_inputs",
    "with_outputs",
    "name_contains",
    "custom"
]


def pytest_addoption(parser):
    group = parser.getgroup("fmus")
    group.addoption(
        "--fmus",
        help="FMU paths",
        nargs="+",
    )

def pytest_generate_tests(metafunc):
    """
    Generate tests based on the FMUs in the specified directory.
    """
    # Get commandline option for FMU paths
    fmus = metafunc.config.getoption("fmus")
    if fmus is None:
        # If no FMU paths are provided, skip the test generation
        return

    # Check if the metafunc has a 'fmu_filter' marker
    fmu_filter = metafunc.definition.get_closest_marker("fmu_filter")
    if fmu_filter is None:
        # If no fmu_filter marker is defined, skip the test generation
        return
    
    # Validate the fmu_filter marker arguments
    for key, _ in fmu_filter.kwargs.items():
        if key not in VALID_FMU_FILTER_KEYS:
            raise ValueError(
                f"Invalid 'fmu_filter' key: {key}. Valid keys are: {', '.join(VALID_FMU_FILTER_KEYS)}"
            )

        metafunc.parametrize("fmu", fmus, ids=[str(pathlib.Path(m).resolve()) for m in fmus])

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "fmu_filter: Filter FMUs based on specific criteria." # avoid warning about unknown markers
    )
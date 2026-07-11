import sys
import sysconfig


def test_runtime_is_conventional_cpython_314() -> None:
    assert sys.implementation.name == "cpython"
    assert sys.version_info[:2] == (3, 14)
    assert sysconfig.get_config_var("Py_GIL_DISABLED") != 1
    assert sys._is_gil_enabled()


def test_supported_dependencies_import() -> None:
    import agno
    import fastapi
    import psycopg
    import pydantic
    import sqlalchemy
    import uvicorn

    assert all((agno, fastapi, psycopg, pydantic, sqlalchemy, uvicorn))

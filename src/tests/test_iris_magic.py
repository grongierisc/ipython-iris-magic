import pytest
from sqlalchemy import create_engine,text
from iris_magic.iris_magic import IrisMagic

def test_create_engine():
    engine = create_engine("iris://superuser:SYS@localhost:51773/USER", connect_args={"timeout": 30}, pool=None)
    assert engine is not None
    with engine.connect() as conn:
        rs = conn.execute(text("SELECT 1"))
        for row in rs:
            assert row[0] == 1

def test_create_connection():
    magic = IrisMagic()
    connection_string = "iris://superuser:SYS@localhost:51773/USER"
    magic.create_connection(connection_string)
    assert magic.conn is not None
    assert magic.iris is not None

def test_create_connection_invalid_string():
    magic = IrisMagic()
    connection_string = "invalid_connection_string"
    with pytest.raises(Exception):
        magic.create_connection(connection_string)

def test_create_routine():
    magic = IrisMagic()
    magic.create_connection("iris://superuser:SYS@localhost:51773/USER")
    magic.create_routine()
    assert magic.iris.classMethodBoolean("%Routine", "Exists", "ExecCode")

def test_iris_cell():
    magic = IrisMagic()
    cell = """
    SET x = 1
    WRITE x
    """
    magic.iris_cell("iris://superuser:SYS@localhost:51773/USER", cell)
    # Add assertions to check the expected output
    assert True

if __name__ == "__main__":
    test_create_engine()
    test_create_connection()
    test_create_connection_invalid_string()
    test_create_routine()
    test_iris_cell()
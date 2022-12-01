# ipython-iris-magic

%%iris magic for IPython, can run ObjectScript command in Notebooks

## Installation

```bash
pip install ipython-iris-magic
```

## Usage

```python
%load_ext iris_magic
```

```python
%%iris iris://superuser:SYS@localhost:1972/USER 
set test = "toto"
zw test
```

Output:

```text
test="toto"
```


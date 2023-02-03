# ipython-iris-magic

%%iris magic for IPython, can run ObjectScript command in Notebooks.

It can be run in any Notebook and does not require any special setup on IRIS or the Notebook.

## Demo

<img width="1153" alt="image" src="https://user-images.githubusercontent.com/47849411/205066143-8273ad36-b148-4111-9525-4801ce341456.png">

As you can see, the first line load the magic, the second line connect to the server, the third line run the ObjectScript command.

All of this demo is in the example/Notebooks/Demo-Iris-Magic.ipynb

To run the demo run the following command in the root of the project:

```bash
docker-compose up
```

Then go to this url: http://127.0.0.1:8888/notebooks/Demo-Iris-Magic.ipynb

### Load the magic

```python
%load_ext iris_magic
```

### Connect to the server

```python
%%iris iris://superuser:SYS@localhost:1972/USER
```

### Run the ObjectScript command

```python
%%iris
Set x = 1
Write x
```
## Installation

In order to use this magic, you need to install the [ipython-iris-magic](https://pypi.python.org/pypi/ipython-iris-magic) package.

```bash
pip install ipython-iris-magic
```

All the dependencies will be installed automatically.



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


You can also use the magic to run SQL query.

### Load the magic

```python
%load_ext sql
```

/!\ You need to install the sql extension first.

The sql extension is not part of the standard IPython installation. You can install it with the following command:

```bash
pip install ipython-sql
```

### Connect to the server

```python
%sql iris://superuser:SYS@localhost:1972/USER
```

### Run the SQL query

```python
%sql SELECT 1
```

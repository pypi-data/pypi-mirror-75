
# More Black! - Denser Black formatting

This is s a fork of [the Black code formatter](https://github.com/psf/black)

### Problem

I love Black formatting because I agree with its formatting choices, but it does have one pathology: [Excessive indenting on data structures](https://github.com/psf/black/issues/626)

```python
schema = {
    "mappings": {
        "test": {
            "properties": {
                "one_value": {
                    "type": "keyword",
                    "store": True,
                }
            }
        }
    }
}
```

The pathology looks even worse for singleton lists; many lines can be wasted on lonely brackets:  

```python
my_method(
    [
        {
            "name": "a",
            "value": 42
        }
    ]
)
```


### Solution: More Black!

When there is only one property (or list item, or parameter), then do not make a new line.

```python
schema = {"mappings": {"test": {"properties": {"one_value": {
    "type": "keyword", 
    "store": True,
}}}}}

```

Singleton lists are especially dense. 

```python
my_method([{
    "name": "a",
    "value": 42
}])
```


## Usage

Please [read the official Black documentation at time of fork](https://github.com/psf/black/blob/537ea8df35b1004bdb228b483907fb5dd92e5257/README.md#usage)


## Development

Be sure you are in the `mo-black` main directory

Setup virtual environment

    python -m venv .venv
    source .venv/bin/activate

Install requirements 

    pip install -r requirements.txt
    pip install -r tests/requirements.txt

Set some environment variables

    export PYTHONPATH=src:.
    export SKIP_AST_PRINT=true

Run the tests 

    python -m unittest tests/test_black.py

Here is the same for Windows...

    c:\Python38\python -m pip install virtualenv
    c:\Python38\python -m virtualenv .venv             
    .venv\Scripts\activate
    pip install -r requirements.txt
    pip install -r tests\requirements.txt
    set PYTHONPATH=src;.
    set SKIP_AST_PRINT=true
    python -m unittest tests\test_black.py

### Upgrade `requirements.txt`

The `requirements.in` file is for humans to update.  Use `pip-compile` to update the locked `requirements.txt` file:

    pip install -r tests\requirements.txt
    pip-compile --upgrade --generate-hashes --output-file requirements.txt requirements.in
    pip install -r requirements.txt

### Development Installation

You can install `mo-black` from the main directory

    python.exe -m pip install .

# Local Resources

This project is easy attempt to emulate Java's Class.getResource() method.

It provides simple access to files that are 'reachable' from directories and/or zip files referenced
in PYTHONPATH.

## Usage

Example:

```python
from local_resources import Resource

with Resource("VERSION") as f:
    version = f.read()
```

It returns read-only file object in binary mode.

Aside of reading knowing files it provides 'list' method which is similar to `os.listdir(path)` with one 
caveat - directories are always returned with '/' appended:

```python
from local_resources import Resource

files_and_dirs = Resource("").list()

for f in files_and_dirs:
    if f.endswith("myfiles/to_print_on_screen"):
        print(f"Do something with path {f}")
    else:
        with Resource(f) as file:
            print(f"File {f}:")
            print(file.read().decode('utf-8'))
``` 

Note: when `list()' method is called there are no resources held after it finished, so there is no need
for `with` statement, nor cleaning up/closing resources at the end.

Note: for root of PYTHONPATH directories use `"""` or `"/"`: `Resource("").list()`.

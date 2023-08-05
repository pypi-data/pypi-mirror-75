import os
import json
from typing import List


def readlines(filename: str, strip_newline: bool = True) -> List:
    '''
# params
```txt
    filename File tobe read
    strip_newline If true strip the newline
```
# example
```python
def read_as_lines():
    lines1 = readlines(brother_path('cfg.txt'))
    print(f"lines1:{lines1}")
```
    '''
    with open(os.path.abspath(filename), 'r') as f:
        lines = f.readlines()

    if not strip_newline:
        return lines

    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip())
    return new_lines


def writelines(lines: List, filename: str, append_newline: bool = True) -> None:
    '''
# params
```txt
    lines Lines to write with
    filename File tobe write
    append_newline If true append a newline to each line
```
# example

code:
```python
def write_as_lines():
    lines = ['hello', 'ezflines']
    writelines(lines, brother_path('cfg.txt'))
```
output:

```txt
    cfg.txt:
    hello
    ezflines
```
    '''
    newlines = []
    for line in lines:
        if append_newline and not line.endswith('\n'):
            newlines.append(f"{line}\n")
        else:
            newlines.append(line)

    with open(filename, 'w') as f:
        f.writelines(newlines)


def readstr(filename: str) -> str:
    '''
# params
```txt
    filename File tobe read
```
# return

```txt
    a string
```
# example

code:
```python
def read_as_string():
    string = readstr(brother_path('cfg.txt'))
    print(f"read_as_string:\n{string}")

```
    '''
    with open(filename, 'r') as f:
        content = f.read()
    return content


def readjson(filename: str) -> dict:
    '''
# params
```txt
    filename File tobe read
```
# return
```txt
    a dict
```

# example

code:
```python
def read_as_json():
    json_obj = readjson(brother_path('cfg.json'))
    print(f"read_as_json: type = {type(json_obj)}")
    images = json_obj["images"]
    for image in images:
        print(f"read_as_json: image = {image}")

```
    '''
    content = readstr(filename)
    return json.loads(content)


def list_by_ext(root_dir, ext):
    '''
## params
```txt
    root_dir: Dir tobe walk
    ext: ExtName of files tobe find by.
```
## return 
```txt
    a List
```

## example

code:
```python

def find_pys():
    files = list_by_ext('.', 'py')
    index = 0
    width = len(f"{len(files)}")
    for file in files:
        print(f"[{index:0{width}}] {file}")
        index += 1
```
output:
```txt
    [00] ./setup.py
    [01] ./example/demo_files.py
    [02] ./example/demo_progress.py
    [03] ./tests/files.test.py
    [04] ./ezutils/files.py
    [05] ./ezutils/__init__.py
    [06] ./ezutils/progress.py
    [07] ./build/lib/ezutils/files.py
    [08] ./build/lib/ezutils/__init__.py
    [09] ./build/lib/ezutils/progress.py
```
    '''
    found_files = []
    for parent, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(ext.lower()):
                charset_file = os.path.join(parent, filename)
                found_files.append(charset_file)
    return found_files

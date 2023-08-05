# ezutils
Utils to save your time on python coding

Life is short we use ezutils !

## 1. Installing
```bash
pip install ezutils
```

## 2. Using files

### 2.1 readlines:

readlines(filename: str, strip_newline: bool = True) 

#### 2.1.1 params:
```txt
filename: the filename tobe read

strip_newline: strip the last space/newline


```
#### 2.1.2 return lines readed from file

#### 2.1.3 Example:

```python
    lines = readlines(brother_path('cfg.txt'))
    print(lines)
```


### 2.2 writelines:

writelines(lines: List, filename, append_newline: bool = True) 

#### 2.2.1 params:
```txt
lines: lines tobe written
filename: file tobe written
append_newline: add a newline to each line writtend
```
#### 2.2.2 return None

Example:

```python
    lines = ['hello', 'ezflines']
    writelines(lines, brother_path('cfg.txt'))
```

### 2.3 readstr:

readstr(filename: str) -> str

#### 2.3.1 params:
```txt
filename: file tobe read
```
#### 2.3.2 return None

### 2.4 readjson:

readjson(filename: str) -> dict

#### 2.4.1 params:
```txt
filename: file tobe read
```
#### 2.4.2 return dict from json parse


## 2.5 DEMO

example/demo_files.py
```python

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from ezutils.files import readlines, writelines, readstr, readjson, list_by_ext


def brother_path(filename): return os.path.join(
    os.path.dirname(__file__), filename)


def read_as_lines():
    lines1 = readlines(brother_path('cfg.txt'))
    print(f"lines1:{lines1}")
    '''
    lines1:['hello', 'ezflines']
    '''
    lines2 = readlines(brother_path('cfg.txt'), False)
    print(f"lines2:{lines2}")
    '''
    lines2:['hello\n', 'ezflines\n']
    '''


def write_as_lines():
    lines = ['hello', 'ezflines']
    writelines(lines, brother_path('cfg.txt'))
    '''
    cfg.txt:
    hello
    ezflines

    '''
    writelines(lines, brother_path('cfg_oneline.txt'), False)
    '''
    cfg_oneline.txt:
    helloezflines
    '''


def read_as_string():
    string = readstr(brother_path('cfg.txt'))
    print(f"read_as_string:\n{string}")


def read_as_json():
    json_obj = readjson(brother_path('cfg.json'))
    print(f"read_as_json: type = {type(json_obj)}")
    images = json_obj["images"]
    for image in images:
        print(f"read_as_json: image = {image}")


def find_pys():
    files = list_by_ext('.', 'py')
    index = 0
    width = len(f"{len(files)}")
    for file in files:
        print(f"[{index:0{width}}] {file}")
        index += 1


if __name__ == "__main__":
    write_as_lines()
    read_as_lines()
    read_as_string()
    read_as_json()
    find_pys()

```
## 3 Using progress

### 3.1 print_progress

print_progress(msg, current, max, max_width=60)

### Demo

example/demo_files.py

```python

#!/usr/bin/env python3
#demo_progress.py

import time

from ezutils.progress import print_progress

if __name__ == '__main__':
    max = 100
    for i in range(max + 1):
        print_progress("MSG:ABC(%d)" % i, i, max)
        time.sleep(0.01)
```
## TODO:

### pillow utils
add roundrect for pillow
see and ANTIALIAS  [circle_corner](https://www.pyget.cn/p/185266)

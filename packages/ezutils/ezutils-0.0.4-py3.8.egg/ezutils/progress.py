#!/usr/bin/env python3
import sys


def print_progress(current, max, msg='',  max_width=60):
    '''
## params:

```txt
    current: number current progress value
    max: number  The max progress value
    msg: string optional  Message show on progress bar.
    max_width: number optional The limit of the length of the progress bar .
```

## example:

print a colored progress bar:
```python
    max = 100
    for i in range(max + 1):
        print_progress(f"MSG:ABC({i})", i, max)
        time.sleep(0.01)
```
output:
```txt
MSG:ABC(3)                            [03.00%]
MSG:ABC(100)                          [ DONE ]
```
    '''
    # [Python如何输出带颜色的文字方法](https://www.cnblogs.com/easypython/p/9084426.html)
    padding = ' '
    if len(msg) > max_width:
        msg = f"{msg[0:max_width-3]}..."
    elif len(msg) < max_width:
        msg = f"{msg}{padding:{max_width-len(msg)}}"

    color_head = '\033[37;42m'
    color_div = '\033[37;44m'
    color_end = '\033[0m'

    rate = float(current)/float(max)
    progress = 100.0*rate
    done_width = int(max_width*rate)
    progress_str = "[ \033[32mDONE\033[0m ]" if progress == 100.0 else f"[{progress:05.02f}%]"

    sys.stdout.write(color_head)
    sys.stdout.write(f"{msg[0:done_width]}")
    sys.stdout.write(color_div)
    sys.stdout.write(f"{msg[done_width:]}")
    sys.stdout.write(color_end)

    sys.stdout.write(f"{progress_str}\r")
    if progress == 100.0:
        sys.stdout.write('\n')

    sys.stdout.flush()

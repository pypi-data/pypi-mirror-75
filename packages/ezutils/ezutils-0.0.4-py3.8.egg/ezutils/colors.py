import math


def hsv2rgb(h, s, v):
    '''
# params
```txt
    h Hue 0-360
    s Saturation 0.0-1.0
    v Value 0.0-1.0
    return (r,g,b)
```
# example
```python
def read_as_lines():
    lines1 = readlines(brother_path('cfg.txt'))
    print(f"lines1:{lines1}")
```
    '''
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def rgb2hsv(r, g, b):
    '''
# params
```txt
    r red   0-255
    g green 0-255
    b blue  0-255
    return (h,s,v)
```
# example
```python
def read_as_lines():
    lines1 = readlines(brother_path('cfg.txt'))
    print(f"lines1:{lines1}")
```
    '''
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

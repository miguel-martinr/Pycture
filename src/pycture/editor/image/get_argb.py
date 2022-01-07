import sys 

# get_argb receives a bgra or argb bytes object and returns a [a, r, g, b] list
if sys.byteorder == 'little':
    get_argb = lambda bgra: [bgra[3], bgra[2], bgra[1], bgra[0]]
else:
    get_argb = lambda argb: argb
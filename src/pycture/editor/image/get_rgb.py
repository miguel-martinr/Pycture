import sys 

# get_rgb receives a bgra or argb bytes object and returns a [r, g, b] list
if sys.byteorder == 'little':
    get_rgb = lambda bgra: [bgra[2], bgra[1], bgra[0]]
else:
    get_rgb = lambda argb: [argb[1], argb[2], argb[3]]
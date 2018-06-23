'''
generate a hex rgb color code depending on the input value
low value generates red
high value generates green
caps are 10 for low and 100 for high
'''

from numpy import interp as map

def rgg (value, min=10, max=100, invert=False):
  med = (max - min) / 2 + min

  r = int(map(value, [med, max], [255, 0]))
  g = int(map(value, [min, med], [0, 255]))

  if invert:
    r, g = g, r

  return '#%02x%02x%02x' % (r, g, 0)


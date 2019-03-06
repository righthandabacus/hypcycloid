from math import sin, cos, radians

import numpy as np
from PIL import Image, ImageDraw

DIMENSION = (500, 500) # coordinate origin at centre
RADIANS = np.pi / 180

def origin():
    """return the pixel coordinate of the cartesian coordinate origin"""
    return (DIMENSION[0] / 2, DIMENSION[1] / 2)

def pixelcoord(coordx, coordy):
    """convert cartesian coordinate to pixel coordinate"""
    ox, oy = origin()
    x, y = int(round(ox+coordx)), int(round(oy-coordy))
    return (x, y)

def circle(draw, centrex, centrey, radius, color="#000000FF"):
    """draw a hollow circle at cartesian coordinate
    """
    # convert cartesian centre to pixel centre
    cx, cy = pixelcoord(centrex, centrey)
    # top left and bottom right coordinates
    rect = [(cx-radius, cy-radius), (cx+radius, cy+radius)]
    # draw
    draw.arc(rect, 0, 360, color)

def fillcircle(draw, centrex, centrey, radius, color="#000000FF"):
    """draw a filled circle at cartesian coordinate
    """
    # convert cartesian centre to pixel centre
    cx, cy = pixelcoord(centrex, centrey)
    # top left and bottom right coordinates, must never reverse
    rect = [(cx-radius, cy-radius), (cx+radius, cy+radius)]
    # draw, same color for outline and fill
    draw.ellipse(rect, color, color)

def lines(draw, coordinates, width=1, color="#000000FF"):
    """draw a broken line"""
    coords = [pixelcoord(*c) for c in coordinates]
    draw.line(coords, color, width)

def makehyperframe(draw, radiusa, radiusb, radiusd, anglet):
    """hypercycloid"""
    # difference in radius
    rsum = radiusa + radiusb
    # sequence of angles from 0 up to t
    ts = np.arange(0, anglet+1, 1) # angles from 0 to t
    # coordinate of the outer circle
    centre = np.array([np.cos(ts * RADIANS), np.sin(ts * RADIANS)]).T * rsum
    # angle of the "dot"
    ds = rsum / radiusb * ts * RADIANS
    # coordinate of the "dot" w.r.t. the centre of the inner circle
    dotoffset = np.array([np.cos(ds), np.sin(ds)]).T * radiusd
    # actual coordinate of the "dot": this is the locus
    dot = centre - dotoffset
    # draw: big circle, small circle, the locus, radius, the dot
    circle(draw, 0, 0, radiusa)
    circle(draw, centre[-1][0], centre[-1][1], radiusb)
    lines(draw, dot, color="#FF0000FF")
    lines(draw, [centre[-1], dot[-1]])
    fillcircle(draw, dot[-1][0], dot[-1][1], 3, "#FF0000FF")

def makehypoframe(draw, radiusa, radiusb, radiusd, anglet):
    """hypocycloid"""
    # difference in radius
    rdelta = radiusa - radiusb
    # sequence of angles from 0 up to t
    ts = np.arange(0, anglet+1, 1) # angles from 0 to t
    # coordinate of the inner circle
    centre = np.array([np.cos(ts * RADIANS), np.sin(ts * RADIANS)]).T * rdelta
    # angle of the "dot"
    ds = rdelta / radiusb * ts * RADIANS
    # coordinate of the "dot" w.r.t. the centre of the inner circle
    dotoffset = np.array([np.cos(ds), -np.sin(ds)]).T * radiusd
    # actual coordinate of the "dot": this is the locus
    dot = centre + dotoffset
    # draw: big circle, small circle, the locus, radius, the dot
    circle(draw, 0, 0, radiusa)
    circle(draw, centre[-1][0], centre[-1][1], radiusb)
    lines(draw, dot, color="#FF0000FF")
    lines(draw, [centre[-1], dot[-1]])
    fillcircle(draw, dot[-1][0], dot[-1][1], 3, "#FF0000FF")

def hypoanimation(radiusa, radiusb, radiusd):
    images = []
    for angle in range(0, 360, 2):
        frame = Image.new("RGBA", DIMENSION, "#FFFFFFFF")
        draw = ImageDraw.Draw(frame)
        makehypoframe(draw, radiusa, radiusb, radiusd, angle)
        images.append(frame)
    return images

def hyperanimation(radiusa, radiusb, radiusd):
    images = []
    for angle in range(0, 360, 2):
        frame = Image.new("RGBA", DIMENSION, "#FFFFFFFF")
        draw = ImageDraw.Draw(frame)
        makehyperframe(draw, radiusa, radiusb, radiusd, angle)
        images.append(frame)
    return images

def main():
    images = hyperanimation(200, 50, 50)
    images[0].save("ani.gif", save_all=True, append_images=images[1:], duration=2, loop=1)

if __name__ == "__main__":
    main()

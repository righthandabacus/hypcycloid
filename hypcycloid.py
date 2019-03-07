import argparse
from math import sin, cos, radians, gcd
from typing import Tuple, List

import numpy as np
from PIL import Image, ImageDraw

RADIANS = np.pi / 180
DIMENSION = (500, 500) # coordinate origin at centre

def origin() -> Tuple[float, float]:
    """return the pixel coordinate of the cartesian coordinate origin"""
    return (DIMENSION[0] / 2, DIMENSION[1] / 2)

def pixelcoord(coordx: float, coordy: float) -> Tuple[int, int]:
    """convert cartesian coordinate to pixel coordinate"""
    ox, oy = origin()
    x, y = int(round(ox+coordx)), int(round(oy-coordy))
    return (x, y)

def circle(draw, centrex, centrey, radius, color="#AAAAAAFF") -> None:
    """draw a hollow circle

    Args:
        draw: ImageDraw object
        centrex, centrey: Cartesian coordinate of the circle centre
        radius: Radius, in pixels
        color: line color. RGBA color as recognized by ImageDraw object
    """
    # convert cartesian centre to pixel centre
    cx, cy = pixelcoord(centrex, centrey)
    # top left and bottom right coordinates
    rect = [(cx-radius, cy-radius), (cx+radius, cy+radius)]
    # draw
    draw.arc(rect, 0, 360, color)

def fillcircle(draw, centrex, centrey, radius, color="#AAAAAAFF") -> None:
    """draw a filled circle

    Args:
        draw: ImageDraw object
        centrex, centrey: Cartesian coordinate of the circle centre
        radius: Radius, in pixels
        color: fill color. RGBA color as recognized by ImageDraw object
    """
    # convert cartesian centre to pixel centre
    cx, cy = pixelcoord(centrex, centrey)
    # top left and bottom right coordinates, must never reverse
    rect = [(cx-radius, cy-radius), (cx+radius, cy+radius)]
    # draw, same color for outline and fill
    draw.ellipse(rect, color, color)

def lines(draw, coordinates: List[Tuple[float, float]], width=1, color="#AAAAAAFF") -> None:
    """draw line segments connecting a sequence of coordinates

    Args:
        draw: ImageDraw object
        coordinates: List of tuples of cartesian coordinates of points. Line
                     segments will be joining each consecutive points.
        width: line width in pixels
        color: line color. RGBA color as recognized by ImageDraw object
    """
    coords = [pixelcoord(*c) for c in coordinates]
    draw.line(coords, color, width)

def makeframe(draw, R, r, rho, t, phi, hypo=True):
    """draw one frame of hypotrochoid/hypertrochoid animation"""
    if hypo:
        Rr = R - r  # difference in radii
        i = 1
    else:
        Rr = R + r  # sum in radii
        i = -1
    # sequence of angles from 0 up to t
    tt = np.arange(0, t + 1, 1)
    # coordinates of the smaller circle at various angle
    centre = np.array([np.cos(tt * RADIANS), np.sin(tt * RADIANS)]).T * Rr
    # angles of the "dot"
    dd = (Rr / r * tt + phi) * RADIANS
    # coordinates of the "dot" w.r.t. the centre of the inner circle
    dotoffset = np.array([i * np.cos(dd), -np.sin(dd)]).T * rho
    # actual coordinates of the "dot": this is the locus
    dot = centre + dotoffset
    # draw: big circle, small circle, the locus, radius, the dot
    circle(draw, 0, 0, R)
    circle(draw, centre[-1][0], centre[-1][1], r)
    lines(draw, dot, color="#FF0000FF")
    lines(draw, [centre[-1], dot[-1]])
    fillcircle(draw, dot[-1][0], dot[-1][1], 3, "#FF0000FF")

def animation(R, r, rho, phi, hypo=True):
    """Create animation as sequence of images

    Returns:
        List of image objects
    """
    # compute the number of degrees to trace the locus
    N = int(360 * r / gcd(R, r))+1
    # draw frame by frame
    images = []
    for angle in range(0, N, 5):
        frame = Image.new("RGBA", DIMENSION, "#FFFFFFFF")
        draw = ImageDraw.Draw(frame)
        makeframe(draw, R, r, rho, angle, phi, hypo)
        images.append(frame)
    return images

def main():
    global DIMENSION
    # Arg parsing
    parser = argparse.ArgumentParser(
        description = "Hyp{o,er}trochoid GIF animation generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-W", "--width", default=DIMENSION[0], type=int, help="Image width in pixels")
    parser.add_argument("-H", "--height", default=DIMENSION[1], type=int, help="Height in pixels")
    parser.add_argument("-o", "--hypo", action="store_true", default=False, help="Draw hypotrohoid")
    parser.add_argument("-r", "--rollradius", dest="r", type=int, default=40, help="Radius of the rolling circle")
    parser.add_argument("-R", "--fixradius", dest="R", type=int, default=150, help="Radius of the fixed circle")
    parser.add_argument("-p", "--pointradius", dest="rho", type=int, default=40, help="Distance of the locus point to centre of rolling circle")
    parser.add_argument("-q", "--pointangle", dest="phi", type=int, default=0, help="Angle of the locus point from the contact point of the two circles")
    parser.add_argument("outfile", default="animation.gif", help="output filename")
    args = parser.parse_args()
    DIMENSION = (args.width, args.height)

    # drawing and save
    images = animation(args.R, args.r, args.rho, args.phi, args.hypo)
    images[0].save(args.outfile, save_all=True, append_images=images[1:], duration=2, loop=1)

if __name__ == "__main__":
    main()

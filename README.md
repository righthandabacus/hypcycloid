Generate animated GIF or animated WebP of the locus of a hypotrochoid/hypertrochoid


```
usage: hypcycloid.py [-h] [-W WIDTH] [-H HEIGHT] [-o] [-r R] [-R R] [-p RHO]
                     [-q PHI]
                     outfile

Hyp{o,er}trochoid GIF animation generator

positional arguments:
  outfile               output filename

optional arguments:
  -h, --help            show this help message and exit
  -W WIDTH, --width WIDTH
                        Image width in pixels (default: 500)
  -H HEIGHT, --height HEIGHT
                        Height in pixels (default: 500)
  -o, --hypo            Draw hypotrohoid (default: False)
  -r R, --rollradius R  Radius of the rolling circle (default: 40)
  -R R, --fixradius R   Radius of the fixed circle (default: 150)
  -p RHO, --pointradius RHO
                        Distance of the locus point to centre of rolling
                        circle (default: 40)
  -q PHI, --pointangle PHI
                        Angle of the locus point from the contact point of the
                        two circles (default: 0)
```

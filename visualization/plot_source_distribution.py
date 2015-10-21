# -*- coding: utf-8 -*-
# Based on vispy: gallery 10

import sys

import numpy as np
import vispy.scene
from vispy.scene import visuals
from vispy.visuals.transforms import STTransform

from crpropa import *
from shared_objects import *

def load_sources():
    return np.genfromtxt( sys.argv[1] ) / Mpc

def main():

    canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    sources = load_sources()
    scatter = add_points( view, sources )

    obsPosition = [ 118.34, 117.69, 119.2 ]
    add_observer( view, obsPosition, 1 )

    add_box( scatter )

    view.camera = 'turntable'  # or try 'arcball'

if __name__ == '__main__':
    import sys
    main()
    if sys.flags.interactive != 1:
        vispy.app.run()

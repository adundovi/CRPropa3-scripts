# -*- coding: utf-8 -*-
# Based on vispy: gallery 10

import sys

import numpy as np
import vispy.scene
from vispy.scene import visuals

from crpropa import *
from shared_objects import *

def load_detections():
    raw_data = np.genfromtxt( sys.argv[1] )
    return raw_data[:,5:5+3]

def main():

    canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    detections = load_detections()
    add_points( view, detections )

    view.camera = 'turntable'

if __name__ == '__main__':
    import sys
    main()
    if sys.flags.interactive != 1:
        vispy.app.run()

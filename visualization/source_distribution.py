# -*- coding: utf-8 -*-
# Based on vispy: gallery 10

import sys

import numpy as np
import vispy.scene
from vispy.scene import visuals
from vispy.visuals.transforms import STTransform

from crpropa import *

def load_sources():
    return np.genfromtxt( sys.argv[1] ) / Mpc

def put_sources( view, sources ):
    """ Scatter data
    """
    scatter = visuals.Markers()
    scatter.set_data( sources, edge_color=None, face_color=(1, 1, 1, .5), size=5 )

    view.add( scatter )


def put_observer( view, coords, radius, color='black', edge_color='red' ):
    """ Put the observer on the scene
        radius and coords in Mpc
    """

    observer = visuals.Sphere(radius=radius, method='latitude', parent=view.scene,
                              color=color, edge_color=edge_color)
    observer.transform = STTransform( translate=coords )

    # add a colored 3D axis for orientation
    axis = visuals.XYZAxis( parent=view.scene )
    axis.transform = STTransform( translate=[ c-1 for c in coords ] )

def main():

    canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()

    sources = load_sources()
    put_sources( view, sources )

    obsPosition = [ 118.34, 117.69, 119.2 ]
    put_observer( view, obsPosition, 1 )

    view.camera = 'turntable'  # or try 'arcball'

if __name__ == '__main__':
    import sys
    main()
    if sys.flags.interactive != 1:
        vispy.app.run()

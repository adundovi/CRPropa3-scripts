import numpy as np

import vispy.scene
from vispy.scene import visuals
from vispy.visuals.transforms import STTransform

def add_points( view, points, size=5 ):
    """ Scatter data given by the list of (x,y,z) coodinates
    """
    scatter = visuals.Markers()
    scatter.set_data( points, edge_color=None, face_color=(1, 1, 1, .5), size=size )

    view.add( scatter )

    return scatter

def add_observer( view,
                  coords = [ 118.34, 117.69, 119.2 ],
                  radius = 1,
                  color='black',
                  edge_color='red' ):
    """ Put the observer on the scene
        radius and coords in Mpc
    """

    observer = visuals.Sphere(radius=radius, method='latitude', parent=view.scene,
                              color=color, edge_color=edge_color)
    observer.transform = STTransform( translate=coords )

    return observer

def add_axes( view, coords = [ 118.34, 117.69, 119.2 ] ):
    # add a colored 3D axis for orientation

    axis = visuals.XYZAxis( parent=view.scene )
    axis.transform = STTransform( translate=[ c-1 for c in coords ] )

def add_box( view, size=132, offset=54 ):
    box_coord = np.array([[0, 0, 0],
                          [0, 1, 0],
                          [1, 1, 0],
                          [1, 0, 0],
                          [0, 0, 0],
                          [0, 0, 1],
                          [0, 1, 1],
                          [0, 1, 0],
                          [0, 0, 0],
                          [0, 1, 0],
                          [0, 1, 1],
                          [1, 1, 1],
                          [1, 1, 0],
                          [0, 1, 0]], dtype=np.float32)

    box_pos = box_coord*size + offset

    box = visuals.Line(pos=box_pos, color=(0.7, 0, 0, 1), method='gl',
                                      name='unit box', parent=view)


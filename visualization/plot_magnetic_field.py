# -*- coding: utf-8 -*-

import sys
import numpy as np

from vispy import app, scene
from vispy.scene import visuals
from vispy.util.filter import gaussian_filter
from vispy.visuals.transforms import STTransform


def put_observer( view, coords, radius, color='black', edge_color='blue' ):
    """ Put the observer on the scene
        radius and coords in Mpc
    """
    observer = visuals.Sphere(radius=radius, method='latitude', parent=view.scene,
                              color=color, edge_color=edge_color)
    observer.transform = STTransform( translate=coords )

def put_text( view, pos, text, font_size = 18 ):
    print text
    t = visuals.Text( text, parent=view, color='white')
    t.font_size = font_size
    t.pos = pos

def put_axes( view ):
    
    size = 20
    domain_x = ( 118.34-size/2, 118.34+size/2 )
    domain_y = ( 117.69-size/2, 117.69+size/2 )

    xax = scene.Axis(pos=[[-0.5, -0.5], [0.5, -0.5]], domain=domain_x, tick_direction=(0, -1),
                     font_size=16, axis_color='white', tick_color='white', text_color='white',
                     parent = view )
    xax.transform = scene.STTransform(translate=(0, 0, -0.2))

    yax = scene.Axis(pos=[[-0.5, -0.5], [-0.5, 0.5]], domain=domain_y, tick_direction=(-1, 0),
                     font_size=16, axis_color='white', tick_color='white', text_color='white',
                     parent= view )
    yax.transform = scene.STTransform(translate=(0, 0, -0.2))

    # missing Z ax - (not yet implemented in Vispy)

    # Add a 3D axis to keep us oriented
    #axis = scene.visuals.XYZAxis(parent=view.scene)

def main():
    canvas = scene.SceneCanvas(keys='interactive', bgcolor='black')
    view = canvas.central_widget.add_view()
    view.camera = scene.TurntableCamera(up='z', fov=60)

    z = np.loadtxt( sys.argv[1] ) # in T
    z *= 10**12 / 10 # rescale (10 pT, 10^-7 G) / 10

    text = "Max: %7.2fx10^-6 G" % z.max()
    put_text( view, (130, 20), text )
    text = "Min: %7.2fx10^-6 G" % z.min()
    put_text( view, (130, 45), text )
    text = "Avg: %7.2fx10^-6 G" % np.average(z)
    put_text( view, (130, 70), text )

    z = gaussian_filter(z, (10, 10)) * 10
    p1 = scene.visuals.SurfacePlot(z=z, color=(0.1, 0.1, 1, 0.9))
    p1.transform = scene.transforms.MatrixTransform()
    p1.transform.scale([1/249., 1/249., 1/249.])
    p1.transform.translate([-0.4, -0.4, 0])

    #obsPosition = Vector3d(118.34, 117.69, 119.2) * Mpc
    put_observer( view, (0,0,0), 1./20 )

    view.add(p1)
    put_axes( view.scene )
    p1._update_data()  # cheating.
    cf = scene.filters.ZColormapFilter('hot', zrange=(z.min(), z.max()))
    p1.attach(cf)

    canvas.show()

if __name__ == '__main__':
    main()
    if sys.flags.interactive == 0:
        app.run()

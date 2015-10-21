import sys
import numpy as np

import vispy
from vispy import scene, app
from vispy.scene import visuals

sys.path.append('../python_modules')
from crpropa import *
from shared_objects import add_box, add_observer
from network import RecvCandidateProperties

def load_detections():
    vec = srv.recv()
    x, y, z = vec.values()
    trajectories.append( [x,y,z] )
    return np.array( trajectories )

def update( ev ):
    scatter.set_data( load_detections(), edge_color=None, size=5 )
    view.camera = 'turntable'

trajectories = []

canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
scatter = visuals.Markers()

add_box( scatter )
add_observer( view )

view.add( scatter )

timer = app.Timer(connect=update, interval=0)
timer.start()

srv = RecvCandidateProperties("*:5000")

if __name__ == '__main__':
    if sys.flags.interactive != 1:
        app.run()

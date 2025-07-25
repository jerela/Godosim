"""
This Python script is a tool for visualizing generated images, and optionally, their annotations.
Basic usage: "python annotation_viewer.py --path PATH/TO/ROOT/FOLDER"
The root folder should contain the folders "annotations" and "images", as generated by Godosim.
To enable visualization of annotations, add flags like "--bodies", "--joints", "--markers" (or "-b", "-j", "-m") to show origins of bodies of the musculoskeletal model, positions of joints of the musculoskeletal model, and positions of virtual markers of the musculoskeletal model.
The size of the visualized marker represents its depth (larger circles are closer to the viewer).
Use z and x keys to browse images.
"""

import sys, getopt, os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from pandas import read_csv

# plot the RGB image
def plot_image(path):
    img = plt.imread(path)
    plt.gca().imshow(img)

# plot 2D keypoints such as the positions of body origins, joints, or virtual markers, and include depth information by making the annotation symbol greater when it's close and smaller when it's far from the camera
def plot_keypoints(idx, annotations, pattern, color, radius):
    cols = annotations.filter(like=pattern)
    
    xs = []
    ys = []
    zs = []

    # iterate through column names in the CSV file
    for col in cols:
        if col.endswith('_x'):
           xs.append(annotations[col][idx]) 
        elif col.endswith('_y'):
           ys.append(annotations[col][idx])
        elif col.endswith('_z'):
           zs.append(annotations[col][idx])

    # calculate the closest and furthest depth of keypoints for scaling the depth to [0,1] in the loop that follows
    z_min = min(zs)
    z_max = max(zs)
    
    for x,y,z in zip(xs,ys,zs):
        # scale depth to [0,1] such that 0 indicates closest depth and 1 indicates furthest depth
        z_scaled = (z-z_min)/(z_max-z_min)
        # calculate radius that is scaled according to the keypoint's distance to the camera (depth)
        radius_scaled = 0.5*radius + (1.0-z_scaled)*radius
        circ = Circle((x,y), radius=radius_scaled, facecolor='none', edgecolor=color, linestyle='--', linewidth=2)
        plt.gca().add_patch(circ)

# plot bounding box around the person
def plot_box(idx, annotations, color):
    cols = annotations.filter(like='bb_')
    
    xs = []
    ys = []
    ws = []
    hs = []
    
    for col in cols:
        if col.endswith('_x'):
           xs.append(annotations[col][idx]) 
        elif col.endswith('_y'):
           ys.append(annotations[col][idx])
        elif col.endswith('_w'):
           ws.append(annotations[col][idx])
        elif col.endswith('_h'):
           hs.append(annotations[col][idx])
   
    for x,y,w,h in zip(xs,ys,ws,hs):
        box = Rectangle(xy=(x,y), width=w, height=h, facecolor='none', edgecolor=color, linestyle='-', linewidth=2)
        plt.gca().add_patch(box)

def read_csv_table(path):
    print('Reading ', path)
    return read_csv(path)


# switch images by pressing z and x
def on_press(event):
    # we have to declare write access to variable 'idx' to increment and decrement it
    global idx
    if event.key == 'x':
        idx += 1
    elif event.key == 'z':
        idx -= 1
    # shorthand if statement to keep idx in range of existing data
    idx = 0 if idx < 0 else idx
    idx = len(annotations.index)-1 if idx == len(annotations.index) else idx
    # calls the function to redraw the image and overlaid annotations with the new idx
    redraw()

# initialize the figure and axis and connect the figure to the keyboard event listener
def prepare_figure():
    fig,ax = plt.subplots(1)
    fig.canvas.mpl_connect('key_press_event', on_press)
    # call redraw to show the first image
    redraw()
    return fig,ax
    
def redraw():
    # remove previous drawings
    plt.gca().clear()
    # get the name of the RGB image file and set it as the figure title
    file_name = annotations['file_names'][idx]
    plt.title(file_name)
    # plot RBG image and overlaid annotations
    plot_image(Path(path_root) / 'images/' / (file_name + '.jpg'))
    if display_joints:
        plot_keypoints(idx, annotations, pattern='jp_', color='b', radius=10)
    if display_bodies:
        plot_keypoints(idx, annotations, pattern='bp_', color='g', radius=10)
    if display_markers:
        plot_keypoints(idx, annotations, pattern='vm_', color='r', radius=10)
    plot_box(idx, annotations, color='k')

# globals
idx = 0
path_root = None
annotations = None
display_bodies = False
display_joints = False
display_markers = False

# parse cmd line args and set globals accordingly
def parse_arguments():
    global path_root, display_bodies, display_joints, display_markers
    n = len(sys.argv)
    
    argument_list = sys.argv[1:]
    # b for bodies, j for joints, m for markers, p for path
    opts_short = "bjmp:"
    opts_long = ["bodies", "joints", "markers", "path="]
    
    try:
        # parse arguments and values
        arguments, values = getopt.getopt(argument_list, opts_short, opts_long)
        
        for current_arg, current_val in arguments:
            if current_arg in ("-b", "--bodies"):
                display_bodies = True
            elif current_arg in ("-j", "--joints"):
                display_joints = True
            elif current_arg in ("-m", "--markers"):
                display_markers = True
            elif current_arg in ("-p", "--path"):
                path_root = current_val
                print(path_root)
                
    except getopt.error as err:
        print(str(err))

def main():
    global annotations
    
    parse_arguments()
    
    if path_root is None:
        print('Specify path to the folder with the images and annotations folder with --path path/to/folder')
        return
    
    annotations = read_csv_table(Path(path_root) / 'annotations/annotations.csv')
    
    plt.ion()
    fig,ax = prepare_figure()
    plt.show(block=True)

if __name__ == '__main__':
    main()
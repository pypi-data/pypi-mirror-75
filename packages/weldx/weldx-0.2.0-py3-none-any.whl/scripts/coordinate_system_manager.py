"""Test the coordinate system manager"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import xarray as xr
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from networkx.drawing.nx_agraph import graphviz_layout

import weldx.geometry as geo
import weldx.transformations as tf
import weldx.visualization as vs


def create_geometry():
    shape = geo.Shape()
    shape.add_line_segments([[-3, 1], [-1, 1], [0, 0], [1, 1], [3, 1]])
    profile = geo.Profile(shape)

    trace = geo.Trace(geo.LinearHorizontalTraceSegment(6))

    geometry = geo.Geometry(profile, trace)

    return geometry.rasterize(0.5, 0.5)


def get_color(node_name):
    if node_name == "base":
        return [0.5, 0.5, 0.5]
    elif node_name == "user frame":
        return [1, 1, 0]
    elif node_name == "specimen":
        return [0, 1, 0]
    elif node_name == "flange":
        return [0, 0, 1]
    elif node_name == "torch tcp":
        return [1, 0, 0]
    elif node_name == "camera":
        return [1, 0, 1]
    elif node_name == "scanner tcp":
        return [0, 1, 1]
    print(node_name)
    return None


def plot_graph(graph, title, tree=True):
    fig = plt.figure()
    ax = fig.gca()
    color_map = []
    for node in graph:
        color_map.append(get_color(node))
    if tree is True:
        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, font_weight="bold", node_color=color_map)
        ax.set_title(title)
    else:
        nx.draw(graph, with_labels=True, font_weight="bold", node_color=color_map)
        ax.set_title(title)


def plot_coordinate_system(lcs, ax, color, label):
    if "time" in lcs.coordinates.coords:
        print("time dependent")
        lcs = tf.LocalCoordinateSystem(
            orientation=lcs.orientation, coordinates=lcs.coordinates.data[2]
        )
    vs.plot_coordinate_system(lcs, ax, color=color, label=label)


def transform_to_reference_systems_and_plot(csm, reference_system, geometry_data):
    fig = plt.figure()
    ax = fig.gca(projection="3d")

    color = get_color(reference_system)
    vs.plot_coordinate_system(
        tf.LocalCoordinateSystem(), ax, color=color, label=reference_system
    )

    for node in csm.graph.nodes:
        if node != reference_system:
            color = get_color(node)
            label = None
            if color is not None:
                label = node
            plot_coordinate_system(
                csm.get_local_coordinate_system(node, reference_system),
                ax,
                color=color,
                label=label,
            )

    vs.set_axes_equal(ax)
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()
    ax.plot(x_limits, [0, 0], [0, 0], "k")
    ax.plot([0, 0], y_limits, [0, 0], "k")
    ax.plot([0, 0], [0, 0], z_limits, "k")
    color = get_color(reference_system)
    vs.plot_coordinate_system(tf.LocalCoordinateSystem(), ax, color=color)
    if reference_system != "specimen":
        geometry_data = csm.transform_data(geometry_data, "specimen", reference_system)
    ax.scatter(geometry_data[0], geometry_data[1], geometry_data[2])
    ax.legend()
    ax.set_title("Reference system: " + reference_system)
    return [fig, ax]


# Script -------------------------------------------------------------------------------

coordinates = np.array([[-4, 2, 3], [-4, 2, 4], [-4, 2, 15], [-4, 2, 15]], dtype=float)
times = pd.date_range("2020-03-04", periods=4, freq="S")
coordinates_flange = xr.DataArray(
    data=coordinates, dims=["time", "c"], coords={"time": times, "c": ["x", "y", "z"]}
)
coordinates_flange = coordinates_flange.astype(float)
# print(coordinates_flange)

# create some coordinate systems
tf_lcs = tf.LocalCoordinateSystem

lcs_user_frame_in_base = tf_lcs.from_euler("z", 90, True, coordinates=[-2, 1, 0])
lcs_specimen_in_user_frame = tf.LocalCoordinateSystem(coordinates=[-0.5, -0.5, -1])
lcs_flange_in_base = tf_lcs.from_euler(
    "yz", [90, 10], True, coordinates=coordinates_flange
)
lcs_torch_in_flange = tf.LocalCoordinateSystem(coordinates=[2, 0, 0])
lcs_camera_in_flange = tf_lcs.from_euler("z", -45, True, coordinates=[1, 1, 0])
lcs_scanner_in_flange = tf.LocalCoordinateSystem(coordinates=[0, 0, -1])

print(lcs_flange_in_base.coordinates)
print(lcs_flange_in_base.orientation)

# create and fill coordinate system manager
csm = tf.CoordinateSystemManager("base")
csm.add_coordinate_system("user frame", "base", lcs_user_frame_in_base)
csm.add_coordinate_system("specimen", "user frame", lcs_specimen_in_user_frame)
csm.add_coordinate_system("flange", "base", lcs_flange_in_base)
csm.add_coordinate_system("torch tcp", "flange", lcs_torch_in_flange)
csm.add_coordinate_system("camera", "flange", lcs_camera_in_flange)
csm.add_coordinate_system("scanner tcp", "flange", lcs_scanner_in_flange)


test = csm.get_local_coordinate_system("torch tcp", "base")
print(test.coordinates)
test2 = csm.get_local_coordinate_system("base", "torch tcp")
print(test2.coordinates)
# plot initial graph
# plot_graph(csm.graph, "Initial graph")


nx.drawing.draw_networkx(csm.graph)
plt.show()

# create geometry
geometry_data = create_geometry()

# # Do some transformations and plot
# [fig_0, ax_0] = transform_to_reference_systems_and_plot(csm, "base", geometry_data)
# # plot_graph(csm.graph, "After transformation to base", False)
# # [fig_1, ax_1] = transform_to_refernce_systems_and_plot(csm, "specimen", geometry_data)
# # plot_graph(csm.graph, "After transformation to specimen", False)
# # [fig_2, ax_2] = transform_to_refernce_systems_and_plot(csm, "flange", geometry_data)
# # plot_graph(csm.graph, "After transformation to flange", False)
# plt.show()

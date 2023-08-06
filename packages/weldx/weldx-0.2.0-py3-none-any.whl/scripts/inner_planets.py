import time

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import xarray as xr
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from networkx.drawing.nx_agraph import graphviz_layout
from scipy.spatial.transform import Rotation as Rot
from scipy.spatial.transform import Slerp

import weldx.transformations as tf
import weldx.utility as ut


def plot_graph(graph, title, tree=True):
    """

    Parameters
    ----------
    graph :

    title :

    tree :
        (Default value = True)

   """
    fig = plt.figure()
    ax = fig.gca()
    color_map = []
    for node in graph:
        color_map.append(color_by_name(node))
    if tree is True:
        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True, font_weight="bold", node_color=color_map)
        ax.set_title(title)
    else:
        nx.draw(graph, with_labels=True, font_weight="bold", node_color=color_map)
        ax.set_title(title)


def color_by_name(name):
    """

    Parameters
    ----------
    name :


   """
    if name == "mars":
        return [1, 0, 0]
    elif name == "sun":
        return [1, 1, 0]
    elif name == "2":
        return [0, 1, 0]
    elif name == "moon":
        return [0, 1, 1]
    elif name == "earth":
        return [0, 0, 1]
    else:
        return [1, 0, 1]


def create_orientations(angles, freq, date_start="2020-03-31"):
    """

    Parameters
    ----------
    angles :

    freq :

    date_start :
        (Default value = "2020-03-31")

   """
    times = pd.date_range(date_start, periods=len(angles), freq=freq)

    orientations = xr.DataArray(
        data=tf.rotation_matrix_z(np.array(angles) * 2 * np.pi),
        dims=["time", "c", "v"],
        coords={"time": times, "c": ["x", "y", "z"], "v": [0, 1, 2]},
    )
    return orientations.astype(float)


def create_coordinates(coordinates, freq, date_start="2020-03-31"):
    """

    Parameters
    ----------
    coordinates :

    freq :

    date_start :
        (Default value = "2020-03-31")

   """
    times = pd.date_range(date_start, periods=len(coordinates), freq=freq)

    coordinates = xr.DataArray(
        data=coordinates,
        dims=["time", "c"],
        coords={"time": times, "c": ["x", "y", "z"]},
    )
    return coordinates.astype(float)


def plot_coordinate_system(origin, orientation, axes, color=None, label=None):
    """

    Parameters
    ----------
    origin :

    orientation :

    axes :

    color :
        (Default value = None)
    label :
        (Default value = None)

   """

    p_0 = origin
    p_x = p_0 + orientation[:, 0]
    p_y = p_0 + orientation[:, 1]
    p_z = p_0 + orientation[:, 2]

    axes.plot([p_0[0], p_x[0]], [p_0[1], p_x[1]], [p_0[2], p_x[2]], "r")
    axes.plot([p_0[0], p_y[0]], [p_0[1], p_y[1]], [p_0[2], p_y[2]], "g")
    axes.plot([p_0[0], p_z[0]], [p_0[1], p_z[1]], [p_0[2], p_z[2]], "b")
    if color is not None:
        axes.plot([p_0[0]], [p_0[1]], [p_0[2]], "o", color=color, label=label)
    elif label is not None:
        raise Exception("Labels can only be assigned if a color was specified")


def plot_animation(
    coordinate_systems,
    ref_system,
    num_days,
    date_start="2020-03-31",
    freq="1D",
    plot_nodes=None,
):
    """

    Parameters
    ----------
    coordinate_systems :

    ref_system :

    num_days :

    date_start :
        (Default value = "2020-03-31")
    freq :
        (Default value = "1D")
    plot_nodes :
        (Default value = None)

   """
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    plt.show(block=False)
    time = pd.date_range(date_start, periods=num_days, freq=freq)
    if plot_nodes is None:
        plot_nodes = csm.graph.nodes

    for i in range(num_days):
        ax.clear()
        curr_time = pd.DatetimeIndex([time[i]])
        j = 0
        for node in plot_nodes:
            if node not in plot_nodes:
                continue
            if node == ref_system:
                lcs = tf.LocalCoordinateSystem()
            else:
                lcs = csm.get_local_coordinate_system(node, ref_system)
            lcs_int = lcs.interp_time(curr_time)

            plot_coordinate_system(
                lcs_int.origin.data[0],
                lcs_int.basis.data[0],
                ax,
                color_by_name(node),
                node + " in " + ref_system,
            )
            j += 1

        ax.set_xlim([-6, 6])
        ax.set_ylim([-6, 6])
        ax.set_zlim([-6, 6])
        ax.legend(loc="lower left")
        ax.set_title(str(i))
        plt.draw()
        plt.pause(0.001)


# script -------------------------------------------------------------------------------


def get_positions(num_positions, periods, distance):
    """

    Parameters
    ----------
    num_positions :

    periods :

    distance :


   """
    delta_angle = 360 / (num_positions)
    angles = np.arange(0, 360 * periods + 0.25 * delta_angle, delta_angle) * -1
    rot_matrices = tf.rotation_matrix_z(angles / 180 * np.pi)
    position_keys = rot_matrices[:, 0, :] * distance
    return position_keys


def get_rotations(periods):
    """

    Parameters
    ----------
    periods :


   """
    return np.arange(0, periods + 0.01, 0.25)


# create some time dependent coordinate systems
times = pd.date_range("2020-01-01", periods=10000, freq="1H")

rotations_earth = create_orientations(get_rotations(365), "6H", "2020-01-01")
coordinates_earth_position = create_coordinates(
    get_positions(20, 1, 3), "438H", "2020-01-01"
)
rotations_moon = create_orientations(get_rotations(10), "162H", "2020-01-01")
coordinates_moon = create_coordinates(get_positions(27, 10, 0.25), "24H", "2020-01-01")
rotations_mars = create_orientations(get_rotations(365), "369min", "2020-01-01")
coordinates_mars = create_coordinates(get_positions(24, 1, 6), "687H", "2020-01-01")

earth_position_in_sun = tf.LocalCoordinateSystem(origin=coordinates_earth_position)
earth_in_earth_position = tf.LocalCoordinateSystem(rotations_earth)
moon_in_earth_position = tf.LocalCoordinateSystem(
    basis=rotations_moon, origin=coordinates_moon
)
mars_in_sun = tf.LocalCoordinateSystem(basis=rotations_mars, origin=coordinates_mars)

# lcs_2_in_lcs_1 = lcs_2_in_lcs_1.interp_time(days)

csm = tf.CoordinateSystemManager("sun")
csm.add_coordinate_system("earth position", "sun", earth_position_in_sun)
csm.add_coordinate_system("earth", "earth position", earth_in_earth_position)
csm.add_coordinate_system("mars", "sun", mars_in_sun)
csm.add_coordinate_system("moon", "earth position", moon_in_earth_position)

# plot_graph(csm.graph, "graph")
# csm = csm.interp_time(csm.time_union())
csm = csm.interp_time(times)

plot_animation(csm, "moon", 365, "2020-01-01", "24H", ["sun", "earth", "moon", "mars"])

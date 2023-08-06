import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from scipy.spatial.transform import Rotation as Rot
from scipy.spatial.transform import Slerp

import weldx.transformations as tf
import weldx.utility as ut


def color_by_idx(idx):
    if idx == 0:
        return [1, 0, 0]
    elif idx == 1:
        return [1, 1, 0]
    elif idx == 2:
        return [0, 1, 0]
    elif idx == 3:
        return [0, 1, 1]
    elif idx == 4:
        return [0, 0, 1]
    else:
        return [1, 0, 1]


def create_orientations(angles, freq):
    times = pd.date_range("2020-03-31", periods=len(angles), freq=freq)

    orientations = xr.DataArray(
        data=tf.rotation_matrix_z(np.array(angles) * 2 * np.pi),
        dims=["time", "c", "v"],
        coords={"time": times, "c": ["x", "y", "z"], "v": [0, 1, 2]},
    )
    return orientations.astype(float)


def create_coordinates(coordinates, freq):
    times = pd.date_range("2020-03-31", periods=len(coordinates), freq=freq)

    coordinates = xr.DataArray(
        data=coordinates,
        dims=["time", "c"],
        coords={"time": times, "c": ["x", "y", "z"]},
    )
    return coordinates.astype(float)


def plot_coordinate_system(origin, orientation, axes, color=None, label=None):

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


def plot_animation(coordinate_systems, num_days):
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    plt.show(block=False)
    time = pd.date_range("2020-03-31", periods=num_days, freq="1D")

    for i in range(num_days):
        ax.clear()
        curr_time = pd.DatetimeIndex([time[i]])
        j = 0
        for lcs in coordinate_systems:
            orientation = xr_interpolate_orientation_time(lcs.basis, curr_time).data[0]
            coordinates = xr_interpolate_coordinates_time(lcs.origin, curr_time).data[0]

            plot_coordinate_system(
                coordinates, orientation, ax, color_by_idx(j), "lcs_" + str(j)
            )
            j += 1

        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        ax.legend(loc="lower left")
        plt.draw()
        plt.pause(0.001)


# relevant code ------------------------------------------------------------------------


def xr_interpolate_orientation_time(dsx, times_interp):
    if "time" not in dsx.coords:
        return dsx.expand_dims({"time": times_interp})
    rotations_key = Rot.from_matrix(dsx.data)
    times_key = dsx.time.astype(np.int64)
    rotations_interp = Slerp(times_key, rotations_key)(times_interp.astype(np.int64))
    return xr.DataArray(
        data=rotations_interp.as_matrix(),
        dims=["time", "c", "v"],
        coords={"time": times_interp, "c": ["x", "y", "z"], "v": [0, 1, 2]},
    )


def xr_interpolate_coordinates_time(dsx, times_interp):
    if "time" in dsx.coords:
        return dsx.interp({"time": times_interp})
    else:
        return dsx.expand_dims({"time": times_interp})


def timestamp_union(times):
    timestamp_union = times[0].astype(np.int64).data
    for i in np.arange(1, len(times)):
        timestamp_union = np.union1d(timestamp_union, times[i].astype(np.int64).data)
    return pd.to_datetime(timestamp_union)


def lcs_timestamp_union(lcs_0, lcs_1):
    times = []
    if "time" in lcs_0.basis.coords:
        times += [lcs_0.basis.time]
    if "time" in lcs_0.origin.coords:
        times += [lcs_0.origin.time]
    if "time" in lcs_1.basis.coords:
        times += [lcs_1.basis.time]
    if "time" in lcs_1.origin.coords:
        times += [lcs_1.origin.time]
    if len(times) == 0:
        return None
    else:
        return timestamp_union(times)


def lcs_add(lcs_l, lcs_r):

    timestamp_union = lcs_timestamp_union(lcs_l, lcs_r)
    if timestamp_union is None:
        assert False, "Not implemented"
    else:
        lcs_l_basis = xr_interpolate_orientation_time(lcs_l.basis, timestamp_union)
        lcs_r_basis = xr_interpolate_orientation_time(lcs_r.basis, timestamp_union)
        lcs_l_coord = xr_interpolate_coordinates_time(lcs_l.origin, timestamp_union)
        lcs_r_coord = xr_interpolate_coordinates_time(lcs_r.origin, timestamp_union)

    basis = ut.xr_matmul(lcs_r_basis, lcs_l_basis, dims_a=["c", "v"])
    origin = (
        ut.xr_matmul(
            lcs_r_basis, lcs_l_coord, dims_a=["c", "v"], dims_b=["c"], dims_out=["c"]
        )
        + lcs_r_coord
    )

    lcs = tf.LocalCoordinateSystem(basis, origin)
    return lcs


def lcs_add2(lcs_l, lcs_r):
    o = ut.xr_interp_like(lcs_l.origin, lcs_r.origin)
    b = ut.xr_interp_like(lcs_l.basis, lcs_r.basis)
    lcs_l = tf.LocalCoordinateSystem(b, o)
    basis = ut.xr_matmul(lcs_r.basis, lcs_l.basis, dims_a=["c", "v"])
    origin = (
        ut.xr_matmul(lcs_r.basis, lcs_l.origin, dims_a=["c", "v"], dims_b=["c"])
        + lcs_r.origin
    )
    return tf.LocalCoordinateSystem(basis, origin)


# script -------------------------------------------------------------------------------


# create some time dependent coordinate systems
days = pd.date_range("2020-03-31", periods=366, freq="1D")

rotations_1 = create_orientations([0, 0.25, 0.5, 0.75, 1], "3M")
rotations_1 = xr_interpolate_orientation_time(rotations_1, days)
rotations_2 = create_orientations([0, 1 / 3, 2 / 3, 1, 4 / 3, 5 / 3, 2], "2M")

coordinates_3 = create_coordinates([[2, 0, 1], [2, 0, -1], [-2, 0, -1]], "6M")
coordinates_4 = create_coordinates(
    [[0, 1, 0], [0, -1, 0], [0, 1, 0], [0, -1, 0], [0, 1, 0]], "3M"
)
coordinates_5 = create_coordinates([[1, 0, 0], [0, 2, 0], [0, 0, -1]], "6M")

lcs_1_in_base = tf.LocalCoordinateSystem(basis=rotations_1, origin=[0, 0, 1])
lcs_2_in_lcs_1 = tf.LocalCoordinateSystem(basis=rotations_2, origin=[1, 0, 0])
lcs_3_in_base = tf.LocalCoordinateSystem(origin=coordinates_3)
lcs_4_in_lcs_3 = tf.LocalCoordinateSystem(origin=coordinates_4)
lcs_5_in_lcs_2 = tf.LocalCoordinateSystem(origin=coordinates_5)


lcs_2_in_base = lcs_add(lcs_2_in_lcs_1, lcs_1_in_base)
lcs_4_in_base = lcs_add(lcs_4_in_lcs_3, lcs_3_in_base)
lcs_5_in_base = lcs_add(lcs_5_in_lcs_2, lcs_2_in_base)

times_interp = pd.date_range("2019-03-31", periods=15, freq="11M")


ref = ut.xr_interp_orientation_time(lcs_2_in_lcs_1.basis, times_interp)

print(ref.shape)
print(lcs_2_in_lcs_1.basis.shape)
assert np.allclose(ref[0], lcs_2_in_lcs_1.basis[0])
assert np.allclose(ref[-1], lcs_2_in_lcs_1.basis[-1])
assert np.all(ref.time == times_interp)

# times_interp2 = pd.date_range("2020-03-31", periods=2, freq="12M")

# print(times_interp[times_interp < times_interp2[0]])
# plot_animation(
#    [lcs_1_in_base, lcs_2_in_base, lcs_3_in_base, lcs_4_in_base, lcs_5_in_base], 365
# )

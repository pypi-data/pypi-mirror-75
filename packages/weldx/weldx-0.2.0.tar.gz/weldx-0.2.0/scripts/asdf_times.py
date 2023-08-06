from io import BytesIO
from pprint import pprint as pp

import asdf
import numpy as np
import pandas as pd

from weldx.asdf.extension import WeldxAsdfExtension, WeldxExtension

# Timedelta -------------------------------------------------------
td = pd.Timedelta("5m3ns")

# Timedelta -------------------------------------------------------
td_max = pd.Timedelta("106751 days 23:47:16.854775")

# TimedeltaIndex -------------------------------------------------------
tdi = pd.timedelta_range(start="-5s", end="25s", freq="3s")
tdi_nofreq = pd.TimedeltaIndex([0, 1e9, 5e9, 3e9])

# Timestamp -------------------------------------------------------
ts = pd.Timestamp("2020-04-15T16:47:00.000000001")
ts_tz = pd.Timestamp("2020-04-15T16:47:00.000000001", tz="Europe/Berlin")

# DatetimeIndex -------------------------------------------------------
dti = pd.date_range(start="2020-01-01", periods=5, freq="1D")
dti_tz = pd.date_range(start="2020-01-01", periods=5, freq="1D", tz="Europe/Berlin")
dti_infer = pd.DatetimeIndex(["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"])
dti_nofreq = pd.DatetimeIndex(["2020-01-01", "2020-01-02", "2020-01-04", "2020-01-05"])

# ASDF -------------------------------------------------------
filename = "asdf_times.yaml"
tree = dict(
    td=td,
    td_max=td_max,
    tdi=tdi,
    tdi_nofreq=tdi_nofreq,
    ts=ts,
    ts_tz=ts_tz,
    dti=dti,
    dti_infer=dti_infer,
    dti_nofreq=dti_nofreq,
)

# Write the data to a new file
with asdf.AsdfFile(
    tree,
    extensions=[WeldxExtension(), WeldxAsdfExtension()],
    ignore_version_mismatch=False,
) as ff:
    ff.write_to(filename)

# read back data from ASDF file
with asdf.open(
    filename, copy_arrays=True, extensions=[WeldxExtension(), WeldxAsdfExtension()]
) as af:
    data = af.tree

pp(data)

assert isinstance(data, dict)
for k, v in tree.items():
    assert np.all(data[k] == v)

# Write the data to buffer
with asdf.AsdfFile(
    tree,
    extensions=[WeldxExtension(), WeldxAsdfExtension()],
    ignore_version_mismatch=False,
) as ff:
    buff = BytesIO()
    ff.write_to(buff)
    buff.seek(0)

# read back data from ASDF file contents in buffer
with asdf.open(
    buff, copy_arrays=True, extensions=[WeldxExtension(), WeldxAsdfExtension()]
) as af:
    data = af.tree
assert isinstance(data, dict)

"""Run a complete test on asdf example setup from asdf_template_run.py."""

import asdf
import numpy as np
from pint import UnitRegistry

from weldx.asdf.extension import WeldxAsdfExtension, WeldxExtension
from weldx.asdf.tags.weldx.core.iso_groove import get_groove
from weldx.asdf.tags.weldx.custom.testclass import TestClass
from weldx.constants import WELDX_QUANTITY as Q_

obj = TestClass(
    prop1="ASDF",
    prop2=10,
    prop3=10,
    prop4=True,
    list_prop=["str1", "str2"],
    pint_prop=Q_(3, "m"),
    groove_prop=get_groove(
        groove_type="VGroove",
        **dict(t=Q_(8, "mm"), alpha=Q_(60, "deg"), c=Q_(4, "mm"), b=Q_(2, "mm")),
    ),
)

filename = "asdf_template.asdf"
tree = {"obj": obj}

# Write the data to a new file
with asdf.AsdfFile(
    tree,
    extensions=[WeldxExtension(), WeldxAsdfExtension()],
    ignore_version_mismatch=False,
) as ff:
    ff.write_to(filename, all_array_storage="inline")

# read back data from ASDF file
with asdf.open(
    filename, copy_arrays=True, extensions=[WeldxExtension(), WeldxAsdfExtension()]
) as af:
    data = af.tree
    print(data["obj"])

"""Examples for generating asdf schemas and classes."""

from weldx.asdf.utils import create_asdf_dataclass

create_asdf_dataclass(
    asdf_name="custom/testclass",
    asdf_version="1.0.0",
    class_name="TestClass",
    properties=[
        "prop1",
        "prop2",
        "prop3",
        "prop4",
        "list_prop",
        "pint_prop",
        "groove_prop",
    ],
    required=["prop1", "prop2", "prop3"],
    property_order=["prop1", "prop2", "prop3"],
    property_types=[
        "str",
        "int",
        "float",
        "bool",
        "List[str]",
        "pint.Quantity",
        "VGroove",
    ],
    description=[
        "a string",
        "",
        "a float",
        "a boolean value?",
        "a list",
        "a pint quantity",
        "a groove shape",
    ],
)

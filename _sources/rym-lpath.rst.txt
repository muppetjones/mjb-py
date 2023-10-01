`rym-lpath`
==================================

The `lpath` module serves two primary purposes:

1. Easier access for nested structures
2. Consistent interface regardless of access type

It's a simple enough premise, and possibly over-engineered, but `lpath` can help
lower code redundancy and complexity by reducing the number of try-except blocks
and specialized handling needed for nested structures.

The primary use is `lpath.get`. With `get`, you don't really need anything else
as you can add, remove, and update once you've pulled the appropriate item.


Usage
----------------------------------

.. automodule:: rym.lpath._get

.. automodule:: rym.lpath._set



API
----------------------------------

.. automodule:: rym.lpath
    :members:
    :imported-members:


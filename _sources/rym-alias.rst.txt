`rym-alias`
==================================

The `alias` module provides name wranging functionality.

IMO, far too many software projects are fragile or backwards incompatible
due to trivial name changes, such as "prod", "PROD", or "production".
These name variations may be due to different developers or different
data sources -- it shouldn't matter.

We could setup some AI service with NLP, but that's silly. We want things
easier, not magic. We want to be explicit about the things we alias so
that our users do not have to be.

Usage
----------------------------------

.. automodule:: rym.alias._alias

.. automodule:: rym.alias._aliasresolver


API
----------------------------------

.. automodule:: rym.alias
    :members:
    :imported-members:


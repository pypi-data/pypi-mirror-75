.. SPDX-License-Identifier: CC0-1.0
   SPDX-FileCopyrightText: 2020 Collabora, Ltd. and the Proclamation contributors

Config File JSON Schema
-----------------------

In most cases, you'll have a config file with a single project, and one or more
sections in that project. The following is the config file for Proclamation
itself, which is a fairly common usage:

.. literalinclude:: ../.proclamation.json
  :language: JSON

The full schema supports a number of optional properties, as well as multiple
projects in a single config file for more complex use cases. The full schema is
illustrated below. Note that bold property names indicate a required property.

.. jsonschema:: ../proclamation.schema.json

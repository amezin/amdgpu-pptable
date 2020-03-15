|Tests badge| |flake8 lint badge| |pypi badge|

AMDGPU PowerPlay table parser
=============================

A Python library that converts AMDGPU PowerPlay tables to ctypes structs.

Uses code generated from MIT-licensed AMDGPU Linux driver headers.

For a Qt GUI editor see `amdgpu-pptable-editor-qt <https://github.com/amezin/amdgpu-pptable-editor-qt>`_

Generating ctypes structs
-------------------------

Generated code is tracked in git, it is located in ``src/amdgpu_pptable/generated``.

To re-generate it (with, maybe, different kernel sources)::

$ tox -e generate-ctypes -- -k path/to/kernel/sources


.. |Tests badge| image:: https://github.com/amezin/amdgpu-pptable/workflows/Tests/badge.svg
   :target: https://github.com/amezin/amdgpu-pptable/actions?query=workflow%3ATests
.. |flake8 lint badge| image:: https://github.com/amezin/amdgpu-pptable/workflows/flake8%20lint/badge.svg
   :target: https://github.com/amezin/amdgpu-pptable/actions?query=workflow%3A%22flake8+lint%22
.. |pypi badge| image:: https://img.shields.io/pypi/v/amdgpu-pptable
   :target: https://pypi.org/project/amdgpu-pptable/

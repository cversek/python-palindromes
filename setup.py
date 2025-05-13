"""   
desc:  Build script for palindromes package.
auth:  Craig Wm. Versek (cversek@gmail.com)
date:  2025-05-13
notes: -build with "python setup.py build_ext --inplace"

logs:
- 2025-05-13: updated to use Cython >= 3.1.0
- 2011-03-27: initial version
"""
# import os
# import tomllib  # Python 3.11+
# from setuptools import setup, Extension
# from Cython.Build import cythonize

# # Project root
# here = os.path.abspath(os.path.dirname(__file__))

# ## Package include dir for Cython .pxd files
# #include_dir = os.path.join(here, "palindromes")

# # parse project metadata from pyproject.toml
# with open(os.path.join(here, "pyproject.toml"), "rb") as f:
#     config = tomllib.load(f)
# project_meta = config.get("project", {})

# pkg_name = project_meta.get("name")
# authors = project_meta.get("authors", [])
# if authors:
#     author_info = authors[0]
#     pkg_author = author_info.get("name", "")
#     pkg_author_email = author_info.get("email", "")
# else:
#     pkg_author = pkg_author_email = ""

# # # discover all .pyx modules under palindromes
# # glob_list = []
# # for dirpath, _, filenames in os.walk(include_dir):
# #     for fname in filenames:
# #         if fname.endswith(".pyx"):
# #             rel = os.path.relpath(os.path.join(dirpath, fname), here)
# #             glob_list.append(os.path.splitext(rel)[0].replace(os.path.sep, "."))

# # # build Extension objects with proper include_dirs
# # extensions = []
# # for module in glob_list:
# #     src = module.replace('.', os.path.sep) + ".pyx"
# #     extensions.append(
# #         Extension(
# #             name=module,
# #             sources=[src],
# #             include_dirs=[include_dir],       # only package dir
# #             extra_compile_args=["-O0", "-g", "-Wall"],
# #             extra_link_args=["-g"],
# #         )
# #     )

# # Hard‑coded list of your Cython modules
# extensions = [
#     Extension(
#         name="palindromes.dicttree",
#         sources=["palindromes/dicttree.pyx"],
#         include_dirs=["palindromes"],
#     ),
#     Extension(
#         name="palindromes.cursor",
#         sources=["palindromes/cursor.pyx"],
#         include_dirs=["palindromes"],
#     ),
# ]

# # Single setup() invocation with cythonize
# setup(
#     name         = pkg_name,
#     author       = pkg_author,
#     author_email = pkg_author_email,
#     packages     = [pkg_name],
#     ext_modules  = cythonize(
#         extensions,
#         compiler_directives={"language_level": "3"},
#         build_dir="build",
#     ),
# )

# Debug commands:
#   rm -rf build/ palindromes/*.c palindromes/*.so
#   pip install --use-pep517 -e .
#   pip install .[test]
#   pytest test/unittest_dicttree.py\

import os
from setuptools import setup, Extension
from Cython.Build import cythonize

here = os.path.abspath(os.path.dirname(__file__))

extensions = [
    Extension(
        "palindromes.dicttree",
        ["palindromes/dicttree.pyx"],
        include_dirs=[os.path.join(here, "palindromes")],
    ),
    Extension(
        "palindromes.cursor",
        ["palindromes/cursor.pyx"],
        include_dirs=[os.path.join(here, "palindromes")],
    ),
]

setup(
    name="palindromes",
    version="0.0.2a0",
    author="Craig Wm. Versek",
    author_email="cversek@gmail.com",
    packages=["palindromes"],
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),
    extras_require={
        "test": ["pytest>=7.4.0"],
    },
)

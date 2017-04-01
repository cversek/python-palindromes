"""   
desc:  Build script for palindromes package.
auth:  Craig Wm. Versek (cversek@physics.umass.edu)
date:  3/27/2011
notes: -build with "python setup.py build_ext --inplace"
"""
import sys, os, stat, commands
from setuptools import setup, Extension
#from distutils.core import setup
#from distutils.extension import Extension

# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except ImportError:
    print "You don't seem to have Cython installed. Please get a"
    print "copy from www.cython.org and install it"
    sys.exit(1)

# scan the 'dvedit' directory for extension files, converting
# them to extension names in dotted notation
def scandir(d, files=[]):
    for f in os.listdir(d):
        p = os.path.join(d, f)
        if os.path.isfile(p) and p.endswith(".pyx"):
            files.append(p.replace(os.path.sep, ".")[:-4])
        elif os.path.isdir(p):
            scandir(p, files)
    return files


# generate an Extension object from its dotted name
def makeExtension(ext_name):
    ext_basepath = ext_name.replace(".", os.path.sep)
    #this is a hack to force cythoning of .pyx -> .c files
    ext_pyx_filepath = '%s.pyx' % ext_basepath
    ext_c_filepath   = '%s.c'   % ext_basepath
    if not os.path.exists(ext_c_filepath) or (os.path.getmtime(ext_pyx_filepath) > os.path.getmtime(ext_c_filepath)):
        # For some reason, setup in setuptools does not compile
        # Cython files (!)  Do that manually...
        print "cythoning %s to %s" % (ext_pyx_filepath, ext_c_filepath)
        os.system("cython %s" % ext_pyx_filepath)
    return Extension(
        ext_name,
        [ext_pyx_filepath],
        include_dirs = ["."],   # adding the '.' to include_dirs is CRUCIAL!!
        extra_compile_args = ["-O3", "-Wall"],
        extra_link_args = ['-g'],
        #libraries = [],
        )

# get the list of extensions
EXT_NAMES = scandir("palindromes")

print "found Cython extensions:", EXT_NAMES

# and build up the set of Extension objects
EXTENSIONS = [makeExtension(name) for name in EXT_NAMES]

# finally, we can pass all this to distutils
setup(
      name         = "palindromes",
      version      = "0.0.1a",
      author       = "Craig Versek",
      author_email = "cversek@physics.umass.edu",
      packages     = ['palindromes'],
      ext_modules  = EXTENSIONS,
      cmdclass     = {'build_ext': build_ext},
      #data_files
)

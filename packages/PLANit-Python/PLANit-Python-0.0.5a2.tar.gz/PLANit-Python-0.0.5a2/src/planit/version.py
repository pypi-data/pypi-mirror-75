# version that matches the PLANit-Java version
# Used to:
# 1) Construct the correct name of the used PLANit-jar files
# 2) Construct the version of the Python module via setup.py (hence use of globals)
__planit_version__ = "0.0.5a2"
__py4j_version__ = "0.10.9"

class Version:
    """ access to global versions in OO style
    """
    planit = __planit_version__
    py4j = __py4j_version__
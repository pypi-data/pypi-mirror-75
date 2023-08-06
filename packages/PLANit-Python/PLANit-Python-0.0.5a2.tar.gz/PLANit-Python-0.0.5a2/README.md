# PLANitPy2J
Python component of the PLANit Java/Python interface. Cotnains all the functionality outlined in the user manual regarding PLANit-Python.

PLANitPy2J aims to provide a Python interface into the PLANit project allowing users to parse inputs, create projects, run projects, and persist results all via a Python shell while the underlying PLANit code utilizes the Java VM for its algorithms.

The interaction with Java is made available via a separate project PLANitJ2Py. In PLANitJ2Py we implemented the gateway that allows the interaction between Python and Java. When creating your PLANit-Python project, a java call is made to bootstrap the java side.

We utilise py4j (www.p4j.org) to establish the connection between Java and Python. On the Python side, we provide Python wrapper classes around the Java objects such that the user is not exposed to the Java internals.

For more information on PLANit such as the user the manual, licensing, installation, getting started, reference documentation, and more, please visit [https://trafficplanit.github.io/PLANitManual/](https://trafficplanit.github.io/PLANitManual/)  

# Getting Started

If you want to use PLANit-Python as a user, please refer to the online documentation. This readme is intended solely for developers.

# Dependency on Java Projects

There is a directory "share" which holds JAR files for the Java projects this repositry relies on.  The "share/planit" directory contains a single JAR file compiling all PLANit-Java resources needed for PLANitPy2J to work. the "share/py4j" directory contains the Py4J jar required to setup the interface between PLANit-Java and PLANit-Python.

Any changes to any of the PLANit-Java projects to support the Python side require you to recompile the Java project and place the updated jar in this directory for it to be available to PLANit-Python.

# Versioning

Whenever a change in version occurs for either the planit jars or the py4j jar, the new version(s) must be explicitly identified in this project. We do so in the `src/planit/version.py`. 

Make sure that our version numbering folllows the naming conventions outlined in [PEP0440](https://www.python.org/dev/peps/pep-0440/) because otherwise we are not able to distribute our version via pip. 

By updating the variables to the new version it ensures that:

1) The gateway bootstraps the Java entry point with the right jars in its classpath
2) The setup.py (see [Setup](./#setup)) that is used to create a binary release for pip include the right version number

Failing to do this will cause the runs to fail.

# Py4J

PLANitPy2J relies on Py4J for its interface with the underlying PLANit code which is programmed in Java. The Py4J code gateway and entry point are hidden from the user via the PLANit class which instantiates the Java gateway server by invoking an external subprocess call. The functionality of the gateway is provided in the Py4J jar file which is included in the "rsc" directory.

For more information on Py4J, please see [www.py4j.org](www.py4j.org)

# Conceptual differences compared to PLANit-Java

Current design choices for this Python based PLANit module include

* Only a single PLANit Python instance can be active as the Java interface is created statically. 
* Only a single traffic assignment, network, zoning, demands can be instantiated on the project. More advanced configurations currently require the use of the native Java code
* Only the native PLANit I/O format can be used, if you want to use a third-party/custom input/output format you'll have to use the native Java code instead
* Python Wrappers for the Java classes are utilized to ensure that Python coding conventions regarding methods/variables apply. Hence, the Python interface of PLANit is not a 1:1 copy of the Java source but rather a Pythonic interpretation geared towards maximum usability and minimum configuration 

# Current limitations and peculiarities

It seems that Py4j cannot deal with variable argument lists for methods. The reflection does not seem to work in those cases at least in case of the variable arguments being enums. Therefore avoid using those on the Java side at all times if they are exposed to the user on the Python side

## Dealing with the mapping of enums between Java and Python
It is not difficult to instantiate a Java enum using Py4J, however it has to go through the gateway instance like the following gateway.jvm.<java_packages>.<Enum_name>.<EnumField>. This is cumbersome and unintuitive from a user perspective which we want to avoid in our wrappers. Therefore we only want to use Python enums which then under the hood are converted into their Java counterpart and passed on. The problem is that constructing a Java enum depends on the named variable for the gateway which may change over the lifetime of this project. To avoid such dependencies we instead create all Java Enums on the Java side instead via PLANitJ2Py.createEnum(String canonicalEnumName, String EnumFieldName).

Each Python enum that mimics a Java enum we implement with an additional method java_class_name() (See PLANitEnums.py). We utilize the field value (string) and this method (java canonical class name) to pass on plain strings to the Java side which in turn creates the enum via reflection and returns it. The Enum is then passed in as a parameter to the underlying java call that is being made for the method at hand hiding all details from the user while still using the same conceptual approach as we do in the Java source.

```Python
planIt.assignment.activate_output(OutputType.LINK)
```

with 

```Python
class OutputType(Enum):
    LINK = "LINK"
    
    def java_class_name(self) -> str:
        return "org.planit.output.OutputType"   
```

In activate_output we then call the java side to create the enum and pass on the method call

```Python
    def activate_output(self, output_type : OutputType):
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(),output_type.value)
        self._java_counter_part.activateOutput(output_type_instance)
```

While the Java side creates the enum via reflection

```Java
    public Enum createEnum(String enumCanonicalName, String EnumEntryName) throws ClassNotFoundException, PlanItException {
        Class<?> enumClass = Class.forName(enumCanonicalName);
        if(!enumClass.isEnum()) {
            throw new PlanItException("Class is not an enum");
        }
        return Enum.valueOf((Class<Enum>)enumClass,EnumEntryName);        
    }
```

# Developing for PLANitPy2J

## Preparation

How to install Py4j as a module on your Python installation is discussed in detail on <https://www.py4j.org/install.html>

How to install Python can be found on <https://www.python.org/downloads/>. We are currently using Python version 3.7, but the code has been tested on Python 3.6.

## Testing and running PLANitPy2J in Python

If PLANitPy2J is to be run from the command line, Python must be installed on the computer.  If it is to be run from Eclipse, the PyDev plugin must also be installed.

Make sure that the py4j version used in J2Py and this project are the same as the one used in your local python installation when you intend to run planit-python scripts outside of your IDE.

The Python code uses the following Python libraries:

* Py4j
* Pandas
* unittest
* traceback

Install these onto your computer using Python's "pip install" facility if you have not already done so. Similarly, install pip if you haven't already done so.

An example is made available under src/examples/basic/basic.py.  It uses src/examples/basic/input as it project directory, and a macroscopicinput.xml input file is located in this directory. It contains a very simple network with three origins and destinations without any route choice, shaped in the form of a triangle (Tipi). It can be used to test if the PLANitPython interface is setup correctly.

The file `test_suite.py` in the testcases/ dir of the project runs several Python unit tests. This script uses the `test_utils.py file` (in the test_util package) to set up PLANit runs from Python.  

To run `test_suite.py` from Eclipse using PyDev, right-click it and select Run as/Python unit-test.  To run from the command prompt, navigate to the directory where it is stored (<path_of_project>/src/tests) and enter "python test_suite.py".

The tests in test_suite.py use XML input files and CSV comparison files in  sub-directories of the directory "testcases".  The testcases are a subset of the equiavlent Java test cases.
 
As mentioned, All Python unit tests have a Java equivalent in the PLANitIO repo. However there are far fewer unit tests in Python than in Java.  Whereas the Java unit tests are intended to verify that the model results are correct for a variety of inputs, the Python unit tests exists to verify that the Python interface sends the correct values and/or calls to the Java side.

The `__init__()` method of the PLANit.py class can take an argument project_path which tells it where to find the XML input file and put the CSV output files. If the project_path argument is omitted, the current directory (i.e. where the PLANit.py file is located) is used.

# Creating a Setup

A separate readme is created to guide developers on how to create a new setup/installer for PLANit-Python. It is unlikely anyone else that contributors to the project will ever need to look at it, but the interested reader can find it under `SETUP_README.md`

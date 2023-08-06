import re
import os
import sys

from planit import Version

class GatewayConfig(object):   

    # Currently we provide the paths for the local environment AND production environment
    # TODO there should be a mechanism such that we only need one type of definition
    
    RELEASE_SHARE_PATH = os.path.join(os.path.split(sys.executable)[0], 'share')
    IDE_SHARE_PATH = os.path.join('..', '..', 'share')
    # VENV (virtual environment) for Python erroneously results in sys.executable pointing NOT to the root
    # directory of the virtual environment, but to ./Scripts. Hence, we must account for that by alos looking
    # one directory upward.
    # This (as far as I know) is a bug in venv!
    VENV_RELEASE_SHARE_PATH = os.path.join(os.path.split(sys.executable)[0], '..', 'share')
    
    PLANIT_SHARE = os.path.join('planit', '*')
    PY4J_SHARE = os.path.join('py4j', '*')
    
    # the main entry point of the Java gateway implementation for PLANit
    JAVA_GATEWAY_WRAPPER_CLASS =  'org.planit.python.PLANitJ2Py'
    
    
class GatewayState(object):
    #Create a static variable which flags if the java server already is running or not
    gateway_is_running = False
    planit_java_process = None
    # The actual gateway to pass on requests to once the gateway server is known to be running
    python_2_java_gateway = None
    # will contain reference to the Java project instance once the gateway is up and running        
    planit_project = None 


class GatewayUtils(object):
 
    @staticmethod
    def to_camelcase(s):
            """ convert a Python style string into a Java style string regarding method calls and variable names. Especially useful to avoid
            having to call Java functions as Java functions but one can call them as Python functions which are dynamically changed to their
            Java counterparts
            """
            return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s) 


import os

from py4j.java_gateway import get_field
from planit import GatewayUtils
from planit import GatewayState
from planit import OutputType
from planit import RouteIdType
from planit import OutputProperty
from planit import PhysicalCost
from planit import VirtualCost
from planit import Smoothing

class BaseWrapper(object):
    """ Base wrapper class which always holds a java counter part instance and a generic way to pass on method calls to the encapsulated 
        Java instance. This allows one to use the Python naming conventions, i.e. get_x instead of getX() this is automatically catered for
        in these wrappers.
    """

    def __init__(self, java_counterpart):
        """Top-level constructor which defines the Java counterpart to each wrapper
            :param   the Java counterpart to the current object
        """
        self._java_counterpart = java_counterpart

    def __getattr__(self, name):
        """All methods invoked on the assignment wrapper are passed on to the Java equivalent class after transforming the method to
        Java style coding convention
        """            
        def method(*args): #collects the arguments of the function 'name' (wrapper function within getattr)    
            java_name = GatewayUtils.to_camelcase(name)
            # pass all calls on to the underlying PLANit project java class which is obtained via the entry_point.getProject call
            if( args ):
                return getattr(self._java_counterpart, java_name)(*args)
            else:
                return getattr(self._java_counterpart, java_name)()               
        return method
    
    @property
    def java(self):
        """ access to the underlying Java object if required
        """
        if (self._java_counterpart == None):
            raise Exception("No Java counterpart has been found for " + self.__class__.__name__)
        return self._java_counterpart 
    
    def field(self, fieldName):
        """ collect a publicly available member on the java object
        """
        return get_field(self.java, fieldName)

class AssignmentWrapper(BaseWrapper):
    """ Wrapper around the Java traffic assignment builder class instance
    """
    
    def __init__(self, java_counterpart, network_instance):
        super().__init__(java_counterpart)
        self._output_configuration = OutputConfigurationWrapper(self.get_output_configuration()) # collect the output configuration from Java
        self._gap_function = GapFunctionWrapper(self.get_gap_function()) # collect the gap function from Java
        self._network_instance = network_instance
        self._physical_cost_instance = BPRCostWrapper(self.get_physical_cost(), self._network_instance) 
        self._virtual_cost_instance = VirtualCostWrapper(self.get_virtual_cost()) 
        self._smoothing = SmoothingWrapper(self.get_smoothing())
        
        # initialize in case they have defaults available
        #=======================================================================
        # self._link_output_type_configuration = LinkOutputTypeConfigurationWrapper(self._output_configuration.get_output_type_configuration(self.__create_java_output_type(OutputType.LINK)))
        # self._origin_destination_output_type_configuration = OriginDestinationOutputTypeConfigurationWrapper(self._output_configuration.get_output_type_configuration(self.__create_java_output_type(OutputType.OD)))   
        # self._path_output_type_configuration = PathOutputTypeConfigurationWrapper(self._output_configuration.get_output_type_configuration(self.__create_java_output_type(OutputType.PATH)))
        #=======================================================================
        
        for output_type in OutputType:
            output_type_instance = self.__create_java_output_type(output_type)
            if self.is_output_type_active(output_type_instance):
                if output_type.value == "LINK":
                    self._link_output_type_configuration = LinkOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
                elif output_type.value == "OD":
                    self._origin_destination_output_type_configuration = OriginDestinationOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
                elif output_type.value == 'PATH':
                    self._path_output_type_configuration = PathOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
        
        
        
    def __create_java_output_type(self, output_type):
        """ create an output type enum suitable to pass to java 
        """   
        return GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(), output_type.value)
    
    def set(self, assignment_component):
        """ Configure an assignment component on this assignment instance. Note that all these go via the traffic assignment builder in Java
            although we hide that on the Python side to not over-complicate things for the average user. We accept PhysicalCost, VirtualCost and 
            Smoothing choices at this point
        """    
        
        if isinstance(assignment_component, PhysicalCost):
            if (assignment_component == PhysicalCost.BPR):
                self._physical_cost_instance = BPRCostWrapper(self.create_and_register_physical_cost(assignment_component.value), self._network_instance) 
            else:
                raise Exception('Unrecognized link cost function ' + assignment_component.type + ' cannot be set on assignment instance')
        elif isinstance(assignment_component, VirtualCost):
            self._virtual_cost_instance = VirtualCostWrapper(self.create_and_register_virtual_cost(assignment_component.value))
        elif isinstance(assignment_component, Smoothing):
            self._smoothing_instance = SmoothingWrapper(self.create_and_register_smoothing(assignment_component.value))
        else:
            raise Exception('Unrecognized component ' + assignment_component.type + ' cannot be set on assignment instance')
         
    def activate_output(self, output_type : OutputType):
        """ Activate different output types on the assignment. 
            Pass on to Java not as an Enum as Py4J does not seem to properly handle this at this stage
            instead we pass on the enum string which on the Java side is converted into the proper enum instead           
            :param output_type Python enum of available output types
        """ 
        # collect an enum instance by collecting the <package>.<class_name> string from the Output type enum
        output_type_instance = self.__create_java_output_type(output_type)
        if not self.is_output_type_active(output_type_instance):
            if output_type.value == "LINK":
                self._link_output_type_configuration = LinkOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
            elif output_type.value == "OD":
                self._origin_destination_output_type_configuration = OriginDestinationOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
            elif output_type.value == 'PATH':
                self._path_output_type_configuration = PathOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
            else:
                raise ValueError("Attempted to deactivate unknown output type " + output_type.value)     
    
    def deactivate_output(self, output_type: OutputType):   
        """Deactivate specified output type on the assignment
        :param output_type Output type to be deactivated
        """ 
        output_type_instance = self.__create_java_output_type(output_type)
        if self.is_output_type_active(output_type_instance):
            if output_type.value == "LINK":
                self._link_output_type_configuration = LinkOutputTypeConfigurationWrapper(self._java_counterpart.deactivateOutput(output_type_instance))
            elif output_type.value == "OD":
                self._origin_destination_output_type_configuration = OriginDestinationOutputTypeConfigurationWrapper(self._java_counterpart.deactivateOutput(output_type_instance))
            elif output_type.value == 'PATH':
                self._path_output_type_configuration = PathOutputTypeConfigurationWrapper(self._java_counterpart.deactivateOutput(output_type_instance))
            else:
                raise ValueError("Attempted to activate unknown output type " + output_type.value)     
  
    @property
    def gap_function(self):
        """Access to current gap function
        """
        return self._gap_function
    
    @property
    def link_configuration(self):
        """Access to current link output type configuration, if not activated, it is activated so it can be configured
        """
        self.activate_output(OutputType.LINK)
        return self._link_output_type_configuration
    
    @property
    def od_configuration(self):
        """Access to current origin-destination output type configuration, if not activated, it is activated so it can be configured
        """
        self.activate_output(OutputType.OD)
        return self._origin_destination_output_type_configuration
    
    @property
    def output_configuration(self):
        """Access to current output configuration
        """
        return self._output_configuration    
    
    @property
    def path_configuration(self):
        """Access to current path output type configuration, if not activated, it is activated so it can be configured
        """
        self.activate_output(OutputType.PATH)
        return self._path_output_type_configuration
           
    @property
    def physical_cost(self):
        """Access to the physical cost wrapper
        """
        return self._physical_cost_instance
    
    @property
    def smoothing(self):
        """Access to the smoothing wrapper
        """
        return self._smoothing_instance    
    
    @property
    def virtual_cost(self):
        """Access to the virtual cost wrapper
        """
        return self._virtual_cost_instance
    
    
class DemandsWrapper(BaseWrapper):
    """ Wrapper around the Java Demands class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)    
        
class GapFunctionWrapper(BaseWrapper):
    """ Wrapper around the Java GapFunction class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        self._stop_criterion = StopCriterionWrapper(self.get_stop_criterion())  # collect the stop criterion from Java
        
    @property
    def stop_criterion(self):
        return self._stop_criterion

class InitialCostWrapper(BaseWrapper):
    """ Wrapper around the Java initial cost class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class LinkSegmentWrapper(BaseWrapper):
    """ Wrapper around the Java LinkSegments class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class LinkSegmentsWrapper(BaseWrapper):
    """ Wrapper around the Java LinkSegments class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class LinkSegmentExpectedResultsDtoWrapper(BaseWrapper):
    """ Wrapper around the Java Link Segment Expected Results DTO class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class MacroscopicLinkSegmentWrapper(BaseWrapper):
    """ Wrapper around the MacroscopicLinkSegmentType class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)      
 
class MacroscopicLinkSegmentTypeWrapper(BaseWrapper):
    """ Wrapper around the MacroscopicLinkSegmentType class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)      
 
class MacroscopicNetworkWrapper(BaseWrapper):
    """ Wrapper around the Java physical network class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class MemoryOutputIteratorWrapper(BaseWrapper):
    """Wrapper class around MemoryOutputIterator class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
       
class ModeWrapper(BaseWrapper):
    """ Wrapper around the Java mode class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class ModesWrapper(BaseWrapper):
    """ Wrapper around the Java modes class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class OutputConfigurationWrapper(BaseWrapper):
    """ Wrapper around the Java output configuration class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
 
class OutputFormatterWrapper(BaseWrapper):
    """ Wrapper around the Java OutputFormatter wrapper class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class OutputTypeConfigurationWrapper(BaseWrapper): 
    """ Wrapper around the Java link output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
    def add(self, output_property : OutputProperty):
        """Add an output type property to the current output type configuration
        """
        output_property_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_property.java_class_name(), output_property.value)
        self._java_counterpart.addProperty(output_property_instance)
        
    def remove(self, output_property : OutputProperty):
        """Remove an output type property from the current output type configuration
        """
        output_property_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_property.java_class_name(), output_property.value)
        return self._java_counterpart.removeProperty(output_property_instance)
        
    def remove_all_properties(self):
        self._java_counterpart.removeAllProperties()
        
class PhysicalCostWrapper(BaseWrapper):
    """ Wrapper around the Java physical cost class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
  
class PlanItInputBuilderWrapper(BaseWrapper):
    """ Wrapper around the Java InputBuilderListener class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)    
  
class SmoothingWrapper(BaseWrapper):
    """ Wrapper around the Java Smoothing class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class StopCriterionWrapper(BaseWrapper):
    """ Wrapper around the Java StopCriterion class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
    
class TimePeriodWrapper(BaseWrapper):
    """ Wrapper around the Java time period class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class TimePeriodsWrapper(BaseWrapper):
    """ Wrapper around the Java time periods class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class VirtualCostWrapper(BaseWrapper):
    """ Wrapper around the Java assignment class instance
    """    
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class ZoningWrapper(BaseWrapper):
    """ Wrapper around the Java Zoning class instance
    """    
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class BPRCostWrapper(PhysicalCostWrapper):
    """Wrapper around the BPRLinkTravelTimeCost instance
    """
    
    def __init__(self, java_counterpart, network_instance):
        super().__init__(java_counterpart)
        self._network_instance = network_instance
        modes_counterpart = self._network_instance.field("modes")
        self._modes_instance = ModesWrapper(modes_counterpart)
        link_segments_counterpart = self._network_instance.field("linkSegments")
        self._link_segments_instance = LinkSegmentsWrapper(link_segments_counterpart)
        
    def set_default_parameters(self, alpha, beta, mode_external_id=None, link_segment_type_external_id=None):
        """Set the default BPR functions parameters 
        :param alpha value of alpha parameter
        :param beta value of beta parameter
        :param mode_external_id if included, default parameters only apply to this mode
        :param link_segment_type_external_id if included, default parameters apply to this link segment type and mode
        """
        if (mode_external_id == None):
            self._java_counterpart.setDefaultParameters(alpha, beta)
        else:
            mode_counterpart = self._modes_instance.get_mode_by_external_id(mode_external_id, True)
            if (link_segment_type_external_id == None):
                self._java_counterpart.setDefaultParameters(mode_counterpart, alpha, beta)
            else:
                link_segment_type_counterpart = self._network_instance.get_macroscopic_link_segment_type_by_external_id(link_segment_type_external_id, True)
                link_segment_type_instance = MacroscopicLinkSegmentTypeWrapper(link_segment_type_counterpart)
                self.setDefaultParameters(link_segment_type_instance.java, mode_counterpart, alpha, beta)
                
    def set_parameters(self, alpha, beta, mode_external_id, link_segment_external_id):
        """Set the default BPR functions parameters 
        :param alpha value of alpha parameter
        :param beta value of beta parameter
        :param mode_external_id, parameters only apply to this mode
        :param link_segment_external_id, parameters apply to this link segment 
        """        
        link_segment_counterpart = self._link_segments_instance.get_link_segment_by_external_id(link_segment_external_id, True)
        link_segment_instance = LinkSegmentWrapper(link_segment_counterpart)
        mode_counterpart = self._modes_instance.get_mode_by_external_id(mode_external_id, True)
        self._java_counterpart.setParameters(link_segment_instance.java, mode_counterpart, alpha, beta)

class MemoryOutputFormatterWrapper(OutputFormatterWrapper):
    """ Wrapper around the Java PlanItOutputFormatter class instance
    """
    
    def __init__(self, java_counterpart, demands_instance, network_instance):
        """
        :param self this object
        :param java_counterpart Java counterpart for MemoryOutputFormatter object
        :param project_instance the instance of the project being run
        """
        super().__init__(java_counterpart)
        self._demands_instance = demands_instance
        self._network_instance = network_instance
                   
    def iterator(self, mode_external_id, time_period_external_id, no_iterations, output_type):
        """Return the  wrapper for MemoryOutputIterator object for this MemoryOutputFormatter
        :param mode_external_id the external Id of the current mode
        :param time_period_external_id the external Id of the current time period
        :param no_iterations the iteration the output iterator applies to
        :param output_type the output type for the current output
        :return the wrapper for the memory output iterator
        """
        time_periods_counterpart = self._demands_instance.field("timePeriods")
        time_periods = TimePeriodsWrapper(time_periods_counterpart)
        time_period_counterpart = time_periods.get_time_period_by_external_id(time_period_external_id, True);
        time_period = TimePeriodWrapper(time_period_counterpart)        
        modes_counterpart = self._network_instance.field("modes")
        modes = ModesWrapper(modes_counterpart)
        mode_counterpart = modes.get_mode_by_external_id(mode_external_id, True)
        mode = ModeWrapper(mode_counterpart)       
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(), output_type.value)
        memory_output_iterator_counterpart = self._java_counterpart.getIterator(mode.java, time_period.java, no_iterations, output_type_instance)
        memory_output_iterator = MemoryOutputIteratorWrapper(memory_output_iterator_counterpart)
        return memory_output_iterator
   
    def get_position_of_output_value_property(self, output_type, output_property):
        """Returns the position in the results array of the specified output value property
        :param output_type the output type for the current output
        :param output_property the specified output value property
        :result the position in the results array of the specified property
        """
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(), output_type.value)
        output_property_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_property.java_class_name(), output_property.value)
        position = self._java_counterpart.getPositionOfOutputValueProperty(output_type_instance, output_property_instance)
        return position
    
    def get_position_of_output_key_property(self, output_type, output_property):
        """Returns the position in the results array of the specified output key property
          :param output_type the output type for the current output
          :param output_property the specified output property
          :result the position in the results array of the specified key property
        """
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(), output_type.value)
        output_property_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_property.java_class_name(), output_property.value)
        position = self._java_counterpart.getPositionOfOutputKeyProperty(output_type_instance, output_property_instance)
        return position
        
class PlanItOutputFormatterWrapper(OutputFormatterWrapper):
    """ Wrapper around the Java PlanItOutputFormatter class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        # Initialize the output project path to the current run directory
        # Modellers may overwrite this default later
        project_path = os.getcwd()
        self.set_output_directory(project_path)        
              
class LinkOutputTypeConfigurationWrapper(OutputTypeConfigurationWrapper):
    """ Wrapper around the Java link output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
       
class OriginDestinationOutputTypeConfigurationWrapper(OutputTypeConfigurationWrapper):
    """ Wrapper around the Java origin-destination output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

    def activate(self, od_skim_sub_output_type):
        """Activate an OD skim output type
        """
        od_skim_sub_output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(od_skim_sub_output_type.java_class_name(), od_skim_sub_output_type.value)
        self._java_counterpart.activateOdSkimOutputType(od_skim_sub_output_type_instance)
 
    def deactivate(self, od_skim_sub_output_type):
        """Deactivate an OD skim output type
        """
        od_skim_sub_output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(od_skim_sub_output_type.java_class_name(), od_skim_sub_output_type.value)
        self._java_counterpart.deactivateOdSkimOutputType(od_skim_sub_output_type_instance)         
        
class PathOutputTypeConfigurationWrapper(OutputTypeConfigurationWrapper):
    """ Wrapper around the Java path output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
    def set_path_id_type(self,  route_id_type : RouteIdType):
        route_id_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(route_id_type.java_class_name(), route_id_type.value)
        self._java_counterpart.setPathIdType(route_id_type_instance)
import os
import pandas as pd
from planit import TrafficAssignment
from planit import OutputType
from planit import OutputProperty
from planit import RouteIdType
from planit import OutputFormatter
from planit import ODSkimSubOutputType
from builtins import staticmethod

class PlanItHelper:
    
    @staticmethod
    def run_test5(plan_it, max_iterations, epsilon, description, output_type_configuration_option, project_path=None, deactivate_file_output=False):
        """Top-level method which runs unit test case 5
        :param plan_it PLANit object (with any required initial costs already defined
        :param max_iterations the maximum number of iterations for the current unit test
        :param epsilon the convergence epsilon for the current unit test
        :param description the name to be used to identify input and output files
        :param output_type_configuration_option used to specify which properties to remove from link output type configuration
        :param project_path directory of XML input file (if omitted, defaults to None which will make methods use the current directory)
        :param deactivate_file_output if True, deactivate the file output formatter and store results in memory only
        """        
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)         
        plan_it.assignment.physical_cost.set_default_parameters(0.8, 4.5, 2, 1)

        # TODO : Add a unit test which testsX plan_it.assigment.physical_cost.set_default_parameters()
        # testRouteChoiceCompareWithOmniTRANS5() is a  good one for this
        #plan_it.assignment.set(VirtualCost.FIXED)
        #plan_it.assignment.set(Smoothing.MSA)
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.activate_output(OutputType.LINK)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)
  
        if output_type_configuration_option == 1:
            plan_it.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)
        elif output_type_configuration_option == 2:
            plan_it.assignment.link_configuration.remove(OutputProperty.DOWNSTREAM_NODE_EXTERNAL_ID)
            plan_it.assignment.link_configuration.remove(OutputProperty.UPSTREAM_NODE_EXTERNAL_ID)
  
        plan_it.assignment.activate_output(OutputType.OD)
        plan_it.assignment.od_configuration.deactivate(ODSkimSubOutputType.NONE)
        plan_it.assignment.od_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.od_configuration.remove(OutputProperty.RUN_ID)
        plan_it.assignment.activate_output(OutputType.PATH)
        plan_it.assignment.path_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
         
        plan_it.activate(OutputFormatter.MEMORY)
        if deactivate_file_output:
            plan_it.deactivate(OutputFormatter.PLANIT_IO)
        else:
            plan_it.output.set_xml_name_root(description)                
            plan_it.output.set_csv_name_root(description)     
            if (project_path is not None):  
                plan_it.output.set_output_directory(project_path)
        plan_it.run()
        return plan_it
   
    @staticmethod
    def run_mode_test(plan_it, max_iterations, epsilon, description, output_type_configuration_option, project_path=None, deactivate_file_output=False):
        """Top-level method which runs unit mode test
        :param plan_it PLANit object (with any required initial costs already defined
        :param max_iterations the maximum number of iterations for the current unit test
        :param epsilon the convergence epsilon for the current unit test
        :param description the name to be used to identify input and output files
        :param output_type_configuration_option used to specify which properties to remove from link output type configuration
        :param project_path directory of XML input file (if omitted, defaults to None which will make methods use the current directory)
        :param deactivate_file_output if True, deactivate the file output formatter and store results in memory only
        """        
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)         
        # TODO : Add a unit test which testsX plan_it.assigment.physical_cost.set_default_parameters()
        # testRouteChoiceCompareWithOmniTRANS5() is a  good one for this
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.activate_output(OutputType.LINK)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)
  
        if output_type_configuration_option == 1:
            plan_it.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)
        elif output_type_configuration_option == 2:
            plan_it.assignment.link_configuration.remove(OutputProperty.DOWNSTREAM_NODE_EXTERNAL_ID)
            plan_it.assignment.link_configuration.remove(OutputProperty.UPSTREAM_NODE_EXTERNAL_ID)
  
        plan_it.assignment.activate_output(OutputType.OD)
        plan_it.assignment.od_configuration.deactivate(ODSkimSubOutputType.NONE)
        plan_it.assignment.od_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.od_configuration.remove(OutputProperty.RUN_ID)
        plan_it.assignment.activate_output(OutputType.PATH)
        plan_it.assignment.path_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
         
        plan_it.activate(OutputFormatter.MEMORY)
        if deactivate_file_output:
            plan_it.deactivate(OutputFormatter.PLANIT_IO)
        else:
            plan_it.output.set_xml_name_root(description)                
            plan_it.output.set_csv_name_root(description)     
            if (project_path is not None):  
                plan_it.output.set_output_directory(project_path)
                
        plan_it.assignment.physical_cost.set_default_parameters(0.8, 4.5, 1, 1)
        link_segment_external_id = 3
        mode_external_id = 1 
        plan_it.assignment.physical_cost.set_parameters(1.0, 5.0, mode_external_id, link_segment_external_id)       
                
        plan_it.run()
        return plan_it
 
    @staticmethod
    def run_test(plan_it, max_iterations, epsilon, description, output_type_configuration_option, project_path=None, deactivate_file_output=False):
        """Top-level method which runs unit tests
        :param plan_it PLANit object (with any required initial costs already defined
        :param max_iterations the maximum number of iterations for the current unit test
        :param epsilon the convergence epsilon for the current unit test
        :param description the name to be used to identify input and output files
        :param output_type_configuration_option used to specify which properties to remove from link output type configuration
        :param project_path directory of XML input file (if omitted, defaults to None which will make methods use the current directory)
        :param deactivate_file_output if True, deactivate the file output formatter and store results in memory only
        """        
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)         
        # TODO : Add a unit test which testsX plan_it.assigment.physical_cost.set_default_parameters()
        # testRouteChoiceCompareWithOmniTRANS5() is a  good one for this
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.activate_output(OutputType.LINK)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)
  
        if output_type_configuration_option == 1:
            plan_it.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)
        elif output_type_configuration_option == 2:
            plan_it.assignment.link_configuration.remove(OutputProperty.DOWNSTREAM_NODE_EXTERNAL_ID)
            plan_it.assignment.link_configuration.remove(OutputProperty.UPSTREAM_NODE_EXTERNAL_ID)
  
        plan_it.assignment.activate_output(OutputType.OD)
        plan_it.assignment.od_configuration.deactivate(ODSkimSubOutputType.NONE)
        plan_it.assignment.od_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.od_configuration.remove(OutputProperty.RUN_ID)
        plan_it.assignment.activate_output(OutputType.PATH)
        plan_it.assignment.path_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
         
        plan_it.activate(OutputFormatter.MEMORY)
        if deactivate_file_output:
            plan_it.deactivate(OutputFormatter.PLANIT_IO)
        else:
            plan_it.output.set_xml_name_root(description)                
            plan_it.output.set_csv_name_root(description)     
            if (project_path is not None):  
                plan_it.output.set_output_directory(project_path)
        plan_it.run()
        return plan_it
  
    @staticmethod
    def run_test_with_zero_flow_outputs(plan_it, max_iterations, epsilon, description, output_type_configuration_option, project_path=None, deactivate_file_output=False):
        """Top-level method which runs unit tests with zero flow outputs included
        :param plan_it PLANit object (with any required initial costs already defined
        :param max_iterations the maximum number of iterations for the current unit test
        :param epsilon the convergence epsilon for the current unit test
        :param description the name to be used to identify input and output files
        :param output_type_configuration_option used to specify which properties to remove from link output type configuration
        :param project_path directory of XML input file (if omitted, defaults to None which will make methods use the current directory)
        :param deactivate_file_output if True, deactivate the file output formatter and store results in memory only
        """        
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)         
        # TODO : Add a unit test which testsX plan_it.assigment.physical_cost.set_default_parameters()
        # testRouteChoiceCompareWithOmniTRANS5() is a  good one for this
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.output_configuration.set_persist_zero_flow(True)
        
        plan_it.assignment.activate_output(OutputType.LINK)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)
  
        if output_type_configuration_option == 1:
            plan_it.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)
        elif output_type_configuration_option == 2:
            plan_it.assignment.link_configuration.remove(OutputProperty.DOWNSTREAM_NODE_EXTERNAL_ID)
            plan_it.assignment.link_configuration.remove(OutputProperty.UPSTREAM_NODE_EXTERNAL_ID)
  
        plan_it.assignment.activate_output(OutputType.OD)
        plan_it.assignment.od_configuration.deactivate(ODSkimSubOutputType.NONE)
        plan_it.assignment.od_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.od_configuration.remove(OutputProperty.RUN_ID)
        plan_it.assignment.activate_output(OutputType.PATH)
        plan_it.assignment.path_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
         
        plan_it.activate(OutputFormatter.MEMORY)
        if deactivate_file_output:
            plan_it.deactivate(OutputFormatter.PLANIT_IO)
        else:
            plan_it.output.set_xml_name_root(description)                
            plan_it.output.set_csv_name_root(description)     
            if (project_path is not None):  
                plan_it.output.set_output_directory(project_path)
        plan_it.run()
        return plan_it

    @staticmethod
    def run_test_without_activating_outputs(plan_it, max_iterations, epsilon, description, output_type_configuration_option, project_path=None, deactivate_file_output=False):
        """Top-level method which runs unit tests without activating output configurations (these should come on automatically)
        :param plan_it PLANit object (with any initial costs already defined)
        :param max_iterations the maximum number of iterations for the current unit test
        :param epsilon the convergence epsilon for the current unit test
        :param description the name to be used to identify input and output files
        :param output_type_configuration_option used to specify which properties to remove from link output type configuration
        :param project_path directory of XML input file (if omitted, defaults to None which will make methods use the current directory)
        :param deactivate_file_output if True, deactivate the file output formatter and store results in memory only
        """
        
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)
         
        # TODO : Add a unit test which testsX plan_it.assigment.physical_cost.set_default_parameters()
        # testRouteChoiceCompareWithOmniTRANS5() is a  good one for this
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)
  
        if output_type_configuration_option == 1:
            plan_it.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)
        elif output_type_configuration_option == 2:
            plan_it.assignment.link_configuration.remove(OutputProperty.DOWNSTREAM_NODE_EXTERNAL_ID)
            plan_it.assignment.link_configuration.remove(OutputProperty.UPSTREAM_NODE_EXTERNAL_ID)
  
        #Note that OutputType.OD is deactivated, check later that no OD output file is created
        plan_it.assignment.activate_output(OutputType.OD)
        plan_it.assignment.deactivate_output(OutputType.OD)
        
        plan_it.assignment.path_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
         
        plan_it.activate(OutputFormatter.MEMORY)
        if deactivate_file_output:
            plan_it.deactivate(OutputFormatter.PLANIT_IO)
        else:
            plan_it.output.set_xml_name_root(description)                
            plan_it.output.set_csv_name_root(description)     
            if (project_path is not None):  
                plan_it.output.set_output_directory(project_path)
 
        plan_it.run()
        plan_it.assignment.activate_output(OutputType.OD)
        return plan_it

    
    @staticmethod
    def delete_file(output_type : OutputType, description, file_name, project_path=None):
        """Delete an output file
        :param output_type type of the output file (link, origin-destination or path)
        :param description root name of the output file
        :param project_path directory of the output file
        """
        if project_path == None:
            project_path = os.getcwd()
        full_file_name = PlanItHelper.create_full_file_name(output_type, project_path, description, file_name)
        os.remove(full_file_name)
        
    @staticmethod
    def create_full_file_name(output_type : OutputType, project_path, description, file_name):
        """Create the long name of the output file (containing results created by the current test run)
        :param output_type type of the output file (link, origin-destination or path)
        :param description root name of the output file
        :param project_path directory of the output file
        :param file_name name of the file of standard results
        :return the name of the file containing the test results
        """
        type_name = None
        if output_type.value == "LINK":
            type_name = 'Link'
        elif output_type.value == "OD":
            type_name = 'Origin-Destination'
        else:
            type_name = "Path"
            
        full_file_name = project_path 
        full_file_name += "\\" 
        full_file_name +=  type_name
        full_file_name +=  "_" 
        full_file_name +=  "RunId_0_"
        full_file_name +=  description 
        full_file_name +=  "_" 
        full_file_name += file_name
        return full_file_name
    
    @staticmethod
    def create_short_file_name(output_type : OutputType, project_path, file_name):
        """Create the short name of the output file (containing standard results)
        :param output_type type of the output file (link, origin-destination or path)
        :param project_path directory of the output file
        :param file_name name of the file of standard results
        :return the name of the file containing the standard results
        """
        if output_type.value == "LINK":
            type_name = 'Link'
        elif output_type.value == "OD":
            type_name = 'Origin-Destination'
        else:
            type_name = "Path"
            
        short_file_name = project_path 
        short_file_name += "\\" 
        short_file_name +=  type_name
        short_file_name +=  "_" 
        short_file_name += file_name
        return short_file_name
    
    @staticmethod
    def compare_csv_files(csv_file_location1, csv_file_location2):
        """Compare the contents of two CSV files, returning true if they are equal, false otherwise
        :param csv_file_location1 first CSV file to be compared
        :param csv_file_location2 second CSV file to be compared
        :return true if the files have equal contents, false otherwise
        """
        df1 = pd.read_csv(csv_file_location1)
        df2 = pd.read_csv(csv_file_location2)
        return df1.equals(df2)
    
    @staticmethod
    def compare_csv_files_and_clean_up(output_type : OutputType, description, file_name, project_path=None):
        """Compare the file of test results with the file of standard results, and delete the test results file if they are equal
        :param output_type type of the output file (link, origin-destination or path)
        :param description root name of the output file
        :param project_path directory of the output file
        :param file_name name of the file of standard results
        :return true if the files have equal contents and the results file has been deleted, false otherwise
        """
        if project_path == None:
            project_path = os.getcwd()
        full_file_name = PlanItHelper.create_full_file_name(output_type, project_path, description, file_name)
        short_file_name = PlanItHelper.create_short_file_name(output_type, project_path, file_name)
        comparison_result = PlanItHelper.compare_csv_files(short_file_name, full_file_name)
        if (comparison_result):
            os.remove(full_file_name)
        return comparison_result
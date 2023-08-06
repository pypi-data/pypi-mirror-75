"""This class exists to take the logic for setting up the initial costs out of the PLANit class.  It does not wrap any Java object.  
This class is instantiated as a member of the PLANit object.  It allows top level calls to have the signature "plan_it.initial_cost.set(..."
"""

class InitialCost:
    
    def __init__(self):
        """Initializer for the InitialCosts class
        """
        self._default_initial_cost_file_location = None
        self._initial_cost_location_dictionary = {}
        
    def set(self, initial_cost_file_location, time_period_external_id=None):
        """Set an initial cost file location
        :param initial_cost_file_location location of an initial cost file
        :param time_period_external_id external id of the time period for which these initial costs apply
        """
        if (time_period_external_id == None):
            self._default_initial_cost_file_location = initial_cost_file_location
        else:
            self._initial_cost_location_dictionary[time_period_external_id] = initial_cost_file_location
            
    def get_initial_cost_file_location_by_time_period_external_id(self, time_period_external_id):
        return self._initial_cost_location_dictionary[time_period_external_id]
    
    def get_time_periods_external_id_set(self):
        return self._initial_cost_location_dictionary.keys()
    
    def get_default_initial_cost_file_location(self):
        return self._default_initial_cost_file_location
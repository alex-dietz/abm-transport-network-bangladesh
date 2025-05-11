from components import Bridge, Sink
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


class ModelOutput():
    """
    Collect model output

    Attributes:
    -----------
    bridge_delay_time_all_scenarios: pd.DataFrame
        dataframe with bridge id and total_delay_time
    vehicle_time_all_scenarios: pd.DataFrame
        dataframe with vehicle id and total_drive_time
    """

    def __init__(self) -> None:
        self.bridge_delay_time_all_scenarios = pd.DataFrame(columns=['total_delay_time'])
        self.vehicle_time_scenario = pd.DataFrame()

    def add_scenario_bridge_delay_time(self,model):
        """
        Add bridge waiting time of scenario to global dataframe
        Parameters:
        -----------
        model: BangladeshModel
            model object
        Returns:
        --------
        None
        """
        # loop thorugh bridges and add bridge id and total_delay_time to dictionary
        bridge_dict = {}
        for agent in model.schedule.agents:
            if isinstance(agent, Bridge):
                bridge_id = agent.unique_id
                total_delay_time = agent.total_delay_time                
                bridge_dict[bridge_id] = [agent.name, agent.length, agent.condition, total_delay_time]
        #bridge_dict to dataframe
        bridge_delay_time = pd.DataFrame.from_dict(bridge_dict, orient='index', columns=['name','length','condition','total_delay_time'])
        #add scenario to dataframe
        
        #merge bridge waiting time of scenario to global dataframe
        if self.bridge_delay_time_all_scenarios.size == 0:
            bridge_delay_time['total_delay_time'] = bridge_delay_time['total_delay_time']/7200
            self.bridge_delay_time_all_scenarios = bridge_delay_time
        else:
            self.bridge_delay_time_all_scenarios['total_delay_time'] = self.bridge_delay_time_all_scenarios['total_delay_time']+ bridge_delay_time['total_delay_time']/7200


    def add_scenario_vehicle_time(self,model, iter):
        # loop through vehicles and add vehicle id and record total_drive_time to dictionary
        vehicle_list = []
        for agent in model.schedule.agents:
            if isinstance(agent, Sink):
                # concat into one list
                vehicle_list += agent.driving_times    
        #vehicle_list to dataframe
        df_iter = pd.DataFrame(vehicle_list, columns =['veh_driving_time'])
        #add iteration column
        df_iter.insert(0, 'Iter', iter) 
        #add scenario to dataframe        
        self.vehicle_time_scenario = self.vehicle_time_scenario.append(df_iter)

    def export_vehicle_driving_time(self, scenario):
        """
        Export vehicle driving time to csv
        Parameters:
        -----------
        scenario: int
            scenario number
        Returns:
        --------
        None
        """
        self.vehicle_time_scenario.to_csv(f'output/scenario{scenario}.csv', index=False)

    def get_bridges_with_highest_delay_time(self,number_scenarios):
        """
        Get bridges with highest waiting time over all scenarios
        Parameters:
        -----------
        None
        Returns:
        --------
        pd.DataFrame
            dataframe with bridge id and total_delay_time of bridges with highest waiting time over all scenarios
        """
        self.bridge_delay_time_all_scenarios['total_delay_time'] = self.bridge_delay_time_all_scenarios['total_delay_time']/number_scenarios
        return self.bridge_delay_time_all_scenarios.sort_values(by=['total_delay_time'], ascending=False).head(5)
    
    def reset_model_output(self):
        self.vehicle_time_scenario = pd.DataFrame()

   
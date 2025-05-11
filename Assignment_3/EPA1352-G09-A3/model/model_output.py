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
        self.bridge_delay_time_all_iterations = pd.DataFrame(columns=['name','length','condition','betweenness','total_delay_time','vehicle_count'])
        self.average_speed_scenario = pd.DataFrame()
        

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
                bridge_dict[bridge_id] = [agent.name, agent.length, agent.condition,agent.betweeness, total_delay_time,agent.vehicle_count]
        #bridge_dict to dataframe
        bridge_delay_time = pd.DataFrame.from_dict(bridge_dict, orient='index', columns=['name','length','condition','betweenness','total_delay_time','vehicle_count'])
        #add scenario to dataframe
        
        #merge bridge waiting time of scenario to global dataframe
        if self.bridge_delay_time_all_iterations.size == 0:                        
            self.bridge_delay_time_all_iterations = bridge_delay_time
        else:
            self.bridge_delay_time_all_iterations['total_delay_time'] +=  bridge_delay_time['total_delay_time']
            self.bridge_delay_time_all_iterations['vehicle_count'] +=  bridge_delay_time['vehicle_count']

    def export_delay_data(self,scenario): 
        """
        Export bridge waiting time of scenario to csv
        Parameters:
        -----------
        scenario: int
            scenario number
        Returns:
        --------
        None
        """       
        self.bridge_delay_time_all_iterations.to_csv(f'output/scenario_{scenario}.csv', index=False)

    def store_effective_speeds(self,model):
        """
        Store effective speeds of scenario to global dataframe
        Parameters:
        -----------
        model: BangladeshModel
            model object
        Returns:
        --------
        None
        """
        # loop through vehicles and add vehicle id and record total_drive_time to dictionary
        vehicle_list = []
        for agent in model.schedule.agents:
            if isinstance(agent, Sink):
                # concat into one list
                vehicle_list += agent.effective_speeds
        #vehicle_list to dataframe
        df_iter = pd.DataFrame(vehicle_list, columns =['average_effective_speed'])                
        #add scenario to dataframe        
        self.average_speed_scenario = self.average_speed_scenario.append(df_iter)

    def calculate_average_effective_speed(self):
        """
        Calculate average effective speed over all iterations in scenario
        Parameters:
        -----------
        None
        Returns:
        --------
        float
            average effective speed over all iterations in scenario
        """
        return self.average_speed_scenario['average_effective_speed'].mean()
        
  
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
    

from model_output import ModelOutput
from model import BangladeshModel
import networkx as nx
import pandas as pd
from multiprocessing import Process

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------


def generate_network(df):
        G = nx.Graph()
        roads = df['road'].unique()        
        for road in roads:
            # Select all the objects on a particular road in the original order as in the cvs
            df_objects_on_road = df[df['road'] == road]               
            #loop through dataframe
            for index, row in df_objects_on_road.iterrows():             
                #add nodes
                G.add_node(row['id'], pos=(row['lon'], row['lat']))
                #add edges from previous node to next node
                #if previous and current not both sourcesink
                if not (df.iloc[index-1]['model_type'] == 'sourcesink' and row['model_type'] == 'sourcesink' and df.iloc[index-1]['road'] != row['road']):
                    G.add_edge(df.iloc[index-1]['id'], row['id'],weight=row['length'])                   
        return G

def run_model(scenario,index,run_length,infrastructure,network,network_betweenness):
    # init model output 
    model_output = ModelOutput()
    #set random seed
    seeds = [28, 78, 89, 12, 51, 23, 20, 72, 57, 91]
    #seeds = [28]
    
    

    for seed in seeds:
        sim_model = BangladeshModel(seed=seed,scenario=scenario,infrastructure=infrastructure,network=network,network_betweenness=network_betweenness)

        # Check if the seed is set
        print("Scenario: " + str(index) + " Seed: " + str(sim_model._seed))

        # One run with given steps
        for i in range(run_length):
            sim_model.step()
        #collect bridge delay time for scenarios 1-7
        #model_output.add_scenario_bridge_delay_time(sim_model)
        #collect vehicle effective speed
        model_output.store_effective_speeds(sim_model)        
        model_output.add_scenario_bridge_delay_time(sim_model)

    #print("Scenario: " + str(scenarios.index(scenario)+1) + " done")
    model_output.export_delay_data(index)

    print("Average Effective Speed[km/h] in Scenario " + str(index) +" : "  +str(model_output.calculate_average_effective_speed()))
    
        

if __name__ == "__main__": 
    # run time 5 x 24 hours; 1 tick 1 minute
    #run_length = 1000
    run_length = 5 * 24*60


    #define scenarios
    scenario_0 = [0, 0, 0, 0]
    scenario_1 = [0, 0, 0, 5]
    scenario_2 = [0, 0, 5, 10]
    scenario_3 = [0, 5, 10, 20]
    scenario_4 = [5, 10, 20, 40]
    scenarios = [scenario_0,scenario_1, scenario_2, scenario_3, scenario_4]

    #Input File
    file_name = './input/infrastructure.csv'
    infrastructure = pd.read_csv(file_name)


    #generate model network
    print("Generating network...")
    network = generate_network(infrastructure)
  
  
    network_betweenness = nx.betweenness_centrality(network, weight='weight')
    #network_betweenness = {}
    print("Betweenness centrality calculated")
    #Multiprocessing
    procs = []
    #loop thorugh scenarios
    for scenario in scenarios:
        proc = Process(target=run_model, args=(scenario,scenarios.index(scenario),run_length,infrastructure,network,network_betweenness))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()



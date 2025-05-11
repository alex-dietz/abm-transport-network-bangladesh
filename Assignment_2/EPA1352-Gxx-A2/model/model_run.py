from model_output import ModelOutput
from components import Bridge, Sink
from matplotlib import pyplot as plt
from model import BangladeshModel
import pandas as pd

"""
    Run simulation
    Print output at terminal
"""

# ---------------------------------------------------------------

# run time 5 x 24 hours; 1 tick 1 minute
run_length = 5 * 24 * 60

#define scenarios
scenario_0 = [0, 0, 0, 0]
scenario_1 = [0, 0, 0, 5]
scenario_2 = [0, 0, 0, 10]
scenario_3 = [0, 0, 5, 10]
scenario_4 = [0, 0, 10, 20]
scenario_5 = [0, 5, 10, 20]
scenario_6 = [0, 10, 20, 40]
scenario_7 = [5, 10, 20, 40]
scenario_8 = [10, 20, 40, 80]


scenarios = [scenario_1, scenario_2, scenario_3, scenario_4, scenario_5, scenario_6, scenario_7, scenario_8]
#scenarios = [scenario_0]


# init model output 
model_output = ModelOutput()
#loop thorugh scenarios
for scenario in scenarios:
    #set random seed
    seeds = [28, 78, 89, 12, 51, 23, 20, 72, 57, 91]
    iter = 1    
    print("Scenario: " + str(scenarios.index(scenario)+1) )
    for seed in seeds:
        sim_model = BangladeshModel(seed=seed,scenario=scenario)

        # Check if the seed is set
        print("SEED " + str(sim_model._seed))

        # One run with given steps
        for i in range(run_length):
            sim_model.step()
        #collect bridge delay time for scenarios 1-7
        if scenario != scenario_8:
            model_output.add_scenario_bridge_delay_time(sim_model)
        #collect vehicle drive time
        model_output.add_scenario_vehicle_time(sim_model, iter)
        iter += 1
    
    # write veh_time data to csv
    model_output.export_vehicle_driving_time(scenarios.index(scenario)+1)
    #reset vehicle times for next scenario
    model_output.reset_model_output()


print("Bridges with highest average delay time per vehicle in minutes over all scenarios: ")
print(model_output.get_bridges_with_highest_delay_time(len(scenarios)-1))


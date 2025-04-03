from pstats import Stats
from pandas import read_excel
import os
from numpy import nan
from itertools import product
from mip import Model, xsum, BINARY, INTEGER, OptimizationStatus
import csv
from inputs_data_reading_3 import inputs_data_read_3
from pathlib import Path
import gurobipy as grb



import datetime


# folder_path = '/Users/bhanu/Desktop/Thesis 2.0/Instances_Folder/Instanzen_j10_FSRCPSP_complete' # Replace with the actual folder path
folder_path = '/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Instances_Folder/Instances_j10_FSRCPSP'
folder = Path(folder_path)



def main():
    print("In Main Function")
    #ignored_list = ["j103_4", "j104_5", "j108_5"]
    for file in folder.iterdir():
        print(file.name)
        if file.is_file() and not file.name.startswith('.') and not file.name.startswith('results'):
            file_name_without_extension, file_extension = os.path.splitext(file.name)
            
            
            # if file_name_without_extension in ["j104_10"]:
            if not file.name.startswith('.') and file_name_without_extension == "j103_9":
                print(file_name_without_extension)
                # print("Inside investigation file")
                (total_activities_count, unified_preced_array, es_ls_combined_list, lower_bound_resource_dictionary, upper_bound_resource_dictionary,
                    m1_val, m2_val, total_time_horizon_time_units_value, R_kt, workload_dictionary, work_load_all_scenarios_list) = inputs_data_read_3(file.name, file_name_without_extension, folder_path)
            
                schedule_activities_fn(total_activities_count, unified_preced_array, es_ls_combined_list, lower_bound_resource_dictionary, upper_bound_resource_dictionary,
                    m1_val, m2_val, total_time_horizon_time_units_value, R_kt, workload_dictionary, work_load_all_scenarios_list, file_name_without_extension)

    print("Main ended")

# Assuming you have already defined your MIP model 'model'

def fix_start_times_from_file(x, file_path):
    # Read start times from the file
    with open(file_path, 'r') as file:
        start_times_data = eval(file.read())

    # Fix start times in the model
    for activity_number, time_point in start_times_data:
        try:
            # Convert activity_number and time_point to integers
            activity_number = int(activity_number)
            time_point = int(time_point)

            # Fix the start time of the corresponding activity
            var_to_fix_start = x[activity_number][time_point]
            var_to_fix_start.lb = 1
            var_to_fix_start.ub = 1
        except (ValueError, IndexError):
            print(f"Error processing start time data: {activity_number}, {time_point}")

# # Example usage:
# file_path = 'path/to/your/start_times.txt'
# fix_start_times_from_file(model, file_path)



def schedule_activities_fn(total_activities_count, unified_preced_array,
     es_ls_combined_list, lower_bound_resource_dictionary, upper_bound_resource_dictionary,
     m1_val, m2_val, total_time_horizon_time_units_value, R_kt, workload_dictionary, work_load_all_scenarios_list, file_name_without_extension):

      print(es_ls_combined_list)
      print(unified_preced_array)
      print(len(work_load_all_scenarios_list))

      # Specify the folder path you want to create
      folder_path = '/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Matched_Results_j10_Deterministic_ES'

      # Check if the folder already exists
      if not os.path.exists(folder_path):
        # If it doesn't exist, create the folder
        os.makedirs(folder_path) 

      # for scenario in range(0, len(work_load_all_scenarios_list)):
      print("Embedding All Scenarios into Model")
      n = total_activities_count - 2  # note there will be exactly 12 jobs (n=10 jobs plus the two 'dummy' ones)

      (R, J, T) = (range(1), range(total_activities_count), range(total_time_horizon_time_units_value))

      # at the moment our scope is a single resource
      K = range(0,1)

      P = range(0, len(work_load_all_scenarios_list))
      print(P)

      print("R is {}".format(R))
      print("J is {}".format(J))
      print("T is {}".format(T))

      model = Model()
      model.rel_gap = 0.01

      x = [[model.add_var(name="x({},{})".format(i, t), var_type=BINARY) for t in T] for i in J]
      y_pi = [[[model.add_var(name="y({},{}, {})".format(p, i, t), var_type=BINARY) for t in T] for i in J] for p in P]
      r_pi_ikt = [[[[model.add_var(name="r({},{},{},{})".format(p,i,k,t), var_type=INTEGER) for t in T] for k in K] for i in J] for p in P]
      d_pi_i = [[model.add_var(name="d({}, {})".format(p,i)) for i in J]for p in P]

      v_pi = [model.add_var(name="v({})".format(p), var_type=BINARY) for p in P]
      w_pi = [model.add_var(name="w({})".format(p), var_type=BINARY) for p in P]
      ro_pi = [model.add_var(name="ro({})".format(p), var_type=BINARY) for p in P]



      model.objective = xsum(t * x[n + 1][t] for t in T)
      #   model.Heuristics = 0.05
    #   fix_start_values_folder = '/Users/bhanu/Desktop/Thesis 2.0/Matched_Results_j10_Deterministic_ES'
      fix_start_values_folder = '/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Processed_Outputs'
      file_name_with_ext = file_name_without_extension+'.txt'
      file_path = os.path.join(fix_start_values_folder, file_name_with_ext)
      print('##############')
      print(file_path)
      fix_start_times_from_file(x, file_path)
      

      #constraint 15.4
      for i in J:
       for t in T:
          model += x[i][t] >= 0
          model += x[i][t] <= 1

      #constraint 15.5
      for p in P:
          for i in J:
              for t in T:
                  model += y_pi[p][i][t] >=0
                  model += y_pi[p][i][t] <=1
      
      #constraint 15.1.2.3
      for p in P:
          model += w_pi[p] >=0
          model += w_pi[p] <=1
          model += v_pi[p] >=0
          model += v_pi[p] <=1
          model += ro_pi[p] >=0
          model += ro_pi[p] <=1

      #constraint 14 ; check if it needs to be seperated
      for p in P:
          for i in J:
              for k in K:
                  for t in T:
                      model += d_pi_i[p][i] >= 0
                      model += r_pi_ikt[p][i][k][t] >= 0


      #constraint 2
      for j in J:
          model += xsum(x[j][t] for t in T) == 1

      #constraint 3
      for (j, s) in unified_preced_array:
          for p in P:
              lhs =  xsum(t * x[s][t] for t in range(es_ls_combined_list[s][0],es_ls_combined_list[s][1])) - xsum(t * x[j][t] for t in range(es_ls_combined_list[j][0],es_ls_combined_list[j][1]))
              rhs =  d_pi_i[p][j] - (m1_val * w_pi[p])
              model += lhs >= rhs
      
      # #constraint 4
      for p in P:
          for k in K:
              for t in T:
                  sum_r_ik_t = xsum(r_pi_ikt[p][i][k][t] for i in J)
                  model += sum_r_ik_t <= R_kt[t]

      #constraint 5
      for p in P:
          for i, k in product(J, K):
              model += xsum(r_pi_ikt[p][i][k][t] for t in range(es_ls_combined_list[i][0],es_ls_combined_list[i][1])) == work_load_all_scenarios_list[p][i]
      
      lb_rs_allocation = list(lower_bound_resource_dictionary.values())
      ub_rs_allocation = list(upper_bound_resource_dictionary.values())

      # Constraint 6: Ensure resource allocation stays within bounds
      for p in P:
          for i in J:
              for k in K:
                  for t in T:
                      lhs = lb_rs_allocation[i] * xsum(x[i][tau] for tau in range(t + 1))
                      rhs = ub_rs_allocation[i] * xsum(x[i][tau] for tau in range(t + 1))
                      model += lhs >= r_pi_ikt[p][i][k][t] <= rhs
      

      #constraint 7
      for p in P:
          for i in J:
              for t in T:
                  lhs = xsum(r_pi_ikt[p][i][k][tau] for tau in range(t, len(T)) for k in K)
                  model += lhs >= y_pi[p][i][t]

      #constraint 8
      for p in P:
          for i in J:
              for t in T:
                  lhs = xsum(r_pi_ikt[p][i][k][tau] for tau in range(t, len(T)) for k in K)
                  model += lhs <= m2_val * y_pi[p][i][t]
      
      #constraint 9
      for p in P:
          for i in J:
              if i == 0 or i == n + 1:
                  continue  # Skip i=0 and i=n+1
              model += xsum(y_pi[p][i][t] + xsum(x[i][tau] for tau in range(t + 1)) - 1 for t in T) <= d_pi_i[p][i]
    
    #constraint 10
      for p in P:
          for i in J:
              for k in K:
                  for t in T:
                      lhs = lb_rs_allocation[i] * (y_pi[p][i][t] + xsum(x[i][tau] for tau in range(t + 1)) - 1)
                      model += lhs <= r_pi_ikt[p][i][k][t]

    #constraint 11
      for p in P:
          for i in J:
              for k in K:
                  for t in T:
                      lhs_2 = ub_rs_allocation[i] * (y_pi[p][i][t] + xsum(x[i][tau] for tau in range(t + 1)) - 1)
                      model += lhs_2 >= r_pi_ikt[p][i][k][t]
    



      #constraint 12
      for p in P:
          lhs = w_pi[p] + v_pi[p]
          rhs = (2 * ro_pi[p])
          model += lhs <= rhs

       
       #constraint 13
      sample_size = 10
      episilon = 0.2
      lhs = xsum(ro_pi[p] for p in P)
      rhs = sample_size * episilon
      model += lhs <= rhs

      start_time = datetime.datetime.now()
      status = model.optimize()
      end_time = datetime.datetime.now()

      # Calculate the execution time in seconds
      execution_time = (end_time - start_time).total_seconds()
      print(f"Execution time: {execution_time} seconds")
      
      print("Schedule: ")

    
      if status == OptimizationStatus.OPTIMAL:
          print("w_pi")
          w_pi_list = []
          for p in P:
              w_pi_list.append(abs(w_pi[p].x))
          print(w_pi_list)
          print("v_pi")
          v_pi_list = []
          for p in P:
              v_pi_list.append(abs(v_pi[p].x))
          print(v_pi_list)
          print("ro_pi")
          ro_pi_list = []
          for p in P:
              ro_pi_list.append(abs(ro_pi[p].x))
          print(ro_pi_list)

          # Infeasible solutions printing
          for ro in range(0, len(ro_pi_list)):
              if ro_pi_list[ro] == 1:
                  print("Scenario {} is infeasible".format(ro+1))



      for (j, t) in product(J, T):
          if x[j][t] is not None and x[j][t].x is not None and x[j][t].x >= 0.99:
              # Find the maximum duration across all scenarios for activity j
              max_duration = max([d_pi_i[p][j].x for p in P if ro_pi_list[p] != 1])
              print("Activity {}: begins at t={} and finishes at t={}".format(j, t, t+max_duration))


      print("Makespan = {}".format(model.objective_value))


      if status == OptimizationStatus.OPTIMAL:
          Resource_utilization_distribution_array = [[[0 for _ in range(int(model.objective_value))] for _ in J] for _ in P]
          for t in range(0, int(model.objective_value)):
              for i in J:
                  for p in P:
                      Resource_utilization_distribution_array[p][i][t] = abs(r_pi_ikt[p][i][0][t].x)


      output_file = file_name_without_extension+'.txt'
      summary_file = 'results_summary_determinstic_sol_matched_es.txt'
      # Construct the full file path including the folder and filename
      file_path = os.path.join(folder_path, output_file)
      summary_file_path = os.path.join(folder_path, summary_file)
      consolidated_row = ''

      # Summary File Writing
      with open(summary_file_path, 'a', newline='') as summary_file:
          summary_writer = csv.writer(summary_file, delimiter='\t')
          consolidated_row = file_name_without_extension+'\t'+ str(model.objective_value)+ '\t'+ str(execution_time)+ ' seconds'
          summary_writer.writerow([consolidated_row])

      #Each Instance specific output generator
      with open(file_path, 'a', newline='') as file:
          writer = csv.writer(file, delimiter='\t')  # Use tab as the delimiter

          # writer.writerow(["# For Scenario pi{}".format(scenario+1)])
          writer.writerow(['-' * 100])
          writer.writerow(["Optimality: "])
          writer.writerow([status])

          # Check if the model is feasible
          if status == OptimizationStatus.OPTIMAL:  # Gurobi status code for feasible solution
              writer.writerow(["Overall the model is feasible."])
              writer.writerow(['-' * 100])
              for ro in range(0, len(ro_pi_list)):
                  if ro_pi_list[ro] == 1:
                      writer.writerow(["Infeasibility: "])
                      writer.writerow(["Scenario {} is infeasible".format(ro+1)])
                      writer.writerow(['-' * 100])
              writer.writerow(["Schedule: "])
              for (j, t) in product(J, T):
                  if x[j][t] is not None and x[j][t].x is not None and x[j][t].x >= 0.99:
                      max_duration = max([d_pi_i[p][j].x for p in P if ro_pi_list[p] != 1])
                      writer.writerow(["Activity {}: begins at t={} and finishes at t={}".format(j, t, round(t+max_duration))])
              writer.writerow(['-' * 100])
              writer.writerow(["The Resource Utilisation across the time horizon looks as follows: "])

              for column_index in range(total_activities_count):
                  column_data = [row[column_index] for row in Resource_utilization_distribution_array]
                  writer.writerow(['-' * 100])
                  writer.writerow(["Activity {} - The Resource Allocation for each scenario: ".format(column_index)])
                  for item in column_data:
                      writer.writerow([item])
          else:
               writer.writerow(["The model is not feasible "])
      print(f'Data has been written to {output_file}')


#only problem is the lower bound resource allocation, rest all need to be validated again
if __name__ == "__main__":
    main()
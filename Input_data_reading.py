from pandas import read_excel, ExcelFile
from numpy import nan
import os
import numpy as np

def inputs_data_read_optimized(file_name, file_name_without_extension, folder_path):
    file_path = os.path.join(folder_path, file_name)
    print("%%\n" + file_path)

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        with ExcelFile(file_path) as xls:
            # Read all sheets at once
            precedence_activities = xls.parse("a(i,j)", index_col=0).fillna(0).astype(int)
            total_activities_count = precedence_activities.shape[0]
            
            # Vectorized precedence processing
            rows, cols = np.where(precedence_activities == 1)
            unified_preced_array = [[int(r), int(c)] for r, c in zip(rows, cols)]

            # ES/LS processing with vectorization
            es_df = xls.parse("ES", header=None)
            early_start_dictionary = es_df.set_index(0)[1].to_dict()
            
            ls_df = xls.parse("LS", header=None)
            latest_start_dictionary = ls_df.set_index(0)[1].to_dict()
            
            # Maintain original order using sorted keys
            es_ls_combined_list = [
                [early_start_dictionary[f"i{i}"], latest_start_dictionary[f"i{i}"]]
                for i in range(total_activities_count)
            ]

            # Resource bounds processing
            lr_df = xls.parse("l_r(i,k)", header=None)
            lower_bound_resource_dictionary = lr_df.set_index(0)[2].to_dict()
            
            ur_df = xls.parse("u_r(i,k)", header=None)
            upper_bound_resource_dictionary = ur_df.set_index(0)[2].to_dict()

            # M values
            m1_val = xls.parse("M1", header=None).iloc[0, 0]
            m2_val = xls.parse("M2", header=None).iloc[0, 0]

            # Time horizons
            time_horizons = xls.parse("t", header=None)[0].tolist()
            total_time_horizon_time_units_value = len(time_horizons)

            # Resource capacity
            rk_df = xls.parse("Rk", header=None)
            R_kt = rk_df[2].tolist()

            # Workload processing with vectorization
            workload_df = xls.parse("w(i,k,pi)").fillna(0)
            workload_matrix = workload_df.values
            num_scenarios = workload_matrix.shape[1] - 2
            
            # Vectorized scenario extraction
            work_load_all_scenarios_list = [
                workload_matrix[:, col].tolist() 
                for col in range(2, 2 + num_scenarios)
            ][:-1]  # Remove last element as per original logic

            # Workload dictionary
            workload_dictionary = {row[0]: row[2] for row in workload_matrix}

    except Exception as e:
        print(f"Error while reading Excel file: {e}")
        return

    # Print results in original format
    print(total_activities_count, unified_preced_array, es_ls_combined_list, 
          lower_bound_resource_dictionary, upper_bound_resource_dictionary,
          m1_val, m2_val, total_time_horizon_time_units_value, R_kt,
          workload_dictionary, work_load_all_scenarios_list)

if __name__ == "__main__":
    inputs_data_read_optimized(
        "j102_2.xlsx",
        "j102_2",
        "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Instances_Folder/Instances_j10_FSRCPSP"
    )
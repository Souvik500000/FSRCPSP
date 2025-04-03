from pandas import read_excel
from numpy import nan
import os


def inputs_data_read_3(file_name, file_name_without_extension, folder_path):

    # Check if the file exists
    if not os.path.exists(folder_path):
        print(f"File not found: {folder_path}")
        return
    file_path = os.path.join(folder_path, file_name)
    print("%%")
    print(file_path)

    try:
        precedence_activities = read_excel(file_path, sheet_name="a(i,j)", index_col=0)
        precedence_activities = precedence_activities.replace(nan, 0)
        precedence_activities = precedence_activities.to_numpy()

        total_activities_count = len(precedence_activities)
        unified_preced_array = []

        # Add precedence constraints.
        for i in range(len(precedence_activities)):
            for j in range(len(precedence_activities[0])):
                if precedence_activities[i][j] == 1:
                    unified_preced_array.append([i,j])

    except Exception as e:
        print(f"Error while reading Excel file: {e}")

    #reading Early start time of activities
    early_start_df = read_excel(file_path,
     sheet_name="ES",  header=None)
    early_start_numpy_array = early_start_df.values
    
    early_start_dictionary = {}
    # Iterate over the NumPy array.
    for row in early_start_numpy_array:
        key = row[0]
        value = row[1]
        early_start_dictionary[key] = value

    #reading Latest start time of activities
    latest_start_df = read_excel(file_path,
     sheet_name="LS",  header=None)
    latest_start_numpy_array = latest_start_df.values
    latest_start_dictionary = {}
    # Iterate over the NumPy array.
    for row in latest_start_numpy_array:
        key = row[0]
        value = row[1]
        latest_start_dictionary[key] = value


    es_ls_combined_list = []

    for key in early_start_dictionary:
        early_start = early_start_dictionary[key]
        latest_start = latest_start_dictionary[key]
        es_ls_combined_list.append([early_start, latest_start])



    

    # reading Lower boundary resource values
    lower_bound_resource_allocation_df = read_excel(file_path,
     sheet_name="l_r(i,k)",  header=None)
    lower_bound_resource_numpy_array = lower_bound_resource_allocation_df.values
    lower_bound_resource_dictionary = {}
    # Iterate over the NumPy array.
    for row in lower_bound_resource_numpy_array:
        key = row[0]
        value = row[2]
        lower_bound_resource_dictionary[key] = value  

    # reading Upper boundary resource values
    upper_bound_resource_allocation_df = read_excel(file_path,
     sheet_name="u_r(i,k)", header=None)
    upper_bound_resource_numpy_array = upper_bound_resource_allocation_df.values

    upper_bound_resource_dictionary = {}
    # Iterate over the NumPy array.
    for row in upper_bound_resource_numpy_array:
        key = row[0]
        value = row[2]
        upper_bound_resource_dictionary[key] = value  
    
     

    # reading M1 value
    m1_val = read_excel(file_path,
     sheet_name="M1", nrows=1, header=None)
    m1_val = m1_val.values[0][0]

    # reading M2 value
    m2_val = read_excel(file_path,
     sheet_name="M2", nrows=1, header=None)
    m2_val = m2_val.values[0][0]

    #  Toral time horizons
    total_time_horizons = read_excel(file_path,
     sheet_name="t", header=None) 
    total_time_horizons_values = total_time_horizons.values
    total_time_horizons_values_list = []
    for row in total_time_horizons_values:
        total_time_horizons_values_list.append(row[0])
    
    total_time_horizon_time_units_value = len(total_time_horizons_values_list)
    

    #  resource capacity at time horizons
    resource_capacity_at_each_time_horizons = read_excel(file_path,
     sheet_name="Rk", header=None) 
    resource_capacity_at_each_time_horizons = resource_capacity_at_each_time_horizons.values

    R_kt = []
    for row in resource_capacity_at_each_time_horizons:
        R_kt.append(row[2])
    resource_capacity_at_each_time_horizons_dictionary = {}
    for row in resource_capacity_at_each_time_horizons:
        key = row[1]
        value = row[2]
        resource_capacity_at_each_time_horizons_dictionary[key] = value
    #R =  np.take(resource_capacity_at_each_time_horizons, 2, axis=1)

    # Check if it is constant resource capacity across the time horizon.
    is_constant_resource_capacity = True
    for value in resource_capacity_at_each_time_horizons_dictionary.values():
        if value != list(resource_capacity_at_each_time_horizons_dictionary.values())[0]:
            is_constant_resource_capacity = False
            break

    constant_resource_availability_value = 0
    # Extract the value.
    if is_constant_resource_capacity:
        constant_resource_availability_value = list(resource_capacity_at_each_time_horizons_dictionary.values())[0]


   # Reading workload based on scenarios
    workload_matrix = read_excel(file_path,
     sheet_name="w(i,k,pi)")
    workload_matrix = workload_matrix.replace(nan, 0)
    workload_numpy_array = workload_matrix.values

        # Get the number of columns (excluding the first two columns)
    num_columns = workload_numpy_array.shape[1] - 2

    # Create a list of lists for each column
    work_load_all_scenarios_list = [[] for _ in range(num_columns)]

    # Iterate through the columns (starting from the 3rd column) and append values to the respective lists
    for col_index in range(2, workload_numpy_array.shape[1]):
        for row_index in range(workload_numpy_array.shape[0]):
            work_load_all_scenarios_list[col_index - 2].append(workload_numpy_array[row_index, col_index])

    # result = [row[2:].tolist() for row in workload_numpy_array]
    # print(result)
    # due to excel file formatting issue an extra element of [0's] getting created
    # so popping that
    work_load_all_scenarios_list.pop()

    workload_dictionary = {}
    # Iterate over the NumPy array.
    for row in workload_numpy_array:
        key = row[0]
        value = row[2]
        workload_dictionary[key] = value  

    #considering only one scenario currently and constant resource k1
    return(total_activities_count, unified_preced_array, es_ls_combined_list, lower_bound_resource_dictionary, upper_bound_resource_dictionary,
     m1_val, m2_val, total_time_horizon_time_units_value, R_kt
      , workload_dictionary, work_load_all_scenarios_list)



# if __name__ == "__main__":
#     inputs_data_read_3()
    
if __name__ == "__main__":
    file_name = "j102_2.xlsx"  # Replace with your Excel file name
    file_name_without_extension = "j102_2"  # Replace with the file name without extension
    folder_path = "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Instances_Folder/Instances_j10_FSRCPSP"  # Replace with the path to the folder containing the file
    inputs_data_read_3(file_name, file_name_without_extension, folder_path)
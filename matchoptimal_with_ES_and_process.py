import csv
import os
from pathlib import Path
from pandas import read_excel
import ast



# instances_folder_path = '/Users/bhanu/Desktop/Thesis 2.0/Instances_Folder/Instances_j10_FSRCPSP'

instances_folder_path = "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Instances_Folder/Instanzen_j10_FSRCPSP_complete"
# instances_folder_path = '/Users/bhanu/Desktop/Thesis 2.0/Instances_Folder/Instanzen_j10_FSRCPSP_complete'
# input_folder_path = '/Users/bhanu/Desktop/Thesis 2.0/output_logs_extract_schedule' # Replace with the actual folder path
input_folder_path = "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/output_logs_extract_schedule"
folder = Path(input_folder_path)


# final_output_file_from_this_module = '/Users/bhanu/Desktop/Thesis 2.0/matched_optimal_with_es_results_j10'
final_output_file_from_this_module="/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/matched_optimal_with_es_results_j10"

for file in folder.iterdir():
        activity_schedule = []
        if file.is_file() and not file.name.startswith('.'):
            print(file.name)
            file_name_without_extension, file_extension = os.path.splitext(file.name)

            with open(input_folder_path+'/'+file_name_without_extension+'.txt', 'r') as file:
                content = file.read()
                #   # Skip non-Python lines (lines starting with dashes)
                # lines = [line for line in content.split('\n') 
                # if not line.startswith('-') and not line.startswith('Optimality:') and not line.startswith('Overall') and 
                # not line.startswith('Infeasibility') and not line.startswith('Scenario') and not line.startswith('Schedule')]

                # # Join the remaining lines and evaluate
                # valid_content = '\n'.join(lines)
                # print(valid_content)
                activity_start_finish = ast.literal_eval(content)
                print(activity_start_finish)

            excel_file_path = os.path.join(instances_folder_path, file_name_without_extension+'.xlsx')
            #reading Early start time of activities
            early_start_df = read_excel(excel_file_path,
            sheet_name="ES",  header=None)
            early_start_numpy_array = early_start_df.values

            early_start_dictionary = {}
            # Iterate over the NumPy array.
            for row in early_start_numpy_array:
                key = row[0]
                value = row[1]
                early_start_dictionary[key] = value
            print(early_start_dictionary)

            es_list_for_each_activity = []
            for key in early_start_dictionary:
                early_start = early_start_dictionary[key]
                es_list_for_each_activity.append(early_start)
            print(es_list_for_each_activity)

            optimal_solution_matched_es = []
            for tuple_1, value in zip(activity_start_finish, es_list_for_each_activity):
                if tuple_1[1] == value:
                    optimal_solution_matched_es.append([tuple_1[0],tuple_1[1]])
            print(optimal_solution_matched_es)
            
            output_file = file_name_without_extension+'.txt'
            file_path = os.path.join(final_output_file_from_this_module, output_file)
            print(file_path)
            # Check if the folder already exists
            if not os.path.exists(final_output_file_from_this_module):
                os.makedirs(final_output_file_from_this_module) 

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file, delimiter='\t')   
                writer.writerow([optimal_solution_matched_es])
            
print("End")
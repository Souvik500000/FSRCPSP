import csv
import os
from pathlib import Path




# folder_path = '/Users/bhanu/Desktop/Thesis 2.0/output_logs_extract_schedule'
folder_path = "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/output_logs_extract_schedule"
# input_folder_path = '/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/__MACOSX/FSRCPSP_Codes/output_folder_Stochastic_FSRCPSP'  # Replace with the actual folder path
input_folder_path = "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/output_folder_Stochastic_FSRCPSP/j10 stochastic e0.2 fix and optimize All 50"
folder = Path(input_folder_path)

for file in folder.iterdir():
        activity_schedule = []
        if file.is_file() and not file.name.startswith('.'):
            print(file.name)
            file_name_without_extension, file_extension = os.path.splitext(file.name)

            with open(input_folder_path+'/'+file_name_without_extension+'.txt', 'r') as file:
                # Flag to identify the Activity section
                in_activity_section = False

                for line in file:
                    if line.startswith("The Resource"):
                        print("inside")
                        break
                    if line.startswith("Activity"):
                        in_activity_section = True
                        print(line)
                        print(line.split(': ')[0].split(' ')[1])
                        activity_number = line.split(': ')[0].split(' ')[1]
                        activity_info = line.split(': ')[1].split(' ')
                        print(activity_info)
                        #activity_number = int(activity_info[0][:-1])  # Extracting the activity number
                        start_time = int(activity_info[2][2:])  # Extracting the start time
                        print(start_time)
                        finish_time = int(activity_info[6][2:])  # Extracting the finish time
                        print(finish_time)
                        activity_schedule.append((activity_number, start_time, finish_time))
                    elif line.strip().startswith("Resource"):
                        in_activity_section = False

                output_file = file_name_without_extension+'.txt'
                file_path = os.path.join(folder_path, output_file)
            # Check if the folder already exists
                if not os.path.exists(folder_path):
                    # If it doesn't exist, create the folder
                    os.makedirs(folder_path) 

                with open(file_path, 'w', newline='') as file:
                    writer = csv.writer(file, delimiter='\t')   
                    writer.writerow([activity_schedule])
    

print(activity_schedule)

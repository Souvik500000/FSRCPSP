import pandas as pd
from gurobipy import Model, GRB, quicksum
from pathlib import Path
import numpy as np

def inputs_data_read_3(file_name, folder_path):
    """Improved data loader with error handling"""
    try:
        folder_path = Path(folder_path) 
        file_path = Path(folder_path) / file_name   # Correct file path
    
        if not folder_path.exists():
            print(f"Error: File {folder_path} not found")
            return None

        print(f"Looking for file at: {file_path}")  # Debug: Print file path

        with pd.ExcelFile(file_path) as xls:
            # Load precedence matrix
            precedence_df = pd.read_excel(xls, "a(i,j)", index_col=0)
            precedence_df = precedence_df.fillna(0).astype(int)
            rows, cols = np.where(precedence_df == 1)
            precedences = [[int(r), int(c)] for r, c in zip(rows, cols)]

            # Load time windows
            es = pd.read_excel(xls, "ES", header=None).set_index(0)[1].to_dict()
            ls = pd.read_excel(xls, "LS", header=None).set_index(0)[1].to_dict()
            es_ls = [[es[k], ls[k]] for k in sorted(es.keys())]
            
            print(f"Data read successfully: {precedences}, {es_ls}")  # Debug line
            print(f"Precedence matrix:\n{precedence_df}")  # Debug: Print precedence matrix
            print(f"Earliest start times: {es}")  # Debug: Print ES
            print(f"Latest start times: {ls}")  # Debug: Print LS

            return {
                'total_activities': precedence_df.shape[0],
                'precedences': precedences,
                'time_windows': es_ls,
                'activity_ids': [f"i{i}" for i in range(precedence_df.shape[0])]
            }

    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def generate_start_times(file_name, folder_path, output_folder):
    """Generates and saves start times for activities using Gurobi"""
    data = inputs_data_read_3(file_name, folder_path)
    if not data:
        return

    # Create optimization model
    model = Model("Project_Scheduling")
    n = data['total_activities']
    T = range(data['time_windows'][-1][1] + 1)  # Maximum possible time
    
    # Decision variables
    x = [[model.addVar(name=f"x({i},{t})", vtype=GRB.BINARY) 
         for t in T] for i in range(n)]
    
    # Objective: Minimize makespan (last activity's start time)
    model.setObjective(quicksum(t * x[-1][t] for t in T), GRB.MINIMIZE)
    
    # Constraints
    for i in range(n):
        # Activity must start exactly once
        model.addConstr(quicksum(x[i][t] for t in T) == 1)
        
        # Time window constraints
        es, ls = data['time_windows'][i]
        
        # Relax time windows for activities that must start after i0
        if i != 0:  # Skip i0 (fixed to start at 0)
            es += 1  # Allow activities to start 1 unit later
            ls += 10  # Allow activities to start 10 units later
        
        # Adjust ES for i3
        if i == 3:  # i3 must start after i0
            es = 0  # Allow i3 to start at time 0
        
        print(f"Activity {i}: ES={es}, LS={ls}")  # Debug: Print time windows

        for t in T:
            if t < es or t > ls:
                model.addConstr(x[i][t] == 0)

    # Precedence constraints
    for (j, s) in data['precedences']:
        print(f"Precedence: Activity {j} must precede Activity {s}")  # Debug: Print precedence
        if j == 0 and s == 3:  # i0 must precede i3
            model.addConstr(quicksum(t * x[s][t] for t in T) >= quicksum(t * x[j][t] for t in T) + 19)
        else:
            model.addConstr(quicksum(t * x[s][t] for t in T) >= quicksum(t * x[j][t] for t in T))
    
    # Solve model
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        # Extract start times
        start_times = []
        for i in range(n):
            for t in T:
                if x[i][t].x >= 0.99:
                    start_times.append([i, t])
        
        # Save to file
        output_path = Path(output_folder) / f"{Path(file_name).stem}.txt"
        with open(output_path, 'w') as f:
            f.write(str(start_times))
        print(f"Start times saved to {output_path}")
    else:
        print("No optimal solution found")
        
        # Use Gurobi's IIS to identify conflicting constraints
        print("Computing IIS to identify conflicting constraints...")
        model.computeIIS()
        iis_file = Path(output_folder) / f"{Path(file_name).stem}_model.ilp"
        model.write(str(iis_file))
        print(f"Conflicting constraints saved to {iis_file}")

if __name__ == "__main__":
    # Configuration
    INPUT_FOLDER = "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Instances_Folder/Instances_j10_FSRCPSP"
    OUTPUT_FOLDER = "/Users/souvikchakraborty/Downloads/Project/FSRCPSP_Codes/FSRCPSP_Codes/Processed_Outputs"
    
    # Create output folder if it doesn't exist
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    
    # Iterate over all files in the input folder
    input_folder = Path(INPUT_FOLDER)
    for file in input_folder.iterdir():
        if file.is_file() and file.suffix == ".xlsx":
            print(f"Processing file: {file.name}")
            generate_start_times(
                file_name=file.name,
                folder_path=INPUT_FOLDER,
                output_folder=OUTPUT_FOLDER
            )
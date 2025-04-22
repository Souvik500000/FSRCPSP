# Project: Flexible Resource-Constrained Project Scheduling Problem (FSRCPSP) Solver

This repository contains a set of Python scripts designed to solve the Flexible Resource-Constrained Project Scheduling Problem (FSRCPSP). The scripts implement both deterministic and stochastic approaches to find optimal or near-optimal schedules.

## Overview

The scripts are organized to handle different aspects of the FSRCPSP, including:

* **Data Input**: Reading and processing input data from Excel files.
* **Deterministic Scheduling**: Solving the deterministic version of the problem using mathematical programming.
* **Stochastic Scheduling**: Addressing the problem with uncertainty in activity durations.
* **Solution Analysis**: Extracting and analyzing solution logs.
* **Solution Matching**: Comparing generated schedules with early start schedules.

## Script Descriptions

Here's a breakdown of the purpose of each script:

* `inputs_data_reading_3.py`:  Reads input data for the FSRCPSP from Excel files. It extracts information such as precedence relations between activities, early start times, late start times, resource availability, and workload information.  This script is designed to handle instances with up to 10 jobs.
* `inputs_data_reading_4_j30.py`: Similar to `inputs_data_reading_3.py`, but this script is tailored to read input data for instances with 30 jobs. It may handle slightly different data formats or calculations specific to the larger problem size.
* `Deterministic_range_FAO_j10.py`: Implements a deterministic solver for the FSRCPSP. It uses a mathematical programming model to generate a schedule that minimizes the makespan while respecting precedence and resource constraints. This version is designed for instances with 10 jobs.  It appears to have some debugging code related to infeasibility analysis.
* `FAO_Determinstic_matched_ES_j10.py`:  Also a deterministic solver for 10-job instances.  It likely has some modifications or enhancements compared to `Deterministic_range_FAO_j10.py`, possibly focusing on matching the generated schedule with early start times.
* `FAO_Determinstic_matched_ES_j30.py`:  A deterministic solver specifically for 30-job instances.  It incorporates input data reading from `inputs_data_reading_4_j30.py` and adapts the scheduling model to the larger problem scale.
* `fix_opt_eith_matched_es_j10.py`: This script seems to focus on fixing or adjusting an existing optimal solution, likely by incorporating or matching it with early start times.  It operates on 10-job instances.
* `Stochastic_FSRCPSP_j10.py`:  Tackles the FSRCPSP with stochastic activity durations (uncertainty).  It likely uses a more complex model or solution approach to handle the different possible scenarios.  This script is for 10-job instances.
* `Stochastic_FSRCPSP_j30.py`:  The stochastic version of the solver for 30-job instances, using input functions from  `inputs_data_reading_4_j30.py`.
* `extracting_logs.py`:  Post-processing script to extract relevant information (e.g., activity schedules) from solver output logs.  It parses the log files and saves the extracted data into a more structured format (CSV).
* `matchoptimal_with_ES_and_process.py`:  Analyzes the output of the scheduling solver. It reads the generated schedules and compares them with the early start times of activities, potentially to evaluate the solution quality or identify specific characteristics.

## Dependencies

* Python 3.x
* pandas
* numpy
* mip (Mathematical Optimization Library)
* pathlib
* csv
* os
* datetime

## Usage

1.  Ensure all dependencies are installed (`pip install pandas numpy mip pathlib`).
2.  Place the Excel input data files in the appropriate directories (e.g.,  `/Users/bhanu/Desktop/Thesis 2.0/Instances_Folder/Instanzen_j10_FSRCPSP_complete`, `/Users/bhanu/Desktop/Thesis 2.0/Instances_Folder/Instances_j30_FSRCPSP`).  *Note:* You may need to adjust the `folder_path` variables in the scripts to match your local file structure.
3.  Run the desired Python script (e.g., `python FAO_Determinstic_matched_ES_j30.py`).
4.  Output files (schedules, logs, etc.) will be generated in the directories specified in the scripts.

## Important Notes

* The scripts contain hardcoded file paths.  You **must** modify these paths to match your local environment.
* Some scripts include commented-out code or debugging statements.
* The scripts are designed to handle specific input data formats. Ensure your Excel files adhere to the expected structure (sheet names, data layout, etc.).
* The scripts differentiate between 10-job and 30-job problem instances, using separate input reading and solver scripts for each.

## Further Development

* Generalize file paths to be more flexible (e.g., using command-line arguments).
* Implement more robust error handling and input validation.
* Add more comprehensive logging.
* Optimize the solution algorithms for better performance.
* Incorporate visualization of the generated schedules.

Entropy Calculation Scripts

This repository contains Python scripts for calculating entropy based on different data sources. 
These scripts are useful for computational chemistry and molecular simulations, where entropy calculations are required for vibrational, internal and  c2 entropy.
Files

    vib_entropy.py: Calculates vibrational entropy from a log or text file containing frequency data or force constants in normal modes.
    int_c2_entro.py: Computes internal entropy (int_entropy) and C2 entropy (c2) from a CSV file of MMPBSA analysis results, specifically extracting GGAS values.

    Usage
1. vib_entropy.py

This script calculates vibrational entropy (S_total) based on frequencies or FI values from a log or text file.
Arguments:

    file_path: Path to the log or text file.
    --file_type: Specify log (default) for files with quadratic force constants or text for files with simple frequency values.

Command Example:

python vib_entropy.py path/to/your/file --file_type log

Output:

    Prints the total entropy (S_total) and R * S_total to the console.
    Saves FI(I,J) values to extracted_FI_values.txt if file_type is set to log.
2. int_c2_entro.py

This script computes internal entropy and C2 entropy based on GGAS values from an MMPBSA analysis CSV file.
Predefined Path:

    The input file path is set to /home/esma/workspace/pyentropy/FINAL_RESULTS_MMPBSA.csv. Modify this if your data is located elsewhere.

Outputs:

    Prints internal entropy (int_entropy), standard deviation, variance, and C2 entropy to the console.

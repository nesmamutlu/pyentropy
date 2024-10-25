import pandas as pd
import numpy as np
import argparse

K = 0.69504
R = 8.31446
T = 298.15

def calculate_Si(Theta_i, T):
    Si = ((Theta_i / T) / (np.exp(Theta_i / T) - 1)) - np.log(1 - np.exp(-Theta_i / T))
    return Si

parser = argparse.ArgumentParser(description="Calculate entropy from a log or text file.")
parser.add_argument('file_path', type=str, help='Path to the log or text file containing FI(I,J) or frequencies data')
parser.add_argument('--file_type', type=str, choices=['log', 'text'], default='log', help='Specify if the file is log or text')
args = parser.parse_args()

file_path = args.file_path
file_type = args.file_type

frequencies_FI = []
frequencies_list = []  

with open(file_path, 'r') as file:
    inside_fi_block = False
    for line in file:
        if file_type == 'log':
            if "QUADRATIC FORCE CONSTANTS IN NORMAL MODES" in line:
                inside_fi_block = True
            elif inside_fi_block and "Num. of" in line:
                inside_fi_block = False
            elif inside_fi_block:
                try:
                    data = line.split()
                    if len(data) == 5:
                        frequencies_FI.append(float(data[2]))
                except ValueError:
                    pass
        elif file_type == 'text':
            try:
                frequencies_list.append(float(line.strip()))
            except ValueError:
                pass  

if file_type == 'log' and frequencies_FI:
    with open("extracted_FI_values.txt", 'w') as fi_file:
        fi_file.write("FI(I,J) values:\n")
        for fi_value in frequencies_FI:
            fi_file.write(f"{fi_value}\n")

if frequencies_FI:
    df = pd.DataFrame(frequencies_FI, columns=["FI(I,J)"])
    df['Theta_i'] = df["FI(I,J)"] / K
    df['Theta_i/T'] = df["Theta_i"] / T
elif frequencies_list:
    df = pd.DataFrame(frequencies_list, columns=["Frequencies (cm-1)"])
    df['Theta_i'] = df["Frequencies (cm-1)"] / K
    df['Theta_i/T'] = df["Theta_i"] / T

if 'Theta_i' in df.columns:
    df['S_i'] = df.apply(lambda row: calculate_Si(row['Theta_i'], T), axis=1)

if 'S_i' in df.columns:
    S_total = df['S_i'].sum()
    S_total_R = R * S_total/4.184
    print(f"Total Entropy (S_total): {S_total}")
    print(f"Total Entropy multiplied by R (R * S_total): {S_total_R}")


print(df)



import pandas as pd
import numpy as np
K= 0.69504
R= 8.31446
T = 298.15


file_path = "/home/esma/workspace/Entropy/TEST_METHANE.LOG"

frequencies_FI = []

with open(file_path, 'r') as file:
    inside_fi_block = False
    for line in file:
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

df = pd.DataFrame(frequencies_FI, columns=["FI(I,J)"])

df['Theta_i'] = df["FI(I,J)"] / K
df['Theta_i/T'] = df["Theta_i"] / T

def calculate_Si(Theta_i, T):
    exp_term = np.exp(Theta_i / T)
    Si =((Theta_i / T) / (np.exp(Theta_i / T) - 1)) - np.log(1 - np.exp(-Theta_i / T))
    return Si


df['S_i'] = df.apply(lambda row: calculate_Si(row['Theta_i'], T), axis=1)
S_total = df['S_i'].sum()
S_total_R = R * S_total
print(f"Total Entropy (S_total): {S_total}")
print(f"Total Entropy multiplied by R (R * S_total): {S_total_R}")

print(df)




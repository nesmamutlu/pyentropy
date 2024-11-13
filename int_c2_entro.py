import pandas as pd
import numpy as np
import argparse

RT = 0.592451984

def read_ggas_values(file_path):
    ggas_values = []
    found_header = False
    with open(file_path, 'r') as file:
        ggas_column_index = None  
        for line in file:
            columns = line.strip().split(',')
            if not found_header:
                if 'Delta Energy Terms' in line:
                    found_header = True  
                continue
            if ggas_column_index is None:
                if 'GGAS' in columns:
                    ggas_column_index = columns.index('GGAS')
                continue
            if ggas_column_index is not None and len(columns) > ggas_column_index:
                try:
                    ggas_values.append(float(columns[ggas_column_index]))
                except ValueError:
                    continue
    return ggas_values

def calculate_int_entropy(df, RT):
    entropy = RT * np.log(np.average(df['EXP']))
    return entropy

def calculate_std_dev_and_variance(df):
    std_dev = df['GGAS'].std()  
    variance = df['GGAS'].var() 
    return std_dev, variance

def calculate_c2(variance, RT):
    return variance / (2 * RT)

def main(file_path):
    ggas_values = read_ggas_values(file_path)
    ggas_df = pd.DataFrame(ggas_values, columns=['GGAS'])
    avg = ggas_df['GGAS'].mean()
    
    ggas_df['EXP'] = np.exp((ggas_df['GGAS'] - avg) / RT)
    
    int_entropy = calculate_int_entropy(ggas_df, RT)
    std_dev, variance = calculate_std_dev_and_variance(ggas_df)
    c2 = calculate_c2(variance, RT)
    
    print("Internal Entropy (int_entropy):", int_entropy)
    print("Standard Deviation (std_dev):", std_dev)
    print("Variance (variance):", variance)
    print("C2 Entropy (c2):", c2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculates entropy using GGAS values.")
    parser.add_argument("file_path", type=str, help="Path to the CSV file with GGAS values")
    args = parser.parse_args()
    
    main(args.file_path)


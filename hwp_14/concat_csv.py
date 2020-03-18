import pandas as pd

f1 = pd.read_csv('df_1.csv')
f2 = pd.read_csv('df_2.csv')
# print(f1.columns)
# print(f2.columns)
f1.drop("Unnamed: 0", axis = 1, inplace = True)
f2.drop("Unnamed: 0", axis = 1, inplace = True)
merged = pd.concat([f1, f2], ignore_index=True, axis=0)
merged.to_csv('merged.csv')
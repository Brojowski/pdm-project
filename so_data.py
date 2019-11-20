#%%
import csv



with open('stackoverflow.csv', 'r') as so_csv:
    reader = csv.reader(so_csv)
    header = reader.next()
    for row in reader:
        
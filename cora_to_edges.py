# This script assumes that the CORA dataset is in a local 
# mysql database. Modify the mysql connector to use another
# location.
# https://relational.fit.cvut.cz/dataset/CORA
# It outputs a list of edges to cora_edges.csv in the format:
# vertex1, vertex2, edgeWeight

#%%
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="alex",
    database="cora"
)
cursor = mydb.cursor()

#%% Pull all paper words out

cursor.execute("SELECT paper_id, word_cited_id FROM content ORDER BY paper_id")

papersToWords = dict()

for row in cursor:
    if not row[0] in papersToWords:
        papersToWords[row[0]] = list()
    
    papersToWords[row[0]].append(str(row[1]))

print(papersToWords)

#%%

def similarity(v1WordsList, v2WordsList):
    v1words = set(v1WordsList)
    v2words = set(v2WordsList)
    return len(v1words.intersection(v2words)) / len(v1words.union(v2words))

#%% Generate Edge weights

cursor.execute("SELECT citing_paper_id, cited_paper_id FROM cites")

citingKey = 'citing'
citedKey = 'cited'
edgeWeightKey = 'eWeight'

edges = list()

for citation in cursor:
    res = dict()
    citing = citation[0]
    res[citingKey] = citing 
    cited = citation[1]
    res[citedKey] = cited
    res[edgeWeightKey] = similarity(papersToWords[citing], papersToWords[cited])
    if res[edgeWeightKey] > 0:
        edges.append(res)

edges

# %% Write Edge to CSV file
import csv

with open('cora_edges.csv', 'w+') as coraEdgesFile:
    writer = csv.writer(coraEdgesFile)
    for e in edges:
        print(e)
        props = [v for k,v in e.items()]
        writer.writerow(props)




# %%

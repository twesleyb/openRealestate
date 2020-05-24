#!/usr/bin/env python3

import re
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN

## User parameters:

def combine_complexes(df,stop_words,ngram_range,eps):
    complexes = [re.sub(r"[^a-zA-Z0-9]+", ' ', name) for name in df.Complex]
    vectorizer = TfidfVectorizer(strip_accents="ascii", 
            lowercase=True, 
            stop_words=stop_words, 
            ngram_range=ngram_range, 
            binary=True, 
            use_idf=False)
    tf_idfs = vectorizer.fit_transform(complexes)
    clusterer = DBSCAN(eps=eps, min_samples=2)
    clusters = pd.Series(clusterer.fit_predict(tf_idfs))
    k = clusters.max()
    print("Total number of clusters: {}.".format(k),file=sys.stderr)
    return(clusters)
# EOF

# Ignore these words.
stop_words = ['complex','protein']

# Read input data.
df = pd.read_csv('complexes.csv', header=0)

# First round of clustering.
part1 = combine_complexes(df,stop_words,ngram_range=(0,3),eps=1)
df['Cluster'] = part1.values

# Subset the data and try again.
idx = clusters < 1
subdf = df[idx]

# Second round of clustering.
part2 = combine_complexes(subdf,stop_words,ngram_range=(1,3),eps=1)

# Add cluster to df.
df.loc[idx,'Cluster'] = part2.values + 2 + max(part1)

# Save to csv.
df.to_csv("clustered.csv")

# Examine the result.
for i in range(clusters.max()):
    print(f"\n\nMembers of cluster {i}:")
    print(df.loc[clusters==i,:])

# Recluster the large cluster:
df = pd.read_csv('recluster.csv', header=0)

# Third round of clustering.
part3 = combine_complexes(df,stop_words,ngram_range=(0,3),eps=1.1)
df['Cluster'] = part3.values

# Examine the result.
df.to_csv('recluster_result.csv')

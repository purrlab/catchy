import pandas as pd
import numpy as np
np.random.seed(1907)

df = pd.read_csv('../../data/papers_citations_per_year.csv')
df["citation_total"] = df[list(df.columns[5:])].sum(axis=1)
df_sorted_by_total_citations = df.sort_values(by=["venue_published","year_published","citation_total"])

lst_selected_papers = []
for venue in df_sorted_by_total_citations["venue_published"].unique():
    df_venue = df_sorted_by_total_citations[df_sorted_by_total_citations["venue_published"].isin([venue])]
    for year in df_venue["year_published"].unique():
        df_venue_year = df_venue[df_venue["year_published"]==year]
        df_venue_year = df_venue_year.reset_index()
        nb_papers = len(df_venue_year)
        lst_idx_paper_selected = []
        for i in range(10):
            nb_papers_ten_percent = int(nb_papers*10/100)
            lst_idx_paper_selected.append(np.random.randint(i*nb_papers_ten_percent,min((i+1)*nb_papers_ten_percent,nb_papers)))
        lst_selected_papers.append(df_venue_year.iloc[lst_idx_paper_selected])

df_selected_papers = pd.concat(lst_selected_papers)
df_selected_papers.to_csv("../../data/selected_papers_annotations.csv",index=False)
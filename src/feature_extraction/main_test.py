'''
Get all features from given list of papers
code structure:
src/feature_extraction/
│
├── main_test.py               # Main script: loads data, extracts features, saves CSV
├── get_feature_a.py
├── get_feature_b.py
├── ...
data/metadata/
├── selected_papers_annotations_final.csv
data/imgs/
├── ...  (For test time, download the imgs and pdfs from google drive)
data/pdfs/
├── ... (For test time, download the imgs and pdfs from google drive)
  
'''

import pandas as pd
import csv
import os
from tqdm import tqdm


# FORMAT: from get_feature_a import get_feature_a1, get_feature_a2, get_feature_a3
from get_features_lftk import get_features_lftk_all

'''
metadata contains:
['index', 'title', 'venue_published', 'year_published', 'authors',
       'abstract', 'pdf_path', 'img_path', 'semanticscholar_id',
       'citation_count_openalex', 'citations_per_year_openalex',
       'citation_count_semantics', 'citations_per_year_semantics']

output scv contains title,venue_published,year_published; 
       and features extracted from the paper
'''

INPUT_CSV = "data/metadata/selected_papers_annotations_final.csv"
OUTPUT_CSV = "results/extracted_features/" + INPUT_CSV.split('/')[-1].replace('.csv', '_features.csv')



def load_dataset(csv_path):
    """Loads metadata as a DataFrame and yields rows as dicts."""
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        yield row.to_dict()



def main():

    results = []

    for file in tqdm(load_dataset(INPUT_CSV)):
        try:
            features_lftk = get_features_lftk_all(file)
            # TODO: 
            # other features
            # ....
            result = {
                'title': file.get('title'),
                'venue_published': file.get('venue_published'),
                'year_published': file.get('year_published'),
                **features_lftk,
                # TODO
                # other features 
            }
            results.append(result)

            

        except Exception as e:
            print(f"Error processing {file.get('pdf_path')}: {e}")    
        


    if results:
        keys = results[0].keys()
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

    
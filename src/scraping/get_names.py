"""
Script to obtain citations per year for downloaded papers
usage (inside root folder):  python ./scraping/get_citations.py
"""
import glob
import pandas as pd
import requests
import time
from collections import Counter
from tqdm import tqdm
import csv
import re
from dotenv import find_dotenv, load_dotenv
import os

YEARS = [2024,2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013]

if __name__ == "__main__":
    load_dotenv(find_dotenv())

    paths_pdf = glob.glob("./data/pdfs/*/*.pdf")
    papers_names = [path.split("/")[-1].removesuffix(".pdf") for path in paths_pdf]
    venues_papers = [path.split("/")[-2] for path in paths_pdf]
    with open("./data/papers_names_years_venues.csv", "a") as csv_file:
        fieldnames = ["title","venue_published","year_published","pdf_path"]
        fieldnames += [f"citations_{year}" for year in YEARS]
        csvwriter = csv.writer(csv_file)
        paper_num = 0
        for path,title,venue in tqdm(zip(paths_pdf,papers_names,venues_papers),total=len(paths_pdf)):
            row = [title,venue[:-4],venue[-4:],path]
            csvwriter.writerow(row)

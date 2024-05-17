"""
This script gather the list of papers from venues in the Resources/data/venues.csv.
The result will be a csv file in Results/extraction/papers_from_venues.csv 

Usage:
From root directory:
    python request_dblp.py
"""
import requests
import csv
import time
import pandas as pd
import os
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import html

def get_papers_from_venue(venue_name,api_link):
    """
    Query dblp api with api_link parameter to search gather papers from the venue specified in venue_name between start_year and end_year.
    @params:
        -venue_name (string): Name of the venue (ex: "MICCAI" or "MIDL")
        -api_link (string): dblp api link for the specific venue
    @return:
        A list of dictionary, each element containing the following fields: doi,title,venue 
    """
    indice_paper = 0
    nextPage = True
    #Dictionnary with doi as key and title as value
    lst_paper = []
    while nextPage:
        # Construct the url adding the index of the first paper (useful to parse multiple page)
        request_url = f"{api_link}&f={indice_paper}"   
        request = requests.get(request_url)
        if request.status_code == 200:
            r_json = request.json()
            if r_json["result"]["hits"]["@sent"] != '0':
                for paper in r_json["result"]["hits"]["hit"]:
                    if ("doi" not in paper["info"] and "title" not in paper["info"]) or paper["info"]["venue"] != venue_name:
                        continue
                    
                    title = paper["info"].get("title","None")
                    title = title.replace(",","")
                    title = title.replace("\n","")
                    title = title.replace("/"," ")
                    title = title.removesuffix(".")
                    title = html.unescape(title)

                    year = paper["info"].get("year","None")
                    venue = paper["info"].get("venue","None")
                    doi = paper["info"].get("doi","None")
                    lst_paper.append({
                        "doi":doi,
                        "title":title,
                        "venue":venue,
                        "year":year
                    })
                indice_paper += 1000
            else:
                nextPage = False
            
            #To follow API guidelines to not send too much request in a short amount of time (https://dblp.org/faq/1474706.html)
            time.sleep(2)
        elif request.status_code == 429:
            print("TOO MANY REQUEST, RETRY LATER")
            nextPage = False
        else:
            print(f"ERROR {request.status_code} DURING REQUEST, RETRY LATER!")
            nextPage = False
    return lst_paper

def get_fulltext_url(paper):
    """
    Query OpenAlex API with the doi of the paper.
    @param:
        -doi: doi of the paper to search for
        -venue: name of the venue the paper was published in (useful for saving and futur usage)
    @return:
        -dictionary with the paper information if found on openalex, None otherwise
    """
    doi = paper["doi"]
    
    request_url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    request = requests.get(request_url)
    if request.status_code == 200:
        r_json = request.json()
        if r_json["open_access"] and r_json["open_access"]["oa_url"]:
            fulltext_url = r_json["open_access"]["oa_url"]
        else:
            if r_json["primary_location"]:
                if r_json["primary_location"]["pdf_url"]:
                    fulltext_url = r_json["primary_location"]["pdf_url"]
                elif r_json["primary_location"]["landing_page_url"].endswith("pdf"):
                    fulltext_url = r_json["primary_location"]["landing_page_url"]
                else:
                    fulltext_url = None
            else:
                fulltext_url = None
        
        return fulltext_url
    return None

def download_pdf(paper,paper_url):
    title = paper["title"]
    year = paper["year"]
    os.makedirs(f"../../data/pdfs/CHI{year}/", exist_ok=True)

    try:
        r_fulltext = requests.get(paper_url,allow_redirects=True,timeout=10)
        if r_fulltext.status_code == 200:
            open(f"../../data/pdfs/ICML{year}/{title}","wb").write(r_fulltext.content)
            try:
                #Try to read the pdf (Raise an error if the file is an invalid pdf)
                PdfReader(f"../../data/pdfs/ICML{year}/{title}",strict=True)
                return True
            except PdfReadError:
                #If a PdfReadError is raised, the pdf is invalid and therefore removed from downloaded list
                os.remove(f"../../data/pdfs/ICML{year}/{title}") 
                return False
        else:
            return False

    except requests.exceptions.RequestException as ce:
        return False

def main():
    #For each venue, gather the list of paper
    venue = "CHI"
    years = [2023,2013]

    # years = [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013]
    lst_papers_all = [] 
    for year in years:
        api_url = f"https://dblp.dagstuhl.de/search/publ/api?q=toc%3Adb/conf/chi/chi{year}.bht%3A&h=1000&format=json"
        lst_papers_venue = get_papers_from_venue(venue,api_url)
        lst_papers_all += lst_papers_venue


    # for paper in lst_papers_all:
    #     print("Fetching url for",paper["title"])
    #     fulltext_url = get_fulltext_url(paper)
    #     if fulltext_url:
    #         print("URL obtained:",fulltext_url,"Downloading paper...")
    #         downloaded_status = download_pdf(paper,fulltext_url)
    #     else:
    #         downloaded_status = False
    #     print("Paper download status:",downloaded_status,"\n")
    #     paper["downloaded"] = downloaded_status

    df_papers = pd.DataFrame(lst_papers_all)
    df_papers.to_csv("./chi_papers.csv")
    # #Save the results in papers_from_venues.csv
    # fields = ["doi", "title", "venue"]
    # with open("./Results/extraction/papers_from_venues.csv", "w", newline="") as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=fields)
    #     # Write the header row (column names)
    #     writer.writeheader()
        
    #     # Write the data
    #     for paper in lst_papers_all:
    #         writer.writerow(paper)
    


if __name__ == "__main__":
    print("Extraction started")
    main()
    print("Extraction finished, see results at Results/extraction/papers_from_venues.csv")
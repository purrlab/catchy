#Following idea from Deep Paper Gestalt: https://arxiv.org/pdf/1812.08775, convert pdfs into images of grid 2x4
import glob
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import os

"""
From https://stackoverflow.com/questions/37921295/python-pil-image-make-3x3-grid-from-sequence-images.
"""
def image_grid(imgs, rows, cols):
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs[:8]):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

def paper_pdf_to_image(paper_path):
    images_from_path = convert_from_path(paper_path)
    grid_img = image_grid(images_from_path,2,4)
    
    path_to_save = paper_path.replace("pdfs","imgs").removesuffix(".pdf")
    print()
    os.makedirs(f"./data/imgs/{path_to_save.split("/")[-2]}/", exist_ok=True)
    grid_img.save(path_to_save+".png")

def main():
    #Get list of pdfs
    pdfs = glob.glob("./data/pdfs/*/*.pdf")
    #For each pdf, convert into image and save
    for paper_path in tqdm(pdfs):
        paper_pdf_to_image(paper_path)
        break

if __name__ == "__main__":
    main()
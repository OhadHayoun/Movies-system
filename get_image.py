import requests
import shutil
import pandas as pd
from bs4 import BeautifulSoup
import os

def check_folder():
    directory_path = os.getcwd()
    print("My current directory is : " + directory_path)
    folder_name = os.path.basename(directory_path)
    print("My directory name is : " + folder_name)
    return directory_path


def clear_folder():
    # Get directory name
    mydir = 'posters'
    ## Try to remove tree; if failed show an error using try...except on screen
    try:
        shutil.rmtree(mydir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

def getdata(url):
    r = requests.get(url)
    return r.text

def get_img_src_by_title(md_df, titles_list = []):

    BASE_URL = 'https://www.imdb.com/title/'

    # md_df = pd.read_csv(DIR_PATH + 'movies_metadata.csv')
    # md_df = pd.read_csv(file_path)

    imdb_id_list = []
    images_src = []

    for title in titles_list:
        imdb_id_list.append(md_df['imdb_id'][md_df['title'] == title].values[0])
        # imdb_id_list.append(md_df['imdb_id'][md_df['title'] == title].values[0])

    images_src = []

    # getting images source urls
    for i in range(len(titles_list)):
        htmldata = getdata(BASE_URL + imdb_id_list[i])
        soup = BeautifulSoup(htmldata, 'html.parser')
        # l1 = soup.find_all('img')
        poster_div = soup.find('div', {'class': 'poster'})
        images = poster_div.findAll('img')
        # images_src.append(images[0]['src'].split('_V1_')[0]+ '_V1_') # for bigger images
        images_src.append(images[0]['src']) # for small images


    return images_src


def get_img_src(DIR_PATH, n_images):

    BASE_URL = 'https://www.imdb.com/title/'

    md_df = pd.read_csv(DIR_PATH + 'movies_metadata.csv')
    imdb_id_list = md_df['imdb_id'].tolist()
    titles_list = md_df['title'].tolist()

    images_src = []

    # getting images source urls
    for i in range(n_images):
        htmldata = getdata(BASE_URL + imdb_id_list[i])
        soup = BeautifulSoup(htmldata, 'html.parser')
        # l1 = soup.find_all('img')
        poster_div = soup.find('div', {'class': 'poster'})
        images = poster_div.findAll('img')
        images_src.append(images[0]['src'].split('_V1_')[0]+ '_V1_')

    return images_src , titles_list

# downloading images
def save_images(images_src, titles_list):
    if not os.path.exists('posters'):
        os.makedirs('posters')

    for i,src in enumerate(images_src):
        # saving file
        resp = requests.get(src, stream=True)
        # Open a local file with wb ( write binary ) permission.
        local_file = open('posters/' + titles_list[i] + '.jpg', 'wb')
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        resp.raw.decode_content = True
        # Copy the response stream raw data to local image file.
        shutil.copyfileobj(resp.raw, local_file)
        # Remove the image url response object.
        del resp


def main(csv_file,titles_list):


    images_src = get_img_src_by_title(csv_file, titles_list)

    # images_src, titles_list = get_img_src(CSV_DIR_PATH,n_images)
    save_images(images_src, titles_list)

if __name__ == '__main__':

    directory_path = check_folder()
    CSV_DIR_PATH = "C:\\Users\\liat grinberg\\Desktop\\Ohad\\ITC course\\Project 2\\Data files\\Kaggle data-small\\"
    n_images = 5

    titles_list = ['Toy Story', 'Heat']
    csv_file = 'movies_data.csv'

    main(csv_file,titles_list)
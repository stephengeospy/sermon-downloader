from bs4 import BeautifulSoup
import requests
import urllib
import datetime

''' 
URL of the archive web-page which provides link to 
all video lectures. It would have been tiring to 
download each video manually. 
In this example, we first crawl the webpage to extract 
all the links and then download videos. 
'''

# specify the URL of the archive here 
archive_url = "https://cdn.sermons.love/mp4/Joseph%20Prince/"

def get_video_links(): 
    
    # create response object 
    r = requests.get(archive_url) 
    
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content,'html5lib') 
    
    # find all links on web-page 
    links = soup.findAll('a') 

    # filter the link sending with .mp4 
    video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')] 

    return video_links 


def download_video_series(video_links): 

    for link in video_links: 

        '''iterate through all links in video_links 
        and download them one by one'''
        
        #print(f'URL: {link}')
        # obtain filename by splitting url and getting last string 
        file_name_raw = link.split('/')[-1]
        file_name = urllib.parse.unquote(file_name_raw, encoding='utf-8', errors='replace')

        print(f'Downloading file: {file_name}')
        
        # create response object 
        r = requests.get(link, stream=True) 
        
        # download started 
        with open(f'resources/{file_name}', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024): 
                if chunk: 
                    f.write(chunk)

        print(f'End time: {datetime.datetime.now()}')
        #print(f'{file_name} downloaded!')

    print(f'All videos downloaded!')
    return


if __name__ == "__main__": 

    # # getting all video links 
    # video_links = get_video_links()
    # print(video_links)

    # with open('listfile.txt', 'w') as f:
    #     for item in video_links:
    #         f.write(item + "\n")

    video_links = []
    with open("resources/list_full_videos_download_ERROR.txt", "r") as f:
        video_links = f.readlines()

    video_links = [x.strip('\n') for x in video_links ]
    print(video_links)

    # download all videos
    print(f'Start time: {datetime.datetime.now()}')
    download_video_series(video_links) 

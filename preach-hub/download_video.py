import requests
import datetime
from bs4 import BeautifulSoup


def check_timeline(timeline, download_link):
    if (len(timeline.split(':')) > 2) or int(timeline.split(':')[0]) > 20:
        print("Success", timeline, download_link)
        download_link, title = download_link
        return timeline, download_link, title
    else:
        return None


def get_video_links():
    # create response object 
    r = requests.get(download_url, verify=False)
    
    # create beautiful-soup object 
    soup = BeautifulSoup(r.content, 'html5lib')

    # Find all lists
    all_lists = soup.findAll('li', {"class": "col-xs-6 col-sm-4 col-md-3"})

    # find all links on web-page
    span_time_lines = [x.find("span", {"class": "pm-label-duration"}).text for x in all_lists]
    download_links = [(x.findAll("a")[1]['href'], x.findAll("a")[1]['title']) for x in all_lists]

    # filter the link sending with .mp4
    filtered_links = [x for x in map(check_timeline, span_time_lines, download_links) if (not x == None) and ('vid=' in x[1])]

    return filtered_links


def download_video_series(video_links):
    """iterate through all links in video_links and download them one by one"""

    for video_link in video_links:
        timeline, link, title = eval(video_link)

        print(f'Downloading file: {title}')

        r = requests.get(link, stream=True)
        with open(f'resources/{title}.mp4', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)

        print(f'End time: {datetime.datetime.now()}')

    print(f'All videos downloaded!')
    return


if __name__ == "__main__":

    # specify the URL of the archive here
    download_url = "https://www.preachub.com/search.php?keywords=Joseph+Prince"

    # getting all video links
    video_links = get_video_links()
    print(video_links)

    with open('resources/preachhub_jp_sermon_links.txt', 'w') as f:
        for item in video_links:
            print(item, file=f, end="\n")

    # with open("resources/preachhub_jp_sermon_links.txt", "r") as f:
    #      video_links = f.readlines()
    #
    # video_links = [x.strip('\n') for x in video_links]

    # download all videos
    print(f'Start time: {datetime.datetime.now()}')
    download_video_series(video_links)

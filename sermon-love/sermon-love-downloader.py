from bs4 import BeautifulSoup
import requests
import urllib
import datetime
import sys
import os


def get_video_links():
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.content, 'html5lib')
    links = soup.findAll('a')
    video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')]
    return video_links 


def compare_with_master(video_links):
    with open(f"resources/{master_file}") as f:
        master_links = f.readlines()
        master_links = [x.strip('\n') for x in master_links]
        return [link for link in video_links if link not in master_links]


def write_new_to_master(new_link):
    with open(f"resources/{master_file}", "a") as f:
        print(new_link, file=f)


def download_video_series(video_links):
    print(f'Start time: {datetime.datetime.now()}')

    for link in video_links:
        file_name_raw = link.split('/')[-1]
        file_name = urllib.parse.unquote(file_name_raw, encoding='utf-8', errors='replace')

        print(f'Downloading file: {file_name}')
        try:
            r = requests.get(link, stream=True)
            with open(f'resources/{file_name}', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)

            print(f'End time: {datetime.datetime.now()}')
            write_new_to_master(link)
        except Exception as e:
            print(f"Failed to download - {file_name}")
            print(e)
            sys.exit(1)

    print(f'All videos downloaded!')


if __name__ == "__main__":
    master_file = "sermon_love_jp_master_list.txt"
    archive_url = "https://cdn.sermons.love/mp4/Joseph%20Prince/"

    # getting all video links
    video_links = get_video_links()

    # Check for new links against master list and write down
    new_links = compare_with_master(video_links)

    if len(new_links) > 0:
        print("New Video Links have come up!!")
        for index, link in enumerate(new_links):
            print(index, link)

        arg = input("You want to process to download? - \n")

        if arg.upper() == 'YES':
            download_video_series(new_links)
        else:
            print("Not downloading now, see you later!!")
    else:
        print("There are no new video links now!!")

    # video_links = []
    # with open("resources/list_full_videos_download_ERROR.txt", "r") as f:
    #     video_links = f.readlines()

    # video_links = [x.strip('\n') for x in video_links ]
    # print(video_links)

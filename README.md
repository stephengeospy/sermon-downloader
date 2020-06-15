# Sermon Downloader
Sermon Downloader is a web scraping project to download the videos from two websites:  
1. [PreachHub](https://www.preachub.com/search.php?keywords=joseph+prince) 
2. [SermonLove](https://cdn.sermons.love/mp4/Joseph%20Prince/)

## Packages required 
The main packages required and have to be installed:
1. `requests` for performing our HTTP requests.  
2. `BeautifulSoup4` for handling all of our HTML processing.

To install these dependencies with `pip`:
```shell
pip install requests BeautifulSoup4
```

## How the web scrapping has been done
1. The python script scrapes all the video links (ending with `.mp4`) from the specified URLs and makes a list. 
2. This list of video links is then compared with the set of links present in a master file (that is having links to the videos already downloaded) and create a list of new links.
3. The new videos are then downloaded and the master file is updated accordingly.

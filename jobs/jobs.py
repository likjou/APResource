from main.models import TorFile
from torrentool.api import Torrent
import os
from tracker_scraper import scrape

def getinfo():
    print("job running...")
    all_files = TorFile.objects.all()

    #total peers and seed
    total_completed = 0
    total_seeds = 0
    total_leechers = 0

   

    for files in all_files:
        #keep all tracker responses
        results = []
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = BASE_DIR + "/media/" +str(files.file_field)

        #parse file using torrent tool
        my_torrent = Torrent.from_file(path)

        #get info_hash using torrent tool
        info_hash = my_torrent.info_hash

        #Torrent urls by torrent tool
        announce_url = my_torrent.announce_urls
        url_list = []

        #parse urls using urlparse
        for list in announce_url:
            for urls in list:
                url_list.append(urls.rstrip("/announce")) 

        #connect and record the response of tracker
        for url in url_list:
            try:
                res = scrape(tracker=url,hashes=[info_hash])[info_hash]
                response = {
                "seeds" : res['seeds'],
                "leechers" : res['peers'],
                "completed" : res['complete'],
                "url" : url,    
                }
                results.append(response)
            except Exception as e:
                print(e)
        
        for result in results:
            total_completed = total_completed + result['completed']
            total_seeds = total_seeds + result['seeds']
            total_leechers = total_leechers + result['leechers']
        files.total_completed = total_completed
        files.total_seeds = total_seeds
        files.total_leechers = total_leechers
        files.save()
    print("job Done.")
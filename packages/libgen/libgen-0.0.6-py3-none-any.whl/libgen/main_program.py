import json
import requests
import argparse
from pprint import pprint
from libgen import Scraper


def main():
    args = argparse.ArgumentParser(description="cli tool for library genesis")
    args.add_argument('--url', help='download by url')
    args.add_argument('--id', help='download by id')
    args.add_argument("--output", help="output file name")
    args.add_argument("search", help="search the library", nargs='?')
    args.add_argument("download", help="download a file")
    res = args.parse_args()

    if res.search:
        search_term = res.search
        data = Scraper.get_data(search_term)
        pprint(data)
    if res.download:
        if res.url:
            link = res.url
            if res.output:
                output_path = res.output
            else:
                output_path = None
            output = Scraper.download(link, output_path)
            if not output:
                print('[ERROR] Invalid URL')
        elif res.id:
            resp = requests.get(f'http://gen.lib.rus.ec/json.php?ids={res.id}&fields=Author,Title, md5')
            if resp:
                data = json.loads(resp.content)
                data = data[0]
                author = data["author"]
                title = data["title"]
                md5 = data["md5"]
                link = f"http://93.174.95.29/main/{md5}"
                print(f"[INFO] Author: {author}")
                print(f"[INFO] Title : {title}")
                if res.output:
                    output_path = res.output
                else:
                    output_path = None
                output = Scraper.download(link, output_path)
                if not output:
                    print('[ERROR] Download failed...')
            else:
                print("[ERROR] Invalid ID")
        # else:
        #     print("[INFO] Please provide a valid download method")
    else:
        print("[INFO] No arguments provided... Try `libgen --help` for more")

import uuid
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


class Scraper:
    @staticmethod
    def get_data(query):
        query = query.replace(" ", "+")
        url = f"https://libgen.is/search.php?req={query}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        data = soup.find_all('table')[2]
        data = data.find_all('tr')
        data = data[1:]
        dataset = []
        for d in data:
            info = d.find_all('td')
            information = {
                "id": info[0].text,
                "author": info[1].text,
                "name": info[2].text,
                "publisher": info[3].text,
                "year": info[4].text,
                "lang": info[6].text,
                "size": info[7].text,
                "format": info[8].text,
                "link": info[9].find_all('a')[0].get('href'),
            }
            dataset.append(information)
        return dataset

    @staticmethod
    def download(ref, output_path=None):
        url = None
        res = requests.get(ref)
        soup = BeautifulSoup(res.text, "html.parser")
        for info in soup.find_all('a'):
            if info.text == "GET":
                url = info.get('href')
        if url is not None:
            if output_path is None:
                output_path = str(uuid.uuid4()) + '.' + url.split('.')[-1]
            res = requests.get(url, stream=True)
            file_size = int(res.headers.get("Content-Length", 0))
            progress = tqdm(
                res.iter_content(1024),
                f"Downloading: {output_path}",
                total=file_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024
            )
            with open(output_path, "wb") as f:
                for data in progress:
                    f.write(data)
                    progress.update(len(data))
            return True
        return False

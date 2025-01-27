import requests
from bs4 import BeautifulSoup
from utils import *
import py7zr
import wget

curr_dir  = os.path.dirname(__file__)
class Stack_Exchange_Downloader():

    def __init__(self, name):
        """
        :param name: name of stackexchange site to download. If all, will download all stackexchanges & metas.
        """
        sitesmap = requests.get("https://ia600107.us.archive.org/27/items/stackexchange/Sites.xml").content
        self.name = name.replace("http://", "").replace("https://", "").replace(".com", "").replace(".net", "")
        self.sites = {}
        self.parse_sitesmap(sitesmap)

    def parse_sitesmap(self, sitesmap):
        soup = BeautifulSoup(sitesmap, "lxml")
        for site in soup.find_all("row"):
            url = site['url'].replace("https://", "")
            site_name = url.replace(".com", "").replace(".net", "")
            download_link = "https://archive.org/download/stackexchange/" + url + ".7z"
            if url == "stackoverflow.com":
                download_link = "https://archive.org/download/stackexchange/Stackoverflow.com-Posts.7z"
            self.sites[site_name] = {"url" : url, "download" : download_link}

    def download(self):
        if self.name == "all":
            for k in self.sites:
                wget.download(self.sites[k]["download"], curr_dir + '/dumps')
        else:
            wget.download(self.sites[self.name]["download"], curr_dir + '/dumps')

    def extract(self):
        if self.name == "all":
            for k in self.sites:
                # archive = py7zr.SevenZipFile('dumps/{}'.format(self.sites[k]["download"].replace("https://archive.org/download/stackexchange/", "")
                #                                                , mode='r'))
                # archive.extractall()
                # archive.close()
                command = "py7zr x {}/dumps/{} {}/dumps/{}".format(curr_dir, self.sites[k]["download"].replace("https://archive.org/download/stackexchange/", ""), curr_dir, k)
                print(command)
                if os.system(command):
                    print('Extraction for {} failed!'.format(k))
        else:
            # archive = py7zr.SevenZipFile(
            #     'dumps/{}'.format(self.sites[self.name]["download"].replace("https://archive.org/download/stackexchange/", "")
            #                       , mode='r'))
            # archive.extractall()
            # archive.close()
            command = "py7zr x {}/dumps/{} {}/dumps/{}".format(curr_dir, self.sites[self.name]["download"].replace("https://archive.org/download/stackexchange/", ""), curr_dir, self.name)
            print(command)
            if os.system(command):
                print('Extraction for {} failed!'.format(self.name))
from bs4 import BeautifulSoup
from bs4 import element
import sys
import os
import urllib3.request
import certifi
import hashlib
import json
import pathlib
import argparse
import platform
import pkg_resources

from progressbar import DataTransferBar
from requests_download import download, HashTracker, ProgressTracker

class MetaData():
    author = ""
    authorUrl = ""
    description = ""
    paletteName = ""

    def __init__(self, url):
        src = BeautifulSoup(http.request("GET", url).data, "html.parser")

        sectionData = src.find("section", {"class":"left"})

        desc = ""
        for value in sectionData.contents[4:]:
            if type(value) is element.NavigableString:
                desc += value
            else:
                desc += value.text

        self.description = desc.strip()

        self.paletteName = sectionData.find("h1").text

        self.paletteName = self.paletteName[:self.paletteName.rfind(" Palette")]
        
        if sectionData.find("p", {"class":"attribution"}) is not None:
            authorData = sectionData.find("p", {"class":"attribution"}).find("a")
            self.author = authorData.text
            self.authorUrl = "https://lospec.com" + authorData["href"]
    
    def __str__(self):
        return self.author + "\n" + self.authorUrl + "\n" + self.description + "\n" + self.paletteName


user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where(), headers=user_agent)


hasher = HashTracker(hashlib.sha256())
progress = ProgressTracker(DataTransferBar())

EXTENSIONS_PATH = ""

if platform.system() == "Windows":
    EXTENSIONS_PATH = pathlib.Path.home().joinpath("AppData").joinpath("Roaming").joinpath("Aseprite").joinpath("extensions")
elif platform.system() == "Linux":
    EXTENSIONS_PATH = pathlib.Path.home().joinpath(".config").joinpath("extensions")
elif platform.system() == "Darwin":
    EXTENSIONS_PATH = pathlib.Path.home().joinpath("Library").joinpath("Application Support").joinpath("Aseprite").joinpath("extensions")
else:
    print("Unknown platform") 

EXTENSIONS = [
    "-1x.png",
    "-8x.png",
    "-32x.png",
    ".pal",
    ".ase",
    ".txt",
    ".hex",
    ".gpl"
]

def importLospec(url):

    for extension in EXTENSIONS:
        url = url.replace(extension, "")

    url_gpl = url +".gpl"
    
    filename = os.path.basename(url_gpl)

    metadata = MetaData(url)

    PALETTES_PATH = ""
    if metadata.author != "":
        PALETTES_PATH = EXTENSIONS_PATH.joinpath(metadata.author)
    else:
        PALETTES_PATH = EXTENSIONS_PATH.joinpath("lospec-palettes")

    PALETTES_PATH.mkdir(parents=True, exist_ok=True)
        

    JSON_FILE_PATH =  PALETTES_PATH.joinpath("package.json")

    jsonmetadata = ""

    if not JSON_FILE_PATH.exists():

        src = pkg_resources.resource_string(__name__, "template.json").decode("utf-8")

        jsonmetadata = json.loads(src)

        if metadata.author != "":
            jsonmetadata["name"] = metadata.author
            jsonmetadata["displayName"] = metadata.author
            jsonmetadata["description"] = "Palettes created by " + metadata.author + " on Lospec"
            jsonmetadata["author"]["name"] = metadata.author
            jsonmetadata["author"]["url"] = metadata.authorUrl
    else:
        f = open(JSON_FILE_PATH, mode="r")
        jsonmetadata = json.load(f)
        f.close()
        

    download(url_gpl, PALETTES_PATH.joinpath(filename), trackers=(hasher, progress))

    name = metadata.paletteName

    jsonmetadata["contributes"]["palettes"].append({"id":name, "path":filename})

    f = open(JSON_FILE_PATH, "w")
    json.dump(jsonmetadata, f, indent=4, sort_keys=True)
    f.close()




def main():

    parser = argparse.ArgumentParser(description="Import palettes from Lospec to Aseprite")
    #parser.add_argument("-d", action="store", dest="outdir", help="Output directory for your files")
    parser.add_argument("url", action="store", help="Url of the palette page or file")

    res = parser.parse_args()
    #print(MetaData(res.url))
    importLospec(res.url)


if __name__ == "__main__":
    main()
    
    
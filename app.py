# 4chan web scraper link: http://boards.4chan.org/pol/thread/195975634/british-english-or-american

import requests, os, random, zipfile, shutil
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, url):
        content = self.getContent(url)
        self.dir = ""

        if not content:
            raise Exception('Invalid URL')

        links = self.getLinks(content)

        if len(links) == 0 or links == False:
            raise Exception('Cant get image links!')

        self.downloadImages(links)


    def getContent(self, url):
        try:
            return requests.get(url)
        except:
            return False


    def getLinks(self, soup):
        content = BeautifulSoup(soup.content)
        links = list()

        try:
            elements = content.find_all('a', {'class': 'fileThumb'})
        except: 
            return False
            

        for link in elements:
            temp = BeautifulSoup(str(link))
            link = temp.find('a', {'class': 'fileThumb'}, href=True)
            links.append("http:" + link['href'])

        return links


    def downloadImages(self, links):
        x = 0
        n = random.randint(1, 10000)
        self.dir = 'dir' + str(n)

        if os.path.isdir(self.dir):
            n = n * 7
        else:
            self.dir = 'dir' + str(n)
            os.mkdir(self.dir)

        for link in links:
            x += 1
            ext = 'jpg'
            try:
                linkExt = link[-3] + link[-2] + link[-1] 

                if linkExt == 'gif':
                    ext = 'gif'
                
                img_data = requests.get(link).content

                with open(self.dir + '/' + 'image' + str(x) + '.' + ext, 'wb') as handler:
                    handler.write(img_data)

                ext = 'png'
            except:
                print('Failed to get image')

        zf = zipfile.ZipFile("imageszip" + str(n) + ".zip", "w")

        if not zf:
            raise Exception('Failed to create zip')

        for dirname, subdirs, files in os.walk(self.dir):
            zf.write(dirname)
            for filename in files:
                zf.write(os.path.join(dirname, filename))

        zf.close()

        shutil.rmtree('dir' + str(n))
        self.dir = "imageszip" + str(n)


    def getDirectory(self):
        return self.dir

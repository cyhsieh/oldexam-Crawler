from pyquery import PyQuery as pq
import requests,os,time

class Prochtml():
    def __init__(self, html):
        self.html = html
        self.examtype = ""
        self.exam = ""
        self.subject = ""
        self.rootpath = "oldexamifles"
        self.site = "http://wwwc.moex.gov.tw"
        self.proxies = {
            "http":"proxy.cht.com.tw:8080" ,
            "https":"proxy.cht.com.tw:8080"
        } 
    def proc(self):
        for tr in pq(self.html)(".ULQandA tr"):
            # print(pq(tr).html())
            if pq(tr)("td").hasClass("level1"):
                # examtype
                self.examtype = pq(tr)("div").text()
                # print(self.examtype)
                continue
            elif pq(tr)("td").hasClass("level2"):
                # exam
                self.exam = pq(tr)("div div").text()
                print("--"+self.examtype+"-"+self.exam)
                continue
            else:
                # subject
                path = self.rootpath+os.sep+self.examtype+os.sep+self.exam+os.sep
               #  if not os.path.exists(path):
               #      os.makedirs(path)
                self.subject = pq(tr)("div div").text()
                print(self.subject)
                for file in pq(tr)("table tr td"):
                    a = pq(file)("a")
                    if pq(a).text():
                        filetype = pq(a).text()
                        filelink = pq(a).attr("href").replace("../..", self.site)
                        filename = path+filetype+"_"+self.subject+".pdf"
                        self.subject = pq(tr)("div div").text()
                        if not os.path.exists(path):
                            os.makedirs(path)
                        if os.path.exists(filename):
                            continue
                        '''
                        downloadfile = requests.get(filelink,stream=True, proxies=self.proxies)
                        with open(filename,"wb") as f:
                            for chunk in downloadfile.iter_content(chunk_size=1024):
                                f.write(chunk)
                                '''
                        print(pq(file)("a").text()+"link: "+filelink)
    def proc2(self):
        for tr in pq(self.html)(".ULQandA tr"):
            # print(pq(tr).html())
            if pq(tr)("td").hasClass("level1"):
                # examtype
                self.examtype = pq(tr)("table tr td").eq(1).text()
                # print(self.examtype)
                continue
            elif pq(tr)("td").hasClass("level2"):
                # exam
                self.exam = pq(tr)("table tr td").eq(2).text()
                print("--"+self.examtype+"-"+self.exam)
                continue
            else:
                # subject
                path = self.rootpath+os.sep+self.examtype+os.sep+self.exam+os.sep
               #  if not os.path.exists(path):
               #      os.makedirs(path)
                self.subject = pq(tr)("table tr td").eq(3).text()
                # print(self.subject)
                for file in pq(tr)("table tr td"):
                    a = pq(file)("a")
                    if len(a) > 1:
                        continue
                    if pq(a).text():
                        filetype = pq(a).text()
                        filelink = pq(a).attr("href").replace("../..", self.site)
                        filename = path+filetype+"_"+self.subject+".pdf"
                        # self.subject = pq(tr)("div div").text()
                        if not os.path.exists(path):
                            os.makedirs(path)
                        if os.path.exists(filename):
                            continue
                        downloadfile = requests.get(filelink,stream=True, proxies=self.proxies)
                        with open(filename,"wb") as f:
                            for chunk in downloadfile.iter_content(chunk_size=1024):
                                f.write(chunk)
                        print(self.subject+"-"+pq(file)("a").text()+"link: "+filelink)
                    # print()

# f = open("result.html","r")
f = open("source0.html","r", encoding="utf-8")
# print(f.read())
proc = Prochtml(f.read())
proc.proc2()

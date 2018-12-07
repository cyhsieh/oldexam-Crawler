#coding=utf-8

from pyquery import PyQuery as pq
from urllib.request import urlretrieve
import requests, os, time
# html = requests.get(pchomeurl, headers=headers)
# req = requests.post(url,headers=headers,proxies=proxies, data=payload)
# req = requests.post(url,headers=headers, data=payload)

# print(req)

# print(req.text)

# pqcontent = pq(req.text)
def prochtml(html="", site=""):
    proxies = {
     "http":"proxy.cht.com.tw:8080" ,
     "https":"proxy.cht.com.tw:8080"
     }
    pqcontent = pq(html)
    # pqcontent = pq(request.text)
    # print(pqcontent.outerHtml())
    result = pqcontent(".ULQandA")
    # print (result.outerHtml())
    # with open("result.html","w", encoding="utf-8") as f:
        # f.write(result.outerHtml())
    f_year = pqcontent(".level1")
    # print(len(pqcontent(".level1").eq(0).parents("tr").nextAll("tr .level2")))
    # print(len(pqcontent("#ctl00_holderContent_tblExamQand .level2")))
    changetype = False
    path = "./"
    for exam in pqcontent(".ULQandA .level1"):
        if changetype:
            print("\nchange!!\n")
            changetype=False
            continue
        ### year and exam type
        # examtype = pq(i)("td").eq(1).text()
        # print(examtype)
        #pq(i)("td").eq(1).text()## exam name
        # examname = pq(i).parents("tr").next("tr .level2")
        examtype = pq(exam)("table tr td div").text()
        for examname in pq(exam).parents("tr").nextAll("tr .level2").items():
            ename = pq(examname).text()
            print(ename)
            path = "oldexamFiles" + os.sep + examtype + os.sep + ename + os.sep
            print(path)
            if not os.path.exists(path):
                os.makedirs(path)
            # print(len(pq(examname).parents("tr").nextAll("tr .link_3 li table tr td div")))
            for subject_td in pq(examname).parents("tr").nextAll("tr td"):
                if pq(subject_td).hasClass("level2"):
                    break

                nexttr = pq(subject_td).parent("tr").next("tr td")
                if nexttr.hasClass("level1"):
                    changetype = True

                for subject in pq(subject_td)(".link_3 li table tr td div"):
                    print("\n"+pq(subject).text())
                    subject_name = pq(subject).text()
                    for files in pq(subject).parent("td").siblings():
                        if pq(files).text() is not "":
                            file_url = pq(files)("a").attr("href").replace("../..", site)
                            # print(file_url)
                            print(pq(files).text()+":"+file_url,end=",")
                            filename = path+os.sep+pq(files).text()+"_"+subject_name+".pdf"
                            if not  os.path.exists(filename):
                                '''
                                urlretrieve(file_url,filename)
                                # r = requests.get(file_url,proxies=proxies,stream=True)
                                r = requests.get(file_url,stream=True)
                                with open(filename,"wb") as f:
                                     for chunk in r.iter_content(chunk_size=1024):
                                         f.write(chunk)
                                print("download "+filename)
                                # time.sleep(0.5)
                                '''
            print(end="\n\n")
    '''
    for sec in result:
        for l1 in pqcontent("#ctl00_holderContent_tblExamQand .level1"):
            print(l1.html())
        for l2 in pqcontent("#ctl00_holderContent_tblExamQand .level2"):
            print(l2.html())
    '''
def prochtml2(html,site):
    f = open("output.txt","w")
    for year_exam in pq(html)(".level1").eq(0):
        print("OO"+pq(year_exam)(".link_1 div").text())
        f.write("OO"+pq(year_exam)(".link_1 div").text()+"\n")
        for each_exam in pq(year_exam).parent("tr").nextAll("tr .level2"):
            print("--"+pq(each_exam).text())
            f.write("--"+pq(each_exam).text()+"\n")
            for each_subject in pq(each_exam).parent("tr").nextAll("tr .link_3"):
                subject = pq(each_subject)("div").text()
                print("++++"+subject)
                f.write("++++"+subject+"\n")
                nexttr = pq(each_subject).parent("div").parent("td").parent("tr").next("tr td")
                if nexttr.hasClass("level1"):
                    print("\n"+"XXXChange!!!"+nexttr("div").text()+"\n")
                    f.write("\n"+"XXXChange!!!"+nexttr("div").text()+"\n\n")

###main
site = "http://wwwc.moex.gov.tw"
url = "http://wwwc.moex.gov.tw/main/exam/wFrmExamQandASearch.aspx?menu_id=156"
headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
proxies = {
    "http":"proxy.cht.com.tw:8080" ,
    "https":"proxy.cht.com.tw:8080"
} 
postdata = open("postdata",'r',encoding="utf-8")
# print(postdata.read())
# postdatas = {postdata_content}
postdatas = {}
for line in postdata.readlines():
    parse = line.split(":")
    if len(parse) == 1:
        postdatas[parse[0]] = ""
    elif len(parse) == 2:
        postdatas[parse[0]] = parse[1].strip()
    # print(line.split(":"))
# print(postdatas)
postdata.close()
# request = requests.post(url, data=postdatas, headers=headers, proxies=proxies)
# request = requests.post(url, data=postdatas, headers=headers)
# print(request.text)
# pqcontent = pq(url,headers, method="post")
html = open("source.html").read()
# with open("result.html", 'w',encoding="utf-8") as f:
     # f.write(request.text)
prochtml2(html,site)
'''
for year_exam in pq(request.text)(".level1").eq(0):
    print("OO"+pq(year_exam)(".link_1 div").text())
    for each_exam in pq(year_exam).parent("tr").nextAll("tr .level2"):
        print("--"+pq(each_exam).text())
        for each_subject in pq(each_exam).parent("tr").nextAll("tr .link_3"):
            subject = pq(each_subject)("div").text()
            print("++++"+subject)
            nexttr = pq(each_subject).parent("div").parent("td").parent("tr").next("tr td")
            if nexttr.hasClass("level1"):
                print("!!!Change!!!"+nexttr("div").text())
                '''

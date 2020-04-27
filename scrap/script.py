# importing libs
from bs4 import BeautifulSoup
import requests
# url="https://blog.forumias.com/10-pm-current-affairs-quiz-april-20-2020/"
urlPre="https://blog.forumias.com/10-pm-current-affairs-quiz"
################################################################################################################




def func(url):

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    # print(soup.prettify()) # print the parsed data of html

    olClass="wpProQuiz_list"
    liClass="wpProQuiz_listItem"
    quizDivClass="wpProQuiz_quiz"

    pageFileName="build/html/page.html"

    for soupItem in soup.find_all("div", {"class": quizDivClass}):
        print("writing content to {} : {}".format(pageFileName, len(soupItem)))
        file1 = open(pageFileName, "a") #append mode 
        file1.write("<h2>{}</h2>---\n{}".format(url, soupItem)) 
        file1.close() 

def build():

    print("Making single bulid file")

    import os
    os.system("cat build/html/pre.html > build/html/index.html")
    os.system("cat build/html/page.html >> build/html/index.html")
    os.system("cat build/html/pos.html >> build/html/index.html")



#################################################################################################################
from datetime import date, timedelta
pastXDays=60
delta = timedelta(days=1)
start_date = date.today()
while pastXDays>0:
    year, month, day, hour, min = map(str, start_date.strftime("%Y %B %d %H %M").split())
    url="{}-{}-{}-{}".format(urlPre, month.lower(), day, year)
    func(url)
    start_date = start_date - delta
    pastXDays = pastXDays-1





#################################################################################################################




build()





# importing libs
from bs4 import BeautifulSoup
import requests
# url="https://blog.forumias.com/10-pm-current-affairs-quiz-april-20-2020/"


################################################################################################################

def buildForumQuiz():
    urlPre = "https://blog.forumias.com/10-pm-current-affairs-quiz"

    from datetime import date, timedelta
    pastXDays = 60
    delta = timedelta(days=1)
    start_date = date.today()
    while pastXDays > 0:
        year, month, day, hour, min = map(
            str, start_date.strftime("%Y %B %d %H %M").split())
        url = "{}-{}-{}-{}".format(urlPre, month.lower(), day, year)
        func(url, "build/html/Forumpage.html")
        start_date = start_date - delta
        pastXDays = pastXDays-1


#################################################################################################################

def getQuizLinks(pre_page):
    # get main page content
    html_content = requests.get(urlPre).text
    soup = BeautifulSoup(html_content, "lxml")

    # find all links and extract APril Links from them
    allLinks = soup.find_all("a", href=True)
    return allLinks


def buildInsightsQuiz():
    urlPreCurrent = "https://www.insightsonindia.com/insights-current-affairs-questions/"
    urlPreStatic = "https://www.insightsonindia.com/insightsias-static-quizzes/"

    allLinks = getQuizLinks(urlPreCurrent)
    # april current affairs quiz
    AprilURLS = [link['href']
                 for link in allLinks if "april-2020" in link['href']]

    for url in AprilURLS:
        # append to insightspage.html
        func(url, "build/html/insightspage.html")

#################################################################################################################


def func(url, pageFileName):

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    # print(soup.prettify()) # print the parsed data of html

    olClass = "wpProQuiz_list"
    liClass = "wpProQuiz_listItem"
    quizDivClass = "wpProQuiz_quiz"

    for soupItem in soup.find_all("div", {"class": quizDivClass}):
        print("writing content to {} : {}".format(pageFileName, len(soupItem)))
        file1 = open(pageFileName, "a")  # append mode
        file1.write("<h2>{}</h2>---\n{}".format(url, soupItem))
        file1.close()

#################################################################################################################


def build():
    buildInsightsQuiz()
    print("done for Insights Quiz. ")
    buildForumQuiz()
    print("done for Forum Quiz. \n ")
    print("Making single bulid file for Insights and ForumIAS")

    import os
    os.system("cat build/html/pre.html > build/html/index.html")
    os.system("cat build/html/*page.html >> build/html/index.html")
    os.system("cat build/html/pos.html >> build/html/index.html")

    # make it ready to deploy on netlify
    os.system("cp build/html/index.html deploy/index.html")


#################################################################################################################

if __name__ == "__main__":
    build()

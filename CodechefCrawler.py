import os

import requests
from bs4 import BeautifulSoup

HTTP_STATUS_CODE_NOT_FOUND = 404
codechef_home_url = "https://www.codechef.com"


class CodechefCrawler:
    username = ""
    profile_url = ""
    problems_count = 0
    reply = None

    def __init__(self, username):
        self.username = username
        self.profile_url = "https://www.codechef.com/users/" + username

    def check_username(self):
        self.reply = requests.get(self.profile_url)
        if self.reply.status_code == HTTP_STATUS_CODE_NOT_FOUND:
            return False
        else:
            return True


    def crawl(self):

        html_content = self.reply.content
        soup = BeautifulSoup(html_content, "html.parser")
        problems = soup.select("span > a")

        for problem in problems:

            problem_name = problem.string
            problem_link = codechef_home_url + problem["href"]
            result = requests.get(problem_link)
            submission_content = result.content
            submission_soup = BeautifulSoup(submission_content, "html.parser")
            tablebox_section = submission_soup.find("div", class_="tablebox-section")

            if tablebox_section != None:
                rows = tablebox_section.select("tr")

                for current_row in rows:
                    try:

                        if current_row.img != None and current_row.img["src"] == "/misc/tick-icon.gif":
                            solution_href = (current_row.find_all("a")[1])["href"]
                            solution_url = codechef_home_url + solution_href
                            print(solution_url)

                            solution_result = requests.get(solution_url, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
                            solution_content = solution_result.content
                            solution_soup = BeautifulSoup(solution_content, "html.parser")
                            solution = solution_soup.find(id="solutiondiv")
                            file_extension = solution.find("pre")["class"][0]
                            file_name = problem_name + "." + file_extension
                            solution_plain_text_url = codechef_home_url + (solution.select("pre > div > a")[0]["href"])
                            print(solution_plain_text_url)

                            solution_plain_text_request = requests.get(solution_plain_text_url, headers={
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
                            solution_plain_text_soup = BeautifulSoup(solution_plain_text_request.content, "html.parser")
                            self.write_solutions(solution_plain_text_soup.text, file_name)
                            print("downloaded....." + file_name)
                            self.problems_count = self.problems_count + 1
                            print(self.problems_count)
                            break
                    except:
                        print("Download failed....")


    def write_solutions(self, solution, file_name):

        directory = "Codechef"
        author_info = "// Author : dinesh6752\n\n"
        current_working_directory = os.getcwd()
        current_directory_base_name = os.path.basename(os.path.normpath(current_working_directory))
        print(current_directory_base_name)

        if current_directory_base_name != directory:
            if not os.path.exists(directory):
                os.makedirs(directory)
            os.chdir(directory)
        with open(file_name, "w") as file:
            file.writelines(author_info + solution)


    def download(self):
        is_valid = self.check_username()
        if is_valid == True:
            print("yep")
            self.crawl()
        else:
            print("Please Enter Valid Username")

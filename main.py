from CodechefCrawler import  CodechefCrawler

def main():
    print("select your Choice")
    print("1.Codechef")
    choice = "1"
    if(choice == "1"):
        print("Enter the Username")
        user_name = "dinesh6752"
        codechef = CodechefCrawler(user_name)
        codechef.download()


if __name__ == '__main__':
    main()

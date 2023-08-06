__version__ = '0.1.0'

def name():
    print("BaiYunWei")

def birthday():
    print("11.4")

def love_each_other():
    print("2018.10.1")

def i_say_u():
    print("People who love each other will meet again.")
    print("Like us.")

def if_not_we_final():
    print("I hope we are all happy.")

def main():
    password = input("Please input Love password:")
    if password == "WLoveB":
        while(1):
            hello = input("Please input your operation:")
            if hello == "name":
                name()
            elif hello == "birthday":
                birthday()
            elif hello == "love_each_other":
                love_each_other()
            elif hello == "i_say_u":
                i_say_u()
            elif hello == "if_not_we_final":
                if_not_we_final()
            else:
                print("I like you very much.Baby Bai!")
    else:
        print("ByeBye~")

if __name__ == '__main__':
    main()

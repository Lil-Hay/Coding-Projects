from os import system
from time import sleep

def main():
    while True:
        system("cls")
        User_choice = input("Do you want to use Python (1) or C (2) for board generation? (C is alot faster and less resource intensive): ")
        if User_choice == '1':
            import Main_Python
            Main_Python.main()
            break
        elif User_choice == '2':
            import Main_C
            Main_C.main()
            break
        else:
            print("Please enter a valid choice")
            sleep(2)

if __name__ == '__main__':
    main()
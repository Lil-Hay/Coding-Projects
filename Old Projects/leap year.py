import time

def check_for_leep_year(year):
    if year % 4 == 0:
        return True
    else:
        return False


print("please enter a year")

user_answer_valid = False
while user_answer_valid == False:
    try:
        user_year = int(input())
        user_answer_valid = True
    except:
        print("Please enter a valid number")

is_leap_year = check_for_leep_year(user_year)
if is_leap_year == False:
    print(user_year, "is not a leap year")
elif is_leap_year == True:
    print(user_year, "is a leap year")

time.sleep(2)
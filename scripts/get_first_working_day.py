import pandas as pd
import workdays
import datetime

def return_first_day_of_working(year, month) :
    
    if month == 3 :
        if year % 4 == 0 :
            start_date = datetime.datetime(year, month-1, 29)
        else :
            start_date = datetime.datetime(year, month-1, 28)
    elif month is 5 or 7 or 10 or 12 :
        start_date = datetime.datetime(year, month-1, 30)
    else :
        start_date = datetime.datetime(year, month-1, 31)
    return workdays.workday(start_date, days=1)

print(return_first_day_of_working(2017, 5))
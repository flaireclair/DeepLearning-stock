import workdays
import datetime

def return_last_day_of_working(year, month) :
    
    if month == 3 :
        if year % 4 == 0 :
            start_date = datetime.datetime(year, month-1, 29)
            end_date = datetime.datetime(year, month, 31)
        else :
            start_date = datetime.datetime(year, month-1, 28)
            end_date = datetime.datetime(year, month, 31)
    elif month is 5 or 7 or 10 or 12 :
        start_date = datetime.datetime(year, month-1, 30)
        end_date = datetime.datetime(year, month, 31)
    elif month == 2 :
        if year % 4 == 0 :
            start_date = datetime.datetime(year, month-1, 31)
            end_date = datetime.datetime(year, month, 29)
        else :
            start_date = datetime.datetime(year, month-1, 31)
            end_date = datetime.datetime(year, month, 28)
    else :
            start_date = datetime.datetime(year, month-1, 31)
            end_date = datetime.datetime(year, month, 30)

    day_num =  workdays.networkdays(start_date, end_date)
    return workdays.workday(start_date, days=day_num)

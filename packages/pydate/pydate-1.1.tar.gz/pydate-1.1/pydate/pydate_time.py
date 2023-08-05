#!/usr/bin/env python3

class Year:

    # Constructor
    def __init__(self, year):
        if (type(year) is not int):
            raise TypeError("The year argument isn't an int!")

        if (len(str(year)) > 4 or len(str(year)) < 4):
            raise ValueError("The year argument must have 4 digits!")

        self.year = year

    # Return the year attribute value. 
    def get_year(self):
        return self.year()

    # Change the year attribute value.
    def set_year(self, year):
        if (type(year) is not int):
            raise TypeError("The year argument isn't an int!")

        if (len(str(year)) > 4 or len(str(year)) < 4):
            raise ValueError("The year argument must have 4 digits!")

        self.year = year

    # Increment the year attribute value by 1.
    def inc_year(self):
        if (self.year == 9999):
            raise ArithmeticError("The year attribute is out of bounds!")
        else:
            self.year += 1

    # Decrement the year attribute value by 1.
    def dec_year(self):
        if (self.year == 0):
            raise ArithmeticError("The year attribute is out of bounds!")
        else:
            self.year -= 1

    # Return a string representing the Year class attribute values.
    def tostring(self):
        return str(self.year)

class Date(Year):

    # Constructor
    def __init__(self, year, month, day):
        super().__init__(year)

        if (type(month) is not int):
            raise TypeError("The month argument isn't an int!")

        if (type(day) is not int):
            raise TypeError("The day argument isn't an int!")

        if (month < 1 or month > 12):
            raise ValueError("The month argument must be between 1 and 12!")

        if (day < 1 or day > 31):
             raise ValueError("The day argument must be between 1 and 31!")

        self.month = month
        self.day = day

    # Return the month attribute value. 
    def get_month(self):
        return self.month

    # Return the day attribute value. 
    def get_day(self):
        return self.day

    # Return the Gregorian month name.
    def get_gregorian(self):
        if (self.month == 1):
            return "January"
        elif (self.month == 2):
            return "February"
        elif (self.month == 3):
            return "March"
        elif (self.month == 4):
            return "April"
        elif (self.month == 5):
            return "May"
        elif (self.month == 6):
            return "June"
        elif (self.month == 7):
            return "July"
        elif (self.month == 8):
            return "August"
        elif (self.month == 9):
            return "September"
        elif (self.month == 10):
            return "October"
        elif (self.month == 11):
            return "November"
        elif (self.month == 12):
            return "December"

    # Change the month attribute value. 
    def set_month(self, month):
        if (type(month) is not int):
            raise TypeError("The month argument isn't an int!")

        if (month < 1 or month > 12):
            raise ValueError("The month argument must be between 1 and 12!")

        self.month = month

    # Change the day attribute value.
    def set_day(self, day):
        if (type(day) is not int):
            raise TypeError("The day argument isn't an int!")
        
        if (day < 1 or day > 31):
            raise ValueError("The day argument must be between 1 and 31!")

        self.day = day

    # Increment the month attribute value by 1.
    def inc_month(self):
        if (self.month == 12):
            raise ArithmeticError("The month attribute is out of bounds!")
        else:
            self.month += 1

    # Increment the day attribute value by 1.
    def inc_day(self):
        if (self.day == 31):
            raise ArithmeticError("The day attribute is out of bounds!")
        else:
            self.day += 1

    # Decrement the month attribute value by 1.
    def dec_month(self):
        if (self.month == 1):
            raise ArithmeticError("The month attribute is out of bounds!")
        else:
            self.month -= 1

    # Decrement the day attribute value by 1.
    def dec_day(self):
        if (self.day == 1):
            raise ArithmeticError("The day attribute is out of bounds!")
        else:
            self.day -= 1

    # Return a string representing the Date class attribute values. 
    def tostring(self):
        return str("{0}-{1}-{2}").format(self.year, self.month, self.day)

class Time:

    # Constructor
    def __init__(self, hour, minute, second):
        if (type(hour) is not int):
            raise TypeError("The hour argument isn't an int!")

        if (type(minute) is not int):
            raise TypeError("The minute argument isn't an int!")

        if (type(second) is not int):
            raise TypeError("The second argument isn't an int!")

        if (hour < 0 or hour > 23):
            raise ValueError("The hour argument must be between 0 and 23!")

        if (minute < 0 or minute > 59):
            raise ValueError("The minute argument must be between 0 and 59!")

        if (second < 0 or second > 59):
            raise ValueError("The second argument must be between 0 and 59!")

        self.hour = hour
        self.minute = minute
        self.second = second

    # Return the hour attribute value.
    def get_hour(self):
        return self.hour

    # Return the minute attribute value.
    def get_minute(self):
        return self.minute

    # Return the second attribute value.
    def get_second(self):
        return self.second

    # Change the hour attribute value. 
    def set_hour(self, hour):
        if (type(hour) is not int):
            raise TypeError("The hour argument isn't an int!")

        if (hour < 0 or hour > 23):
            raise ValueError("The hour argument must be between 0 and 23!")

        self.hour = hour

    # Change the minute attribute value.
    def set_minute(self, minute):
        if (type(minute) is not int):
            raise TypeError("The minute argument isn't an int!")

        if (minute < 0 or minute > 59):
            raise ValueError("The minute argument must be between 0 and 59!")

        self.minute = minute

    # Change the second attribute value.
    def set_second(self, second):
        if (type(second) is not int):
            raise TypeError("The second argument isn't an int!")

        if (second < 0 or second > 59):
            raise ValueError("The second argument must be between 0 and 59!")

        self.second = second

    # Increment the hour attribute by 1.
    def inc_hour(self):
        if (self.hour == 23):
            raise ArithmeticError("The hour attribute is out of bounds!")
        else:
            self.hour += 1

    # Increment the minute attribute by 1.
    def inc_minute(self):
        if (self.minute == 59):
            raise ArithmeticError("The minute attribute is out of bounds!")
        else:
            self.minute += 1

    # Increment the second attribute by 1.
    def inc_second(self):
        if (self.second == 59):
            raise ArithmeticError("The second attribute is out of bounds!")
        else:
            self.second += 1

    # Decrement the hour attribute by 1.
    def dec_hour(self):
        if (self.hour == 0):
            raise ArithmeticError("The hour attribute is out of bounds!")
        else:
            self.hour -= 1

    # Decrement the minute attribute by 1.
    def dec_minute(self):
        if (self.minute == 0):
            raise ArithmeticError("The minute attribute is out of bounds!")
        else:
            self.minute -= 1

    # Decrement the second attribute by 1.
    def dec_second(self):
        if (self.second == 0):
            raise ArithmeticError("The second attribute is out of bounds!")
        else:
            self.second -= 1

    # Return a string representing the Time class attribute values. 
    def tostring(self):
        return str("{0}:{1}:{2}").format(self.hour, self.minute, self.second)

class DateTime(Date, Time):

    # Constructor
    def __init__(self, year, month, day, hour, minute, second):
        Date.__init__(self, year, month, day)
        Time.__init__(self, hour, minute, second)

    # Return a string representing the DateTime class attribute values.
    def tostring(self):
        return str("{0}-{1}-{2} {3}:{4}:{5}").format(self.year, self.month, self.day, self.hour, self.minute, self.second)
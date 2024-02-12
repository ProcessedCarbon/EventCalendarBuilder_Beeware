import string
import re
from eventcalendarbuilder.PythonFiles.Managers.DateTimeManager import DateTimeManager
import eventcalendarbuilder.PythonFiles.EdittedPackages.wordninja as wordninja
import logging

class TextProcessingManager:
    _accepted_chars = ["-", " to "]
    _special_chars = string.punctuation

    # Splits string based on a list of delimiters
    def MultipleDelimSplitString(string, delims):
        """
        Splits a string by a list of delimiters. Does not function well with brackets as delimiters

        :param string (str): string to be split
        :param delimiters (list): list of delimiters

        return: list of split strings
        """
        new_string = TextProcessingManager.RemoveEnDashU2013(string)
        pattern = r'|'.join(delims)
        return re.split(pattern, new_string)
    
    # Creates a date dictionary 
    def GetDateStruct(day, month, year):
        """
        Returns a structure with day, month and year. 

        :param day (str): day 
        :param month (str): month 
        :param year (str): year 

        return: structured date
        """
        return  {
                "day" : re.sub(r'[^0-9]', '', day),
                "month" : DateTimeManager.isMonth(month) and month or None,
                "year" : DateTimeManager.isYear(year) and year or None
            }
    
    # Checks each special char in string and removes ones that are not in special_char_to_keep
    def RemoveUncessarySpecialChars(string, special_char_to_keep):
        """
        Returns the new string where all uneeded characters are removed or the original string 
        if no characters are removed. 

        :param string (str): text to remove uneeded characters 
        :param special_char_to_keep (list): list of chars to keep

        return: structured date
        """
        for c in string:
                if c in TextProcessingManager._special_chars:
                    if c not in special_char_to_keep:
                        string = string.replace(c, '')

        return string

    # Split word into a list and removes the empty elements
    def SplitWordAndRemoveEmptySlots(text):
        splitted = wordninja.split(text)
        return [x for x in splitted if x != '']

    # Removes the special char of dash not from UTF8
    def RemoveEnDashU2013(text:str):
        return text.replace(u'\u2013', "-")

    # Converts any time given to a 12H format
    def ConvertToTimedFormat(time_text: str):
        """
        Converts time_text to a acceptable time format for datetime parsing. Does not handle seconds,
        they are treated as 00 and are placed in there for the purpose of fulfilling format criteria. 

        :param time_text (str): string of text to convert to

        return: accpetable format for datetime parsing
        """        
        string_obj = str(time_text)

        # Remove all spaces and special char from string object
        for c in string_obj:
            if c == " " or c.isalnum() == False:
                string_obj = string_obj.replace(c, "")
        
        # Check return None if time includes seconds, if not check if first digit of hour is single
        if len(string_obj) > 6:
            #print(f"[{__name__}] INVALID PARAM GIVEN!")
            logging.error(f"[{__name__}] INVALID PARAM GIVEN!")
            return None
        
        # Pad string with zeros till length is even, do not take into account last 2 char when counting len
        while len(string_obj[:len(string_obj) - 2]) % 2 != 0:
            string_obj = "0" + string_obj

        # check if string has seconds included
        # Disregard seconds because timing of an event rarely comes in w/ seconds

        H = string_obj[:2]
        M = (DateTimeManager.isAPeriod(string_obj[2:4]) or string_obj[2:4] == "")and "00" or string_obj[2:4]
        P = DateTimeManager.isAPeriod(string_obj[-2:]) and string_obj[-2:].upper() or ""

        return H + ":" + M + ":00" + " " + P 

    # Formats date to comply with google calendar API (2023-05-17)
    def ProcessDate(date_text: str)->str:
        """
        Returns a list of strings formatted in the way that can be used for Google Calendars. 

        :param date_text (str): string of text that has the dates 

        return: list of formatted dates suitable for google calendars
        """

        if date_text == "None" or "" or len(date_text) <= 0:
            #print(f"[{__name__}] INVALID PARAM GIVEN!")
            logging.error(f"[{__name__}] INVALID PARAM GIVEN!")
            return []

        date_to_use = TextProcessingManager.RemoveUncessarySpecialChars(string=date_text, special_char_to_keep=TextProcessingManager._accepted_chars)
        splitted_date = TextProcessingManager.MultipleDelimSplitString(string=date_to_use, delims=TextProcessingManager._accepted_chars)

        # Find year
        # At this point max each array slot should have max DD MM YYYY
        list_of_processed = []
        for date in splitted_date:
            remove_empty = TextProcessingManager.SplitWordAndRemoveEmptySlots(text=date)

            # Remove anything that is not a month or number
            for var in remove_empty:
                if var.isdigit() == False and not DateTimeManager.isMonth(var):
                    remove_empty.remove(var)

            # Len == 1 > Only has day
            # Len == 2 > Has both day and month
            # Len == 3 > Has all day, month and year
            date_struct = TextProcessingManager.GetDateStruct(day=remove_empty[0], 
                                             month=len(remove_empty) > 1 and remove_empty[1] or 0,
                                             year=len(remove_empty) > 2 and remove_empty[2] or 0
                                            )
            # Get reference month and year from a substring that has one
            founded_month = date_struct['month'] != None and date_struct['month'] or None
            founded_year = date_struct['year'] != None and date_struct['year'] or None

            list_of_processed.append(date_struct)
        # Assign year and month to be used for substrings that do not posses one
        currentDate = DateTimeManager.getCurrentDate()
        year = founded_year != None and founded_year or currentDate.year
        month = founded_month != None and founded_month or currentDate.month

        res = []
        for struct in list_of_processed:
            struct['month'] = struct['month'] == None and month or struct['month']
            struct['year'] = struct['year'] == None and year or struct['year']

            s_date = str(struct['day']) + str(struct['month']) + str(struct['year'])
            res.append(DateTimeManager.FormatToDateTime(date_string=s_date, format='%Y-%m-%d'))

        return len(res) == 1 and res[0] or res
    
    # Format date to comply with google calendar (16:30:00)
    def ProcessTime(time_text: str)->str:
        """
        Returns a list of time strings formatted in the way that can be used for Google Calendars. 

        :param time_text (str): string of text that has the dates 

        return: list of formatted times suitable for google calendars
        """
        if time_text == "None" or time_text=="" or len(time_text) <= 0:
            #print(f"[{__name__}] INVALID PARAM GIVEN!")
            logging.error(f"[{__name__}] INVALID PARAM GIVEN!")
            return []

        # Form new list of accepted chars which include delims and time periods
        new_accepted_chars = TextProcessingManager._accepted_chars + DateTimeManager._period

        # Remove uncessary special chars and delim string
        time_to_use = TextProcessingManager.RemoveUncessarySpecialChars(string=time_text, special_char_to_keep=new_accepted_chars)
        splitted_time = TextProcessingManager.MultipleDelimSplitString(string=time_to_use, delims=TextProcessingManager._accepted_chars)

        list_of_correct_time_format = []
        for time in splitted_time:
            # Remove empty elements in list
            time_list = TextProcessingManager.SplitWordAndRemoveEmptySlots(text=time)
            
            # Remove uncessary chars from list
            for text in time_list:
                if text.isdigit() == False and not DateTimeManager.isAPeriod(text):
                    time_list.remove(text)
            
            # Combine remaining char in list to form the time string
            time_string = str(time_list)
            time_format = TextProcessingManager.ConvertToTimedFormat(time_string)
            if time_format != None:
                list_of_correct_time_format.append(time_format)
            
        # Check if there are any time format without a period
        period = ""
        for format in list_of_correct_time_format:
            if DateTimeManager.isAPeriod(format[-2:]):
                period = format[-2:].upper()
                break
        
        # If period is found, assume rest of timing uses that period else do own calculation to get period and 12hr format
        if period != "":
            for i in range(len(list_of_correct_time_format)):
                format = list_of_correct_time_format[i]
                if DateTimeManager.isAPeriod(format[-2:]) == False:
                    list_of_correct_time_format[i] += str(period)
        else:
            for i in range(len(list_of_correct_time_format)):
                format = list_of_correct_time_format[i]
                split = format.split(":")
                H = split[0]
                period = (int(H) >= 12) and "PM" or "AM"
                H = (int(H) >= 12) and str(int(H) - 12) or str(H)
                split[0] = H
                new_format = ':'.join(split)
                new_format += period
                list_of_correct_time_format[i] = new_format

        # Convert all 12H to 24H format and return the result
        result = []
        for time_format in list_of_correct_time_format:
            time_obj = DateTimeManager.convertTime12HTo24H(time_format)
            if time_obj != None:
                result.append(time_obj)

        # If result only contains a single value just return that value
        return result

    def ProcessDateToICSFormat(date:str)->dict:
        if date != None:
            params = date.split("-")
            return {
                "year" : int(params[0]),
                "month" : int(params[1]),
                "day" : int(params[2])
            }
        return None

    def ProcessTimeToICSFormat(time:list[str])->dict:
        res = []
        for t in time:
            if t != None:
                params = t.split(":")
                res.append({
                    "hour" : int(params[0]),
                    "min" : int(params[1]),
                    "second" : int(params[2]),
                })
        return res if len(res) > 0 else None

    def ProcessICS(s_date:dict, e_date:dict, time:list[dict]):
        s_day = int(s_date["day"])
        s_month = int(s_date["month"])
        s_year = int(s_date["year"])

        e_day = int(e_date["day"])
        e_month = int(e_date["month"])
        e_year = int(e_date["year"])

        s_time = time[0]
        s_h = int(s_time["hour"])
        s_m = int(s_time["min"])
        s_s = int(s_time["second"])

        e_time = time[1]
        e_h = int(e_time["hour"])
        e_m = int(e_time["min"])
        e_s = int(e_time["second"])
        
        s_ics_datetime = DateTimeManager.getDateTime(hour=s_h,min=s_m,sec=s_s,
                                                     day=s_day,month=s_month,year=s_year)
        e_ics_datetime = DateTimeManager.getDateTime(hour=e_h,min=e_m,sec=e_s,
                                                     day=e_day,month=e_month,year=e_year)
        return s_ics_datetime, e_ics_datetime
    
    # Tries and match a string to the regex, returns None if no match is found
    def CheckStringFormat(text, regex='[0-9]{2}:[0-9]{2}:[0-9]{2}'):
        return re.match(regex, text)

    
    
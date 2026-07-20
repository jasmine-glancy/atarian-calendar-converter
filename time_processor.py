"""Processes the time functions and date formatting"""

from datetime import datetime
import pandas as pd

class AtarianConverter:
    
    def __init__(self, gregorian_date_string):
        """Cleans input dates"""
        
        self.date_format = "%Y-%m-%d"

        # Convert string to datetime object
        self.datetime_object = datetime.strptime(gregorian_date_string, self.date_format)
        
    def extract_world_calendar(self):
        """Using pandas, extract the Date and End Dates"""
        
        # Read the world events
        dataframe = pd.read_csv('world_calendar.csv', usecols=['Label', 'Date', 'End Date', 'Duration'])
    
        return dataframe
    
    def _normalize_date_value(self, value):
        """Normalize a single date value into a consistent dictionary."""
        if value is None or (isinstance(value, float) and pd.isna(value)) or (
            isinstance(value, str) and str(value).strip() == ""
        ):
            return {
                "Era": None,
                "Year": None,
                "Month": None,
                "Day": None,
                "Greenseat Year": None,
            }

        value = str(value).strip()
        era = "BC" if "BC" in value else "AD"
        cleaned_value = value.replace("BC", "").strip()

        if not cleaned_value:
            return {
                "Era": era,
                "Year": None,
                "Month": None,
                "Day": None,
                "Greenseat Year": None,
            }

        cleaned_value = cleaned_value.split()[0]
        date_parts = cleaned_value.split("-")

        year = None
        month = 1
        day = 1

        if len(date_parts) > 0 and date_parts[0]:
            year = int(date_parts[0])

        if len(date_parts) > 1 and date_parts[1]:
            month = int(date_parts[1])

        if len(date_parts) > 2 and date_parts[2]:
            day = int(date_parts[2])

        return {
            "Era": era,
            "Year": year,
            "Month": month,
            "Day": day,
            "Greenseat Year": -year if era == "BC" and year is not None else year,
        }

    def clean_world_dates(self, data):
        """Normalize date values from a string, pandas Series, or DataFrame column."""
        
        # If the data is a Pandas data, continue to process it
        if isinstance(data, pd.DataFrame):
            
            # Make a copy of the dataframe
            normalized = data.copy()
            
            # Processes both start and end dates
            for column in ("Date", "End Date"):
                if column in normalized.columns:
                    normalized_series = normalized[column].apply(self._normalize_date_value)
                    normalized = pd.concat(
                        [
                            normalized.reset_index(drop=True),
                            pd.json_normalize(normalized_series).add_prefix(
                                f"{column.lower().replace(' ', '_')}_"
                            ),
                        ],
                        axis=1,
                    )
            return normalized

        if isinstance(data, pd.Series):
            return data.apply(self._normalize_date_value)

        return self._normalize_date_value(data) 

    def determine_day(self):
        """Extracts the day chosen by the user"""
          
        self.day = self.datetime_object.day
        
        return self.day
                
    def determine_month(self):
        """Based on the entered month, returns the Atarian season"""
        
        # Pull date from the formatted date from the user
        self.month = self.datetime_object.month
        
        # # TODO: use the below for "2nd month of the..." outputs
        # # Establish the month category
        # if int(self.month) in (3, 6, 9, 12):
        #     return self.number_suffix(1)
        
        # elif int(self.month) in (4, 7, 10, 1):
        #     return self.number_suffix(2)

        # elif int(self.month) in (5, 8, 11, 2):
        #     return self.number_suffix(3)
        
        # The below outputs the month number without "st", "nd", or "rd"
        # Establish the month category
        if int(self.month) in (3, 6, 9, 12):
            return 1
        
        elif int(self.month) in (4, 7, 10, 1):
            return 2

        elif int(self.month) in (5, 8, 11, 2):
            return 3

    def number_suffix(self, number):
        """Code recommended by Google Copilot"""
        
        n_str = str(number) # Convert to string
        num = int(number)
        if 11 <= num % 100 <= 13:
            return n_str + "th"
    
        suffixes = {1: "st", 2: "nd", 3: "rd"}
        return n_str + suffixes.get(num % 10, "th")
            
    def determine_season(self):
        """Based on the entered month, returns the Atarian season"""
        
        # The Greenseat year begins during the Blooming Season (starting in March)
        if int(self.month) in (3, 4, 5):
            return "Blooming Season"
        
        # The Burning Season (runs fron June to August)
        elif int(self.month) in (6, 7, 8):
            return "Burning Season"
        
        # The Falling Season (runs from Sept to Nov)
        elif int(self.month) in (9, 10, 11):
            return "Falling Season"
    
        # The Greenseat year ends during the Freezing Season (from Dec to February)
        elif int(self.month) in (12, 1, 2):
            return "Freezing Season"
        
    def determine_year(self):
        """Pulls the entered year"""
        
        # Finds the year the user chose
        self.year = self.datetime_object.year
        
        return self.year
    
    def find_guardian_era(self, entered_date, dataframe):
        """Based on the user's entered year, finds the guardian of Ataria for that year"""
        
        try:
            # 1. Find the user's entered year
            user_greenseat_year = entered_date["Greenseat Year"]
            
            # 2. Filter rows where the user's year falls between the start and end columns
            mask = (
                (dataframe["Label"].str.contains("Guardian", case=False, na=False)) &
                (dataframe["Start Year"] <= user_greenseat_year) &
                (dataframe["End Year"] >= user_greenseat_year)
            )

            matched_rows = dataframe.loc[mask]

            # 3. Process matches
            if not matched_rows.empty:
                # If matched_rows isn't empty, find and clean the first value
                try:
                    guardian_label = matched_rows["Label"].iloc[0]
                    
                    # Picks "High Chieftain Riel" out of "High Chieftain Riel's Guardianship"
                    full_guardian_name = guardian_label.split("'")
                    
                    deconstructed_guardian_name = full_guardian_name[0].split(" ")
                    
                    # # Debugging
                    # print(f"Guardian: {deconstructed_guardian_name[2]}")
                    
                    guardian_era = f"Guardianship of {deconstructed_guardian_name[2].title()}"
                    
                    # # Debugging 
                    # print(f"This is the {guardian_era}!")
                    return guardian_era
                except Exception as e:
                    print(f"Can't extract Guardian name. Exception: {e}")
                
            
        except Exception as e:
            print(f"Can't find Guardian era. Exception: {e}")

    def find_guardian_year(self, entered_date, dataframe):
        """Return the ordinal year within the matched guardian's guardianship."""
        
        print(f"Entered date: {entered_date}")
        try:
            
            if dataframe is None:
                print("The Dataframe is empty!")
                return None
            
            
            # 1. Find the user's entered year
            user_greenseat_year = entered_date["Greenseat Year"]
            
            # 2. Filter rows where the user's year falls between the start and end columns
            mask = (
                dataframe["Label"].str.contains("Guardian", case=False, na=False)
                & (dataframe["Start Year"] <= user_greenseat_year)
                & (dataframe["End Year"] >= user_greenseat_year)
            )

            matched_rows = dataframe.loc[mask]
            
            # If the guardian year is before 105-10-15, then output "pre-guardianship"
            if entered_date["Greenseat Year"] <= 105 and entered_date["Month"] <= 10 and entered_date["Day"] <= 14:
                return "Before the Guardians"
            
        
            # If the matched rows aren't empty and we are able to pull
            start_year = matched_rows["Start Year"].iloc[0]
            if matched_rows.empty or pd.isna(start_year):
                return None
            
            
            # 3. Process matches
            if not matched_rows.empty:
                
                # # Debugging
                # print(matched_rows[["Label", "Start Year", "End Year"]])
                
                # Get the current Guardian year based on the date the user entered
                ## For example, If given the year 05-21-114, it should read Month 3 of the 9th Blooming Season 
                
                try:
                    # # Debugging 
                    # print(f"Start Year: {start_year}")
                    start_year = int(start_year)
                    
                    # Find the difference between the user's Greenseat year and the start 
                        # year of the person who guards Ataria
                    difference = user_greenseat_year - start_year
                    
                    # The program should never return the 0th year
                    guardian_year = difference + 1
                    
                    # print(f"This is during the {guardian_year} guardian year")
                    
                    return guardian_year
                    
                except Exception as e:
                    print(f"Found matches, but can't find Guardian year. Exception: {e}")
                    return None  
                           
        except Exception as e:
            print(f"Can't find Guardian year. Exception: {e}")
            return None      
                  
    def format_chapter_head_date(self, month, season, guardian, guardian_year, parsed_user_date):
        """Formats the final string"""
        try:
            # Output example: Day 24, Burning Season Month 3 of the 131st Greenseat season cycle (8/24)
            
            if guardian_year == "Before the Guardians":
                return f"{guardian_year}, Month {month} of the {self.number_suffix(parsed_user_date["Greenseat Year"])} {season} ({self.month}/{self.day})"
            else:    
                return f"{guardian}, Month {month} of the {self.number_suffix(number=guardian_year)} {season} ({self.month}/{self.day})"

        except Exception as e:
            print(f"Please choose a different date. Exception: {e}")
             
    def format_date(self, day, month, season, year):
        """Formats the final string"""
        try:
            # Output example: Day 24, Burning Season Month 3 of the 131st Greenseat season cycle (8/24)
            return f"Day {day}, {season} Month {month} of the {self.number_suffix(number=year)} Greenseat season cycle ({self.month}/{self.day})"

        except Exception as e:
            print(f"Can't format the date. Please choose a different date. Exception: {e}")
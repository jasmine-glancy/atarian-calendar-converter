"""Processes the time functions and date formatting"""

from datetime import datetime

class AtarianConverter:
    
    def __init__(self, gregorian_date_string):
        """Cleans input dates"""
        
        date_format = "%m/%d/%Y"

        # Convert string to datetime object
        self.datetime_object = datetime.strptime(gregorian_date_string, date_format)
        
    def extract_date_parts(self):
        
        self.year = self.datetime_object.year
        self.month = self.datetime_object.month
        self.day = self.datetime_object.day
    
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
            return "Falling Season"
        
    def determine_month(self):
        """Based on the entered month, returns the Atarian season"""
        
        # Establish the month category
        if int(self.month) in (3, 6, 9, 12):
            return self.number_suffix(1)
        
        elif int(self.month) in (4, 7, 10, 1):
            return self.number_suffix(2)

        elif int(self.month) in (5, 8, 11, 2):
            return self.number_suffix(3)

    # TODO: Determine Guardianship era
    
    def number_suffix(self, n_str):
        """Code recommended by Google Copilot"""
        
        n_str = str(n_str) # Convert to string
        num = int(n_str)
        if 11 <= num % 100 <= 13:
            return n_str + "th"
    
        suffixes = {1: "st", 2: "nd", 3: "rd"}
        return n_str + suffixes.get(num % 10, "th")
            
        
    def format_date(self, season):
        """Formats the final string"""
        try:
            print(f"{self.number_suffix(self.day)} Day of the {season} ({self.month}/{self.day})")

        except Exception as e:
            print(f"Please choose a different date. Exception: {e}")
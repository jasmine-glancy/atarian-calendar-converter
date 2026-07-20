"""Outputs a character's sun sign based on the input dates"""

from datetime import datetime
import pandas as pd

class BirthdayFacts:
    
    def __init__(self, gregorian_date_string):
        """Cleans input dates in preparation for returning a character's sun sign"""
        
        self.shortened_string = gregorian_date_string[5:]
        self.date_format = "%m-%d"

        # Convert string to datetime object
        self.datetime_object = datetime.strptime(self.shortened_string, self.date_format)
        
    def open_json_file(self):
        """Opens the JSON file and deserialize its content"""
        
        try:
            dataframe = pd.read_json("sun_signs.json")
        except Exception as e:
            print(f"Error: Exception {e}")
    
        return dataframe
    
    def star_sign(self, zodiac_data):
        """Your sun or star sign is the zodiac constellation 
        the sun was in when you were born."""
        
        try: 
            # Define the target user date variables
            user_month = int(self.datetime_object.month)
            user_day = int(self.datetime_object.day)
            
            # Create the two evaluation masks
            is_start_month = (zodiac_data["start_month"] == user_month) & (user_day >= zodiac_data["start_day"])
            is_end_month = (zodiac_data["end_month"] == user_month) & (user_day <= zodiac_data["end_day"])

            # Filter the dataframe using the OR (|) operator
            matched_sign_df = zodiac_data[is_start_month | is_end_month]

            # Extract the first matching row as a dictionary
            if not matched_sign_df.empty:
                result = matched_sign_df.iloc[0].to_dict()
                print(f"Sign found: {result["sun_sign"]}")
            else:
                print("No sign matches this date.")
            
        # Process matches
        except Exception as e:
            print(f"Can't find star sign: {e}")
        
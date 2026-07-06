"""The Atarian Calendar Converter takes a date input by 
the user and returns the equivilant Atarian date"""

from time_processor import AtarianConverter

# 1. Start the application
print("Welcome to the Atarian Calendar Converter!")

# 2. Ask the user for a Gregorian date (March 2nd, 2026)
gregorian_date_string = input("Which date do you want to convert? (M/DD/YYYY): ")

convert = AtarianConverter(gregorian_date_string)
print(gregorian_date_string)
convert.extract_date_parts()

season = convert.determine_season()
convert.format_date(season=season)
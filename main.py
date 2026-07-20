"""The Atarian Calendar Converter takes a date input by 
the user and returns the equivilant Atarian date"""

from astrological_sign import BirthdayFacts
from time_processor import AtarianConverter
import pandas as pd

# 1. Start the application
print("Welcome to the Atarian Calendar Converter!")

# ------------------- #
# Gather date 
# ------------------- #

# 2. Ask the user for a Gregorian date (March 2nd, 2026)
gregorian_date_string = input("Which date do you want to convert? (YYYY-MM-DD): ")

# ------------------- #
# Transform date 
# ------------------- #

# 3. Based on the user's chosen date, return it for verification
convert = AtarianConverter(gregorian_date_string)
print(gregorian_date_string)

# 4. Extract Pandas dates
results = convert.extract_world_calendar()

# 5. Normalize the Pandas dates

# 5a. Normalize start dates
start_dates = convert.clean_world_dates(results["Date"])
dataframe_start = pd.json_normalize(start_dates).add_prefix("Start ")

# 5b. Normalize end dates
end_dates = convert.clean_world_dates(results["End Date"])
dataframe_end = pd.json_normalize(end_dates).add_prefix("End ")

# 6. Combine the cleaned dataframe
clean_dataframe = pd.concat([results.reset_index(drop=True), dataframe_start, dataframe_end], axis=1)

# print(clean_dataframe)

# 7: Normalize user dates
parsed_user_date = convert._normalize_date_value(gregorian_date_string)

print(f"Parsed user date is {parsed_user_date}")

# 8: Find the Guardian of Ataria for the entered date
guardian = convert.find_guardian_era(parsed_user_date, clean_dataframe)

# 9. Extract Day
day = convert.determine_day()

# 10. Determine month
month = convert.determine_month()

# 11. Determine the season: Falling, Freezing, Burning, Blooming
season = convert.determine_season()

# 12. Extract year
year = convert.determine_year()

# 13. Find Guardian year
guardian_year = convert.find_guardian_year(entered_date=parsed_user_date, dataframe=clean_dataframe)

# ------------------------ #
# Format date 
# ------------------------ #

# 14. Format the long date based on the Greenseat Calendar
long_date = convert.format_date(day=day, month=month, season=season, year=year)

print(f"Long Date: {long_date}")

# 15. Format chapter head
chapter_head = convert.format_chapter_head_date(month=month, season=season, guardian_year=guardian_year, guardian=guardian, parsed_user_date=parsed_user_date)

print(f"Chapter Head: {chapter_head}")

# ------------------------- #
# Character creation assist
# ------------------------- #

# 16. Based on the user's date, output a character's astrological sign if they were born on this date
zodiac = BirthdayFacts(gregorian_date_string)

# 17. Open the JSON file containing Zodiac data
zodiac_signs = zodiac.open_json_file()

# 18. Return the character's star sign
zodiac.star_sign(zodiac_data=zodiac_signs)


"""The Atarian Calendar Converter takes a date input by 
the user and returns the equivilant Atarian date"""

from time_processor import AtarianConverter

# 1. Start the application
print("Welcome to the Atarian Calendar Converter!")

# ------------------- #
# Gather date 
# ------------------- #

# 2. Ask the user for a Gregorian date (March 2nd, 2026)
gregorian_date_string = input("Which date do you want to convert? (M/DD/YYYY): ")

# ------------------- #
# Transform date 
# ------------------- #

# 3. Based on the user's chosen date, return it for verification
convert = AtarianConverter(gregorian_date_string)
print(gregorian_date_string)

# # Extract the Day, Month, and Year from the user's date
# convert.extract_date_parts()

# 4. Extract Day
day = convert.determine_day()

# 5. Determine month
month = convert.determine_month()

# 6. Determine the season: Falling, Freezing, Burning, Blooming
season = convert.determine_season()

# 7. Extract year
year = convert.determine_year()

# Finally, format the date based on the Greenseat Calendar
convert.format_date(day=day, month=month, season=season, year=year)
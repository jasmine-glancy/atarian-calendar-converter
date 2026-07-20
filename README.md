# Atarian Calendar Converter

A custom Author-assistant tool to help me convert our [Gregorian calendar](https://en.wikipedia.org/wiki/Gregorian_calendar) into an equivilant Atarian date.

I'm a busy woman and this will help my sanity, saving valuable gray matter for creative and planning functions.

## 📚 Table of Contents

- [Atarian Calendar Converter](#atarian-calendar-converter)
  - [📚 Table of Contents](#-table-of-contents)
  - [📌 Overview](#-overview)
  - [✨ Features](#-features)
  - [📖 Output Example](#-output-example)
  - [🗂️ Project Structure](#️-project-structure)
  - [⚙️ How It Works](#️-how-it-works)
    - [Workflow](#workflow)
  - [🔌 Modules](#-modules)
    - [AtarianConverter](#atarianconverter)
      - [Primary Responsibilities](#primary-responsibilities)
    - [BirthdayFacts](#birthdayfacts)
      - [Responsibilities](#responsibilities)
      - [Data Flow](#data-flow)
  - [🔗 Dependencies](#-dependencies)
  - [💻 Running the Program](#-running-the-program)
  - [🔣 Expected Input](#-expected-input)
  - [🎯 Core Functions](#-core-functions)
  - [💾 Technologies Used](#-technologies-used)
  - [💭 Future Enhancements](#-future-enhancements)
  - [📜 License](#-license)

## 📌 Overview

Convert any Gregorian date into its equivalent Atarian Calendar date and generate lore-rich information about that day, including:

- Atarian (Greenseat) calendar date
- Guardian Era and Year
- Season
- Chapter heading format
- Character astrological sign

The project is designed as both a worldbuilding tool and a character creation assistant for stories set in the world of Ataria.

## ✨ Features

- Convert Gregorian dates (YYYY-MM-DD) into the Atarian calendar
- Determine the current:
  - Day
  - Month
  - Season
  - Greenseat Year

- Identify which Guardian rules during the selected date
- Calculate the year within a Guardian's reign
- Generate formatted Atarian dates for novels and documents
- Generate chapter heading dates
- Determine a character's astrological sign

## 📖 Output Example

```text
Welcome to the Atarian Calendar Converter!

Which date do you want to convert? (YYYY-MM-DD):
0120-08-24

Parsed user date is: {'Era': 'AD', 'Year': 120, 'Month': 8, 'Day': 24, 'Greenseat Year': 120}

Long Date: Day 24, Burning Season Month 3 of the 120th Greenseat season cycle (8/24)

Chapter Head: Guardianship of Riel, Month 3 of the 16th Burning Season (8/24)

Sign found: Virgo
```

## 🗂️ Project Structure

```text
atarian-calendar-converter/
│
├── main.py
├── time_processor.py
├── astrological_sign.py
│
├── data/
│   ├── world_calendar.csv
│   └── sun_signs.json
│
├── README.md
└── requirements.txt
```

## ⚙️ How It Works

The application follows a straightforward pipeline.

```text
User Date
      │
      ▼
Gregorian Date Parser
      │
      ▼
Normalize World Calendar Data
      │
      ▼
Find Matching Atarian Date
      │
      ├────────► Guardian Era
      ├────────► Guardian Year
      ├────────► Season
      ├────────► Month
      ├────────► Day
      ▼
Format Output
      │
      ├────────► Long Date
      ├────────► Chapter Header
      └────────► Zodiac Sign
```

### Workflow

1. **User Input**

   The user enters a Gregorian date in the format YYYY-MM-DD.

   Example: `0126-03-02`

2. **Calendar Extraction**

   The converter loads the world calendar and extracts all Atarian calendar information.

   `results = convert.extract_world_calendar()`

3. **Data Normalization**

   Both the start and end dates of every calendar period are normalized into comparable values.

   This allows efficient date comparisons.

   `clean_world_dates()`

4. **User Date Normalization**

   The user's Gregorian date is internally cleaned of dates tagged "BC"

   `parsed_user_date`

   Example

   ```python
   {
       "Greenseat Year": 142,
       "Month": 5,
       "Day": 18
   }
   ```

5. **Guardian Lookup**

   Using the normalized calendar, the converter determines:
   - Who the Guardian of Ataria is when given a date
   - How many years the Guardian has ruled since they became the High Chieftain

   Functions used:
   - find_guardian_era()
   - find_guardian_year()

6. **Date Components**

   The converter extracts individual pieces of the Atarian date.
   - determine_day()
   - determine_month()
   - determine_year()
   - determine_season()

7. **Date Formatting**

   Two formatted outputs are generated; a long date for timeline purposes and a shorter one for chapter headings.

   `Long Date: Day 24, Burning Season Month 3 of the 120th Greenseat season cycle`

   Generated using `format_date()`

   _Chapter Heading_

   Example output: `Guardianship of Riel, Month 3 of the 16th Burning Season`

   Generated using `format_chapter_head_date()`

8. **Astrological Sign**

   The project loads zodiac data from JSON with `open_json_file()`

   The character's sign is determined using `star_sign()`

## 🔌 Modules

### AtarianConverter

Responsible for all calendar conversion logic.

#### Primary Responsibilities

- Parse Gregorian dates
- Load world calendar
- Normalize date data
- Determine seasons
- Determine months
- Determine years
- Find Guardian Era
- Find Guardian Year
- Format dates

### BirthdayFacts

Responsible for character astrology.

#### Responsibilities

- Load zodiac JSON
- Determine astrological sign
- Return character birth information

#### Data Flow

```text
Gregorian Date
        │
        ▼
datetime
        │
        ▼
AtarianConverter
        │
        ├────► World Calendar CSV
        │
        ├────► Normalize Dates
        │
        ├────► Determine Calendar Values
        │
        ▼
Formatted Atarian Date
        │
        ▼
BirthdayFacts
        │
        ▼
Zodiac Sign
```

## 🔗 Dependencies

- Python 3.11+
- pandas

## 💻 Running the Program

```bash
python main.py
```

You will be prompted to enter a date.

```bash
Which date do you want to convert? (YYYY-MM-DD):
```

## 🔣 Expected Input

Dates must follow ISO-8601 formatting.

Valid: `2026-03-02`

Invalid:

```text
3/2/2026
March 2 2026
02-03-2026
```

## 🎯 Core Functions

|           Function           |           Purpose           |
| :--------------------------: | :-------------------------: |
|  `extract_world_calendar()`  |  Load the calendar dataset  |
|    `clean_world_dates()`     |  Normalize calendar dates   |
|  `_normalize_date_value()`   |    Normalize user input     |
|    `find_guardian_era()`     |  Find the active Guardian   |
|    `find_guardian_year()`    | Calculate the Guardian year |
|      `determine_day()`       |   Return the Atarian day    |
|     `determine_month()`      |  Return the Atarian month   |
|     `determine_season()`     |  Return the Atarian season  |
|      `determine_year()`      |   Return the Atarian year   |
|       `format_date()`        |    Produce the long date    |
| `format_chapter_head_date()` |  Produce a chapter heading  |
|      `open_json_file()`      |      Load zodiac data       |
|        `star_sign()`         |  Determine the zodiac sign  |

## 💾 Technologies Used

- Python
- pandas
- JSON
- CSV
- datetime

## 💭 Future Enhancements

- Holiday and festival lookup
- Additional horoscope systems
- Output character's birthstone and birth flower
- Handling for leap years

## 📜 License

This project is intended as a worldbuilding and storytelling utility for the fictional setting of Ataria. Feel free to adapt and expand it for your own creative projects, while preserving appropriate attribution if you redistribute modified versions.

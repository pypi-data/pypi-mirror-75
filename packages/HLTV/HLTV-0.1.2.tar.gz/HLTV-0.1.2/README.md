This python library functions as an HLTV API to extract, parse, and format data from [HLTV.org](https://www.hltv.org/). This library allows for real time data extraction to use in your code. This library is still in its beta stages and is being rapidly updated/altered with new features still being added/adjusted.

## Installation 

    pip install HLTV

## Dependencies

```
pip install bs4

pip install lxml
```

## Usage

**Importing**

```python
from HLTV import *
```

**FUNCTIONS**

    get_live_matches()
        returns a list of all LIVE matches on HLTV along with the maps being played and the star ratings
    
    get_upcoming_matches()
        returns a list of all upcoming matches on HLTV
    	
    get_important_upcoming_matches(star_rating=1)
        returns a list of all upcoming matches on HLTV with the star rating argument (should be between 0 and 5)
    
    get_match_results()
        returns a list of results from the past 100 matches on HLTV
    
    get_important_match_results(star_rating=1)
        returns a list of results from the past 100 matches on HLTV with or above the star rating argument
    	
    get_top_teams()
        returns a list of the top 30 teams
    	
    get_best_players(time_filter=30)
        returns a list of the top players within a certain time frame (ex: 30 days ago until today)

## Uninstallation

    pip uninstall HLTV

from urllib import request, parse, error
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup


def get_live_matches():
    """returns a list of all LIVE matches on HLTV along with the maps being played and the star ratings"""
    matches_page = request.urlopen(request.Request("https://www.hltv.org/matches",
                                                   headers={'User-Agent': 'Chrome'})).read().decode("utf-8")
    live_matches = BeautifulSoup(matches_page, "lxml").find("div", {'class', "liveMatchesContainer"})
    if live_matches is None:
        return []
    else:
        teams = [line.getText() for line in live_matches.find_all("div", {'class', "matchTeamName text-ellipsis"})]
        matches = [(team1, team2) for team1, team2 in tuple(zip(teams, teams[1:]))[::2]]
        liveMatchContainer = live_matches.find_all("div", {'class', "liveMatch-container"})
        maps = [str(line.get('data-maps')).split(',') for line in liveMatchContainer]
        stars = [line.get('stars') for line in liveMatchContainer]
        return [{'teams': teams, 'maps': maps, 'stars': stars} for teams, maps, stars in zip(matches, maps, stars)]


def get_upcoming_matches():
    """returns a list of all upcoming matches on HLTV"""
    matches_page = request.urlopen(request.Request("https://www.hltv.org/matches",
                                                   headers={'User-Agent': 'Chrome'})).read().decode("utf-8")
    teams = [line.getText() for line in BeautifulSoup(matches_page, "lxml").find("div",
             {'class', "upcomingMatchesContainer"}).find_all(
             class_=lambda v: v is not None and (v == "team text-ellipsis" or v == "matchTeamName text-ellipsis"))]
    return [(team1, team2) for team1, team2 in tuple(zip(teams, teams[1:]))[::2]]


def get_important_upcoming_matches(star_rating=1):
    """returns a list of all upcoming matches on HLTV with the star rating argument (should be between 0 and 5)"""
    matches_page = request.urlopen(request.Request("https://www.hltv.org/matches?",
                                                   headers={'User-Agent': 'Chrome'})).read().decode("utf-8")
    teams = [line.getText() for line in BeautifulSoup(matches_page, "lxml").find("div",
             {'class', "upcomingMatchesContainer"}).find_all(
             class_=lambda v: v is not None and (v == "team text-ellipsis" or v == "matchTeamName text-ellipsis"))]
    stars = [int(line.get('stars')) for line in BeautifulSoup(matches_page, "lxml").find("div",
             {'class', "upcomingMatchesContainer"}).find_all("div", {"class", "upcomingMatch "})
             if line.get('team1') is not None]
    matches = [(team1, team2) for team1, team2 in tuple(zip(teams, teams[1:]))[::2]]
    assert len(matches) == len(stars), "Internal Exception :: get_important_upcoming_matches() :: misMatches detected"
    return [match for match, star in zip(matches, stars) if star == star_rating]


def get_match_results(offset=0):
    """returns a list of results from past 100 matches on HLTV starting from the offset param"""
    results_page = BeautifulSoup(request.urlopen(request.Request("https://www.hltv.org/results?offset=" + str(offset),
                                                 headers={'User-Agent': 'Chrome'})).read().decode("utf-8"), "lxml")
    team_won = [line.getText() for line in results_page.find_all("div", {'class', "team team-won"})]
    team_lost = [line.getText() for line in results_page.find_all("div", {'class', "team "})]
    winning_score = [line.getText() for line in results_page.find_all("span", {'class', "score-won"})]
    losing_score = [line.getText() for line in results_page.find_all("span", {'class', "score-lost"})]
    return [{'team_won': team_won, 'team_lost': team_lost, 'winning_score': winning_score, 'losing_score': losing_score}
            for team_won, team_lost, winning_score, losing_score, in
            zip(team_won, team_lost, winning_score, losing_score)][len(team_won) - 100:]


def get_important_match_results(star_rating=1, offset=0):
    """returns a list of 100 past matches on HLTV with or above the star rating argument starting from the offset"""
    arg = {'offset': offset, 'stars': star_rating}
    results_page = BeautifulSoup(request.urlopen(request.Request("https://www.hltv.org/results?" + parse.urlencode(arg),
                                                 headers={'User-Agent': 'Chrome'})).read().decode("utf-8"), "lxml")
    team_won = [line.getText() for line in results_page.find_all("div", {'class', "team team-won"})]
    team_lost = [line.getText() for line in results_page.find_all("div", {'class', "team "})]
    winning_score = [line.getText() for line in results_page.find_all("span", {'class', "score-won"})]
    losing_score = [line.getText() for line in results_page.find_all("span", {'class', "score-lost"})]
    return [{'team_won': team_won, 'team_lost': team_lost, 'winning_score': winning_score, 'losing_score': losing_score}
            for team_won, team_lost, winning_score, losing_score, in
            zip(team_won, team_lost, winning_score, losing_score)][len(team_won) - 100:]


def get_top_teams():
    """returns a list of the top 30 teams"""
    day = date.today()
    hltv_teams_page = None
    for i in range(30):
        try:
            day -= timedelta(days=1)
            hltv_teams_page = request.urlopen(request.Request("https://www.hltv.org/ranking/teams/" +
                                              day.strftime('%Y/%B/%d').lower(), headers={'User-Agent': 'Chrome'}))
            break
        except error.HTTPError as exception:
            if exception.code != 404:
                raise exception
    assert hltv_teams_page is not None, "Internal Exception :: get_top_teams() :: web page not found"
    data = BeautifulSoup(hltv_teams_page.read().decode("utf-8"), "lxml")
    return [info.get('title') for info in data.find_all("img", {'class': ""}) if info.get('title') is not None]


def get_best_players(time_filter=90):
    """returns a list of the top players within a certain time filter (ex: 90 days ago till now)"""
    params = {'startDate': (datetime.today() - timedelta(time_filter)).strftime('%Y/%B/%d'),
              'endDate':  datetime.today().strftime('%Y/%B/%d'), 'rankingFilter': 'Top20'}
    stats_page = request.urlopen(request.Request("https://www.hltv.org/stats/players?" + parse.urlencode(params),
                                                 headers={'User-Agent': 'Chrome'})).read().decode("utf-8")
    formatted_data = BeautifulSoup(stats_page, "lxml")
    players = [info.find('a').getText() for info in formatted_data.find_all("tr") if info.find('a') is not None]
    countries = [info.find_all('img')[0].get('title') for info in formatted_data.find_all("tr")[1:]
                 if info.find_all('img') is not None]
    teams = [info.find_all('img')[1].get('title') for info in formatted_data.find_all("tr")[1:]
             if info.find_all('img') is not None]
    kdr = [info.find_all('td')[4].getText() for info in formatted_data.find_all("tr")[1:]
           if info.find_all('td') is not None]
    rating = [info.find_all('td')[5].getText() for info in formatted_data.find_all("tr")[1:]
              if info.find_all('td') is not None]
    return [{'ranking': str(i + 1), 'player': player, 'team': team, 'country': country, 'KDR': kdr, 'rating': rating}
            for i, (player, team, country, kdr, rating) in enumerate(zip(players, teams, countries, kdr, rating))]


if __name__ == '__main__':
    print(get_live_matches())
    print(get_upcoming_matches())
    print(get_important_upcoming_matches())
    print(get_match_results())
    print(get_important_match_results())
    print(get_top_teams())
    print(get_best_players())

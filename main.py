import ScraperFC as sfc
import traceback

#reductions of leagues to FBRef
league_FBRef = {
    0 : 'Champions League', 1 : 'Europa League', 2 : 'Europa Conference League', 3 : 'EPL', 4 : 'Ligue 1',
    5 : 'Bundesliga', 6 : 'Serie A', 7 : 'La Liga'
}


def get_league_table(season, num_of_league):
    scraper = sfc.FBRef()
    table = None
    try:
        table = scraper.scrape_league_table(year=season, league=league_FBRef[num_of_league])
    except:
        traceback.print_exc()
    finally:
        scraper.close()
    return table


def print_league_table(table):
    cnt_teams = table.shape[0]
    tab = table.to_dict()
    sizes_for_table = {
        'Rk' : 2, 'Squad': 16, 'MP': 2, 'W' : 2, 'D' : 2, 'L' : 2, 'GF' : 3, 'GA' : 3, 'GD' : 3, 'Pts': 3,
        'Pts/MP' : 6, 'xG': 4, 'xGA' : 4, 'xGD' : 4, 'xGD/90': 5, 'Last 5' : 6, 'Attendance' : 10,
        'Top Team Scorer' : 42, 'Goalkeeper' : 15, 'Notes': 5
    }
    for value in tab.keys():
        cnt_tables = max(0, sizes_for_table[value]-len(value))+1
        print(value[:sizes_for_table[value]], end=' '*cnt_tables)
    print()
    for id in range(cnt_teams):
        for value in tab.keys():
            cnt_tables = max(0, sizes_for_table[value] - len(str(tab[value][id]))) + 1
            print(str(tab[value][id])[:sizes_for_table[value]], end = ' '*cnt_tables)
        print()
    return

table = get_league_table(2024, 3)
print_league_table(table)
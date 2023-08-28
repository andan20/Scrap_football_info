import ScraperFC as sfc
import traceback
import pandas as pd

scraper = sfc.FBRef()
'''
table = dict()
try:
    lg_table = scraper.scrape_league_table(year=2024, league='EPL')
    table = lg_table.to_dict()
except:
    traceback.print_exc()
finally:
    scraper.close()

name_size = 16
attendance_size = 9
num_size = 5
for column in table.keys():
    space_cnt = 1
    if column=='Squad' or column=='Goalkeeper' or column=='Goalkeeper':
        space_cnt = max(1, name_size-len(column))
    elif column=='Top Team Scorer':
        space_cnt = max(1, name_size*2-5-len(column))
    elif column == 'Squad':
        space_cnt = max(1, attendance_size - len(column))
    else:
        space_cnt = max(1, num_size - len(column))
    print(column, end = ' '*space_cnt)
print()

for i in range(20):
    for column in table.keys():
        space_cnt = 1
        if column == 'Squad' or column == 'Goalkeeper' or column == 'Goalkeeper':
            space_cnt = max(1, name_size - len(str(table[column][i])))
        elif column == 'Top Team Scorer':
            space_cnt = max(1, name_size * 2-5 - len(str(table[column][i])))
        elif column == 'Squad':
            space_cnt = max(1, attendance_size - len(str(table[column][i])))
        else:
            space_cnt = max(1, num_size - len(str(table[column][i])))
        print(table[column][i], end=' '*space_cnt)
    print()
'''
link = 'https://fbref.com/en/matches/44b9a07c/West-Ham-United-Chelsea-August-20-2023-Premier-League'

try:
    match = scraper.scrape_match(link=link)
except:
    # Catch and print any exceptions.
    traceback.print_exc()
finally:
    # Again, make sure to close the scraper when you're done
    scraper.close()

otv = match['Home Player Stats'].values[0]['Team Sheet'].values[0].iat[0,0]
print(otv, type(otv))

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


def main(year):
    '''
    year: the selected sports edition 

    Note 1: the structure of the Wikipedia changes over time. Therefore, the framework below may not apply. The exact structure of the page must be studied and the html tags where the data is located should be replaced
    Note 2: for a given sport's edition, the pages display the score data differently. Therefore, this framework might need to be modified several times for a given sport if subsequent editions' page structures are different  
    '''
    file_name = "basketball_" + str(year)

    # sample Wikipedia url where year is replaced for each iteration to select the next sports edition 
    url = (
        "https://en.wikipedia.org/wiki/Basketball_at_the_"
        + str(year)
        + "_Summer_Olympics_–_Men%27s_tournament"
    )
    # scrapping the score table for the sport 
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser") 
    # the data is stored in a tr (table row) with a style: vertical-align:top
    score_table = soup.find_all("tr", style=("vertical-align:top"))

    players_list = [[], []]
    scores_list = [[], []]
    # iterating over the score table to scrape player 1 and player 2 data 
    for i in range(len(score_table)):
        matches = []

        # scrapping player 1 data from td (table data)
        player1 = score_table[i].find_all("td")[0].get_text().strip()
        players_list[0].append(player1)

        # scrapping player 2 data from td (table data)
        player2 = score_table[i].find_all("td")[2].get_text().strip()
        players_list[1].append(player2)

        # scrapping score data from td (table data)
        scores = score_table[i].find_all("td")[1].get_text().strip()

        # using regular expression to clean the scores data which i in the format "1-2"
        pattern = "\d+"
        matches = re.findall(pattern, scores)

        scores_list[0].append(int(matches[0]))
        scores_list[1].append(int(matches[1]))

    # Creating the data frame with scores data for sport's current edition 
    data = {
        "Player 1": players_list[0],
        "Score 1": scores_list[0],
        "Player 2": players_list[1],
        "Score 2": scores_list[1],
        "Winner": "",
    }
    df = pd.DataFrame(data)

    # finding the winners for each match based on player1 and player2 scores 
    for row in range(len(df)):
        if df.iloc[row, 1] > df.iloc[row, 3]:
            df.iloc[row, 4] = df.iloc[row, 0]
        elif df.iloc[row, 1] < df.iloc[row, 3]:
            df.iloc[row, 4] = df.iloc[row, 2]
        elif df.iloc[row, 1] == df.iloc[row, 3]:
            df.iloc[row, 4] = "Draw"
        else:
            df.iloc[row, 4] = "Not enough data"

    # export to an excel file
    df.to_excel(file_name + ".xlsx", index=False)

for year in range(2008, 2021, 4):
    main(year)

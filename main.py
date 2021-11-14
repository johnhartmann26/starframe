# This is a python script to parse a UDisc CSV export and count starframes amongst the card
import csv


def set_players():
    player_number = 1
    players = []
    player = "null"
    while player != "":
        player = input(f'Player {player_number} (Leave blank if done)')
        player_number += 1
        if player != "":
            players.append(player)
    return players


def csv_splitter(players):
    rounds = []
    card = []
    with open('UDisc_Scorecards.csv', newline="") as csv_file:
        scorecard_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in scorecard_reader:
            if row[0] == 'Par':
                rounds.append(card)
                card = [row]
            elif player_filter(players, row, 0):
                card.append(row)
    return rounds


def player_filter(players, card, index):
    match_found = False
    for player in players:
        if player in card[index]:
            match_found = True
    return match_found


def starframe_counter(rounds, players):
    starframe_count = 0
    for card in rounds:
        if len(card) >= len(players) + 1:
            cards_birdies = []
            par = []
            for player in card:
                if player[0] == 'Par':
                    par = player
                else:
                    # logs player's name, then checks for birdies
                    birdies = [player[0]]
                    for score in range(6, len(par)):
                        if player[score] != "0" and player[score] < par[score]:
                            birdies.append(score - 5)
                    cards_birdies.append(birdies)
            last_hole_birdied = 0
            for player_card in cards_birdies:
                if type(player_card[-1]) is int:
                    if last_hole_birdied < player_card[-1]:
                        last_hole_birdied = player_card[-1]
            starframes = [
                f'Course: {card[0][1]}',
                f'Timestamp: {card[0][3]}',
            ]
            for hole in range(1, last_hole_birdied + 1):
                starframe = True
                for row in cards_birdies:
                    if hole not in row:
                        starframe = False
                if starframe:
                    starframes.append(hole)
            starframe_count += len(starframes) - 2
    return starframe_count


def main():
    players = set_players()
    rounds = csv_splitter(players)
    starframe_count = starframe_counter(rounds, players)
    print(f'{players} have participated in {starframe_count} total starframes.')


if __name__ == '__main__':
    main()

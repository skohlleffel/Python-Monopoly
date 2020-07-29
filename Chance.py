import random as rd


# if the player passes go, he gets 200 dollars
def go(players):
    players.money += 200
    return print('You passed GO! You get 200 dollars!')


def community(player, monopoly, total_players, park):
    print()
    input('Press Enter to draw a card!')
    options = ['Go To Jail', 'Community House Card', 'Get Out of Jail Free (+50 dollars)',
               'Stock pays you 45 dollars', 'Each Player pays you 50 dollars', 'Advance to Go',
               'School Tax (-150)', 'Doctor Fee (-50)', 'Xmas Fund Matures (+100)', 'Income Tax Refund (+20)',
               'Beauty Contest (+10)',
               'Life Insurance Matures (+100)', 'Receive for services 25 dollars', 'Bank error in your favor (+200)',
               'You inherit 100 dollars'
               ]
    option = rd.choice(options)
    print('Card: ', option)
    input('Press enter to continue')
    if option == 'Go To Jail':
        player.position = 30
    elif option == 'Community House Card':
        total = 0
        for prop in monopoly:
            for p in player.properties:
                if prop.name == p and prop.houses < 5:
                    player.money -= prop.houses * 40
                    total += prop.houses * 40
                elif prop.name == p and prop.houses == 5:
                    player.money -= 115
                    total += 115
        park.money += total
        print('You paid {} dollars in housing costs'.format(total))
    elif option == 'Get Out of Jail Free (+50 dollars)':
        player.money += 50
    elif option == 'Stock pays you 45 dollars':
        player.money += 45
    elif option == 'Each Player pays you 50 dollars':
        for i in range(len(total_players)):
            if total_players[i].name != player.name:
                total_players[i].money -= 50
                player.money += 50
                print('{} paid 50 dollars to {}'.format(total_players[i].name, player.name))
    elif option == 'Advance to Go':
        go(player)
        player.position = 0
    elif option == 'School Tax (-150)':
        player.money -= 150
        park.money += 150
    elif option == 'Doctor Fee (-50)':
        player.money -= 50
        park.money += 50
    elif option == 'Xmas Fund Matures (+100)':
        player.money += 100
    elif option == 'Income Tax Refund (+20)':
        player.money += 20
    elif option == 'Beauty Contest (+10)':
        player.money += 10
    elif option == 'Life Insurance Matures (+100)':
        player.money += 100
    elif option == 'Receive for services 25 dollars':
        player.money += 25
    elif option == 'Bank error in your favor (+200)':
        player.money += 200
    elif option == 'You inherit 100 dollars':
        player.money += 100
    print()


def chance(player, monopoly, total_players, park):
    print()
    input('Press Enter to draw a card!')
    options = ['Go To Jail', 'Advance to St. Charles Place', 'Pay Poor Tax', 'Chance House Card', 'Go Back 3 Spaces',
               'Advance to Nearest Utility', 'Advance to Boardwalk', 'Get Out of Jail Free (+50 dollars)',
               'Bank pays you 50 dollars', 'Pay Each Player 50 dollars', 'Advance to Nearest Railroad',
               'Advance to Reading Railroad', 'Advance to Go', 'Advance to Illinois Ave.',
               'Advance to Nearest Railroad', 'Your building loan matures (+150 dollars)'
               ]
    option = rd.choice(options)
    print('Card: ', option)
    input('Press enter to continue')
    if option == 'Go To Jail':
        player.position = 30
    elif option == 'Advance to St. Charles Place':
        player.position = 11
    elif option == 'Pay Poor Tax':
        print('That will cost 15 dollars')
        player.money -= 15
        park.money += 15
    elif option == 'Chance House Card':
        total = 0
        for prop in monopoly:
            for p in player.properties:
                if prop.name == p and prop.houses < 5:
                    player.money -= prop.houses * 25
                    total += prop.houses * 25
                elif prop.name == p and prop.houses == 5:
                    player.money -= 100
                    total += 100
        park.money += total
        print('You paid {} dollars in housing costs'.format(total))
    elif option == 'Go Back 3 Spaces':
        player.position -= 3
    elif option == 'Advance to Nearest Utility':
        if player.position < 12:
            player.position = 12
        elif 12 < player.position < 28:
            player.position = 28
        elif player.position >= 28:
            go(player)
            player.position = 12
    elif option == 'Advance to Boardwalk':
        player.position = 39
    elif option == 'Get Out of Jail Free (+50 dollars)':
        player.money += 50
    elif option == 'Bank pays you 50 dollars':
        player.money += 50
    elif option == 'Pay Each Player 50 dollars':
        for i in range(len(total_players)):
            if total_players[i].name != player.name:
                total_players[i].money += 50
                player.money -= 50
                print('{} paid 50 dollars to {}'.format(player.name, total_players[i].name))
    elif option == 'Advance to Nearest Railroad':
        if 5 < player.position < 15:
            player.position = 15
        elif 15 < player.position < 25:
            player.position = 25
        elif 25 < player.position < 35:
            player.position = 35
        elif player.position > 35:
            go(player)
            player.position = 5
    elif option == 'Advance to Reading Railroad':
        go(player)
        player.position = 5
    elif option == 'Advance to Go':
        go(player)
        player.position = 0
    elif option == 'Advance to Illinois Ave.':
        if player.position < 24:
            player.position = 24
        elif player.position > 24:
            go(player)
            player.position = 24
    elif option == 'Your building loan matures (+150 dollars)':
        player.money += 150
    print()
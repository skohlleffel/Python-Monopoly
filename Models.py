import random as rd
from Trades import trade, accept_trade
from collections import Counter
from Chance import chance, community, go
import pandas as pd


# roles the dice for the player
def role():
    input('Press enter to roll')
    return rd.randint(1, 6), rd.randint(1, 6)


# the turn for players
def turn(total_players, players, d_count, monopoly, park):
    print()
    print('Free Parking:', park.money)
    for i in range(len(total_players)):
        if not total_players[i].out:
            print(total_players[i].name)
        if players.trades:
            if total_players[i].name == players.trades['t_name']:
                accept_trade(players, total_players[i], monopoly)

    # for loop prints previous position
    for prop in monopoly:
        if players.position == prop.position:
            print()
            print('{}\'s turn!'.format(players.name))
            print('Previous Position:', prop.name)
            print()
    trade(total_players, players)
    check_4_monopoly(players, monopoly)
    print()
    # initiates player role
    d1, d2 = role()
    print('Your role:', d1, d2)
    d_count += 1
    print('Role counter:', d_count)
    j = jail(players, monopoly, d_count)
    if j:
        return players.position, d1, d2
    # moves the player in accordance with the role value
    players.position += (d1 + d2)
    j = jail(players, monopoly, d_count)
    if j:
        return players.position, d1, d2
    if players.position > 39:
        players.position -= 40
        go(players)
    for prop in monopoly:
        if players.position == prop.position:
            print('You have landed on {}'.format(prop.name))
        if players.position == prop.position and prop.name == 'Free Parking':
            fp(players, park)
        if players.position == prop.position and prop.name == 'Chance':
            chance(players, monopoly, total_players, park)
            j = jail(players, monopoly, d_count)
            if j:
                return players.position, d1, d2
        if players.position == prop.position and prop.name == 'Community Chest':
            community(players, monopoly, total_players, park)
            j = jail(players, monopoly, d_count)
            if j:
                return players.position, d1, d2
    for prop in monopoly:
        if players.position == prop.position and prop.name == 'Luxury Tax':
            luxury_tax(players, monopoly, prop.pay, park)
        elif players.position == prop.position and prop.name == 'Income Tax':
            income_tax(players, monopoly, prop.pay, park)
    # resets position if the player passes boardwalk
    for prop in monopoly:
        if players.position == prop.position and prop.owned:
            pay(total_players, players, monopoly)
    print()
    # initiates buy function
    buy(players, monopoly)
    check_4_monopoly(players, monopoly)
    add_houses(players, monopoly)
    # player gets to take another turn if he roles doubles
    remove_houses(players, monopoly)
    if d1 == d2 and d_count < 3:
        print('doubles, role again!')
        turn(total_players, players, d_count, monopoly, park)
    return players.position, d1, d2


def jail(players, monopoly, d_count):
    for prop in monopoly:
        if prop.position == players.position:
            if prop.name == 'Go To Jail' or d_count >= 3:
                print('You are now in jail.')
                players.jail = True
                players.position = 10
                return True
            else:
                return False


def fp(player, park):
    print()
    print('You have landed on free parking!')
    print('You receive {} dollars!'.format(park.money))
    input('Press enter to continue')
    player.money += park.money
    park.money = 0


# if the property is available to buy, player has that option
def buy(players, monopoly):
    for prop in monopoly:
        # checks player's board position and if the property is owned
        if players.position == prop.position and prop.owned is False:
            choice = input('Would you like to buy {} for {} dollars? '.format(prop.name, prop.cost))
            # checks if player has the money to buy the property
            if choice == 'yes' and players.money >= prop.cost:
                # subtracts player's property cost from player's money
                players.money -= prop.cost
                # changes the owned attribute to player's name
                prop.owned = players.name
                # adds property to the player's properties
                players.properties[prop.name] = [
                    prop.position, prop.rent, prop.cost, prop.house_cost, prop.color, prop.owned, prop.houses
                ]
                return players, monopoly, print('You chose to purchase')
            elif players.money <= prop.cost:
                return players, monopoly, print('You don\'t have enough money buddy')
            else:
                return players, monopoly, print('You chose not to purchase')


def pay(total_players, players, monopoly):
    for i in range(len(total_players)):
        for prop in monopoly:
            if total_players[i].name == prop.owned and players.name != prop.owned and prop.position == players.position:
                print('You have landed on an owned property.')
                input('Press enter to pay')
                if prop.color != 'railroad' and prop.color != 'utility':
                    if total_players[i].monopolies:
                        for mon in total_players[i].monopolies:
                            if mon == prop.color and prop.houses == 0:
                                price = prop.rent[0]*2
                            elif mon == prop.color and prop.houses != 0:
                                price = prop.rent[prop.houses]
                            else:
                                price = prop.rent[0]
                    else:
                        price = prop.rent[0]
                if prop.color == 'railroad':
                    amount = []
                    for p, v in total_players[i].properties.items():
                        print(v)
                        if v[4] == 'railroad':
                            amount.append(p)
                    print(amount)
                    price = prop.rent[len(amount) - 1]
                if prop.color == 'utility':
                    print()
                    print('Role to see how much you pay!')
                    d1, d2 = role()
                    print('Your role: ', d1, d2)
                    r = d1 + d2
                    amount = []
                    for p, v in total_players[i].properties.items():
                        if v[4] == 'utility':
                            amount.append(p)
                    if len(amount) == 2:
                        price = r * 10
                    if len(amount) == 1:
                        price = r * 4
                print('You owe {} {} dollars.'.format(prop.owned, price))
                print()
                if players.money >= price:
                    players.money -= price
                    total_players[i].money += price
                else:
                    total_players[i].money += players.money
                    players.money -= price
                    for p in monopoly:
                        for name, value in players.properties.items():
                            if p.name == name:
                                p.owned = total_players[i].name
                                value[5] = total_players[i].name
                    total_players[i].properties.update(players.properties)
                    players.properties = {}
                print('You have paid {} dollars to {}'.format(price, prop.owned))
                print('Owner:', total_players[i].money)
                print('Payer:', players.money)
                return


def check_if_out(players):
    if players.money <= 0:
        players.out = True
        return
    else:
        return


def add_houses(players, monopoly):
    add_list = []
    if players.monopolies:
        print('Would you like to add houses?')
        add = input('Type \'yes\' to add houses otherwise press \'enter\': ')
        print()
        if players.monopolies and add == 'yes':
            print()
            print('Available properties to add houses.')
            for mon in players.monopolies:
                for prop in monopoly:
                    if mon == prop.color:
                        print(prop.name, prop.color)
                print()
            choice = input('What color would you like to add houses to? ').split(', ')
            for c in choice:
                same_color = []
                for mon in players.monopolies:
                    for prop in monopoly:
                        if c == mon and mon == prop.color:
                            same_color.append(prop)
                add_list.append(same_color)
            if add_list:
                for mono in add_list:
                    print('Houses for {} properties cost {} dollars a piece'.format(mono[0].color, mono[0].house_cost))
                    input('Press enter to continue.')
                    print()
                    print('How many houses would you like to buy for your {} monopoly'.format(mono[0].color))
                    amount = int(input('Type the amount of houses that you would like to add per property: '))
                    if players.money - (mono[0].house_cost * amount * 2) > 0:
                        for p in mono:
                            if p.houses + amount <= 5:
                                p.houses += amount
                                players.money -= p.house_cost * amount
                    elif players.money - (mono[0].house_cost * amount * 2) > 0:
                        return print('You do not have enough money!')
                return print('Your Money: ', players.money)
            else:
                return
        else:
            return print('You did not add houses')
    else:
        return


def remove_houses(players, monopoly):
    remove_list = []
    if players.monopolies:
        print(players.monopolies)
        print('Would you like to remove houses?')
        remove = input('Type \'yes\' to remove houses otherwise press \'enter\': ')
        print()
        if players.monopolies and remove == 'yes':
            print()
            print('Available properties to remove houses.')
            for mon in players.monopolies:
                for prop in monopoly:
                    if mon == prop.color and prop.houses > 0:
                        print(prop.name, prop.color)
                print()
            choice = input('What color would you like to remove houses to? ').split(', ')
            for c in choice:
                same_color = []
                for mon in players.monopolies:
                    for prop in monopoly:
                        if c == mon and mon == prop.color:
                            same_color.append(prop)
                            print(same_color)
                remove_list.append(same_color)
                print(remove_list)
            if remove_list:
                for mono in remove_list:
                    print('Houses for {} properties cost {} dollars a piece'.format(mono[0].color, mono[0].house_cost))
                    input('Press enter to continue.')
                    print()
                    print('How many houses would you like to remove from your {} monopoly'.format(mono[0].color))
                    amount = int(input('Type the amount of houses that you would like to remove per property: '))
                    for p in mono:
                        if p.houses - amount >= 0:
                            p.houses -= amount
                            players.money += p.house_cost * amount
                return print('Your Money: ', players.money)
            else:
                return
        else:
            return print('You did not remove houses')
    else:
        return


def check_4_monopoly(players, monopoly):
    p_list = []
    b_list = []
    for values in players.properties.values():
        p_list.append(values[4])
    for prop in monopoly:
        b_list.append(prop.color)
    for k, v in Counter(b_list).items():
        for i, j in Counter(p_list).items():
            if k == i:
                if v == j and i not in players.monopolies:
                    return players.monopolies.append(i)
                if v != j and i in players.monopolies:
                    return players.monopolies.remove(i)


def income_tax(players, monopoly, tax, park):
    # checks player's board position and if the property is a tax tile
    print('Would you like to pay {} dollars or 10% of your total cash value? '.format(tax))
    choice = input('Type flat or 10% ')
    if choice == 'flat':
        players.money -= tax
        park.money += tax
    else:
        park.money += (players.money / 10)
        players.money -= (players.money / 10)
    check_if_out(players)
    if players.out:
        for prop in monopoly:
            for p, value in players.properties.items():
                if prop.name == p:
                    prop.owned = False
        return print('You are out!')
    else:
        return print('You paid your tax.')


def luxury_tax(players, monopoly, tax, park):
    print('You have to pay {} dollars in tax.'.format(tax))
    input('Press Enter to continue.')
    players.money -= tax
    park.money += tax
    check_if_out(players)
    if players.out:
        for prop in monopoly:
            for p, value in players.properties.items():
                if prop.name == p:
                    prop.owned = False
        return print('You are out!')
    else:
        return print('You paid your tax.')


# initiates the board from a property_data.csv which contains the board space information
def initiate():
    monopoly = []
    with open('property_data.csv', 'r', ) as csv_file:
        board = pd.read_csv(csv_file)
    for index, row in board.iterrows():
        if row[2] != 'FALSE':
            rent = []
            for i in row[2].split(', '):
                i = float(i)
                rent.append(i)
        else:
            rent = False
        # saves each space as a Property instance
        space = Property(row[0], row[1], rent, row[3], row[4], row[5], row[6], row[7], row[8])
        monopoly.append(space)
    return monopoly


class Player:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 1500
        self.properties = {}
        self.trades = {}
        self.monopolies = []
        self.jail = False
        self.jail_counter = 0
        self.out = False


class Property:

    def __init__(self, name, position, rent, cost, house_cost, color, owned, pay, houses):
        self.name = name
        self.position = position
        self.rent = rent
        self.cost = cost
        self.house_cost = house_cost
        self.color = color
        self.owned = owned
        self.pay = pay
        self.houses = houses


class Parking:

    def __init__(self):
        self.money = 0



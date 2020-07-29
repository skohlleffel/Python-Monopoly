from Models import Player, initiate, turn, check_if_out, role, Parking

monopoly = []
players = {}
p_count = int(input('How many players: '))

b = initiate()
free_parking = Parking()

for i in range(p_count):
    players[i] = Player('{}_{}'.format('player', i))

while len(players) > 1:
    for i in range(len(players)):
        check_if_out(players[i])
        if not players[i].out and not players[i].jail:
            r_count = 0
            result = turn(players, players[i], r_count, b, free_parking)
            print()
            print('Money:', players[i].money)
            print('Properties:', end=' ')
            for p in players[i].properties:
                print(p, end=' | ')
            print()
        elif players[i].out:
            print('{} is out'.format(players[i].name))
        elif players[i].jail and players[i].jail_counter < 3:
            print('{} is in jail'.format(players[i].name))
            print('Role to be released next turn!')
            print()
            d1, d2 = role()
            print('Your role: ', d1, d2)
            if d1 == d2:
                print()
                print('You got doubles. You will be released next turn!')
                players[i].jail = False
                players[i].jail_counter = 0
            else:
                print()
                print('Would you like to pay to be released next turn?')
                choice = input('Type yes or no: ')
                if choice == 'yes' and players[i].money > 50:
                    print('You will be released next turn for 50 dollars!')
                    players[i].money -= 50
                    free_parking.money += 50
                    players[i].jail = False
                    players[i].jail_counter = 0
                else:
                    print('You will remain in jail')
                    players[i].jail_counter += 1
            print()
        elif players[i].jail and players[i].jail_counter == 3 and players[i].money > 50:
            print('You are being released from jail for 50 dollars.')
            players[i].jail = False
            players[i].jail_counter = 0
            players[i].money -= 50
            free_parking.money += 50
            r_count = 0
            result = turn(players, players[i], r_count, b)
            print('Money:', players[i].money)
            print('Properties:', end=' ')
            for p in players[i].properties:
                print(p, end=' | ')
            print()









def accept_trade(recipient, trader, monopoly):
    print('Trade offer from {}'.format(trader.name))
    if 'r_prop' in recipient.trades and 't_prop' in recipient.trades and 'r_money' in recipient.trades:
        print('Trade offer: You receive {} and {} dollars. In return you give {} to {}'.format(recipient.trades['r_prop'], recipient.trades['r_money'], recipient.trades['t_prop'], recipient.trades['t_name']))
    elif 'r_prop' in recipient.trades and 't_prop' in recipient.trades and 't_money' in recipient.trades:
        print('yep 102')
        print(
            'Trade offer: You receive {}. In return you give {} and {} dollars to {}'.format(recipient.trades['r_prop'],
                                                                                             recipient.trades['t_prop'],
                                                                                             recipient.trades['t_money'],
                                                                                             recipient.trades['t_name']))
    elif 'r_prop' in recipient.trades and 't_money' in recipient.trades:
        print(
            'Trade offer: You receive {}. In return you give {} dollars to {}'.format(recipient.trades['r_prop'],
                                                                                             recipient.trades[
                                                                                                 't_money'],
                                                                                             recipient.trades[
                                                                                                 't_name']))
    elif 'r_prop' in recipient.trades and 't_prop' in recipient.trades:
        print(
            'Trade offer: You receive {}. In return you give {} to {}'.format(recipient.trades['r_prop'],
                                                                                      recipient.trades[
                                                                                          't_prop'],
                                                                                      recipient.trades[
                                                                                          't_name']))

    elif 't_prop' in recipient.trades and 'r_money' in recipient.trades:
        print(
            'Trade offer: You receive {} dollars. In return you give {} to {}'.format(recipient.trades['r_money'],
                                                                              recipient.trades[
                                                                                  't_prop'],
                                                                              recipient.trades[
                                                                                  't_name']))
    print()
    choice = input('Would you like to make the trade? ')
    if choice == 'yes':
        for prop in monopoly:
            if 'r_prop' in recipient.trades:
                for owned in recipient.trades['r_prop']:
                    if prop.name == owned:
                        prop.owned = recipient.name
                        # adds property to the player's properties
                        recipient.properties[prop.name] = [
                            prop.position, prop.rent, prop.cost, prop.house_cost, prop.color, prop.owned,
                        ]
            if 't_prop' in recipient.trades:
                for owned in recipient.trades['t_prop']:
                    if prop.name == owned:
                        prop.owned = trader.name
                        # adds property to the player's properties
                        trader.properties[prop.name] = [
                            prop.position, prop.rent, prop.cost, prop.house_cost, prop.color, prop.owned,
                        ]
        if 'r_money' in recipient.trades:
            trader.money -= recipient.trades['r_money']
            recipient.money += recipient.trades['r_money']
        if 't_money' in recipient.trades:
            trader.money += recipient.trades['t_money']
            recipient.money -= recipient.trades['t_money']
        if 'r_prop' in recipient.trades:
            for prop in recipient.trades['r_prop']:
                del trader.properties[prop]
        if 't_prop' in recipient.trades:
            for prop in recipient.trades['t_prop']:
                del recipient.properties[prop]
        recipient.trades = {}
        print()
        print(recipient.money, recipient.properties)
        print(trader.money, trader.properties)
        print()
        return print('The trade was executed!')
    else:
        recipient.trades = {}
        return print('You rejected the trade!')


def trade(total_players, players):
    print('Would you like to initiate a trade? ')
    choice = input('Type \'yes\' to trade, otherwise press enter: ')
    if choice == 'yes':
        print('Players:')
        for i in range(len(total_players)):
            if total_players[i].name != players.name:
                print(total_players[i].name)
        print()
        p_to_trade = input('Who would you like to trade with? ')
        for i in range(len(total_players)):
            if p_to_trade == total_players[i].name and p_to_trade != players.name:
                print('{}\'s properties {}'.format(players.name, players.properties))
                print('{}\'s money {}'.format(players.name, players.money))
                print()
                print('{}\'s properties {}'.format(p_to_trade, total_players[i].properties))
                print('{}\'s money {}'.format(p_to_trade, total_players[i].money))
                print()
                print('What would you like to offer? ')
                offer = input('Type money or property or both: ')
                print()
                print('What would you like in return? ')
                receive = input('Type money or property or both: ')
                if offer == 'money' and receive == 'property':
                    money_for_prop(total_players[i], players)
                elif offer == 'property' and receive == 'money':
                    prop_for_money(total_players[i], players)
                elif offer == 'property' and receive == 'property':
                    prop_for_prop(total_players[i], players)
                elif offer == 'property' and receive == 'both':
                    prop_for_both(total_players[i], players)
                elif offer == 'both' and receive == 'property':
                    both_for_prop(total_players[i], players)
                else:
                    return print('That trade does not make sense')
    else:
        print('You chose not to trade.')
        return print()


# 0 = trader name, 1 = recipient properties, 2 = recipient money, 3 = trader properties, 4 = trader money
def both_for_prop(recipient, trader):
    print('Your properties: {}'.format(trader.properties))
    print('Your money: {}'.format(trader.money))
    print('His properties: {}'.format(recipient.properties))
    p_for_recipient = input('What properties would you like to offer? ').split(', ')
    m_for_recipient = int(input('How much money would you like to offer? '))
    p_for_trader = input('What properties would you like in return? ').split(', ')
    recipient.trades['t_name'] = trader.name
    for prop in p_for_recipient:
        if prop in trader.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['r_prop'] = p_for_recipient
    for prop in p_for_trader:
        if prop in recipient.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['t_prop'] = p_for_trader
    if m_for_recipient < trader.money:
        recipient.trades['r_money'] = m_for_recipient
        return print(recipient.trades)
    else:
        recipient.trades = {}
        return print('The trade is not viable')


def prop_for_both(recipient, trader):
    print('Your properties: {}'.format(trader.properties))
    print('His money: {}'.format(recipient.money))
    print('His properties: {}'.format(recipient.properties))
    p_for_recipient = input('What properties would you like to offer? ').split(', ')
    m_for_trader = int(input('How much money would you like in return? '))
    p_for_trader = input('What properties would you like in return? ').split(', ')
    recipient.trades['t_name'] = trader.name
    for prop in p_for_recipient:
        if prop in trader.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['r_prop'] = p_for_recipient
    for prop in p_for_trader:
        if prop in recipient.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['t_prop'] = p_for_trader
    if m_for_trader < recipient.money:
        recipient.trades['t_money'] = m_for_trader
        return print(recipient.trades)
    else:
        recipient.trades = {}
        return print('The trade is not viable')


def prop_for_money(recipient, trader):
    print('Your properties: {}'.format(trader.properties))
    print('His money: {}'.format(recipient.money))
    p_for_recipient = input('What properties would you like to offer? ').split(', ')
    m_for_trader = int(input('How much money would you like in return? '))
    recipient.trades['t_name'] = trader.name
    for prop in p_for_recipient:
        if prop in trader.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['r_prop'] = p_for_recipient
    if m_for_trader < recipient.money:
        recipient.trades['t_money'] = m_for_trader
        return print(recipient.trades)
    else:
        recipient.trades = {}
        return print('The trade is not viable')


def prop_for_prop(recipient, trader):
    print('Your properties: {}'.format(trader.properties))
    print('His properties: {}'.format(recipient.properties))
    p_for_recipient = input('What properties would you like to offer? ').split(', ')
    p_for_trader = input('What properties would you like in return? ').split(', ')
    recipient.trades['t_name'] = trader.name
    for prop in p_for_recipient:
        if prop in trader.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['r_prop'] = p_for_recipient
    for prop in p_for_trader:
        if prop in recipient.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['t_prop'] = p_for_trader
    return print(recipient.trades)


def money_for_prop(recipient, trader):
    print('Your money: {}'.format(trader.money))
    print('His properties: {}'.format(recipient.properties))
    m_for_recipient = int(input('How much money would you like to offer? '))
    p_for_trader = input('What properties would you like in return? ').split(', ')
    recipient.trades['t_name'] = trader.name
    for prop in p_for_trader:
        if prop in recipient.properties:
            pass
        else:
            recipient.trades = {}
            return print('The trade is not viable')
    recipient.trades['t_prop'] = p_for_trader
    if m_for_recipient < trader.money:
        recipient.trades['r_money'] = m_for_recipient
        return print(recipient.trades)
    else:
        recipient.trades = {}
        return print('The trade is not viable')
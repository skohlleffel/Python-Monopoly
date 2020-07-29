import csv
from Models import Player, Property

property_list = []

# creates data for properties on the board
with open('property_data.csv', 'w', ) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Board Position', 'Rent', 'Cost', 'House Cost', 'Color'])
    for i in range(23):
        n = input('Name? ')
        p = int(input('Board Position? '))
        r = list(map(int, input('Rent Costs? ').strip().split()))[:6]
        c = int(input('Property Cost? '))
        h = int(input('House Cost? '))
        co = input('Color? ')
        property_list.append(Property(n, p, r, c, h, co))

    for prop in property_list:
        writer.writerow([prop.name, prop.position, prop.rent, prop.cost, prop.house_cost, prop.color])

# creates data for railroads on the board
with open('property_data.csv', 'a', ) as csvfile:
    writer = csv.writer(csvfile)
    for i in range(6):
        n = input('Name? ')
        p = int(input('Board Position? '))
        r = int(input('Rent? '))
        c = int(input('Property Cost? '))
        co = input('Group? ')
        property_list.append(Railroad(n, p, r, c, co))

    for prop in property_list:
        writer.writerow([prop.name, prop.position, prop.rent, prop.cost, prop.color])

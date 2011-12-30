#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import random


lastnames = ['Mendoza', 'Pascual','Castillo', 'Villanueva', 'Ramos', 'Diaz', 'Rivera','Aquino','Navarro','Mercado', 'Rossi', 'Russo',
                'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco', 'Bruno', 'Gallo', 'Conti',
        'Hansen', 'Johansen', 'Olsen','Larsen','Andersen', 'Pedersen', 'Nilsen', 'Kristiansen', 'Jensen', 'Karlsen', 'Johnsen', 'Pettersen',
        'Berg', 'Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davis', 'Robinson', 'Wright', 'Thompson', 'Evans',
        'Walker', 'White',  'Roberts', 'Green', 'Hall', 'Wood', 'Jackson', 'Clarke',]

firstnames = ['Joseph', 'Juan','Kishore', 'Ramos', 'Diago', 'Bobby','Navarro','Mercado',
                'Aiden', 'Ethan', 'Lucas', 'Liam', 'Noah', 'Jacob', 'Jayden', 'Jack', 'Logan', 'Cayden',
                'Daniel', 'Joseph', 'Michael', 'David', 'Matthew', 'Alexander', 'Jacob', 'Nicholas', 'Jack', 'Samuel,'
                'Léa', 'Florence', 'Emma', 'Rosalie', 'Jade', 'Juliette', 'Camille', 'Gabrielle', 'Maika', 'Mia',
                'Emma', 'Ava', 'Olivia', 'Emily', 'Brooklyn', 'Chloe', 'Madison', 'Alexis', 'Hailey', 'Hannah']


names = []
for i in xrange(0,200):
    first = firstnames[random.randint(0,len(firstnames)-1)]
    last = lastnames[random.randint(0,len(lastnames)-1)]
    names.append((first, last))

print names

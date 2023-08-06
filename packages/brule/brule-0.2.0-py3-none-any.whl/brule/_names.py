FIRST_NAMES = {
    'male': {
        'initials': {
            'a': ['Alan', 'Albert', 'Alvin', 'Arthur'],
            'b': ['Bobby','Billy', 'Barney', 'Benny', 'Buster', 'Barry'],
            'c': ['Charles','Charlie','Karl','Carl', 'Chuck'],
            'd': ['Dan', 'Donny', 'Deryl', 'Darvin','Danny','Douglas', 'Doyle'],
            'e': ['Eddy', 'Eddie', 'Ernie', 'Earl', 'Elbert', 'Elmo', 'Edgar'],
            'f': ['Franky', 'Fabio', 'Frank', 'Fred', 'Freddy', 'Franklin', 'Francis'],
            'g': ['Gary', 'Jerry', 'Gerald', 'Garfield', 'Greg', 'Gus', 'George', 'Georgie'],
            'h': ['Harry', 'Hank', 'Harold', 'Howard', 'Huey'],
            'i': ['Irwin', 'Ivan'],
            'j': ['Jimmy', 'Jerry','Johnny', 'Jeffry', 'Joey', 'Jackie'],
            'k': ['Kevin', 'Kenny', 'Karl', 'Kyle', 'Kirby', 'Keith'],
            'l': ['Larry', 'Lloyd', 'Louie', 'Leroy', 'Lester', 'Lenny'],
            'm': ['Mickey','Michael', 'Mikey', 'Marcus', 'Melvin', 'Marivn'],
            'n': ['Norman', 'Nelson', 'Ned'],
            'o': ['Oscar', 'Omar', 'Otis'],
            'p': ['Paul', 'Peter', 'Perry', 'Pedro'],
            'q': ['Kevin', 'Kenny', 'Karl', 'Kyle', 'Kirby', 'Keith'],
            'r': ['Richie', 'Roy', 'Randy', 'Ronnie', 'Ronald', 'Robbie', 'Reggie'],
            's': ['Sammy', 'Stevie', 'Scotty', 'Stanley'],
            't': ['Tony', 'Timmy', 'Tommy', 'Teddy', 'Terry'],
            'v': ['Vinny', 'Victor'],
            'w': ['Walter', 'Willy', 'Wallace', 'Willis'],
        },
        'other': [
            'Jimmy', 'Johnny', 'Tony', 'Randy', 'Danny', 'Billy',
            'Stevie', 'Franky', 'Jerry', 'Gary', 'Bobby', 'Tommy',
            'Ronnie', 'Robbie', 'Timmy', 'Willy', 'Jackie'
        ]
    },
    'female': {
        'initials': {
            'a': ['Amy', 'Abby', 'Ally', 'Annie'],
            'b': ['Betty', 'Beverly', 'Babara', 'Betsy', 'Bonnie'],
            'c': ['Cindy', 'Cynthia', 'Carly', 'Carol'],
            'd': ['Doris', 'Debbie', 'Daisy', 'Dolores'],
            'e': ['Emily', 'Erica', 'Edna'],
            'f': ['Frannie','Francis', 'Fanny'],
            'g': ['Gretchen', 'Gloria'],
            'h': ['Hannah', 'Honey', 'Herma', 'Helen'],
            'j': ['Jenny', 'Jacky', 'Jessie'],
            'k': ['Katie', 'Kathy', 'Kelly', 'Karen'],
            'l': ['Lucy', 'Lisa', 'Lora'],
            'm': ['Mary', 'Martha', 'Margo'],
            'n': ['Nancy', 'Nicky', 'Norma'],
            'p': ['Paulie', 'Patty', 'Penny'],
            'r': ['Rita', 'Roxy', 'Rosy'],
            's': ['Sally', 'Sarah', 'Sharla', 'Shawna', 'Suzy', 'Sunshine'],
            't': ['Tiffany', 'Tina', 'Tracy', 'Toni'],
            'w': ['Wanda', 'Wendy', 'Wilma'],
        },
        'other': [
            'Sally', 'Cindy', 'Doris', 'Wendy', 'Mary', 'Lisa',
            'Francis', 'Betty', 'Bonnie', 'Annie', 'Debbie',
            'Suzy', 'Jenny'
        ]
    }
}

# aggregate some fields
FIRST_NAMES['male']['all'] = [name for names in FIRST_NAMES['male']['initials'].values() for name in names]
FIRST_NAMES['female']['all'] = [name for names in FIRST_NAMES['female']['initials'].values() for name in names]
FIRST_NAMES['all'] = [FIRST_NAMES['male']['all'] + FIRST_NAMES['female']['all']]

LAST_NAMES = {
    'suffix': [
        'ingus', 'ringus', 'rangus', 'angus', 
        'rungus', 'ungus', 'ringle', 'ingle', 
        'rangle', 'ramble', 'rungo',
    ],
    'no_r_suffix': [
        'ingus', 'angus', 'ungus', 'ingle',
        'angle', 'amble', 'umble',
    ],
    'vowel_suffix': [
        'Bringle', 'Brangus', 'Bringo', 'Bingus',
        'Brungus', 'Brangle', 'Brungo', 'Bramble',
        'Crangus', 'Drangus', 'Dangus', 'Dingus',
        'Dringus', 'Jangles', 'Jangus', 'Pringle',
        'Rangus', 'Ringus',
    ]
}
import sqlite3


# connect to the appropriate database
# (if it doesn't exist, it will be automatically created)
connecteddb = sqlite3.connect("databases/PaperMario.db")

# obtain the cursor for the db (allows us to interact with it)
cursor = connecteddb.cursor()

# make sure to enable foreign keys!
cursor.execute("PRAGMA foreign_keys = ON")

# create a table
##cursor.execute("""DROP TABLE IF EXISTS items""")
##cursor.execute("""CREATE TABLE items (
##                    name text,
##                    description text,
##                    droppedBy text,
##                    buyPrice real,
##                    sellPrice real,
##                    filtered integer,
##                    PRIMARY KEY (name) ) """)
##
##cursor.execute("""DROP TABLE IF EXISTS recipes""")
##cursor.execute("""CREATE TABLE recipes (
##                product text,
##                ing1 text,
##                ing2 text,
##                numOfIngredients integer,
##                PRIMARY KEY (ing1, ing2),
##                FOREIGN KEY (product) REFERENCES items (name) ON DELETE CASCADE,
##                FOREIGN KEY (ing1) REFERENCES items (name) ON DELETE CASCADE,
##                FOREIGN KEY (ing2) REFERENCES items (name) ON DELETE CASCADE)""")

# add a new item to the table
##cursor.execute("""INSERT INTO items (name, description) VALUES ('mushroom', 'heals 5hp')""")

# add multiple items to the table
itemList = [('apple', '5hp found in crate in boo\'s mansion (8bit mario jar room)', None, None, None, 0),
            ('apple pie', '5hp 15fp', None, None, None, 1),
            ('bland meal', '10hp 10fp', None, None, None, 1),
            ('blue berry', '5fp, found in southeast flower fields', None, None, None, 0),
            ('bubble berry', '5hp, found in southeast flower fields', None, None, None, 0),
            ('cake', '15fp', None, None, None, 1),
            ('cake mix', '1fp, dropped by shy guys in main station far left room', None, None, None, 0),
            ('coco pop', '3hp 15fp', None, None, None, 1),
            ('coconut', '', None, None, None, 0),
            ('dizzy dial', 'paralyze all enemies', None, None, None, 1),
            ('dried fruit', '15hp dropped by pokey', None, None, None, 0),
            ('dried pasta', '3hp 2fp', None, None, None, 0),
            ('dried shroom', '1hp, dropped by black oink', None, None, None, 0),
            ('egg', '5hp, found in bush by mt rugged train station', None, None, None, 0),
            ('fire flower', '3 damage all enemies, dropped by pink oink', None, None, None, 0),
            ('fried egg', '10hp', None, None, None, 1),
            ('fried shroom', '6hp 2fp', None, None, None, 1),
            ('goomnut', '3fp, dropped by tree in goomba village', None, None, None, 0),
            ('honey shroom', '5hp 5fp', None, None, None, 1),
            ('honey super', '10hp 5fp', None, None, None, 1),
            ('honey syrup', '5fp', None, None, None, 0),
            ('hot shroom', '15hp 5fp', None, None, None, 1),
            ('iced potato', '5hp, in shiver city toad house after napping', None, None, None, 0),
            ('jammin\' jelly', '50fp, dropped by silver oink', None, None, None, 0),
            ('jelly pop', '64 fp', None, None, None, 1),
            ('jelly super', '10hp 50fp', None, None, None, 1),
            ('jelly ultra', '50hp 50fp', None, None, None, 1),
            ('kooky cookie', '15fp, mario gets electric, sleepy, or transparent', None, None, None, 1),
            ('koopa leaf', '3fp', None, None, None, 0),
            ('koopa tea', '7fp', None, None, None, 1),
            ('koopasta', '7hp 7fp', None, None, None, 1),
            ('lemon', '1hp 2fp', None, None, None, 0),
            ('life shroom', 'revive 10hp, dropped by shroom oink', None, None, None, 0),
            ('lime', '3fp', None, None, None, 0),
            ('maple shroom', '5hp 10fp', None, None, None, 1),
            ('maple super', '10hp 10fp', None, None, None, 1),
            ('maple syrup', '10fp, dropped by shy guys in main station far left room, by bees in flower fields, and by flower oink', None, None, None, 0),
            ('maple ultra', '50hp 10fp', None, None, None, 1),
            ('melon', '15hp, trade successful Tayce T. recipes with Yellow Yoshi mother (lavalava island)', None, None, None, 0),
            ('mistake', '1hp 1fp', None, None, None, 1),
            ('mushroom', '5hp', None, None, None, 0),
            ('nutty cake', '10fp', None, None, None, 1),
            ('pebble', '1 damage single enemy, found lying around in ice palace (may not respawn)', None, None, None, 0),
            ('potato salad', 'potato salad', None, None, None, 1),
            ('pow block', 'flip shell 2 damage all enemies', None, None, None, 1),
            ('red berry', '5hp, dropped by tree in east flower fields', None, None, None, 0),
            ('repel gel', 'invisible, dropped by ? oink', None, None, None, 1),
            ('shooting star', '6 damage all enemies, dropped by star oink', None, None, None, 1),
            ('shroom steak', '30hp 10fp', None, None, None, 1),
            ('snowman doll', '4 damage all enemies', None, None, None, 1),
            ('spaghetti', '6hp 4fp', None, None, None, 1),
            ('special shake', '20fp', None, None, None, 1),
            ('spicy soup', '', None, None, None, 1),
            ('stinky herb', '5fp, dropped by vine panels in flower fields', None, None, None, 0),
            ('stone cap', 'turn to stone unable to move (assume high defense)', None, None, None, 1),
            ('stop watch', 'paralyze all enemies', None, None, None, 1),
            ('strange leaf', '5fp found in bush outside boo\'s mansion', None, None, None, 0),
            ('super shroom', '10hp, dropped by white oink', None, None, None, 0),
            ('super soda', 'cures shrink poison 5fp', None, None, None, 1),
            ('tasty tonic', 'cures poison shrink', None, None, None, 1),
            ('thunder bolt', '5 damage single enemy', None, None, None, 1),
            ('thunder rage', '5 damage all enemies, dropped by tiger oink', None, None, None, 1),
            ('ultra shroom', '50hp, randomly appears in shiver city toad house after nap, dropped by gold oink', None, None, None, 0),
            ('volt shroom', 'damage enemies on touch', None, None, None, 0),
            ('whacka\'s bump', '25hp 25fp', None, None, None, 1),
            ('yellow berry', '3hp 3fp, dropped in southwest flower fields', None, None, None, 0),
            ]
##cursor.executemany("""INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)""", itemList)


recipeList = [('apple pie', 'cake mix', 'apple', 2),
                ('bland meal', 'dried pasta', 'goomnut', 2),
                ('bland meal', 'dried pasta', 'mushroom', 2),
                ('bland meal', 'fire flower', 'goomnut', 2),
                ('bland meal', 'goomnut', 'koopa leaf', 2),
                ('bland meal', 'super shroom', 'fire flower', 2),
                ('cake', 'cake mix', None, 1),
                ('coco pop', 'cake mix', 'coconut', 2),
                ('fried egg', 'egg', None, 1),
                ('fried shroom', 'mushroom', None, 1),
                ('fried shroom', 'super shroom', None, 1),
                ('honey shroom', 'honey syrup', 'mushroom', 2),
                ('honey super', 'honey syrup', 'super shroom', 2),
                ('hot shroom', 'volt shroom', None, 1),
                ('jelly pop', 'cake mix', 'jammin\' jelly', 2),
                ('jelly super', 'jammin\' jelly', 'super shroom', 2),
                ('jelly ultra', 'jammin\' jelly', 'ultra shroom', 2),
                ('kooky cookie', 'cake mix', 'koopa leaf', 2),
                ('kooky cookie', 'maple syrup', 'cake mix', 2),
                ('koopa tea', 'koopa leaf', None, 1),
                ('koopasta', 'dried pasta', 'koopa leaf', 2),
                ('life shroom', 'koopa leaf', 'volt shroom', 2),
                ('maple shroom', 'maple syrup', 'mushroom', 2),
                ('maple super', 'super shroom', 'maple syrup', 2),
                ('maple ultra', 'maple syrup', 'ultra shroom', 2),
                ('mistake', 'apple', 'dried pasta', 2),
                ('mistake', 'apple', 'fire flower', 2),
                ('mistake', 'cake', None, 1),
                ('mistake', 'dizzy dial', None, 1),
                ('mistake', 'dried fruit', None, 1),
                ('mistake', 'dried pasta', 'fire flower', 2),
                ('mistake', 'dried shroom', None, 1),
                ('mistake', 'egg', 'apple', 2),
                ('mistake', 'egg', 'goomnut', 2),
                ('mistake', 'egg', 'lemon', 2),
                ('mistake', 'fried egg', None, 1),
                ('mistake', 'fried shroom', None, 1),
                ('mistake', 'goomnut', 'maple syrup', 2),
                ('mistake', 'hot shroom', None, 1),
                ('mistake', 'iced potato', 'melon', 2),
                ('mistake', 'koopa leaf', 'apple', 2),
                ('mistake', 'koopa leaf', 'fire flower', 2),
                ('mistake', 'koopa tea', None, 1),
                ('mistake', 'lemon', 'dried pasta', 2),
                ('mistake', 'lime', 'coconut', 2),
                ('mistake', 'mistake', None, 1),
                ('mistake', 'red berry', 'bubble berry', 2),
                ('mistake', 'shroom steak', None, 1),
                ('mistake', 'snowman doll', None, 1),
                ('mistake', 'spaghetti', None, 1),
                ('mistake', 'stinky herb', None, 1),
                ('mistake', 'stinky herb', 'maple syrup', 2),
                ('mistake', 'strange leaf', None, 1),
                ('mistake', 'super soda', None, 1),
                ('mistake', 'tasty tonic', None, 1),
                ('mistake', 'thunder bolt', None, 1),
                ('mistake', 'thunder rage', None, 1),
                ('mistake', 'whacka\'s bump', None, 1),
                ('mistake', 'whacka\'s bump', 'honey syrup', 2),
                ('nutty cake', 'goomnut', None, 1),
                ('potato salad', 'iced potato', None, 1),
                ('shroom steak', 'ultra shroom', None, 1),
                ('spaghetti', 'dried pasta', None, 1),
                ('special shake', 'jammin\' jelly', 'maple syrup', 2),
                ('special shake', 'jammin\' jelly', 'melon', 2),
                ('special shake', 'melon', None, 1),
                ('special shake', 'melon', 'maple syrup', 2),
                ('spicy soup', 'fire flower', None, 1),
                ('super shroom', 'honey syrup', 'volt shroom', 2),
                ('super soda', 'apple', None, 1),
                ('super soda', 'blue berry', 'maple syrup', 2),
                ('super soda', 'blue berry', 'yellow berry', 2),
                ('super soda', 'honey syrup', None, 1),
                ('super soda', 'honey syrup', 'koopa leaf', 2),
                ('super soda', 'jammin\' jelly', None, 1),
                ('super soda', 'lime', 'lemon', 2),
                ('super soda', 'maple syrup', None, 1),
                ('super soda', 'red berry', None, 1),
                ('super soda', 'red berry', 'blue berry', 2),
                ('super soda', 'red berry', 'yellow berry', 2),
                ('tasty tonic', 'bubble berry', None, 1),
                ('tasty tonic', 'coconut', None, 1),
                ('tasty tonic', 'lemon', None, 1),
                ('tasty tonic', 'lime', None, 1),
                ('tasty tonic', 'red berry', None, 1),
                ('tasty tonic', 'yellow berry', 'honey syrup', 2),
                ('volt shroom', 'koopa leaf', 'mushroom', 2),
              ]
##cursor.execute("drop table recipes")
##sql = "insert into recipes values (?, ?, ?, ?)"
##cursor.executemany(sql, recipeList)
##
#### save all the changes!
##connecteddb.commit()

### show table info
##cursor.execute("SELECT * FROM items")
##print(cursor.fetchall())

### show table info (with each entry on a seperate line)
### also best to separate the sql and arguments to prevent quoting errors
### Note: when separating args, make sure it's in a list!

### trying to fill in "numOfIngredients" column in recipes table
##sql = 'update recipes set numOfIngredients = ?'
##args = [len(ingredients.split(") ("))+1]

### get all items that contain the word "shroom"
##sql = "select * from recipes where recipes.product = ?"
##args = ["mistake"]

### get all items that can be made using a recipe, but where the product's description includes "hp"
##sql = "select R.*, I.description from items I, recipes R where I.description like ? and R.product = I.name"
##args = ["%hp%"]


sql = "select * from recipes where product = ? or ing1 = ? or ing2 = ?"
args = ["spaghetti", "spaghetti", "spaghetti"]


for row in cursor.execute(sql, args):
    print(row)













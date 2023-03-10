import random, sqlite3

from qset import Qset

from database import table1, table2, table3


def compilations(table):
    with sqlite3.connect("database/database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table};")
        compilation = cursor.fetchall() # A list of all rows in database
        return compilation
    
def quizGen():     
    random_row = random.choice(COMPLETE_SET)
    quizObject = Qset(random_row[1], random_row[2], id = random_row[0])
    return quizObject

COMPLETE_SET = compilations(table3)
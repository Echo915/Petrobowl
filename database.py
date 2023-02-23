from qset import Qset

import sqlite3


def collate(filename, bool_val):
    with open(filename, encoding = "utf-8") as file_object:
        '''encoding helps the computer to understand some characters'''

        # puts the lines in the file into a list and assigns the list to lines
        lines = file_object.readlines()

        # Testing for errors in compiling data
        if bool_val == True:
            while lines:
                print(lines[0])
                del lines[0:2]

        # Creates instances of Qsets and appends them to QUIZ_SET
        while lines:
            qset = Qset(question = lines[0], answer = lines[1])
            QUIZ_SET.append(qset)
            del lines[0:2]

def collation(unrefined = None, refined = None, test = False):
    # Collates unrefined qsets where qsets are sets of files to be collated
    if unrefined != None:
        for qset in unrefined:
            collate(qset, test)

        # Cleaning unrefined qsets 
        for index in QUIZ_SET:
            temp = index.question.split()
            #temp.pop(0)
            for x in temp[0]:
                if x.isdigit() or x == ".":
                    temp[0] = temp[0].replace(x, "")
            index.question = " ".join(temp)

            index.answer = index.answer.replace("Answer.", "")

    # Collates refined qsets
    if refined != None:
        for qset in refined:
            collate(qset)

def create_database(table):
    # Creating database to store data
    delete_table = f"DROP TABLE IF EXISTS {table};"
    create_table = f"""
    CREATE TABLE {table}(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    question TEXT, 
    answer TEXT
    );
    """

    with sqlite3.connect("database/database.db") as connection:
        cursor = connection.cursor()
        #cursor.execute(delete_table)
        cursor.execute(create_table)

        for item in QUIZ_SET:
            insert_value = (item.question, item.answer)
            cursor.execute(f"INSERT INTO {table} (question, answer) VALUES(?, ?);", insert_value)

# Edits or adds new data to database
def update_database(table, state = "insert", data = None, id = None, que = None, ans = None):
    with sqlite3.connect("database/database.db") as connection:
        cursor = connection.cursor()

        # Inserts new data provided in argument into database
        if state == "add":
            if data == None:
                print("Please specify data to add to database")
                return
            
            for qset in data:
                insert_value = (qset.question, qset.answer)
                cursor.execute(f"INSERT into {table} (question, answer) VALUES (?, ?);", insert_value)
            return

        # Edits database at id specified in argument
        if id == None:
            print("Missing required argument 'id'")
            return
        # Edits question
        if que != None:
            cursor.execute(f"UPDATE {table} SET question = ? WHERE id = ?;", (que, id))
        # Edits answer
        if ans != None:
            cursor.execute(f"UPDATE {table} SET answer = ? WHERE id = ?;", (ans, id))
        else:
            # prints out data if no replacement values are specified
            cursor.execute(f"SELECT * FROM {table} WHERE id = ?;", (id,))
            specimen = cursor.fetchone()
            print(specimen[0], specimen[1])
            print(specimen[2])

QUIZ_SET = []

# Files
qset1 = "data/Qset.txt"
qset2 = "data/Qset2.txt"
qset3 = "data/Qset3.txt"

# Training files
train_qset1 = "training/qset1.txt"
train_qset2 = "training/qset2.txt"
train_qset3 = "training/qset3.txt"

# Existing tables in database
"""QA_Pair""" # Main qset
"QA_Pair_Train" # Breakdown for training

#collation([train_qset1])
#create_database() 
"""needs fixing (109, 175, 20)"""

#collation(unrefined=[train_qset3])
#update_database(table="QA_Pair_Train", state="add", data=QUIZ_SET)
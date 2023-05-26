import sqlite3
import os
import datetime
import random


DB_PATH = "../forum.db"
DB_PATH_ABSOLUTE = os.path.abspath(DB_PATH)
CURRENT_USER = False


class Connection():
    # Context manager which makes code more readable and safer to execute
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()
    
    def __enter__(self):
        return self
    
    def __exit__(self, excType, excValue, traceback):
        
        self.conn.commit()
        self.conn.close()

        if excType:
            print(excType)
        if excValue:
            print(excValue)
        if traceback:
            print(traceback)


def init_tables():
    with Connection() as db:
        db.c.execute("DROP TABLE IF EXISTS messages")
        db.c.execute("""CREATE TABLE messages (
            content TEXT, -- Message body, i.e. the actual content you have posted (NOTE: should be a BLOB later on)
            poster INT, -- UID of Original Poster
            post_time TEXT, -- Time of Posting
            id INT  -- Unique message ID
        )""")
        log(f"Created Message Table at {DB_PATH_ABSOLUTE}")

        db.c.execute("DROP TABLE IF EXISTS users")
        # NOTE: Will expand on this later, but just need to get the ball rolling
        db.c.execute("""CREATE TABLE users (
            user_id INT,
            username TEXT,
            password TEXT,  -- Password will be hashed in the flask app
            posted_msgs INT
        )""")
        log(f"Created User Table at {DB_PATH_ABSOLUTE}")


def create_user(userinfo: list):
    global CURRENT_USER
    username = userinfo[0]
    password = userinfo[1]
    id = create_id()
    with Connection() as db:
        db.c.execute("""INSERT INTO users(
            user_id,
            username,
            password,
            posted_msgs
        ) VALUES (?, ?, ?, 0)""", [id, username, password])
    log(f"Created user {id} at {DB_PATH_ABSOLUTE}")
    CURRENT_USER = id  # A Variable for testing user functions within this file


def get_user(id):
    with Connection() as db:
        db.c.execute("SELECT * FROM users WHERE user_id = ?", [id])
        user = db.c.fetchall()[0]
    return user


def create_post(content: str, user: int):
    if user != CURRENT_USER:
        log(f"ERROR: Could not create message: Not Logged in")
        return False
    with Connection() as db:
        db.c.execute("UPDATE users SET posted_msgs = ? WHERE user_id = ?", [get_user(CURRENT_USER)[3] + 1, CURRENT_USER])
    with Connection() as db:
        id = create_id(True)
        db.c.execute("""INSERT INTO messages(
            content,
            poster,
            post_time,
            id
        ) VALUES (?, ?, ?, ?)""", [content, user, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), id])
    log(f"Added message {id} to database at {DB_PATH_ABSOLUTE}")
    log(f"Updated user {CURRENT_USER} at {DB_PATH_ABSOLUTE}")


def fetch_message(id: int):
    with Connection() as db:
        db.c.execute("SELECT * FROM messages WHERE id = ?", [id])
        message = db.c.fetchall()[0]
    return message


# Function which creates an ID for a user or a post
def create_id(*post: bool) -> int:
    if post:
        baseline = str(CURRENT_USER)
        extra = str(get_user(CURRENT_USER)[3])
        return int(baseline + extra)
    baseline = datetime.datetime.today().strftime("%Y%m%d%f")
    hour = datetime.datetime.today().strftime("%H%M")
    ms = datetime.datetime.now().strftime("%f")
    random.seed = int(hour) * int(ms)
    randomness = str(random.randint(1000, 9999))

    return int(baseline + randomness)


def get_messages_all() -> list:
    with Connection() as db:
        msglist = []
        db.c.execute("SELECT content, poster FROM messages")
        messages = db.c.fetchall()
        for msg in messages:
            db.c.execute("SELECT username FROM users WHERE user_id = ?", [msg[1]])
            user = db.c.fetchone()
            msglist.append(f'{user[0]}: {msg[0]}')
        return msglist[::-1]


def delete_message(id: int):
    with Connection() as db:
        db.c.execute("DELETE * FROM messages WHERE id = ?", [id])
    log(f"Deleted Message {id} at {DB_PATH_ABSOLUTE}")


# Function for testing, messing around, whatever really.
def temp(content):
    create_user(["SimTest", "bigpassword3"])
    create_post(content, CURRENT_USER)


# Test function for the database. You end up with a template database.
def test_database():
    # init_tables()
    create_user(["Test", "password123"])
    create_post("Første melding!", 1)
    # create_post("En til melding?", CURRENT_USER)
    # create_post("Meldinger overalt!", CURRENT_USER)
    # create_post("Ok nå er det nok meldinger.", CURRENT_USER)
    # create_post("Enda en melding", CURRENT_USER)
    # create_post("Nyeste melding?", CURRENT_USER)


# Outputs actions done by the database interface to a text file
# Example: "[28/03/2023]: Initialised databases to <path to database>"
def log(status):
    with open("../db.log", "r") as f:
        old = f.read()  # Gets old contents of the file
    with open("../db.log", "w") as f:
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%d/%m/%Y %H:%M:%S")  # Formats datetime info
        f.write(f"[{current_time}]: {status}\n")
        f.write(old)  # Writes the old logs after the newest, so that the file is prepended with the new information


# Clears the log file by opening it in write mode, overwriting everything present.
def clear_log():
    with open("../db.log", "w") as f:
        pass  # Wipes the file, and then does nothing


def main():
    test_database()
    print("Code Executed Successfully")


if __name__ == "__main__":
    main()

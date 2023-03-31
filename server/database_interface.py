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
        # content: message body, i.e. "Hello everyone!"
        # poster: user ID of original poster
        # post_time: Time message was posted
        # id: message ID
        db.c.execute("""CREATE TABLE messages (
            content TEXT,
            poster INT,
            post_time TEXT,
            id INT  -- Unique message ID
        )""")
        log(f"Successfully created Message Table at {DB_PATH_ABSOLUTE}")

        db.c.execute("DROP TABLE IF EXISTS users")
        # NOTE: Will expand on this later, but just need to get the ball rolling
        db.c.execute("""CREATE TABLE users (
            user_id INT,
            username TEXT,
            password TEXT,  -- Password will be hashed in the flask app
            posted_msgs INT
        )""")
        log(f"Successfully created User Table at {DB_PATH_ABSOLUTE}")


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
    log(f"Successfully created user {id} at {DB_PATH_ABSOLUTE}")
    CURRENT_USER = id  # A Variable for testing user functions within this file


def get_user(id):
    with Connection() as db:
        db.c.execute("SELECT * FROM users WHERE user_id = ?", [id])
        user = db.c.fetchall()[0]
    return user


def create_post(content: str, user: int):
    if not CURRENT_USER:
        log(f"ERROR: Could not create message: Not Logged in")
        return False
    with Connection() as db:
        print(get_user(CURRENT_USER)[3])
        db.c.execute("UPDATE users SET posted_msgs = ? WHERE user_id = ?", [get_user(CURRENT_USER)[3] + 1, CURRENT_USER])
        print(get_user(CURRENT_USER)[3])
        id = create_id(True)
        db.c.execute("""INSERT INTO messages(
            content,
            poster,
            post_time,
            id
        ) VALUES (?, ?, ?, ?)""", [content, user, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), id])
    log(f"Successfully added message {id} to database at {DB_PATH_ABSOLUTE}")
    log(f"Successfully updated user {CURRENT_USER} at {DB_PATH_ABSOLUTE}")


def fetch_message(id):
    with Connection() as db:
        db.c.execute("SELECT * FROM messages WHERE id = ?", [id])
        message = db.c.fetchall()[0]
    return message


# Function which creates an ID for a user or a post
def create_id(*post: bool) -> int:
    if post:
        baseline = str(CURRENT_USER)
        return int(baseline) + 0
    baseline = datetime.datetime.today().strftime("%Y%m%d%f")
    hour = datetime.datetime.today().strftime("%H%M")
    ms = datetime.datetime.now().strftime("%f")
    random.seed = int(hour) * int(ms)
    randomness = str(random.randint(1000, 9999))

    return int(baseline + randomness)


# Function for testing, messing around, whatever really.
def temp():
    with Connection() as db:
        pass


# Test function for the database. You end up with a template database.
def test_database():
    init_tables()
    create_user(["Test", "password123"])
    create_post("Hello World!", CURRENT_USER)

# Outputs actions done by the database interface to a text file
# Example: "[28/03/2023]: Successfully initialised databases to <path to database>"
def log(status):
    with open("../db.log", "a") as f:
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%d/%m/%Y %H:%M:%S") # Formaterer informasjonen fra datetime
        f.write(f"[{current_time}]: {status}\n")        


def main():
    test_database()
    print(fetch_message(int(str(CURRENT_USER) + str(get_user(CURRENT_USER)[3] - 1))))
    print("Code Executed Successfully")


if __name__ == "__main__":
    main()
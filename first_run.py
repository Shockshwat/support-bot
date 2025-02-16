with open("constants.txt", "w+") as f:
    f.write(
        f"TOKEN:{input('Enter the bot token: ')}\nGENERAL_CHANNEL:{input('Enter the general channel ID: ')}\nSUPPORT_CHANNEL:{input('Enter the support channel ID: ')}\nLOGGING_CHANNEL:{input('Enter the logging channel ID: ')}\nFAQ_CHANNEL:{input('Enter the FAQ channel ID: ')}\nSTAFF_ROLE:{input('Enter the staff role ID: ')}\nSUPPORTER_ROLE:{input('Enter the supporter role ID: ')}\nDEVELOPER_ROLE:{input('Enter the developer role ID: ')}\nREPORT_CHANNEL:{input('Enter the report channel ID: ')}\nRP_LOG_CHANNEL:{input('Enter the RP log channel ID: ')}\n"
    )
import sqlite3
import os

if not os.path.exists("Data"):
    os.makedirs("Data")

# Check if the file exists, if not create it
if not os.path.isfile("Data/RP.db"):
    conn = sqlite3.connect("Data/RP.db")
    c = conn.cursor()
    c.execute(
        """
     CREATE TABLE IF NOT EXISTS RP (
         id INTEGER PRIMARY KEY,
         RP_given INTEGER DEFAULT 0,
         RP_received INTEGER DEFAULT 0
     )
 """
    )
    conn.commit()
    c.close()
    conn.close()
if not os.path.isfile("Data/warns.db"):
    conn = sqlite3.connect("Data/warns.db")
    c = conn.cursor()
    c.execute(
        """
                CREATE TABLE IF NOT EXISTS warnings (
                    username TEXT,
                    userid INTEGER,
                    warn_date TEXT,
                    reason TEXT
                )
            """
    )
    conn.commit()
    c.close()
    conn.close()

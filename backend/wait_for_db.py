import time
import psycopg2

while True:
    try:
        psycopg2.connect(
            host="db",
            dbname="creditdb",
            user="credituser",
            password="creditpass"
        )
        break
    except:
        time.sleep(1)

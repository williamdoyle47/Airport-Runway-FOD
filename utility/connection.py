import sqlite3
from datetime import date
try:
    conn = sqlite3.connect('detections.db')
    cursor = conn.cursor()

    # cursor.execute("""CREATE TABLE detections(
    #     fodType text default "placeholderType",
    #     coordinates text DEFAULT "[0,0]",
    #     date timestamp text DEFAULT null
    # ) """)

    data = cursor.execute(""" SELECT * FROM detections;""")
    data = data.fetchall()
    i = 0 
    for item in data:
        i = i+1 
        print("\n")
        print(str(i) + ". ", item)

    conn.commit()
    conn.close()

except sqlite3.Error as e:
    print(e)

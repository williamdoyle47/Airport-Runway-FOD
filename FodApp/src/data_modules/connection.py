import sqlite3
import datetime
try:
    conn = sqlite3.connect('detections.db')
    cursor = conn.cursor()

    # cursor.execute("""CREATE TABLE detections(
    #     fodType text default "placeholderType",
    #     coordinates text DEFAULT "[0,0]",
    #     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    #     confidenceScore float DEFAULT 0.6
    # ) """)

    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("screw", "44.87462654456526, -93.23352374789656", 
    #                         datetime.datetime.now(), 0.68))
    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("wrench", "44.88583814551953, -93.23506109382541", 
    #                         datetime.datetime.now(), 0.72))
    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("rubber", "44.89137135265227, -93.20909505790712", 
    #                         datetime.datetime.now(), 0.85))
    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("hammer", "44.87643483672227, -93.20789571538998", 
    #                         datetime.datetime.now(), 0.95))
    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("pliers", "44.8724721221139, -93.23791428396207", 
    #                         datetime.datetime.now(), 0.86))
    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("pliers", "44.89221842098514, -93.20940715281053", 
    #                         datetime.datetime.now(), 0.72))
    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("trash", "44.87974420507467, -93.21723957283892", 
    #                         datetime.datetime.now(), 0.99))
    # cursor.execute("INSERT INTO detections VALUES (?, ?, ?, ?)", ("rivet", "44.87909010759127, -93.21013319768998", 
    #                         datetime.datetime.now(), 0.78))

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

import pyodbc

c = pyodbc.connect(
    '''DRIVER={MySQL ODBC 8.4 Unicode Driver};
    SERVER=localhost;
    DATABASE=vaje;
    UID=pb;
    PWD=pbvaje;'''
)

cursor = c.cursor()

try:
    cursor.execute("DROP TABLE IF EXISTS gostotaPopulacije")
except pyodbc.Error as e:
    print("Napaka pri brisanju tabele gostotaPopulacije:", e)

try:
    cursor.execute("DROP TABLE IF EXISTS gostotaAlianse")
except pyodbc.Error as e:
    print("Napaka pri brisanju tabele gostotaAlianse:", e)

cursor.execute("CREATE TABLE gostotaPopulacije ("
               "id INTEGER PRIMARY KEY,"
               "gostota FLOAT"
               ")")

cursor.execute("CREATE TABLE gostotaAlianse ("
               "aliansa VARCHAR(100),"
               "gostota FLOAT"
               ")")

max_x = 400
min_x = -400
max_y = 400
min_y = -400
id = 0

for i in range(min_x, max_x, 10):
    for j in range(min_y, max_y, 10):
        x1 = i
        x2 = i + 10
        y1 = j
        y2 = j + 10
        cursor.execute("SELECT SUM(population)/100 FROM naselje WHERE x >= {} AND x < {} AND y >= {} AND y < {}"
                       .format(x1, x2, y1, y2))
        skupna_populacija = cursor.fetchone()[0]
        if skupna_populacija is None:
            skupna_populacija = 0
        cursor.execute("SELECT a.alliance, SUM(n.population)/100 AS skupna_populacija "
                       "FROM naselje n "
                       "JOIN igralec i ON n.pid = i.pid "
                       "JOIN aliansa a ON i.aid = a.aid "
                       "WHERE n.x >= {} AND n.x < {} AND n.y >= {} AND n.y < {} "
                       "GROUP BY a.alliance "
                       "ORDER BY skupna_populacija DESC "
                       "LIMIT 1".format(x1, x2, y1, y2))
        najmocnejsa_aliansa = cursor.fetchone()
        id += 1
        cursor.execute("INSERT INTO gostotaPopulacije VALUES ({}, {})".format(id, skupna_populacija))
        if najmocnejsa_aliansa:
            aliansa = najmocnejsa_aliansa[0]
            gostota = najmocnejsa_aliansa[1]
            cursor.execute("INSERT INTO gostotaAlianse VALUES ('{}', '{}')".format(aliansa, gostota))

c.commit()
c.close()

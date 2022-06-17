from MariaDBConnector import MariaDBConnector

# edit connection settings in MariaDBConnector.py
connection = MariaDBConnector().conn
cursor = connection.cursor()

replaces = ['categoriesoftests', 'caracteristicas', 'categoriesofcaracteristicas',
            'categoriesofparametres', 'configuracioofmaquinas', 'configuracioofprogramas',
            'missatgeerrors', 'missatgeinformacios', 'parametres', 'resultats', 'tags', 'tests']

cursor.execute("SELECT Id, Name FROM textreferences WHERE (lower(Name) LIKE '%dynamic.%')")
rows = cursor.fetchall()
for row in rows:
    className = row[1].split('.')[1]
    if className not in replaces:
        continue
    replaceName = className[:-1]
    newName = row[1].replace(className, replaceName)
    cursor.execute("UPDATE textreferences SET Name=? WHERE Id=?", (newName, row[0]))

connection.commit()
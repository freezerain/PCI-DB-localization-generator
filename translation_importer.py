import csv

from MariaDBConnector import MariaDBConnector

# edit connection settings in MariaDBConnector.py
connection = MariaDBConnector().conn
cursor = connection.cursor()

# should DROP current data
isDropTables = False

# language id HARDCODED!!!
with open('trans_local.csv', 'r') as local_file, \
        open('trans_web.csv', 'r') as web_file, \
        open('trans_dynamic.csv', 'r') as dynamic_file, \
        open('trans_static.csv', 'r') as static_file:
    lines_list = list(csv.DictReader(local_file))
    lines_list.extend(list(csv.DictReader(web_file)))
    lines_list.extend(list(csv.DictReader(dynamic_file)))
    lines_list.extend(list(csv.DictReader(static_file)))
    if isDropTables:
        cursor.execute("DELETE FROM textreferences; DELETE FROM textcontents;")
    for line_dict in lines_list:
        ref, name_en, name_es, cont_en, cont_es, desc_en, desc_es, tags, ref_id, \
        cont_en_id, cont_es_id = line_dict.values()

        print(ref_id)
        cursor.execute("SELECT 1 FROM textreferences WHERE Id=?",(ref_id,))
        cursor.fetchall()
        if cursor.rowcount:
            cursor.execute("UPDATE textreferences SET Name=?, Tag=? WHERE Id=?",
                           (ref, tags,ref_id,))
        else:
            cursor.execute(
                f"INSERT INTO textreferences (Name, Tag) VALUES (?, ?)", (ref, tags,))

        cursor.execute("SELECT 1 FROM textcontents WHERE Id=?", (cont_en_id,))
        cursor.fetchall()
        if cursor.rowcount:
            cursor.execute("UPDATE textcontents SET Name=?,Text=?,"
                           "Description=?, TextReferences_Id=? WHERE Id=?",
                           (name_en, cont_en, desc_en, ref_id, cont_en_id,))
        else:
            cursor.execute(
                "INSERT INTO textcontents (Name, Text, Description, Language_Id, TextReferences_Id) "
                f"VALUES (?, ?, ?,?,?)", (name_en, cont_en, desc_en, '1', ref_id,))

        cursor.execute("SELECT 1 FROM textcontents WHERE Id=?", (cont_en_id,))
        cursor.fetchall()
        if cursor.rowcount:
            cursor.execute(
                "UPDATE textcontents SET Name=?,Text=?,Description=?,TextReferences_Id=? "
                "WHERE Id=?", (name_es, cont_es, desc_es, ref_id,cont_es_id))
        else:
            cursor.execute(
                "INSERT INTO textcontents (Name, Text, Description, Language_Id, TextReferences_Id) "
                f"VALUES (?,?,?,?,?)", (name_es, cont_es, desc_es, '2', ref_id, ))
connection.commit()
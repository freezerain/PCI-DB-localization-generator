# Script to add localization strings from CSV - format-strick, rework if table columns will change
def add_to_db(connection, data):
    cursor = connection.cursor()
    # Hardcoded IDs of Languages
    english_id = 1
    spanish_id = 2

    for row in data:
        name = row["string_id"]
        english_content = row["text_english"]
        spanish_content = row["text_spanish"]

        # check if reference exist, create if not, get ID in both cases
        cursor.execute(
            "SELECT Id FROM textreferences WHERE name = ?",
            (name,))
        reference, *rest = cursor.fetchone() or (None,)
        if reference is None:
            cursor.execute(
                "INSERT INTO textreferences (name) VALUES (?)",
                (name,))
            reference = cursor.lastrowid

        # Update ENGLISH if existed, else create
        if english_content:
            cursor.execute(
                "SELECT Id FROM textcontents WHERE TextReferences_Id = ? AND Language_Id = ?",
                (reference, english_id,))
            found_english_id, *rest = cursor.fetchone() or (None,)
            if found_english_id is None:
                cursor.execute(
                    "INSERT INTO textcontents (name, text, Language_Id, TextReferences_Id) VALUES (?, ?, ?, ?)",
                    (name, english_content, english_id, reference,))
            else:
                cursor.execute(
                    "UPDATE textcontents SET text = ? WHERE Id = ?",
                    (english_content, found_english_id,))

        # Update SPANISH if existed, else create
        if spanish_content:
            cursor.execute(
                "SELECT Id FROM textcontents WHERE TextReferences_Id = ? AND Language_Id = ?",
                (reference, spanish_id,))
            found_spanish_id, *rest = cursor.fetchone() or (None,)
            if found_spanish_id is None:
                cursor.execute(
                    "INSERT INTO textcontents (name, text, Language_Id, TextReferences_Id) VALUES (?, ?, ?, ?)",
                    (name, spanish_content, spanish_id, reference,))
            else:
                cursor.execute(
                    "UPDATE textcontents SET text = ? WHERE Id = ?",
                    (spanish_content, found_spanish_id,))
    connection.commit()

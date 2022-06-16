import text_columns_loader

spanish_lang_id = 2


# Script to extract strings from the table and create reference in textreference table
def start_migration(connection):
    cursor = connection.cursor()
    text_column_dict = text_columns_loader.load_text_columns()
    # for each table that dict contains
    for table_key in text_column_dict:
        col_list = text_column_dict[table_key]
        # find primary key for REFERENCE_NAME generation (TABLE.COLUMN.ID)
        cursor.execute(f"SHOW COLUMNS FROM sensamag_sp.{table_key} WHERE `Key` = 'PRI';")
        primary_col, *rest = cursor.fetchone()
        # for each columns of table
        for col_name in col_list:
            cursor.execute(f'SELECT {primary_col},{col_name} FROM {table_key}')
            content_list = cursor.fetchall()
            # for each row of column
            for primary_key, old_content, *rest in content_list:
                # check if cell value is already in TEXTREFERENCE table
                cursor.execute('SELECT 1 FROM textreferences WHERE Name=?', (old_content,))
                if cursor.fetchone() is not None:
                    continue
                # generate reference name
                reference_name = f"{table_key}.{col_name}.{primary_key}"
                cursor.execute("INSERT INTO textreferences (Name) VALUES (?)", (reference_name,))
                # retrive primary key of newly created textreference
                new_reference_id = cursor.lastrowid
                # add old value to TEXTCONTENT table using reference
                cursor.execute(
                    "INSERT INTO textcontents (name, text, Language_Id, TextReferences_Id) VALUES (?, ?, ?, ?)",
                    (reference_name, old_content, spanish_lang_id, new_reference_id,))
                # update old value with new textreference
                cursor.execute(f"UPDATE {table_key} SET {col_name} = ? WHERE {primary_col} = ?",
                               (reference_name, primary_key,))
    connection.commit()



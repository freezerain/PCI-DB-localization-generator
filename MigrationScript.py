import csv
import ast

spanish_lang_id = 2


# Script to extract strings from the table and create reference
def start_migration(connection):
    cursor = connection.cursor()
    dict = _load_text_columns()
    for table_key in dict:
        col_list = dict[table_key]
        cursor.execute(f"SHOW COLUMNS FROM sensamag_sp.{table_key} WHERE `Key` = 'PRI';")
        primary_col, *rest = cursor.fetchone()
        for col_name in col_list:
            cursor.execute(f'SELECT {primary_col},{col_name} FROM {table_key}')
            content_list = cursor.fetchall()
            for primary_key, old_content, *rest in content_list:
                cursor.execute('SELECT 1 FROM textreferences WHERE Name=?', (old_content,))
                if cursor.fetchone() is not None:
                    continue
                reference_name = f"{table_key}.{col_name}.{primary_key}"
                cursor.execute("INSERT INTO textreferences (Name) VALUES (?)", (reference_name,))
                new_reference_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO textcontents (name, text, Language_Id, TextReferences_Id) VALUES (?, ?, ?, ?)",
                    (reference_name, old_content, spanish_lang_id, new_reference_id,))
                cursor.execute(f"UPDATE {table_key} SET {col_name} = ? WHERE {primary_col} = ?",
                               (reference_name, primary_key,))
    connection.commit()


def _load_text_columns():
    with open('text_columns.txt', newline='') as f:
        result_dict = {}
        for line in f.read().splitlines():
            split_result = line.split(":")
            result_dict[split_result[0]] = list(filter(str.strip, split_result[1].split(',')))
        blacklist = _read_blacklist()
        result_dict = dict((k, result_dict[k]) for k in result_dict if k not in blacklist)
        whitelist_dic = _read_whitelist()
        result_dict.update(whitelist_dic)
        return result_dict


def _read_blacklist():
    with open('migration_blacklist.txt') as f:
        return f.read().splitlines()


def _read_whitelist():
    with open('migration_whitelist.txt') as f:
        result_dict = {}
        for line in f.read().splitlines():
            split_result = line.split(":")
            result_dict[split_result[0]] = list(filter(str.strip, split_result[1].split(',')))
        return result_dict

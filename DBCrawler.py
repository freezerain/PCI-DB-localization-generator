import csv


def get_text_columns(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    table_list = cursor.fetchall()
    result_dict = {}
    for table_name, *rest in table_list:
        cursor.execute(
            "SHOW COLUMNS FROM {} WHERE (`Key` != 'PRI') AND "
            "(type='longtext' OR type='varchar' OR type='mediumtext'); ".format(
                "sensamag_sp." + table_name))
        column_list = [column_tuple[0] for column_tuple in cursor]
        if column_list:
            result_dict[table_name] = column_list
    if result_dict:
        _dump_data_to_file(result_dict)


def _dump_data_to_file(data):
    with open('text_columns.txt', 'w', newline='') as f:
        for data_key in data:
            row = data_key + ":"
            for col in data[data_key]:
                row += col + ","
            f.write(row + "\n")

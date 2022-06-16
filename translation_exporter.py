import csv

from MariaDBConnector import MariaDBConnector

# edit connection settings in MariaDBConnector.py
connection = MariaDBConnector().conn
cursor = connection.cursor()

cursor.execute("""select r.Name, c.Name, c.Text, l.Name, c.Description, r.Tag, r.Id, c.Id, l.Id from textcontents c
inner join textreferences r on c.TextReferences_Id = r.Id
inner join localizationlanguages l on c.Language_Id = l.Id""")

lines_dict = {}
for ref, name, cont, lang, desc, tags, ref_id, cont_id, lang_id in cursor:
    if ref not in lines_dict:
        lines_dict[ref] = {'ref': ref, 'ref_id': ref_id, 'tags': tags}
    if lang_id == 1:
        lines_dict[ref].update(
            {'name_en': name, 'cont_en': cont, 'desc_en': desc, 'cont_en_id': cont_id})
    else:
        lines_dict[ref].update(
            {'name_es': name, 'cont_es': cont, 'desc_es': desc, 'cont_es_id': cont_id})

with open('trans_local.csv', 'w', newline='') as local_file, \
        open('trans_web.csv', 'w', newline='') as web_file, \
        open('trans_dynamic.csv', 'w', newline='') as dynamic_file, \
        open('trans_static.csv', 'w', newline='') as static_file:
    fieldnames = ['ref', 'name_en', 'name_es', 'cont_en', 'cont_es', 'desc_en', 'desc_es',
                  'tags', 'ref_id', 'cont_en_id', 'cont_es_id']
    local_writer = csv.DictWriter(local_file, fieldnames=fieldnames)
    web_writer = csv.DictWriter(web_file, fieldnames=fieldnames)
    dynamic_writer = csv.DictWriter(dynamic_file, fieldnames=fieldnames)
    static_writer = csv.DictWriter(static_file, fieldnames=fieldnames)
    local_writer.writeheader()
    web_writer.writeheader()
    dynamic_writer.writeheader()
    static_writer.writeheader()

    for line_ref in lines_dict:
        current_writer = static_writer
        if line_ref.startswith('local.'):
            current_writer = local_writer
        elif line_ref.startswith('web.'):
            current_writer = web_writer
        elif line_ref.startswith('dynamic.'):
            current_writer = dynamic_writer
        row = lines_dict[line_ref]
        current_writer.writerow(row)

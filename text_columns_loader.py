# read from file finded columns of text that we want to migrate
# use whitelist.txt and blacklist.txt files to remove TABLES and add TABLES:[COLUMNS]
def load_text_columns():
    with open('text_columns.txt', newline='') as f:
        result_dict = {}
        # deserialize data
        for line in f.read().splitlines():
            split_result = line.split(":")
            result_dict[split_result[0]] = list(filter(str.strip, split_result[1].split(',')))
        blacklist = _read_blacklist()
        # remove blacklisted TABLES from data
        result_dict = dict((k, result_dict[k]) for k in result_dict if k not in blacklist)
        whitelist_dic = _read_whitelist()
        # add TABLES with COLUMNS to data (possible duplication)
        result_dict.update(whitelist_dic)
        return result_dict


def _read_blacklist():
    with open('migration_blacklist.txt') as f:
        return f.read().splitlines()


# deserialize whitelist format (same as text_columns.txt format)
def _read_whitelist():
    with open('migration_whitelist.txt') as f:
        result_dict = {}
        for line in f.read().splitlines():
            split_result = line.split(":")
            result_dict[split_result[0]] = list(filter(str.strip, split_result[1].split(',')))
        return result_dict

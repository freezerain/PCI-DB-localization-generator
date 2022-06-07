from MariaDBConnector import MariaDBConnector
import CSVReader
import AdditionScript
import MigrationScript
import DBCrawler

doAddition = False
doMigration = True
doCrawler = False
# edit connection settings in MariaDBConnector.py
connection = MariaDBConnector().conn

if doAddition:
    # Parse data from data.csv file
    csvData = CSVReader.read_data()
    # add or update localization strings from csv
    AdditionScript.add_to_db(connection, csvData)

if doCrawler:
    # write to local file all tables with text columns
    DBCrawler.get_text_columns(connection)

if doMigration:
    # migrate old strings value to reference-content tables
    MigrationScript.start_migration(connection)

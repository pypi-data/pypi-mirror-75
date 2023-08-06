from dcclab import Database
from dcclab import Metadata
from dcclab import findFiles
import os


if __name__ == '__main__':
    # Current directory is :
    print('Begining process...')
    directory = os.path.dirname(__file__)
    print('Directory is : {}'.format(directory))

    # Path to the Molecular Tools Platform database is :
    mtpPath = os.path.join(directory, 'database', 'mtp.db')
    print('Path to database "mtp.db" is : {}'.format(mtpPath))

    # We create a database object in rwc mode. If it doesn't exist, we create it.
    # Then we connect to the database.
    # Database is in asynchronous mode for faster inserts.
    print('Connecting to database...')
    if os.path.exists(mtpPath):
        print('Database already exists.')
        database = Database(mtpPath, 'rw')
        print('Dropping all existing tables...')
        database.dropTable('Data-souris')
        database.dropTable('Data-Utilisation')
        database.dropTable('cziMetadata')
        database.dropTable('cziChannels')
        database.commit()
        print('Done.')
    else:
        print("Database doesn't exist yet. Creating it...")
        database = Database(mtpPath, 'rwc')
        print('Done.')

    print('Connecting to database...')
    database.connect()
    database.asynchronous()
    print('...Connected!')

    # Now, we need paths to our metadata (the .czi files and the .csv files.)
    # For the .csv, we have :
    micePath = os.path.join(directory, 'database', 'Data-souris.csv')
    utilPath = os.path.join(directory, 'database', 'Data-Utilisation.csv')
    print('Path to mice data is : {}'.format(micePath))
    print('Path to util data is : {}'.format(utilPath))

    # For the .czi, we have :
    print('Finding czi files in POM...')
    files = findFiles(os.path.join(directory, 'POM', 'injection AAV', 'résultats bruts', 'AAV'), '*.czi') + \
            findFiles(os.path.join(directory, 'POM', 'injection AAV', 'résultats bruts', 'RABV'), '*.czi')
    print('{} czi files were found!'.format(len(files)))

    # Now, we extract the metadata from our files. First, we start with the .csv files.
    # We extract the metadata.
    print('Extracting metadata from .csv files...')
    miceMetadata = Metadata(micePath)
    utilMetadata = Metadata(utilPath)
    print('...Done!')

    # We create tables for the metadata.
    print('Creating tables for the .csv metadata...')
    database.begin()
    database.createTable(miceMetadata.keys)
    database.createTable(utilMetadata.keys)
    database.commit()
    print('...Done!')

    # We insert the .csv Metadata into the tables.
    print('Inserting metadata into the database...')
    entries = miceMetadata.metadata
    database.begin()
    for line in entries.keys():
        database.insert('Data-souris', entries[line])
    database.commit()
    print('Data-souris was processed for {} lines...'.format(len(entries)))

    entries = utilMetadata.metadata
    database.begin()
    for line in entries.keys():
        database.insert('Data-Utilisation', entries[line])
    database.commit()
    print('Data-Utilisation was processed for {} lines...'.format(len(entries)))

    # We now process the czi files into the database.
    # We create the tables.
    database.begin()
    print('Creating the tables into the database...')
    cziMetadata = Metadata(files[0])
    database.createTable(cziMetadata.keys)
    print('Tables were created, processing the files...')
    database.commit()

    database.begin()
    for file in files:
        print('Processing {}...'.format(file))
        cziMetadata = Metadata(file)
        database.insert('cziMetadata', cziMetadata.metadata)
        for channelId in cziMetadata.channels.keys():
            database.insert('cziChannels', cziMetadata.channels[channelId])
    database.commit()
    print('{} czi files were processed!'.format(len(files)))
    print('Disconnecting from database...')
    database.disconnect()
    print('Done! Database was successfully created.')

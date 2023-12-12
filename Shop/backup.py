import os
import sys
import pwd
from tqdm import tqdm
from datetime import datetime

FILENAME = f'backup_{datetime.now().replace(microsecond=0).isoformat().replace(":", "-")}' + \
    f'_{pwd.getpwuid(os.getuid())[0]}.tar.gz'
DATA_FILENAME = f'data_{datetime.now().replace(microsecond=0).isoformat().replace(":", "-")}' + \
    f'_{pwd.getpwuid(os.getuid())[0]}.tar.gz'

def create_tar(filename, directories, change_dir=False):
    print('Creating tar archive...')
    if change_dir:
        os.system(
            f'sudo tar -C {change_dir} -czf {filename} {" ".join(directories)}')
    else:
        os.system(f'sudo tar czf {filename} {" ".join(directories)}')

def extract_tar(filename):
    print('Extracting tar archive...')
    os.system(f'sudo tar xzfp {filename}')

def extract_data_backup(filename):
    print('Deleting results directory...')
    os.system('sudo rm -rf ../results/')
    extract_tar(filename)
    os.system('sudo mv results ../')

def extract_website_backup(filename):
    print('Deleting src, database and db_dump directories...')
    os.system('sudo rm -rf src database db_dump')
    extract_tar(filename)


def download_website_backup():
    print('Checking if MariaDB container is running...')
    if os.system('sudo docker ps | grep mariadb') != 0:
        print('MariaDB container is not running.')
        print('run docker compose up -d')
        sys.exit(1)

    os.system('sudo chmod -R 777 src db_dump')
    os.system(
        'docker exec mariadb mysqldump --user=root --password=admin prestashop > db_dump/db.sql')
    create_tar(FILENAME, ['src', 'db_dump'])
    option = input('Delete created archive? (y/n): ')
    if option == 'y':
        os.system(f'sudo rm -rf {FILENAME}')


def download_data_backup():
    create_tar(DATA_FILENAME, ['results'], change_dir='../')
    option = input('Delete created archive? (y/n): ')
    if option == 'y':
        os.system(f'sudo rm -rf {DATA_FILENAME}')


def display_available_backups(prefix):
    print('Available backups:')
    # Display available backups with numeration
    backups = os.listdir()
    backups = [b for b in backups if b.startswith(prefix) and b.endswith('.tar.gz')]
    for i, b in enumerate(backups):
        print(f'{i+1}. {b}')

    return backups


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid number of arguments.')
        print('Usage: python3 backup.py extract|download')
        sys.exit(1)

    OPERATION = sys.argv[1]

    if OPERATION == 'extract':
        # Choose to extract db or data
        option = input('Extract database or data? (db/dataa): ')
        if option == 'db':
            # Extract database
            backups = display_available_backups('backup')
            option = int(input('Choose backup to extract: '))
            FILENAME = backups[option-1]
            extract_website_backup(FILENAME)
        elif option == 'data':
            # Extract data
            backups = display_available_backups('data')
            option = int(input('Choose backup to extract: '))
            DATA_FILENAME = backups[option-1]
            extract_data_backup(DATA_FILENAME)
        else:
            print('Invalid option. Please specify either db or data.')
    elif OPERATION == 'download':
        # Choose to download db or images
        option = input('Download database or data? (db/data): ')

        if option == 'db':
            # Download database
            download_website_backup()
        elif option == 'data':
            # Download images
            download_data_backup()
        else:
            print('Invalid option. Please specify either db or data.')
    else:
        print('Invalid operation. Please specify either db or data.')

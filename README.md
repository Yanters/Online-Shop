# Prestashop

## Technologies
- Docker
- Prestashop 1.7.8-apache
- MariaDB
- Python
- Scrapy
- Selenium

## Intallation
1. Clone repository
    ```
    git clone https://github.com/Yanters/Online-Shop.git
    ```
2. Change directory
    ```
    cd Shop/ssl
    ```
3. Set up ssl certificate
    ```
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout prestashop.key -out prestashop.crt -subj "/C=PL/ST=Pomorskie/L=Gdansk/O=Kule Hermiony/OU=Kule Hermiony/CN=localhost"
    ```
4. Change directory
    ```
    cd ../..
    ```
5. Create venv
    ```
    python3 -m venv .venv
    ```
6. Activate venv
    ```
    source .venv/bin/activate
    ```
7. Install required packages
    ```
    pip install -r requirements.txt
    ```
8. Change directory
    ```
    cd Shop
    ```

### Without backup
1. Open docker-desktop
2. Initialize docker
    ```
    docker-compose up -d
    ```
3. Go to localhost
4. Install prestashop.
5. Some important configurations
    - nothing marked in SSL configuration
    - Database IP = mariadb
    - Database Password = admin
6. Wait until installation finish
7. Change folder
    ```
    cd src
    ```
8. Remove directory
    ```
    sudo rm -rf install
    ```
9. Rename directory
    ```
    sudo mv admin adminpanel
    ```
10. Create .htaccess
    ```
    sudo touch .htaccess
    sudo chmod 666 .htaccess
    ```
11. Go to localhost:8080/adminpanel
12. Log in

#### SSL configuration
1. In adminpanel go to
    ```
    Preferences -> Moves
    ```
2. Shop domain
    ```
    localhost:8080
    ```
3. SSL domain
    ```
    localhost
    ```
4. Base URL
    ```
    /
    ```
5. Save
6. Go to
    ```
    Preferences -> General
    ```
7. Enable SSL
8. Save
9. Enable SSL on every websides
10. Save

### With backup
1. Download backup:
    ```
    https://1drv.ms/f/s!AlP7iQP3xk8kvh-mrp2Tb5aBAIDu?e=eVLay2
    ```
2. Insert backups into /Shop directory
3. Extract backups
    ```
    python backup.py extract
    ```
    db - shop configuration,
    data - products and categories (/results)

## API
1. Go to 
    ```
    Advanced -> Webservice
    ```
2. Enable API PrestaShop
3. Enable CGI for PHP
4. Save
5. Generate key
    - Key = JKCTYYE6FNEQRR3R3NFHM63VZ8FBPS72
6. Select all permissions
7. Save
8. Go to
    ```
    Preferences -> Moves
    ```
9. Disable friendly URL adress

### Insert data using API
1. Change directory
    ```
    cd api
    ```
2. Start script
    ```
    python main.py
    ```

## Scrap data
1. Change directory
    ```
    cd scraper
    ```
2. Start scrap
    ```
    scrapy crawl category
    scrapy crawl balls
    ```
3. Results will be saved in /result directory

## Authors
- Konrad Nowicki 188671
- Przemysław Szumczyk 188956
- Nikodem Keller 184853
- Artur Śpiewak 188663


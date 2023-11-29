#Kopiowanie Certyfikatów SSL do Kontenera Dockerowego
docker cp ./certs/private.key prestashop:/etc/ssl/private/private.key
docker cp ./certs/certificate.crt prestashop:/etc/ssl/certs/certificate.crt


#Aktualizacja Konfiguracji Wirtualnego Hosta Apache
docker exec -it prestashop rm -rf /etc/apache2/sites-available/000-default.conf
docker cp database/ssl/000-default.conf prestashop:/etc/apache2/sites-available/000-default.conf


docker exec -it prestashop mysql -u root -padmin -D prestashop -h mariadb -e "UPDATE ps_shop_url SET domain='localhost', domain_ssl='mariadb' WHERE id_shop_url=1;"
docker exec -it prestashop mysql -u root -padmin -D prestashop -h mariadb -e "UPDATE ps_homeslider_slides_lang SET url=REPLACE(url, 'localhost', 'mariadb');"
docker exec -it prestashop mysql -u root -padmin -D prestashop -h mariadb -e "UPDATE ps_configuration_lang SET value=REPLACE(value, 'localhost', 'mariadb') WHERE id_configuration=434;"


docker exec -it prestashop a2enmod ssl
docker exec -it prestashop service apache2 restart

docker-compose up -d




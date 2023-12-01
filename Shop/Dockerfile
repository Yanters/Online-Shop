FROM prestashop/prestashop:1.7.8-apache

COPY ./ssl/prestashop.crt /etc/ssl/certs/prestashop.crt
COPY ./ssl/prestashop.crt /usr/local/share/ca-certificates/prestashop.crt
COPY ./ssl/prestashop.key /etc/ssl/private/prestashop.key
COPY ./ssl/prestashop-ssl.conf /etc/apache2/sites-available/prestashop-ssl.conf

RUN update-ca-certificates && a2enmod ssl && a2ensite prestashop-ssl
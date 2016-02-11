FROM mysql:5.7.10
EXPOSE "3306"
ADD *.sql /docker-entrypoint-initdb.d/
ENV MYSQL_ROOT_PASSWORD=password MYSQL_DATABASE=reporting MYSQL_USER=reporter MYSQL_PASSWORD=gener@te
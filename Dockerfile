FROM mysql:5.7.15

MAINTAINER me

ENV MYSQL_DATABASE=<schema_name> \
    MYSQL_ROOT_PASSWORD=<password>

ADD db.sql /docker-entrypoint-initdb.d

EXPOSE 3306
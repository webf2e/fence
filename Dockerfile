FROM python:3.6.5-alpine
MAINTAINER liuwenbin
LABEL version=1.0 \
descript="image only for fence project" \
dependence="mysql, docker run -p 3306:3306 --name mysql -v /path:/etc/mysql/conf.d -v /path:/logs -v /path:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d --restart=always mysql:5.6" \
run="docker run -d --name house -p port:8022 --link mongodb_contain_name:mongo -v /path:/proj/python/house/log -v /path:/proj/python/house/data -v /path:/proj/python/house/static/houseimg -v /data/mongodb:/data/mongodb --restart=always house"
RUN echo "http://mirrors.aliyun.com/alpine/v3.4/main/" > /etc/apk/repositories \
    && apk --no-cache add tzdata zeromq \
    && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone \
    && pip3 install flask flask_apscheduler python-dateutil mysql-connector requests

ADD fence.tar /proj/python/
WORKDIR /proj/python/fence
ENTRYPOINT sh run.sh

EXPOSE 8020

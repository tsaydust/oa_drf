FROM nginx:1.25.5

# 将当前项目代码拷贝到/www下
COPY . /www/

RUN mkdir -p /data/sock

WORKDIR /www

# 以下的cp命令是在容器中运行的
RUN cp /www/nginx_oa.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# 容器中的主要运行的进程，必须以非守护进程运行，否则容器启动后就会立马停掉
ENTRYPOINT nginx -g "daemon off;"
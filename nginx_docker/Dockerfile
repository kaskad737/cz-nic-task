FROM ubuntu:latest

RUN apt-get update && apt-get install -y nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY site.conf /etc/nginx/sites-available/site.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

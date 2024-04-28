#stop container
docker stop gunicorn_container
#remove container
docker container rm gunicorn_container
#remove image
docker rmi gunicorn_image
#create new image
docker build -t gunicorn_image -f Dockerfile .
#running container
docker run -d --name gunicorn_container -p 8000:8000 gunicorn_image

echo "============= Gunicorn successfull=================="






#stop container
docker stop nginx_container
#remove container
docker container rm nginx_container
#remove image
docker rmi nginx_image
#create new image
docker build -t nginx_image -f Dockerfile.nginx .
#running container
udo docker run -d --name nginx_container -p 4000:80 --link gunicorn_container:django-server nginx_image


echo "============= Nginx successfull=================="

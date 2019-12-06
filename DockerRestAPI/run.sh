sudo docker rm $(sudo docker ps -a -q)
sudo docker system prune -f
sudo docker-compose build
sudo docker-compose up


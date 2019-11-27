sudo docker rm $(sudo docker ps -a -q)
sudo docker-compose build
sudo docker-compose up
#sudo docker run -d -p 5000:5000 flask-sample-one
#sudo docker logs -f $(sudo docker ps -q) #if you want to look at logs
#sudo docker exec -it $(sudo docker ps -q) nosetests
#sudo docker exec -it $(sudo docker ps -q) nosetests --exe #if the tests are not runnign for some reason

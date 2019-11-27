sudo docker stop $(sudo docker ps -aq) #stops and removes all contianers then clans up cache
sudo docker rm $(sudo docker ps -aq)
sudo apt-get autoclean

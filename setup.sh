# reroute traffic from port 80 to 8080
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080 

# install all dependencies
sudo apt-get install -y python-pip python-numpy python-scipy python-setuptools
sudo pip install -r requirements.txt 

# install mongo
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start

# add data into mongo
mongoimport --db hillary --collection emails --type csv --headerline --file ./emails/Emails.csv

# run the AI scripts
python clustering.py
python classification.py

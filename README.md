setup minikube, kubectl,...

minikube start

build docker and push image to dockerhub then deploy k8s
cd src/auth/manifests --> kubectl apply -f ./
cd src/rabbit/manifests --> kubectl apply -f ./
cd src/gateway/manifests --> kubectl apply -f ./
cd src/converter/manifests --> kubectl apply -f ./


host.minikube.internal --> ket noi toi may host


de ket noi toi mysql

--> sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
update bellow
[mysqld]
bind-address = 0.0.0.0
--> sudo systemctl restart mysql
sudo ufw allow 3306
check permission mysql current username
--> SELECT Host, User FROM mysql.user WHERE User = 'root';
if Host=local --> 
UPDATE mysql.user SET Host = '%' WHERE User = 'root';
sudo systemctl restart mysql



install mongodb for host machine

sudo nano /etc/mongod.conf
--> update bindIp: 0.0.0.0
sudo systemctl restart mongod
sudo ufw allow 27017



setup /etc/host add lines:
192.168.49.2 mp3converter.com
192.168.49.2 rabbitmq-manager.com

--> with 192.168.49.2 is ip of minukube (get by command: minukube ip)


go to rabbitmq-manager.com --> login guest/guest
create queue: video, mp3 in console (or create by python code)




Important note:
Neu tao ra rabbitmq connection sau 1 khoang thoi gian ma khong lam gi --> no se auto dong connection
Do do moi khi can publish message toi rabbitmq thi moi nen tao connection


Test:
curl -X POST http://mp3converter.com/login -u khanhnd.uet@gmail.com:Admin123
--> output token

curl -X POST -F 'file=@./videoplayback.mp4' -H 'Authorization: Bearer token' http://mp3converter.com/upload
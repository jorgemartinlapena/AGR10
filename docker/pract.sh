sudo lxc init ubuntu:20.04 $1
sudo lxc start $1
echo git
lxc exec $1 -- git clone "https://github.com/gisai/SSR-master-server"
echo cd
lxc exec $1 -- /bin/bash -c "cd SSR-master-server"
echo update
lxc exec $1 -- apt-get -y update
echo installnodejs
lxc exec $1 -- apt-get install -y nodejs
echo npm
lxc exec $1 -- apt-get -y install npm
echo install
lxc exec $1 -- npm install 
lxc exec $1 -- npm install http-errors
lxc exec $1 -- npm install express
lxc exec $1 -- ip a
echo start
lxc exec $1 -- node SSR-master-server/app.js

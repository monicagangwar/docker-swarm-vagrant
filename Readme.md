# Docker Swarm  
Sample 3 node Vagrant setup for getting started with Docker swarm   


![ezgif-1-66e3c945a9](https://cloud.githubusercontent.com/assets/8946358/23815796/b0fb5c62-060f-11e7-8375-c7352eb327b6.gif)  

> **watch whole demo [here](https://vimeo.com/207867476)**

## Installation
Install Vagrant Binary from [here](https://www.vagrantup.com/downloads.html)  
Download ubuntu/trusty64 box from vagrant using the command `vagrant box add ubuntu/trusty64`  
Clone this repo  
```  
git clone https://github.com/monicagangwar/docker-swarm-vagrant.git  
cd docker-swarm-vagrant  
```

## Initialize VMs  
Run `vagrant up`  
  - This will set up 3 VMs - **manager**, **worker-1** & **worker-2** all provisioned with docker  
  - manager node also has Flask app image [monicagangwar/docker-swarm-vagrant](https://hub.docker.com/r/monicagangwar/docker-swarm-vagrant/) installed on it.  
    Which can be run as `docker run -p 8000:8000 --name dsv monicagangwar/docker-swarm-vagrant`  

To ssh into the manager node run `vagrant ssh manager`  
To ssh into worker node run `vagrant ssh worker-1` or `vagrant ssh worker-2`  

## Initialize Swarm manager  
- ssh into manager node  
- run `docker swarm init --advertise-addr <manager-IP-address>:2377`  
    IP address is of the Manager Virtual Machine. Can be found / setup in [Vagrantfile](Vagrantfile)  
    Port 2377 is default for swarm  
    This will generate a command with a token value 
    `docker swarm join --token <token> <manager-IP-address>:2377`  
- ssh into the worker nodes and execute the command generated above  
- run `docker node ls` on the manager node to see the list of nodes and their roles(worker/manager)  
- run `docker network create -d overlay <network-name>`  
    creates an overlay network with the name specified which each of the container can join  
    random-network will be the overlay network that our application containers live on  
    `-d` tells which driver to use. Currently overlay driver is being used  
- run `docker service create --name <service-name> --network <network-name> <image-name>`  
    Creates the service with the given service name on the network specified. This will basically run containers from the image name specified on the nodes connected to the swarm.

## Scale up and down  

- Scale up : `docker service update --replicas 7 <service-name>`    
   Replicates the container 7 times and balances into all available nodes based on a round-robin or any such algorithms. This will launch arbitrary number of containers in each node (including manager)  
   Check which container is running on which node by running `docker service ps <service-name>`  
   Check how many containers are running on the current node by running `docker ps or docker container ls`

- Scale down : `docker service update --replicas 4 <service-name>`
  This command will destroy some of the containers on some of the nodes. Check which containers got destroyed by using the commands specified above.  


## Manage worker nodes  
- Drain : Bring a node down for management purpose  
  `docker node update --availability drain <worker-node-id>`  
  <worker-node-id> can be found by running `docker node ls`  
  This will destroy the containers on the specified worker node and will relaunch them on available nodes  

- Active : Bring up a node drained for management purpose  
  `docker node update --availability active <worker-node-id>`  
  This will activate the drained node and will deploy further scaled up containers on this as well  

## Helper commands  
- `docker service ls`  
   Lists the services created
- `docker network ls`  
   Lists the networks created and available by default  
- `docker node ls`  
   Lists all the nodes in swarm
- `docker service ps <service-name>`  
   Lists all the containers running in all swarm nodes.



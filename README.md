# Personal Expense Tracker Application

### 🚧 Still Under Construction

- Setting up application environment
  - [X] Linux - Bullseye - 5GB RAM - i5 7th Gen
  - [X] Python 3.10.6
  - [X] Flask
  - [X] [Docker & Docker-Compose](#docker)
  - [X] [Kubernetes \[Kubectl & Minikube\]](#kubernetes)
  - [X] [Empathy Map](#empathy-map)
  - [X] [Literature Survey](project-design-&-planning/ideation-phase/literature_survey.pdf)

- Implementing Web Application

- Integrating SendGrid Service

- Deployment of App in IBM Cloud

## Empathy Map

![empathy_map.png](project-design-&-planning/ideation-phase/empathy_map.png)

## Site Map

```
1. index
2. login
3. dashboard
4. logout
5. pricing
6. customers
```

## Docker

<img src="_resources/629c20b332a090d680dface57413914f.png" width=125 alt="Docker LOGO">  
Docker is a virtualization environment which is used to run multiple OS embarked inside a single hardware processor. Docker virtualize OS rather than virtualization hardware like in VM/HyperVisor. These dockers are structurally similar to VM/HyperVisor but unlike it, dockers are fast, lightweight, sandbox and easy to deploy. Docker engines uses small functional units called containers which are simply micro-computers, they have their own memory, network & dependencies. These micro-computers can be as powerful as you want it to be. So, How does these stuff work so fast?? and be light-weight?? Here is the catch... These are purely OS based which means, a Linux kernel based docker can only create and use a Linux based container.. they cant support any other OS, but recently an year ago Microsoft came up with WSL as a solution to this problem.

![Differences between a VM and Docker](_resources/123213123131.png)  

- installing docker  

  `apt install docker.io`

### Creating and Working with Docker

1. Choose an OS to work with. (Lets choose CentOS).
2. Download the image of the specific OS using docker.
3. Create a container with the required parameters.

```sh
# Ubuntu has been chosen
docker pull ubuntu # Downloading Image
docker run -d -t --name "dockos" ubuntu
# Docker container can be used right after creation or even a while after creation.
# -d => Detach after creation
# -t => TTY shell.
docker ps #To manage process status docker containers
docker exec -i -t dockos bash # bash is mentioned as the command to execute
# -i => Interactive shell.
docker info dockos #to view all information of a given docker
# To create a mysql server
docker run -i -d --name dockdb -e MYSQL_ROOT_PASSWORD="" mysql
# Setting up a password is necessary for mysql container to work.
```

#### Docker-file Attributes

```
FROM <IMAGE>
ADD <SRC> <DEST>
COPY <SRC> <DEST>
WORKDIR <MNT DIR>
RUN <during BUILD>
CMD ["sh","ls"]
ENV <VAR> <VALUE>
```

To save myself from wasting time by fondling with these codes, we wrote a script to fasten things up, which can create and destroy images & containers. Seems like there is a way to create multiple containers simultaneously using [docker-compose](https://docs.docker.com/compose/compose-file/).

Voila, docker YAML was a success..., Moving on to Kubernetes -->

## Kubernetes

<img src="_resources/7049552d12ea67dbb20aac93edef6e62.png" width=90px>
Kubernetes, also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications. Docker and Kubernetes go hand in hand with each other as one of its worker modules. 
Things got a little weird when we couldn't access our deployment or pods from our machine, turns out all these are under private IP address and unlike docker they are not exposed automatically and it should be manually exposed by a Kubernetes service. These Kubernetes services are crucial in deployment as they get to tell the nature of orchestration of pods/deployments and expose applications.

### Hierarchy of Kubernetes

```mermaid
graph TD
Deployment --> Pod --> Node
````

### Types of Kubernetes services

- ClusterIP - Default service for communication between Kube API and clusters.
- LoadBalancer -  This type of service helps us to expose the service by using the cloud provider or to load balance a server with multiple or single replica(s).
- NodePort - This type of service helps us to expose the service through the static port with multiple or single replica(s).
- ExtrenalName: This type of service helps us to expose or map the service by using a predefined name ‘externalName’ filed.

![Docker Services](_resources/a7d5cce1b78152b1a5bdf50cf7132c7b.png)

#### This is our interpretation of using 3 pods with single node in Kubernetes.

![Kubernetes using docker](_resources/kubernetes.png)

According to the above figure the, these 3 pods have different IP addresses and their respective open ports.

For example, Network Address = 10.18.7.0, CIDR = 24
 Node A - 10.18.7.1 
 Node B - 10.18.7.2
 Node C - 10.18.7.3

#### This is our interpretation of using 1 pods with single node in Kubernetes.

- installing minikube

```sh
curl -LO "https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb"
```

- installing kubectl

```sh
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

#### Commands

```sh
minikube start --force
kube cluster-info
kube get|describe|delete pods|service|deployment
kube create
kube run 
kube expose
kube edit
```

#### Constrains when trying to implement Kubernetes with docker

![](_resources/da5c27c86414e36e2d458ce06e5ee35c.png)  

![](_resources/84f09c153e9b92b9124ed1fb21c55cee.png)  

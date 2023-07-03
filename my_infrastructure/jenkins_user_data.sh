#!/bin/bash
# Install Docker
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
echo "Docker installed"

# Install Java
sudo apt-get install -y openjdk-11-jre-headless
echo "Java installed"

# Install Python and pip
sudo apt-get install -y python3 python3-pip
echo "Python and pip installed"

# Install jenkinsapi library
sudo pip3 install jenkinsapi
echo "jenkinsapi library installed"

# Pull Jenkins Image
sudo docker pull jenkins/jenkins:lts
echo "Jenkins pulled"

# # Create Jenkins Volume
# sudo docker volume create jenkins_data
# echo "Volume created"

# Run Jenkins within a Docker container
jenkins_container_id=$(sudo docker run -d -p 8080:8080 -p 50005:50000 --name My-Jenkins)
echo $jenkins_container_id 
echo "Jenkins container installed"

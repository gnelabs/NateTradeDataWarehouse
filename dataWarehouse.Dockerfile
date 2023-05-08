######################################################
# Data Warehouse Dockerfile.
#
# Uses a custom Ubuntu image with manually installed
# python as to accomodate cPython libraries.
#
# This image is configured for use in AWS EC2 or Fargate
# containers. Can be used standalone with login support.
#
######################################################

FROM ubuntu:18.04

#Software-properties-common needed to add repos.
RUN apt-get update
RUN apt-get -y install software-properties-common
RUN apt-get -y install pkg-config
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update

#Install timezone data for python3.9's timezone libraries.
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

#Install python3.9. This sets python3 to 3.9 instead of the default 3.6.
RUN apt-get -y install python3.9
RUN apt-get -y install python3-pip
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2
RUN update-alternatives --config python3

#Python devtools needed to use cPython libraries.
RUN apt-get -y install python3.9-dev
RUN apt-get -y install python3.9-distutils

#Set run-as user from root to created user for future commands.
RUN useradd -ms /bin/bash ec2-user
USER ec2-user

#Copy code over.
COPY . /DataWarehouse
WORKDIR /DataWarehouse

#Install python libraries.
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN pip3 install -r dw/requirements.txt

#Do Something. Run a daemon? Up to you.
#CMD ~/.local/bin/something
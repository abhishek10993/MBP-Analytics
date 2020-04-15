#!/bin/sh

#########################################################################################################################
# This install script provides a fully automated installation of the MBP Analytics server.                              #
# It requires systemd as the running init system.                                                                       #
# It installs Java, Python, Spark and Python Flask to run the server.                                                   #
# Moreover it installs git and maven to build the necessary files.                                                      #
#########################################################################################################################


#Installing Java8
echo "\nInstalling Java...\n"
sudo apt-get install -qy openjdk-8-jdk;

echo "\nInstalling Python\n"
#Install Python
sudo apt-get install -qy python3;

echo "\nDownloading Apache Spark\n"
#Download Spark
wget https://downloads.apache.org/spark/spark-3.0.0-preview2/spark-3.0.0-preview2-bin-hadoop2.7.tgz;

# Setup SPARK
sudo mkdir spark;
sudo tar -C spark -xvf spark-3.0.0-preview2-bin-hadoop2.7.tgz;
export SPARK_HOME="$PWD/spark/spark-3.0.0-preview2-bin-hadoop2.7";
wget https://github.com/jpmml/jpmml-sparkml/releases/download/1.6.0/jpmml-sparkml-executable-1.6.0.jar
cp jpmml-sparkml-executable-1.6.0.jar spark/spark-3.0.0-preview2-bin-hadoop2.7/jars/

# Install other packages
sudo apt-get install bash;
sudo apt-get install python3-pip;
pip install pipenv;
pipenv install

#Run the server
bash run_analytics_server.sh

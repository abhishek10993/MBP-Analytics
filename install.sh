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
mkdir spark;
tar -C spark -xvf spark-3.0.0-preview2-bin-hadoop2.7.tgz;
export SPARK_HOME="$PWD/spark/spark-3.0.0-preview2-bin-hadoop2.7";
echo $SPARK_HOME;
wget https://github.com/jpmml/jpmml-sparkml/releases/download/1.6.0/jpmml-sparkml-executable-1.6.0.jar
cp jpmml-sparkml-executable-1.6.0.jar spark/spark-3.0.0-preview2-bin-hadoop2.7/jars/

# Install other packages
sudo apt-get install bash;
sudo apt-get install python3-pip;
sudo -H pip3 install -U pipenv;
sudo pip3 install git+https://github.com/jpmml/pyspark2pmml.git;
sudo pip3 install flask;
sudo pip3 install pandas;
sudo pip3 install numpy;
sudo pip3 install findspark;
sudo pip3 install pyspark;
sudo pip3 install requests;
sudo pip3 install pypmml;
sudo pip3 install scikit-learn;
sudo pip3 install scikit-multiflow;
sudo pip3 install sklearn2pmml;
sudo pip3 install sklearn-pandas;
sudo pip3 install flask-cors;

#Run the server
bash run_analytics_server.sh

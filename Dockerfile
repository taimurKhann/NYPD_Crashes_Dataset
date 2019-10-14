FROM ubuntu

RUN mkdir -p /home/CreditShelf
WORKDIR /home/CreditShelf
COPY . .

RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y nginx
RUN apt-get install -y python-pip
RUN pip install pandas
RUN pip install pymongo
RUN apt-get install -y mongodb
RUN pip install folium
RUN pip install sodapy

RUN service mongodb start

RUN mkdir -p /data/db

CMD ["service","nginx","start"]


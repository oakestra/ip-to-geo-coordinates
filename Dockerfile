FROM python:3.8.5-slim-buster
LABEL org.opencontainers.image.source https://github.com/oakestra/ip-to-geo-coordinates

RUN mkdir /app

#download geolitedb
ADD https://github.com/sapics/ip-location-db/raw/master/geolite2-city/geolite2-city-ipv4.csv.gz /app/db/
RUN gunzip /app/db/geolite2-city-ipv4.csv.gz
ENV GEOLITE_CSV_LOCATION='/app/db/geolite2-city-ipv4.csv'
ENV GEOLITE_CSV_COLUMNS='ip_range_start,ip_range_end,country_code,state1,state2,city,postcode,latitude,longitude,timezone'

ADD requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

ADD . /app

ENV FLASK_ENV=development
# TRUE for verbose logging
ENV FLASK_DEBUG=TRUE
ENV LOGLEVEL=DEBUG

ENV MY_PORT=10007
EXPOSE 10007

CMD flask run --host=0.0.0.0 --port=10007

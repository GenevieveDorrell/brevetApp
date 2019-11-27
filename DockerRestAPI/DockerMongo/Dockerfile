FROM python:3-onbuild
MAINTAINER Genevieve Dorrell "noemail@website.domain"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
# Copying source in current directory into the image
# python:3-onbuild expects the source in /usr/src/app
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
# Commands in a list
CMD ["python", "app.py"] 

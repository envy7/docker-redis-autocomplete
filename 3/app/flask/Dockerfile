# Using python 3.8 image
FROM python:3.8-buster

# Copy the dependency file seperately to make use of docker cache
COPY requirements.txt /tmp/

# Install the dependencies
RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser

RUN mkdir /home/appuser/app

USER appuser

ADD . /home/appuser/app

WORKDIR /home/appuser/app

ENTRYPOINT ["uwsgi"]

CMD ["app.ini"]

# Set the working directory to /app
#WORKDIR /app

# Copy the current directory contents into the container at /app 
#ADD . /app

# Install the dependencies
#RUN pip install -r requirements.txt

# run the command to start uWSGI
#CMD ["uwsgi", "app.ini"]

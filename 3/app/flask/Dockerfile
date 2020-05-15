# Using python 3.8 image
FROM python:3.8-buster

# Copy the dependency file seperately to make use of docker cache
COPY requirements.txt /tmp/

# Install the dependencies
RUN pip install -r /tmp/requirements.txt

# Create non root user
RUN useradd --create-home appuser

# Create home directory for non root user
RUN mkdir /home/appuser/app

# Switch to non root user
USER appuser

# Copy application code
ADD . /home/appuser/app

# Switch working directory
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

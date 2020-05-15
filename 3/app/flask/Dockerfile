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

# Use uswsgi entrypoing to start the application
ENTRYPOINT ["uwsgi"]

# Use the uwsgi configuration
CMD ["app.ini"]
# Use the Nginx image
FROM nginx

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Replace with our own nginx.conf
COPY upstream-flask.conf /etc/nginx/conf.d/

# Create ssl cert directory
RUN mkdir /etc/nginx/ssl/

# Copy cert and key to ssl directoy
ADD ssl /etc/nginx/ssl/

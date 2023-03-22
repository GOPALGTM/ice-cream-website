# Pull base image
FROM python:3.10.6
RUN pip install --upgrade pip
RUN pip install django
# Set work directory
WORKDIR /

# Install dependencies
ADD . .
EXPOSE 8000 

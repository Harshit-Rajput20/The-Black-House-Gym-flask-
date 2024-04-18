# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements file first to leverage Docker cache
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY ./app /app
# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Add wait-for-it.sh script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Run app.py only after the database is ready
CMD ["wait-for-it.sh", "db:3306", "--", "python", "main.py"]


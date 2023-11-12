# Use the official Jupyter base image jupyter/datascience-notebook:latest
FROM jupyter/base-notebook 

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local directory to /app in the container
#COPY . /app

# Copy the updated requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Copy the .env file into the container
#COPY .env /app/.env

# Set a volume for the working directory
VOLUME /app

# Install any additional dependencies (if needed)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install the Neo4j Python driver
RUN pip install --no-cache-dir neo4j==4.0.0

# Expose the port on which Jupyter will run
EXPOSE 8888

# Start Jupyter notebook
CMD ["jupyter", "notebook", "--port=8888","--ip=0.0.0.0", "--no-browser", "--allow-root"]


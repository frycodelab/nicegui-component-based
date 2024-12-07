docker save -o <path for generated tar file> <image name>
docker load -i <path to image tar file>

docker save -o /home/matrix/matrix-data.tar matrix-data
docker load -i <path to copied image file>

#Build
# Use the official NiceGUI image as the base image
FROM zauberzeug/nicegui:latest

# Set working directory
WORKDIR /app

# Copy the application code to the container
COPY ./app /app

# Expose the port your NiceGUI app runs on (default is 8080)
EXPOSE 8080

# Set the default command to run the NiceGUI app
CMD ["python", "main.py"]

docker build -t custom-nicegui .
docker run -d --name nicegui_app -p 8080:8080 -v $(pwd)/app:/app custom-nicegui

#Compose
services:
  nicegui:
    image: zauberzeug/nicegui:latest
    ports:
      - 8080:8080
    volumes:
      - ./app:/app # mounting local app directory
    environment:
      - PUID=1000 # change this to your user id
      - PGID=1000 # change this to your group id
      - STORAGE_SECRET="change-this-to-yor-own-private-secret"

docker-compose up
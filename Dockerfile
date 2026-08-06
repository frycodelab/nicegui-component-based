# Use the official NiceGUI image as the base image
FROM zauberzeug/nicegui:latest

# Upgrade python-engineio and python-socketio to fix KeyError: 'REQUEST_METHOD'
# under concurrent load (engineio bug with ASGI WebSocket scopes)
RUN pip install --upgrade python-engineio python-socketio nicegui[highcharts]
# Set working directory
WORKDIR /app

# Copy the application code to the container
COPY ./app /app

# Expose the port your NiceGUI app runs on (default is 8080)
EXPOSE 8080

# Set the default command to run the NiceGUI app
CMD ["python", "main.py"]
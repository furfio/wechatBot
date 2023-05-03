FROM python:3.10-slim
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update \
    &&apt-get install -y --no-install-recommends ffmpeg libavcodec-extra

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start the Flask app when the container launches
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
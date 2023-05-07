FROM python:3.10-slim
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -r requirements.txt

RUN echo /etc/apt/sources.list
RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN apt-get update \
    &&apt-get install -y --no-install-recommends ffmpeg libavcodec-extra

# install ssh
COPY entrypoint.sh ./

# Start and enable SSH
RUN apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd \
    && chmod u+x ./entrypoint.sh
COPY sshd_config /etc/ssh/

# Expose port 5000 for the Flask app
EXPOSE 5000 2222

# Start the Flask app when the container launches
# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
ENTRYPOINT [ "./entrypoint.sh" ]
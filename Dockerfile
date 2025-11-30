FROM python:3.11-slim



ENV DEBIAN_FRONTEND=noninteractive



RUN apt-get update && apt-get install -y 
build-essential 
default-libmysqlclient-dev 
pkg-config 
&& rm -rf /var/lib/apt/lists/*



WORKDIR /app



COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt



COPY . .



EXPOSE 8000



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

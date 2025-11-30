FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# تحديث النظام وتثبيت المتطلبات الأساسية لتجميع mysqlclient وحزم أخرى
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
        curl \
        git \
        libssl-dev \
        libffi-dev \
        && rm -rf /var/lib/apt/lists/*

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملف requirements وتحديث pip أولاً
COPY requirements.txt .
RUN pip install --upgrade pip
# تثبيت الحزم المطلوبة، مع التأكد من أن Python 3.11 متوافق
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# فتح البورت
EXPOSE 8000

# تشغيل السيرفر
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

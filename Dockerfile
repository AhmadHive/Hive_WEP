FROM python:3.11-slim

# منع الرسائل التفاعلية أثناء التثبيت

ENV DEBIAN_FRONTEND=noninteractive

# تثبيت المتطلبات الأساسية لتجميع mysqlclient وحزم أخرى

RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*

# إعداد مجلد العمل

WORKDIR /app

# نسخ ملف الريكوايرمنتس وتحديث pip أولاً

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع

COPY . .

# فتح البورت

EXPOSE 8000

# تشغيل السيرفر

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

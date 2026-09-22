# Su dung base image Python 3.11 nhe gon
FROM python:3.11-slim
# Thiet lap bien moi truong he thong
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    PYTHONPATH=/app
# Thiet lap thu muc lam viec trong container
WORKDIR /app
# Cai dat cac goi he thong phuc vu xu ly anh va tai lieu PDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
# Sao chep file requirements truoc de tan dung Docker cache
COPY requirements.txt /app/requirements.txt
# Cai dat cac thu vien Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt
# Sao chep toan bo ma nguon ung dung vao container
COPY src/ /app/src/
# Tao thu muc chua du lieu va database runtime
RUN mkdir -p /app/data
# Mo cong ket noi cua dich vu
EXPOSE 5000
# Lenh khoi chay may chu Web Studio
CMD ["python3", "src/frontend/server.py"]
# Use the official Python image as a base image (aliyun - centOS Linux)
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies using yum
#RUN yum update -y && \
#    yum install -y gcc gcc-c++ make libpq-devel && \
#    yum clean all

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip -i https://pypi.doubanio.com/simple/
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.doubanio.com/simple/

# Copy the project files
COPY . /app/

# Expose the port the app runs on
EXPOSE 8006

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

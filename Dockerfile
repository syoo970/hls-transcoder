FROM python:3.9-slim

# Install ffmpeg
RUN apt-get -y update
RUN apt-get install ffmpeg -y

# AWS PYTHON SDK 설치
RUN pip install boto3

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY transcoder.py /app/

# Set environment variables for AWS credentials (ensure to pass them when running the container)
ENV AWS_ACCESS_KEY_ID=your-access-key
ENV AWS_SECRET_ACCESS_KEY=your-secret-key
ENV AWS_DEFAULT_REGION=your-region

# Define environment variables for the S3 bucket and file paths
ENV S3_INPUT_BUCKET=input-bucket-name
ENV S3_INPUT_KEY=input-file.mp4
ENV S3_OUTPUT_BUCKET=output-bucket-name
ENV S3_OUTPUT_KEY=output-folder/

# Run the Python script
CMD ["python", "/app/transcoder.py"]
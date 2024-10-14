import os
import boto3
import subprocess

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

input_bucket = os.getenv('S3_INPUT_BUCKET')
input_key = os.getenv('S3_INPUT_KEY')
output_bucket = os.getenv('S3_OUTPUT_BUCKET')
output_key = os.getenv('S3_OUTPUT_KEY')

input_file = "/app/input.mp4"
output_file = "/app/output.m3u8"

def download_original_file():
    print(f"download start {input_key} from bucket {input_bucket}")
    s3.download_file(input_bucket, input_key, input_file)

def upload_file_to_s3():
    # Upload .m3u8 file
    print(f"Uploading {output_file} to bucket {output_bucket}")
    s3.upload_file(output_file, output_bucket, f"{output_key}output.m3u8")
    
    # Upload all .ts segment files
    for segment_file in os.listdir('/app'):
        if segment_file.endswith('.ts'):
            segment_path = f'/app/{segment_file}'
            s3.upload_file(segment_path, output_bucket, f"{output_key}{segment_file}")

def transcode_to_hls():
    # FFmpeg command to convert mp4 to HLS (m3u8)
    print(f"Starting transcoding {input_file} to HLS format")
    subprocess.run([
        'ffmpeg', '-i', input_file, '-codec: copy', '-start_number', '0',
        '-hls_time', '10', '-hls_list_size', '0', '-f', 'hls', output_file
    ], check=True)
    print("Transcoding completed")

if __name__ == "__main__":
    # Step 1: s3에 업로드된 원본 mp4 파일 다운로드
    download_original_file()

    # Step 2: m3u8 파일로 트랜스코딩 작업 진행
    transcode_to_hls()

    # Step 3: s3 버킷에 m3u8 파일 업로드
    upload_file_to_s3()
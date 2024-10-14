# hls-transcoder

## 개요

mp4 파일을 m3u8(hls) 형태로 변환 시키는 트랜스 코더

## How To Use

1. 도커파일 빌드 후 이미지 생성

```
   docker build -t hls-transcoder .
```

2. docker 컨테이너 실행

- 단 AWS 엑세스 키, 비밀 키, 인 & 아웃 파일 s3 버킷 및 파일 이름은 환경 변수로 주입 필요

```
docker run -e AWS_ACCESS_KEY_ID=your-access-key \
           -e AWS_SECRET_ACCESS_KEY=your-secret-key \
           -e AWS_DEFAULT_REGION=your-region \
           -e S3_INPUT_BUCKET=input-bucket-name \
           -e S3_INPUT_KEY=input-file.mp4 \
           -e S3_OUTPUT_BUCKET=output-bucket-name \
           -e S3_OUTPUT_KEY=output-folder/ \
           hls-transcoder
```

## ec2에서 사용시

- ec2에 역할을 부여 한다면 aws 엑세스 키 및 비밀키를 주입할 필요 없음
  - 단 이럴시 코드 변경 필요(boto3의 액세스 키 및 비밀 키 코드 삭제)

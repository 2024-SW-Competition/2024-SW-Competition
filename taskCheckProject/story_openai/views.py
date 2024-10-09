# story_openai/views.py
# 2024/09/25 ~ 2024/09/28
from django.http import JsonResponse
import openai
from google.cloud import vision
from google.cloud import storage
from django.conf import settings 
import os
from dotenv import load_dotenv
import re

load_dotenv()  # .env 파일을 로드
openai.api_key = os.getenv('OPENAI_API_KEY')

def upload_to_gcs(file, bucket_name, destination_blob_name=None):
    # 이미 절대 경로로 들어온 경우 lstrip을 하지 않도록 수정
    if file.startswith(settings.MEDIA_URL):
        file = file.replace(settings.MEDIA_URL, "", 1)  # MEDIA_URL 제거

    # MEDIA_ROOT 경로와 결합하여 절대 경로로 변환
    file_path = os.path.join(settings.MEDIA_ROOT, file.lstrip('/'))  # MEDIA_ROOT와 결합
    
    # 파일이 실제로 존재하는지 확인
    if not os.path.exists(file_path):
        print(f"파일 경로 확인: {file_path}")  # 경로가 어떻게 해석되는지 확인
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Google Cloud Storage 클라이언트 초기화
    storage_client = storage.Client()

    # 버킷 참조
    bucket = storage_client.bucket(bucket_name)

    # destination_blob_name이 없으면 파일 이름만 추출하여 설정
    if destination_blob_name is None:
        destination_blob_name = os.path.basename(file)

    # GCS에 파일 업로드
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

    # 업로드된 파일의 URL 반환
    print(f"업로드 완료: {blob.public_url}")
    return blob.public_url


# OpenAI API 호출 및 응답 처리
def query_view(request):
    if request.method == 'POST':
        try:
            # POST 요청에서 데이터 받기
            print("post request rececived")
            img_src = request.POST.get('img_src')  # 업로드된 이미지 파일명
            print(f"received img_src:{img_src}")
            print(f"Absolute path: {os.path.abspath(img_src)}")  # 절대 경로로 변환 후 확인
            goal = request.POST.get('goal')
            duration = request.POST.get('duration')
            username = request.POST.get('username')

            # Google Cloud Storage에 이미지 업로드
            print("Uploading image to GCS")
            gcs_url = upload_to_gcs(img_src, bucket_name=settings.GS_BUCKET_NAME, destination_blob_name='uploads/'+img_src)

            # Google Vision API를 통해 이미지 설명 생성
            print(f"image uploaded to gcs at {gcs_url}")
            image_description = generate_image_description(gcs_url)

            # OpenAI API 호출 (이미지 설명과 목표 비교)
            prompt = f"사용자의 목표는 '{goal}'이며 기간은 {duration}일입니다. 이 목표에 맞춰 분석된 이미지 설명은 '{image_description}'입니다. 이 이미지와 목표가 얼마나 일치하는지 평가해 주세요. 몇 % 정도 일치하는지 % 를 알려주시고, 30% 이하면, 사용자에게 이미지를 재업로드하라고 알려주세요. 구어체로 해주세요. {username}님, 이미지를 재업로드해주세요. 혹은, 이미지가 어느정도 일치한다면, 격려의 표현을 해주세요. 예를 들어) 오늘 목표 달성에 성공하셨네요! 등."

            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=1024
            )
            ai_response = response['choices'][0]['message']['content']
            return JsonResponse({'response': ai_response})

        except openai.error.OpenAIError as e:
            print(f"OpenAI Error: {str(e)}")  # OpenAI 에러 로그 출력
            return JsonResponse({'error': f"OpenAI Error: {str(e)}"}, status=500)
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")  # 다른 에러 로그 출력
            return JsonResponse({'error': f"Unexpected Error: {str(e)}"}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# google cloud vision api 사용해서 이미지 설명을 만든다.
def generate_image_description(image_url):
    client = vision.ImageAnnotatorClient(credentials=settings.GS_CREDENTIALS)

    # GCS 파일 URL을 사용하여 이미지 객체 생성
    image = vision.Image()
    image.source.image_uri = image_url

    # Vision API 호출
    response = client.label_detection(image=image)
    labels = response.label_annotations

    # 라벨 기반 설명 생성
    descriptions = [label.description for label in labels]
    description_text = ', '.join(descriptions)

    if response.error.message:
        raise Exception(f'{response.error.message}')

    return description_text

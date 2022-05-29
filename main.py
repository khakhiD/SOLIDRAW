import json

import cv2
import requests

import sys

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40

rest_api_key = '40fdaecbbd83eb558d065bddeb63c7cd'


def kakao_ocr_resize(image_path: str):

    image = cv2.imread(image_path)
    height, width, _ = image.shape
    print(f"height : {height}, width : {width}")

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr(image_path: str, appkey: str):

    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})


def main():
    image_path = 'C:/Users/USER/Desktop/work space/test3.jpg'

    resize_impath = kakao_ocr_resize(image_path)
    print(resize_impath)
    if resize_impath is not None:
        image_path = resize_impath
        print("원본 대신 리사이즈된 이미지를 사용합니다.")

    output = kakao_ocr(image_path, rest_api_key).json()
    outputdata = json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2)
    print("[OCR] output:\n{}\n".format(outputdata))

    # 받은 데이터 array로 변환
    outputdata = json.loads(outputdata)

    for i in range(len(outputdata['result'])):
        # box 모양으로 잘라서 보여주기
        x = outputdata['result'][i]['boxes'][0][0]
        y = outputdata['result'][i]['boxes'][0][1]
        w = (outputdata['result'][i]['boxes'][1][0] - outputdata['result'][i]['boxes'][0][0])
        h = (outputdata['result'][i]['boxes'][2][1] - outputdata['result'][i]['boxes'][0][1])
        # 원본 이미지
        org_image = cv2.imread('C:/Users/USER/Desktop/work space/test3.jpg_resized.jpg')
        # 자른 이미지
        img_trim = org_image[y:y + h, x:x + w]
        # 자른 이미지 보여주기
        cv2.imshow('', img_trim)
        cv2.waitKey(0)
        print(outputdata['result'][i]['recognition_words'][0])


if __name__ == "__main__":
    main()
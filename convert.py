import json
import copy
import cv2
import numpy as np
import requests
import math

LIMIT_PX = 1024
LIMIT_BYTE = 1024 * 1024  # 1MB
LIMIT_BOX = 40


def kakao_ocr(image_path: str, appkey: str):
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'
    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})


def main():
<<<<<<< HEAD
    image_path = 'solidraw/temp/before.png'
=======
    image_path = 'static/img/before.png'
>>>>>>> 8140be272064040facf8d958d446cd682e95fc09
    # 손그림 도면 이미지 로드
    image = cv2.imread(image_path)
    # 로드된 이미지와 같은 가로 세로 사이즈의 초기화 된 직선 보정 이미지 저장
    correction_image = np.zeros_like(image)
    # 로드된 이미지와 같은 가로 세로 사이즈의 초기화 된 결과 이미지 저장
    result_image = np.zeros_like(image)
    result_image = 255 - result_image
    # orig_image 변수에 원본 이미지 카피
    orig_image = image.copy()
    # 원본 이미지 출력
    # cv2.imshow('Original Image', orig_image)
    # cv2.waitKey(0)

    # OCR 함수 호출
    rest_api_key = '40fdaecbbd83eb558d065bddeb63c7cd'
    output = kakao_ocr(image_path, rest_api_key).json()
    output_data = json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2)

    # 받은 데이터 array로 변환
    output_data = json.loads(output_data)

    OCR_room = []
    OCR_size = []
    # 읽어 들인 문자 및 좌표 저장
    for i in range(len(output_data['result'])):
        x1 = output_data['result'][i]['boxes'][0][0]
        y1 = output_data['result'][i]['boxes'][0][1]
        x2 = output_data['result'][i]['boxes'][1][0]
        y2 = output_data['result'][i]['boxes'][2][1]
        recognition_words = output_data['result'][i]['recognition_words'][0]

        if recognition_words.isdigit():
            OCR_size.append([recognition_words, int((x1 + x2) / 2), int((y1 + y2) / 2)])
        else:
            OCR_room.append([recognition_words, int((x1 + x2) / 2), int((y1 + y2) / 2)])

        # 읽어 들인 문자 도면에서 제거
        for j in range(x1 - 1, x2 + 1):
            for k in range(y1 - 1, y2 + 1):
                image[k][j] = [255, 255, 255]

    # 문자 제거 이미지 출력
    # cv2.imshow('Remove Characters', image)
    # cv2.waitKey(0)

    # 이미지 흑백 변환 및 이진화
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    # 외곽선 검출
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 검출된 모든 도형 출력
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv2.imshow('Shape Detection', image)
    # cv2.waitKey(0)

    # 도형 개수 카운트 변수
    cnt = 0
    # 도면의 모서리 끝 좌표
    upper_left = [0, 0]
    upper_right = [0, 0]
    lower_left = [0, 0]
    lower_right = [0, 0]
    # 도면 선 색상 리스트
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
    # 각 공간별 접선 좌표 통일을 위한 좌표 저장 리스트
    points_x = []
    points_y = []

    # 새로 기입할 치수 위치
    size_points = []
    for i in range(len(OCR_size)):
        size_points.append([])
    # 각 방의 보정 좌표 값 저장
    rooms_points = []
    # 치수선 좌표 리스트 (우, 하, 좌, 상)
    size_lines = [[], [], [], []]

    # 직선 보정 도면 출력
    for c in contours:
        # 외곽선 길이 Return
        accuracy = 0.03 * cv2.arcLength(c, True)
        # 외곽선 근사화(단순화)
        approx = cv2.approxPolyDP(c, accuracy, True)

        # 최외각 도형(전체 도면을 감싸는 사각형)일 경우
        if cnt == 0:
            # 도면의 모서리 끝 좌표 계산 및 통일
            upper_left = [int(([approx][0][1][0][0] + [approx][0][2][0][0]) / 2),
                          int(([approx][0][0][0][1] + [approx][0][1][0][1]) / 2)]
            upper_right = [int(([approx][0][0][0][0] + [approx][0][3][0][0]) / 2),
                           int(([approx][0][0][0][1] + [approx][0][1][0][1]) / 2)]
            lower_left = [int(([approx][0][1][0][0] + [approx][0][2][0][0]) / 2),
                          int(([approx][0][2][0][1] + [approx][0][3][0][1]) / 2)]
            lower_right = [int(([approx][0][0][0][0] + [approx][0][3][0][0]) / 2),
                           int(([approx][0][2][0][1] + [approx][0][3][0][1]) / 2)]
            [approx][0][0][0] = upper_right
            [approx][0][1][0] = upper_left
            [approx][0][2][0] = lower_left
            [approx][0][3][0] = lower_right

            # 그려진 도형의 좌표 저장
            for i in range(len(approx)):
                points_x.append(approx[i][0][0])
                points_y.append(approx[i][0][1])

        else:
            # 사각형 내부 도형(공간)일 경우
            if len(approx) == 4:
                # 좌표 순서 통일 (우상 > 우하 > 좌하 > 좌상)
                if (approx[0][0][0] + 100) < approx[1][0][0]:
                    tmp = copy.deepcopy(approx[0])
                    approx[0] = approx[1]
                    approx[1] = tmp
                if not approx[0][0][0] - 20 < approx[1][0][0] < approx[0][0][0] + 20:
                    tmp = copy.deepcopy(approx[1])
                    approx[1] = approx[2]
                    approx[2] = tmp
                if not approx[1][0][1] - 20 < approx[2][0][1] < approx[1][0][1] + 20:
                    tmp = copy.deepcopy(approx[2])
                    approx[2] = approx[3]
                    approx[3] = tmp

                # 도형 끝 좌표 통일을 위해 일부 좌표 깊은 복사
                p1 = copy.deepcopy(approx[0][0][0])
                p2 = copy.deepcopy(approx[2][0][0])
                p3 = copy.deepcopy(approx[1][0][1])
                p4 = copy.deepcopy(approx[0][0][1])

                # 동일 도형 내 좌표 통일
                if upper_right[0] - 11 < approx[0][0][0] < upper_right[0] + 11:
                    approx[0][0][0] = upper_right[0]
                elif lower_left[0] - 11 < approx[0][0][0] < lower_left[0] + 11:
                    approx[0][0][0] = lower_left[0]
                else:
                    approx[0][0][0] = int((approx[0][0][0] + approx[1][0][0]) / 2)
                if upper_right[0] - 11 < approx[1][0][0] < upper_right[0] + 11:
                    approx[1][0][0] = upper_right[0]
                elif lower_left[0] - 11 < approx[1][0][0] < lower_left[0] + 11:
                    approx[1][0][0] = lower_left[0]
                else:
                    approx[1][0][0] = int((p1 + approx[1][0][0]) / 2)

                if upper_right[0] - 11 < approx[2][0][0] < upper_right[0] + 11:
                    approx[2][0][0] = upper_right[0]
                elif lower_left[0] - 11 < approx[2][0][0] < lower_left[0] + 11:
                    approx[2][0][0] = lower_left[0]
                else:
                    approx[2][0][0] = int((approx[2][0][0] + approx[3][0][0]) / 2)
                if upper_right[0] - 11 < approx[3][0][0] < upper_right[0] + 11:
                    approx[3][0][0] = upper_right[0]
                elif lower_left[0] - 11 < approx[3][0][0] < lower_left[0] + 11:
                    approx[3][0][0] = lower_left[0]
                else:
                    approx[3][0][0] = int((p2 + approx[3][0][0]) / 2)

                if upper_right[1] - 11 < approx[0][0][1] < upper_right[1] + 11:
                    approx[0][0][1] = upper_right[1]
                elif lower_left[1] - 11 < approx[0][0][1] < lower_left[1] + 11:
                    approx[0][0][1] = lower_left[1]
                else:
                    approx[0][0][1] = int((approx[0][0][1] + approx[3][0][1]) / 2)
                if upper_right[1] - 11 < approx[1][0][1] < upper_right[1] + 11:
                    approx[1][0][1] = upper_right[1]
                elif lower_left[1] - 11 < approx[1][0][1] < lower_left[1] + 11:
                    approx[1][0][1] = lower_left[1]
                else:
                    approx[1][0][1] = int((approx[1][0][1] + approx[2][0][1]) / 2)

                if upper_right[1] - 11 < approx[2][0][1] < upper_right[1] + 11:
                    approx[2][0][1] = upper_right[1]
                elif lower_left[1] - 11 < approx[2][0][1] < lower_left[1] + 11:
                    approx[2][0][1] = lower_left[1]
                else:
                    approx[2][0][1] = int((p3 + approx[2][0][1]) / 2)
                if upper_right[1] - 11 < approx[3][0][1] < upper_right[1] + 11:
                    approx[3][0][1] = upper_right[1]
                elif lower_left[1] - 11 < approx[3][0][1] < lower_left[1] + 11:
                    approx[3][0][1] = lower_left[1]
                else:
                    approx[3][0][1] = int((p4 + approx[3][0][1]) / 2)

                # 먼저 그려진 도형과 좌표 통일
                for i in range(len(approx)):
                    for j in range(len(points_x)):
                        if points_x[j] - 11 < approx[i][0][0] < points_x[j] + 11:
                            approx[i][0][0] = copy.deepcopy(points_x[j])
                    for j in range(len(points_y)):
                        if points_y[j] - 11 < approx[i][0][1] < points_y[j] + 11:
                            approx[i][0][1] = copy.deepcopy(points_y[j])

                # 그려진 도형의 좌표 저장
                for i in range(len(approx)):
                    points_x.append(approx[i][0][0])
                    points_y.append(approx[i][0][1])

            # 사각형이 아닌 내부 도형(공간)일 경우
            else:
                # 최외곽 좌표와 통일
                for i in range(len(approx)):
                    if upper_right[0] - 15 < approx[i][0][0] < upper_right[0] + 15:
                        approx[i][0][0] = upper_right[0]
                    elif lower_left[0] - 15 < approx[i][0][0] < lower_left[0] + 15:
                        approx[i][0][0] = lower_left[0]
                    if upper_right[1] - 15 < approx[i][0][1] < upper_right[1] + 15:
                        approx[i][0][1] = upper_right[1]
                    elif lower_left[1] - 15 < approx[i][0][1] < lower_left[1] + 15:
                        approx[i][0][1] = lower_left[1]

                # 동일 도형 내 좌표 통일
                for i in range(len(approx)):
                    for j in range(len(approx)):
                        if approx[j][0][0] - 15 < approx[i][0][0] < approx[j][0][0]:
                            approx[j][0][0] = approx[i][0][0]
                        if approx[j][0][1] - 15 < approx[i][0][1] < approx[j][0][1]:
                            approx[j][0][1] = approx[i][0][1]

                # 먼저 그려진 도형과 좌표 통일
                for i in range(len(approx)):
                    for j in range(len(points_x)):
                        if points_x[j] - 11 < approx[i][0][0] < points_x[j] + 11:
                            approx[i][0][0] = copy.deepcopy(points_x[j])
                    for j in range(len(points_y)):
                        if points_y[j] - 11 < approx[i][0][1] < points_y[j] + 11:
                            approx[i][0][1] = copy.deepcopy(points_y[j])

                # 그려진 도형의 좌표 저장
                for i in range(len(approx)):
                    points_x.append(approx[i][0][0])
                    points_y.append(approx[i][0][1])

            rooms_points.append([[approx[3][0][0], approx[3][0][1]], [approx[1][0][0], approx[1][0][1]]])
            Center_1_x = int((approx[0][0][0] + approx[1][0][0]) / 2)
            Center_1_y = int((approx[0][0][1] + approx[1][0][1]) / 2)
            Center_2_x = int((approx[1][0][0] + approx[2][0][0]) / 2)
            Center_2_y = int((approx[1][0][1] + approx[2][0][1]) / 2)
            Center_3_x = int((approx[2][0][0] + approx[3][0][0]) / 2)
            Center_3_y = int((approx[2][0][1] + approx[3][0][1]) / 2)
            Center_4_x = int((approx[3][0][0] + approx[0][0][0]) / 2)
            Center_4_y = int((approx[3][0][1] + approx[0][0][1]) / 2)
            for i in range(len(OCR_size)):
                a1 = abs(Center_1_x - OCR_size[i][1])
                b1 = abs(Center_1_y - OCR_size[i][2])
                a2 = abs(Center_2_x - OCR_size[i][1])
                b2 = abs(Center_2_y - OCR_size[i][2])
                a3 = abs(Center_3_x - OCR_size[i][1])
                b3 = abs(Center_3_y - OCR_size[i][2])
                a4 = abs(Center_4_x - OCR_size[i][1])
                b4 = abs(Center_4_y - OCR_size[i][2])
                c1 = int(math.sqrt((a1 * a1) + (b1 * b1)))
                c2 = int(math.sqrt((a2 * a2) + (b2 * b2)))
                c3 = int(math.sqrt((a3 * a3) + (b3 * b3)))
                c4 = int(math.sqrt((a4 * a4) + (b4 * b4)))
                if c1 < 50:
                    size_points[i].append([Center_1_x + 30, Center_1_y])
                    size_lines[0].append([approx[0][0][0], approx[0][0][1], approx[1][0][0], approx[1][0][1]])
                elif c2 < 50:
                    size_points[i].append([Center_2_x - 20, Center_2_y + 50])
                    size_lines[1].append([approx[1][0][0], approx[1][0][1], approx[2][0][0], approx[2][0][1]])
                elif c3 < 50:
                    size_points[i].append([Center_3_x - 70, Center_3_y])
                    size_lines[2].append([approx[2][0][0], approx[2][0][1], approx[3][0][0], approx[3][0][1]])
                elif c4 < 50:
                    size_points[i].append([Center_4_x - 20, Center_4_y - 40])
                    size_lines[3].append([approx[3][0][0], approx[3][0][1], approx[0][0][0], approx[0][0][1]])

        # 결과 이미지에 도면 그리기
        cv2.drawContours(correction_image, [approx], 0, colors[cnt], 2)
        # cv2.imshow('Straight Line Correction', correction_image)
        # 도형 개수 카운트 증감
        cnt = cnt + 1
    # cv2.waitKey(0)

    # 이미지 흑백 변환
    sized_image = 255 - (cv2.cvtColor(correction_image, cv2.COLOR_BGR2GRAY))
    for i in range(sized_image.shape[0]):
        for j in range(sized_image.shape[1]):
            if sized_image[i][j] != 255:
                sized_image[i][j] = 0

    # 치수 기입
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(size_points)):
        text = str(OCR_size[i][0])
        if len(text) < 4:
            text = ' ' + text

        if size_points[i][0][0] < upper_left[0]:
            result_image = cv2.rotate(result_image, cv2.ROTATE_90_CLOCKWISE)  # 시계 방향으로 90도 회전
            sized_image = cv2.rotate(sized_image, cv2.ROTATE_90_CLOCKWISE)  # 시계 방향으로 90도 회전
            points = (sized_image.shape[0] - size_points[i][0][1] - 22, size_points[i][0][0] + 30)
            result_image = cv2.putText(result_image, text, points, font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            sized_image = cv2.putText(sized_image, text, points, font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            result_image = cv2.rotate(result_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 반시계 방향으로 90도 회전
            sized_image = cv2.rotate(sized_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 반시계 방향으로 90도 회전
        elif size_points[i][0][0] > upper_right[0]:
            result_image = cv2.rotate(result_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 반시계 방향으로 90도 회전
            sized_image = cv2.rotate(sized_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # 반시계 방향으로 90도 회전
            points = (size_points[i][0][1] - 21, sized_image.shape[1] - size_points[i][0][0] - 10)
            result_image = cv2.putText(result_image, text, points, font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            sized_image = cv2.putText(sized_image, text, points, font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            result_image = cv2.rotate(result_image, cv2.ROTATE_90_CLOCKWISE)  # 시계 방향으로 90도 회전
            sized_image = cv2.rotate(sized_image, cv2.ROTATE_90_CLOCKWISE)  # 시계 방향으로 90도 회전
        else:
            points = (size_points[i][0][0] + 2, size_points[i][0][1])
            result_image = cv2.putText(result_image, text, points, font, 1, (0, 0, 0), 1, cv2.LINE_AA)
            sized_image = cv2.putText(sized_image, text, points, font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    # 치수선 기입
    for i in range(len(size_lines)):
        for j in range(len(size_lines[i])):
            if i == 0:
                pt1 = (size_lines[i][j][0] + 10, size_lines[i][j][1])
                pt2 = (size_lines[i][j][0] + 70, size_lines[i][j][1])
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][2] + 10, size_lines[i][j][3])
                pt2 = (size_lines[i][j][2] + 70, size_lines[i][j][3])
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][0] + 60, size_lines[i][j][1] - 10)
                pt2 = (size_lines[i][j][0] + 60, size_lines[i][j][3] + 10)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                center = (size_lines[i][j][0] + 60, size_lines[i][j][1])
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)
                center = (size_lines[i][j][0] + 60, size_lines[i][j][3])
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)
            if i == 1:
                pt1 = (size_lines[i][j][0], size_lines[i][j][1] + 10)
                pt2 = (size_lines[i][j][0], size_lines[i][j][1] + 70)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][2], size_lines[i][j][3] + 10)
                pt2 = (size_lines[i][j][2], size_lines[i][j][3] + 70)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][0] + 10, size_lines[i][j][1] + 60)
                pt2 = (size_lines[i][j][2] - 10, size_lines[i][j][1] + 60)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                center = (size_lines[i][j][0], size_lines[i][j][1] + 60)
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)
                center = (size_lines[i][j][2], size_lines[i][j][1] + 60)
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)
            if i == 2:
                pt1 = (size_lines[i][j][0] - 10, size_lines[i][j][1])
                pt2 = (size_lines[i][j][0] - 70, size_lines[i][j][1])
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][2] - 10, size_lines[i][j][3])
                pt2 = (size_lines[i][j][2] - 70, size_lines[i][j][3])
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][0] - 60, size_lines[i][j][1] + 10)
                pt2 = (size_lines[i][j][0] - 60, size_lines[i][j][3] - 10)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                center = (size_lines[i][j][0] - 60, size_lines[i][j][1])
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)
                center = (size_lines[i][j][0] - 60, size_lines[i][j][3])
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)
            if i == 3:
                pt1 = (size_lines[i][j][0], size_lines[i][j][1] - 10)
                pt2 = (size_lines[i][j][0], size_lines[i][j][1] - 70)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][2], size_lines[i][j][3] - 10)
                pt2 = (size_lines[i][j][2], size_lines[i][j][3] - 70)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                pt1 = (size_lines[i][j][0] - 10, size_lines[i][j][1] - 60)
                pt2 = (size_lines[i][j][2] + 10, size_lines[i][j][1] - 60)
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)
                cv2.line(sized_image, pt1, pt2, (0, 0, 0), 1)
                center = (size_lines[i][j][0], size_lines[i][j][1] - 60)
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)
                center = (size_lines[i][j][2], size_lines[i][j][1] - 60)
                cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                cv2.circle(sized_image, center, 2, (0, 0, 0), 2)

    #cv2.imshow('Sized Image', sized_image)
    # cv2.waitKey(0)

    pt1 = upper_left
    pt2 = lower_right
    cv2.rectangle(result_image, pt1, pt2, (200, 200, 200), -1)
    cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 2)

    # 문 좌표 (좌상, 우상, 좌하, 우하)
    doors_points = [[], [], [], []]

    # 벽 내부의 실제 생활 공간 좌표
    inner_room = []

    for i in range(len(rooms_points)):
        left_boundary_check = True
        up_boundary_check = True
        right_boundary_check = True
        low_boundary_check = True

        pt1 = (rooms_points[i][0][0] + 3, rooms_points[i][0][1] + 3)
        pt2 = (rooms_points[i][1][0] - 3, rooms_points[i][1][1] - 3)
        if rooms_points[i][0][0] == upper_left[0]:
            pt1 = (rooms_points[i][0][0] + 10, pt1[1])
            left_boundary_check = False
        if rooms_points[i][0][1] == upper_left[1]:
            pt1 = (pt1[0], rooms_points[i][0][1] + 10)
            up_boundary_check = False
        if rooms_points[i][1][0] == lower_right[0]:
            pt2 = (rooms_points[i][1][0] - 10, pt2[1])
            right_boundary_check = False
        if rooms_points[i][1][1] == lower_right[1]:
            pt2 = (pt2[0], rooms_points[i][1][1] - 10)
            low_boundary_check = False

        cv2.rectangle(result_image, pt1, pt2, (255, 255, 255), -1)
        cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 2)
        inner_room.append([pt1, pt2])

        if left_boundary_check and up_boundary_check:
            doors_points[0].append([(pt1[0] + 5, pt1[1]), (pt1[0] + 50, pt1[1] - 6)])
        elif right_boundary_check and up_boundary_check:
            doors_points[1].append([(pt2[0] - 5, pt1[1]), (pt2[0] - 50, pt1[1] - 6)])
        elif left_boundary_check and low_boundary_check:
            doors_points[2].append([(pt1[0], pt2[1] - 5), (pt1[0] - 6, pt2[1] - 50)])
        elif right_boundary_check and low_boundary_check:
            doors_points[3].append([(pt2[0], pt2[1] - 5), (pt2[0] + 6, pt2[1] - 50)])

    x_check = False
    y_check = False
    for i in range(len(doors_points)):
        for j in range(len(doors_points[i])):
            for m in range(len(doors_points)):
                for n in range(len(doors_points[m])):
                    if doors_points[i][j][0][0] == doors_points[m][n][1][0]:
                        x_check = True
                    if doors_points[i][j][1][1] == doors_points[m][n][1][1]:
                        y_check = True
                    if x_check and y_check:
                        doors_points[m].pop(n)

    for i in range(len(doors_points)):
        for j in range(len(doors_points[i])):
            cv2.rectangle(result_image, doors_points[i][j][0], doors_points[i][j][1], (255, 255, 255), -1)
            if i == 0:
                pt1 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                pt2 = doors_points[i][j][0][0], doors_points[i][j][1][1] - 45
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)
                pt1 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                cv2.ellipse(result_image, pt1, (45, 45), 0, 270, 360, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)
                pt1 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)
            if i == 1:
                pt1 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                pt2 = doors_points[i][j][0][0], doors_points[i][j][1][1] - 45
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)
                pt1 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                cv2.ellipse(result_image, pt1, (45, 45), 0, 180, 270, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)
                pt1 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)
            if i == 2:
                pt1 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0] - 45, doors_points[i][j][0][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)
                pt1 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                cv2.ellipse(result_image, pt1, (45, 45), 0, 180, 270, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)
                pt1 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)
            if i == 3:
                pt1 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0] - 45, doors_points[i][j][0][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)
                pt1 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (150, 150, 150), 1)

                cv2.ellipse(result_image, pt1, (45, 45), 0, 270, 360, (150, 150, 150), 1)

                pt1 = doors_points[i][j][0][0], doors_points[i][j][0][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][0][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)
                pt1 = doors_points[i][j][0][0], doors_points[i][j][1][1]
                pt2 = doors_points[i][j][1][0], doors_points[i][j][1][1]
                cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

    # print(OCR_room)
    # print(inner_room)

    for i in range(len(inner_room)):
        left_boundary_check = False
        up_boundary_check = False
        right_boundary_check = False
        low_boundary_check = False

        if rooms_points[i][0][0] == upper_left[0]:
            pt1 = (rooms_points[i][0][0] + 10, pt1[1])
            left_boundary_check = True
        if rooms_points[i][0][1] == upper_left[1]:
            pt1 = (pt1[0], rooms_points[i][0][1] + 10)
            up_boundary_check = True
        if rooms_points[i][1][0] == lower_right[0]:
            pt2 = (rooms_points[i][1][0] - 10, pt2[1])
            right_boundary_check = True
        if rooms_points[i][1][1] == lower_right[1]:
            pt2 = (pt2[0], rooms_points[i][1][1] - 10)
            low_boundary_check = True

        for j in range(len(OCR_room)):
            if inner_room[i][0][0] < OCR_room[j][1] < inner_room[i][1][0]:
                if inner_room[i][0][1] < OCR_room[j][2] < inner_room[i][1][1]:
                    if OCR_room[j][0] == '화장실':
                        # print(OCR_room[j][0])
                        # print(inner_room[i])
                        # print(left_boundary_check, up_boundary_check, right_boundary_check, low_boundary_check)

                        if left_boundary_check and up_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][0][1] + 5)
                            pt2 = (inner_room[i][1][0], inner_room[i][0][1] + 5)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 10, inner_room[i][0][1] + 25)
                            pt2 = (inner_room[i][0][0] + 45, inner_room[i][0][1] + 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 12, inner_room[i][0][1] + 23)
                            pt2 = (inner_room[i][0][0] + 43, inner_room[i][0][1] + 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 28, inner_room[i][0][1] + 5)
                            pt2 = (inner_room[i][0][0] + 28, inner_room[i][0][1] + 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 28, inner_room[i][0][1] + 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)

                            pt1 = (inner_room[i][0][0] + 66, inner_room[i][0][1] + 20)
                            pt2 = (inner_room[i][0][0] + 90, inner_room[i][0][1] + 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 68, inner_room[i][0][1] + 20)
                            pt2 = (inner_room[i][0][0] + 88, inner_room[i][0][1] + 40)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            center = (inner_room[i][0][0] + 78, inner_room[i][0][1] + 30)
                            cv2.circle(result_image, center, 8, (0, 0, 0), 1)
                        elif right_boundary_check and up_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][0][1] + 5)
                            pt2 = (inner_room[i][1][0], inner_room[i][0][1] + 5)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 10, inner_room[i][0][1] + 25)
                            pt2 = (inner_room[i][0][0] + 45, inner_room[i][0][1] + 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 12, inner_room[i][0][1] + 23)
                            pt2 = (inner_room[i][0][0] + 43, inner_room[i][0][1] + 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 28, inner_room[i][0][1] + 5)
                            pt2 = (inner_room[i][0][0] + 28, inner_room[i][0][1] + 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 28, inner_room[i][0][1] + 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)

                            pt1 = (inner_room[i][0][0] + 66, inner_room[i][0][1] + 20)
                            pt2 = (inner_room[i][0][0] + 90, inner_room[i][0][1] + 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 68, inner_room[i][0][1] + 20)
                            pt2 = (inner_room[i][0][0] + 88, inner_room[i][0][1] + 40)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            center = (inner_room[i][0][0] + 78, inner_room[i][0][1] + 30)
                            cv2.circle(result_image, center, 8, (0, 0, 0), 1)
                        elif left_boundary_check and low_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][1][1] - 5)
                            pt2 = (inner_room[i][1][0], inner_room[i][1][1] - 5)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 10, inner_room[i][1][1] - 25)
                            pt2 = (inner_room[i][0][0] + 45, inner_room[i][1][1] - 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 12, inner_room[i][1][1] - 23)
                            pt2 = (inner_room[i][0][0] + 43, inner_room[i][1][1] - 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 28, inner_room[i][1][1] - 5)
                            pt2 = (inner_room[i][0][0] + 28, inner_room[i][1][1] - 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 28, inner_room[i][1][1] - 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)

                            pt1 = (inner_room[i][0][0] + 66, inner_room[i][1][1] - 20)
                            pt2 = (inner_room[i][0][0] + 90, inner_room[i][1][1] - 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 68, inner_room[i][1][1] - 20)
                            pt2 = (inner_room[i][0][0] + 88, inner_room[i][1][1] - 40)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            center = (inner_room[i][0][0] + 78, inner_room[i][1][1] - 30)
                            cv2.circle(result_image, center, 8, (0, 0, 0), 1)
                        elif right_boundary_check and low_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][1][1] - 5)
                            pt2 = (inner_room[i][1][0], inner_room[i][1][1] - 5)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 10, inner_room[i][1][1] - 25)
                            pt2 = (inner_room[i][0][0] + 45, inner_room[i][1][1] - 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 12, inner_room[i][1][1] - 23)
                            pt2 = (inner_room[i][0][0] + 43, inner_room[i][1][1] - 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 28, inner_room[i][1][1] - 5)
                            pt2 = (inner_room[i][0][0] + 28, inner_room[i][1][1] - 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 28, inner_room[i][1][1] - 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)

                            pt1 = (inner_room[i][0][0] + 66, inner_room[i][1][1] - 20)
                            pt2 = (inner_room[i][0][0] + 90, inner_room[i][1][1] - 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 68, inner_room[i][1][1] - 20)
                            pt2 = (inner_room[i][0][0] + 88, inner_room[i][1][1] - 40)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            center = (inner_room[i][0][0] + 78, inner_room[i][1][1] - 30)
                            cv2.circle(result_image, center, 8, (0, 0, 0), 1)

                    if OCR_room[j][0] == '주방':
                        # print(OCR_room[j][0])
                        # print(inner_room[i])
                        # print(left_boundary_check, up_boundary_check, right_boundary_check, low_boundary_check)

                        if left_boundary_check and up_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][0][1] + 30)
                            pt2 = (inner_room[i][1][0], inner_room[i][0][1] + 30)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 15, inner_room[i][0][1] + 25)
                            pt2 = (inner_room[i][0][0] + 50, inner_room[i][0][1] + 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 17, inner_room[i][0][1] + 23)
                            pt2 = (inner_room[i][0][0] + 48, inner_room[i][0][1] + 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 33, inner_room[i][0][1] + 5)
                            pt2 = (inner_room[i][0][0] + 33, inner_room[i][0][1] + 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 33, inner_room[i][0][1] + 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                        elif right_boundary_check and up_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][0][1] + 30)
                            pt2 = (inner_room[i][1][0], inner_room[i][0][1] + 30)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 15, inner_room[i][0][1] + 25)
                            pt2 = (inner_room[i][0][0] + 50, inner_room[i][0][1] + 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 17, inner_room[i][0][1] + 23)
                            pt2 = (inner_room[i][0][0] + 48, inner_room[i][0][1] + 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 33, inner_room[i][0][1] + 5)
                            pt2 = (inner_room[i][0][0] + 33, inner_room[i][0][1] + 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 33, inner_room[i][0][1] + 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                        elif left_boundary_check and low_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][1][1] - 30)
                            pt2 = (inner_room[i][1][0], inner_room[i][1][1] - 30)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 15, inner_room[i][1][1] - 25)
                            pt2 = (inner_room[i][0][0] + 50, inner_room[i][1][1] - 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 17, inner_room[i][1][1] - 23)
                            pt2 = (inner_room[i][0][0] + 48, inner_room[i][1][1] - 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 33, inner_room[i][1][1] - 5)
                            pt2 = (inner_room[i][0][0] + 33, inner_room[i][1][1] - 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 33, inner_room[i][1][1] - 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)
                        elif right_boundary_check and low_boundary_check:
                            pt1 = (inner_room[i][0][0], inner_room[i][1][1] - 30)
                            pt2 = (inner_room[i][1][0], inner_room[i][1][1] - 30)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 15, inner_room[i][1][1] - 25)
                            pt2 = (inner_room[i][0][0] + 50, inner_room[i][1][1] - 5)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 17, inner_room[i][1][1] - 23)
                            pt2 = (inner_room[i][0][0] + 48, inner_room[i][1][1] - 7)
                            cv2.rectangle(result_image, pt1, pt2, (0, 0, 0), 1)

                            pt1 = (inner_room[i][0][0] + 33, inner_room[i][1][1] - 5)
                            pt2 = (inner_room[i][0][0] + 33, inner_room[i][1][1] - 15)
                            cv2.line(result_image, pt1, pt2, (0, 0, 0), 2)

                            center = (inner_room[i][0][0] + 33, inner_room[i][1][1] - 15)
                            cv2.circle(result_image, center, 2, (0, 0, 0), 2)

    # cv2.imshow('Result', result_image)
    #cv2.waitKey(0)
<<<<<<< HEAD
    cv2.imwrite('solidraw/static/img/after.png', result_image)
=======
    cv2.imwrite('static/img/after.png', result_image)
>>>>>>> 8140be272064040facf8d958d446cd682e95fc09
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from recognizer.main import PlateNumberRecognition
from fastapi import FastAPI, File, UploadFile
import json
from io import BytesIO
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

recognizer = PlateNumberRecognition()
TINH_TP = {
    "11": "Cao Bằng",
    "12": "Lạng Sơn",
    "14": "Quảng Ninh",
    "15": "TP. Hải Phòng",
    "16": "TP. Hải Phòng",
    "17": "Thái Bình",
    "18": "Nam Định",
    "19": "Phú Thọ",
    "20": "Thái Nguyên",
    "21": "Yên Bái",
    "22": "Tuyên Quang",
    "23": "Hà Giang",
    "24": "Lào Cai",
    "25": "Lai Châu",
    "26": "Sơn La",
    "27": "Điện Biên",
    "28": "Hòa Bình",
    "29": "Hà Nội",
    "30": "Hà Nội",
    "31": "Hà Nội",
    "32": "Hà Nội",
    "33": "Hà Nội",
    "40": "Hà Nội",
    "34": "Hải Dương",
    "35": "Ninh Bình",
    "36": "Thanh Hóa",
    "37": "Nghệ An",
    "38": "Hà Tĩnh",
    "43": "TP. Đà Nẵng",
    "47": "Đắk Lắk",
    "48": "Đắk Nông",
    "49": "Lâm Đồng",
    "50": "TP. Hồ Chí Minh",
    "51": "TP. Hồ Chí Minh",
    "52": "TP. Hồ Chí Minh",
    "53": "TP. Hồ Chí Minh",
    "54": "TP. Hồ Chí Minh",
    "55": "TP. Hồ Chí Minh",
    "56": "TP. Hồ Chí Minh",
    "57": "TP. Hồ Chí Minh",
    "58": "TP. Hồ Chí Minh",
    "59": "TP. Hồ Chí Minh",
    "41": "TP. Hồ Chí Minh",
    "39": "Đồng Nai",
    "60": "Đồng Nai",
    "61": "Bình Dương",
    "62": "Long An",
    "63": "Tiền Giang",
    "64": "Vĩnh Long",
    "65": "TP. Cần Thơ",
    "66": "Đồng Tháp",
    "67": "An Giang",
    "68": "Kiên Giang",
    "69": "Cà Mau",
    "70": "Tây Ninh",
    "71": "Bến Tre",
    "72": "Bà Rịa Vũng Tàu",
    "73": "Quảng Bình",
    "74": "Quảng Trị",
    "75": "Thừa Thiên Huế",
    "76": "Quảng Ngãi",
    "77": "Bình Định",
    "78": "Phú Yên",
    "79": "Khánh Hòa",
    "81": "Gia Lai",
    "82": "Kon Tum",
    "83": "Sóc Trăng",
    "84": "Trà Vinh",
    "85": "Ninh Thuận",
    "86": "Bình Thuận",
    "88": "Vĩnh Phúc",
    "89": "Hưng Yên",
    "90": "Hà Nam",
    "92": "Quảng Nam",
    "93": "Bình Phước",
    "94": "Bạc Liêu",
    "95": "Hậu Giang",
    "97": "Bắc Kạn",
    "98": "Bắc Giang",
    "99": "Bắc Ninh",
}

QUAN_HUYEN = {
    "29": {
        "B1": "Quận Ba Đình",
        "C1": "Quận Hoàn Kiếm",
        "D1": "Quận Hai Bà Trưng",
        "D2": "Quận Hai Bà Trưng",
        "E1": "Quận Đống Đa",
        "E2": "Quận Đống Đa",
        "F1": "Quận Tây Hồ",
        "G1": "Quận Thanh Xuân",
        "H1": "Quận Hoàng Mai",
        "K1": ["Quận Long Biên", "Huyện Gia Lâm"],
        "L1": "Quận Nam Từ Liêm",
        "L5": "Quận Bắc Từ Liêm",
        "T1": "Quận Hà Đông",
        "P1": "Quận Cầu Giấy",
        "U1": "Thị xã Sơn Tây",
        "M1": "Huyện Thanh Trì",
        "Z1": "Huyện Mê Linh",
        "S1": "Huyện Đông Anh",
        "S6": "Huyện Sóc Sơn",
        "V1": "Huyện Ba Vì",
        "V3": "Huyện Phúc Thọ",
        "V5": "Huyện Thạch Thất",
        "V7": "Huyện Quốc Oai",
        "X1": "Huyện Chương Mỹ",
        "X3": "Huyện Đan Phượng",
        "X5": "Huyện Hoài Đức",
        "X7": "Huyện Mỹ Đức",
        "Y1": "Huyện Ứng Hòa",
        "Y3": "Huyện Thường Tín",
        "Y7": "Huyện Phú Xuyên",
    },
    "30": {
        "B1": "Quận Ba Đình",
        "C1": "Quận Hoàn Kiếm",
        "D1": "Quận Hai Bà Trưng",
        "D2": "Quận Hai Bà Trưng",
        "E1": "Quận Đống Đa",
        "E2": "Quận Đống Đa",
        "F1": "Quận Tây Hồ",
        "G1": "Quận Thanh Xuân",
        "H1": "Quận Hoàng Mai",
        "K1": ["Quận Long Biên", "Huyện Gia Lâm"],
        "L1": "Quận Nam Từ Liêm",
        "L5": "Quận Bắc Từ Liêm",
        "T1": "Quận Hà Đông",
        "P1": "Quận Cầu Giấy",
        "U1": "Thị xã Sơn Tây",
        "M1": "Huyện Thanh Trì",
        "Z1": "Huyện Mê Linh",
        "S1": "Huyện Đông Anh",
        "S6": "Huyện Sóc Sơn",
        "V1": "Huyện Ba Vì",
        "V3": "Huyện Phúc Thọ",
        "V5": "Huyện Thạch Thất",
        "V7": "Huyện Quốc Oai",
        "X1": "Huyện Chương Mỹ",
        "X3": "Huyện Đan Phượng",
        "X5": "Huyện Hoài Đức",
        "X7": "Huyện Mỹ Đức",
        "Y1": "Huyện Ứng Hòa",
        "Y3": "Huyện Thường Tín",
        "Y7": "Huyện Phú Xuyên",
    },
    "31": {
        "B1": "Quận Ba Đình",
        "C1": "Quận Hoàn Kiếm",
        "D1": "Quận Hai Bà Trưng",
        "D2": "Quận Hai Bà Trưng",
        "E1": "Quận Đống Đa",
        "E2": "Quận Đống Đa",
        "F1": "Quận Tây Hồ",
        "G1": "Quận Thanh Xuân",
        "H1": "Quận Hoàng Mai",
        "K1": ["Quận Long Biên", "Huyện Gia Lâm"],
        "L1": "Quận Nam Từ Liêm",
        "L5": "Quận Bắc Từ Liêm",
        "T1": "Quận Hà Đông",
        "P1": "Quận Cầu Giấy",
        "U1": "Thị xã Sơn Tây",
        "M1": "Huyện Thanh Trì",
        "Z1": "Huyện Mê Linh",
        "S1": "Huyện Đông Anh",
        "S6": "Huyện Sóc Sơn",
        "V1": "Huyện Ba Vì",
        "V3": "Huyện Phúc Thọ",
        "V5": "Huyện Thạch Thất",
        "V7": "Huyện Quốc Oai",
        "X1": "Huyện Chương Mỹ",
        "X3": "Huyện Đan Phượng",
        "X5": "Huyện Hoài Đức",
        "X7": "Huyện Mỹ Đức",
        "Y1": "Huyện Ứng Hòa",
        "Y3": "Huyện Thường Tín",
        "Y7": "Huyện Phú Xuyên",
    },
    "32": {
        "B1": "Quận Ba Đình",
        "C1": "Quận Hoàn Kiếm",
        "D1": "Quận Hai Bà Trưng",
        "D2": "Quận Hai Bà Trưng",
        "E1": "Quận Đống Đa",
        "E2": "Quận Đống Đa",
        "F1": "Quận Tây Hồ",
        "G1": "Quận Thanh Xuân",
        "H1": "Quận Hoàng Mai",
        "K1": ["Quận Long Biên", "Huyện Gia Lâm"],
        "L1": "Quận Nam Từ Liêm",
        "L5": "Quận Bắc Từ Liêm",
        "T1": "Quận Hà Đông",
        "P1": "Quận Cầu Giấy",
        "U1": "Thị xã Sơn Tây",
        "M1": "Huyện Thanh Trì",
        "Z1": "Huyện Mê Linh",
        "S1": "Huyện Đông Anh",
        "S6": "Huyện Sóc Sơn",
        "V1": "Huyện Ba Vì",
        "V3": "Huyện Phúc Thọ",
        "V5": "Huyện Thạch Thất",
        "V7": "Huyện Quốc Oai",
        "X1": "Huyện Chương Mỹ",
        "X3": "Huyện Đan Phượng",
        "X5": "Huyện Hoài Đức",
        "X7": "Huyện Mỹ Đức",
        "Y1": "Huyện Ứng Hòa",
        "Y3": "Huyện Thường Tín",
        "Y7": "Huyện Phú Xuyên",
    },
    "40": {
        "B1": "Quận Ba Đình",
        "C1": "Quận Hoàn Kiếm",
        "D1": "Quận Hai Bà Trưng",
        "D2": "Quận Hai Bà Trưng",
        "E1": "Quận Đống Đa",
        "E2": "Quận Đống Đa",
        "F1": "Quận Tây Hồ",
        "G1": "Quận Thanh Xuân",
        "H1": "Quận Hoàng Mai",
        "K1": ["Quận Long Biên", "Huyện Gia Lâm"],
        "L1": "Quận Nam Từ Liêm",
        "L5": "Quận Bắc Từ Liêm",
        "T1": "Quận Hà Đông",
        "P1": "Quận Cầu Giấy",
        "U1": "Thị xã Sơn Tây",
        "M1": "Huyện Thanh Trì",
        "Z1": "Huyện Mê Linh",
        "S1": "Huyện Đông Anh",
        "S6": "Huyện Sóc Sơn",
        "V1": "Huyện Ba Vì",
        "V3": "Huyện Phúc Thọ",
        "V5": "Huyện Thạch Thất",
        "V7": "Huyện Quốc Oai",
        "X1": "Huyện Chương Mỹ",
        "X3": "Huyện Đan Phượng",
        "X5": "Huyện Hoài Đức",
        "X7": "Huyện Mỹ Đức",
        "Y1": "Huyện Ứng Hòa",
        "Y3": "Huyện Thường Tín",
        "Y7": "Huyện Phú Xuyên",
    },
}


# # Load JSON data
# try:
#     with open("tinh_tp.json", "r") as file_tinh_tp:
#         TINH_TP = json.load(file_tinh_tp)
#     with open("quan_huyen.json", "r") as file_quan_huyen:
#         QUAN_HUYEN = json.load(file_quan_huyen)
# except FileNotFoundError:
#     print("File tinh_tp.json not found")
#     TINH_TP = {}
#     QUAN_HUYEN = {}
# except json.JSONDecodeError:
#     print("Error parsing JSON file")
#     TINH_TP = {}
#     QUAN_HUYEN = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Convert uploaded file to an image
    image = Image.open(BytesIO(await file.read()))

    # Save the image temporarily if needed
    temp_image_path = "/tmp/temp_image.png"
    image.save(temp_image_path)

    # Process the image with the recognizer
    recognizer.process(temp_image_path)

    # Get recognition results
    results = recognizer.text
    if not results:
        return {"message": "Không tìm thấy biển số xe"}

    tinh_tp = TINH_TP.get(results[:2], "Không tìm thấy")
    quan_huyen = QUAN_HUYEN.get(results[:2], {}).get(results[2:4], "Không tìm thấy")

    return {"results": results, "tinh_tp": tinh_tp, "quan_huyen": quan_huyen}


@app.get("/api/v1/")
async def v1():
    return {"message": "Hello, World!"}


@app.get("/")
async def home():
    return {"message": "Welcome to the API!"}

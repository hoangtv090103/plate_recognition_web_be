import cv2
from matplotlib import pyplot as plt
import imutils
import easyocr
import numpy as np



class PlateNumberRecognition:
    def __init__(self):
        self.img = None
        self.gray = None
        self.edged = None
        self.location = None
        self.cropped_image = None
        self.text = ""
        self.reader = easyocr.Reader(['en'])


    def read_image(self, image_path: str=''):
        if not image_path:
            raise ValueError('Image path is empty!')
        self.img = cv2.imread(image_path)
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def preprocess_image(self):
        """Chuyển đổi ảnh sang grayscale, làm mờ và phát hiện cạnh."""
        bfilter = cv2.bilateralFilter(self.gray, 11, 17, 17)  # Noise reduction
        self.edged = cv2.Canny(bfilter, 30, 200)  # Edge detection

    def find_plate_location(self):
        """Tìm vị trí của biển số xe trong ảnh."""
        if self.edged is None:
            raise ValueError('Edged image is empty!')
        keypoints = cv2.findContours(self.edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                self.location = approx
                break

    def extract_plate(self):
        """ Cắt biển số ra khỏi ảnh gốc."""
        if self.gray is None:
            raise ValueError('Gray image is empty!')
        if self.location is not None:
            mask = np.zeros(self.gray.shape, np.uint8)
            cv2.drawContours(mask, [self.location], 0, 255, -1)

            self.cropped_image = cv2.bitwise_and(self.img, self.img, mask=mask)
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))

            self.cropped_image = self.gray[topx:bottomx + 1, topy:bottomy + 1]

    def recognize_text(self):
        """Nhận dạng ký tự trên biển số xe."""
        result = self.reader.readtext(self.cropped_image)
        
        if not result:
            return
         
        if len(result) == 2:
            self.text = f'{result[0][-2]} {result[1][-2]}'
        else:
            self.text = result[0][-2]

    def annotate_image(self):
        """Thêm văn bản nhận dạng vào ảnh gốc."""
        if self.location is not None and self.text:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.img, text=self.text, org=(self.location[0][0][0], self.location[1][0][1] + 60),
                        fontFace=font, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
            cv2.rectangle(self.img, tuple(self.location[0][0]), tuple(self.location[2][0]), (0, 255, 0), 3)

    def show_images(self):
        """Thêm văn bản nhận dạng vào ảnh gốc."""
        plt.figure(figsize=(10, 10))

        plt.subplot(1, 3, 1)
        plt.title('Grayscale Image')
        plt.imshow(cv2.cvtColor(self.gray, cv2.COLOR_BGR2RGB))

        plt.subplot(1, 3, 2)
        plt.title('Edged Image')
        plt.imshow(cv2.cvtColor(self.edged, cv2.COLOR_BGR2RGB))

        plt.subplot(1, 3, 3)
        plt.title('Detected Plate')
        plt.imshow(cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB))

        plt.show()

    def process(self, image_path: str=''):
        """Quy trình xử lý ảnh hoàn chỉnh từ đầu đến cuối."""
        self.read_image(image_path)
        
        if self.img is None:
            raise ValueError('Image is empty!')
 
        self.preprocess_image()
        self.find_plate_location()
        self.extract_plate()
        self.recognize_text()
        self.annotate_image()
        # self.show_images()

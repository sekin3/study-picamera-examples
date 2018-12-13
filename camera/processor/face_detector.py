from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import cv2

class FaceDetector(object):
    def __init__(self, flip = True):
        self.vs = PiVideoStream(resolution=(800, 608)).start()
        self.flip = flip
        time.sleep(2.0)

        # opencvの顔分類器(CascadeClassifier)をインスタンス化する
        self.face_cascade = cv2.CascadeClassifier('camera/processor/model/haarcascades/haarcascade_frontalface_default.xml')

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        frame = self.process_image(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def process_image(self, frame):
        # opencvでframe(カラー画像)をグレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 上記でグレースケールに変換したものをインスタンス化した顔分類器の
        # detectMultiScaleメソッドで処理し、認識した顔の座標情報を取得する
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)
        
        # 取得した座標情報を元に、cv2.rectangleを使ってframe上に
        # 顔の位置を描画する
        num = 0
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
            num = num + 1
    #スケールの書き込み関数
    #def make_scale(im,length=40,from_edge = 15,thick = 2,hight = 6, font_size = 0.6,pix_size = 10):

        w = 200
        h = 200
            #横線
        cv2.line(im,(w-length-from_edge,h-from_edge),(w-from_edge,h-from_edge),(255,255,0),thick)
        #縦線左
        cv2.line(im,(w-length-from_edge,h-from_edge-hight/2),(w-length-from_edge,h-from_edge+hight/2),(255,255,0),thick)
        #縦線右
        cv2.line(im,(w-from_edge,h-from_edge-hight/2),(w-from_edge,h-from_edge+hight/2),(255,255,0),thick)

        #1ピクセルのサイズから長さを計算
        size = pix_size*length
        text = str(num)
        #フォントの指定
        #font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        #font = cv2.FONT_HERSHEY_SIMPLEX
        font = cv2.FONT_HERSHEY_PLAIN
        #文字の書き込み
        cv2.putText(im,text,(w-length-from_edge-5,h-from_edge-hight),font, font_size,(255,255,0))

        # frameを戻り値として返す
        return frame

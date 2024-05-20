import cv2 #OpenCV를 사용하기위해 import해줍니다.
import numpy as np #파이썬의 기본 모듈중 하나인 numpy

def main():
    camera = cv2.VideoCapture(1) #카메라를 비디오 입력으로 사용. -1은 기본설정이라는 뜻
    camera.set(3,800) #띄울 동영상의 가로사이즈 160픽셀
    camera.set(4,600) #띄울 동영상의 세로사이즈 120픽셀
    
    while( camera.isOpened() ): #카메라가 Open되어 있다면,
        ret, frame = camera.read() #비디오의 한 프레임씩 읽습니다. ret값이 True, 실패하면 False, fram에 읽은 프레임이 나옴
        cv2.imshow( 'normal' , frame)  #'normal'이라는 이름으로 영상을 출력
        
        #crop_img =frame[60:120, 0:160] #세로는 60~120픽셀, 가로는 0~160픽셀로 crop(잘라냄)한다.
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #이미지를 회색으로 변경
        
        blur = cv2.GaussianBlur(gray, (5,5) , 0) #가우시간 블러로 블러처리를 한다.
        
        ret,thresh1 = cv2.threshold(blur, 123, 255, cv2.THRESH_BINARY_INV) #임계점 처리로, 123보다 크면, 255로 변환
        #123밑의 값은 0으로 처리한다. 흑백으로 색을 명확하게 처리하기 위해서
        
        cv2.imshow('thresh1', thresh1)  #처리된 영상인 thresh1을 출력한다.
        
        if cv2.waitKey(1) == ord('q'): #만약 q라는 키보드값을 읽으면 종료합니다.
            break
        
    cv2.destroyAllWindows() #이후 openCV창을 종료합니다.
     
if __name__ == '__main__':
    main()
import cv2 #OpenCV를 사용하기위해 import해줍니다.
import numpy as np #파이썬의 기본 모듈중 하나인 numpy

def main():
    camera = cv2.VideoCapture(0) #카메라를 비디오 입력으로 사용. -1은 기본설정이라는 뜻
    camera.set(3,320) #띄울 동영상의 가로사이즈 160픽셀
    camera.set(4,240) #띄울 동영상의 세로사이즈 120픽셀
    
    while( camera.isOpened() ): #카메라가 Open되어 있다면,
        ret, frame = camera.read() #비디오의 한 프레임씩 읽습니다. ret값이 True, 실패하면 False, fram에 읽은 프레임이 나옴
        cv2.imshow( 'normal' , frame)  #'normal'이라는 이름으로 영상을 출력
        
        crop_img_1 =frame[120:180, 0:160] #세로는 60~120픽셀, 가로는 0~160픽셀로 crop(잘라냄)한다.
        crop_img_2 =frame[120:180, 161:320]

        gray_1 = cv2.cvtColor(crop_img_1, cv2.COLOR_BGR2GRAY) #이미지를 회색으로 변경
        
        blur_1 = cv2.GaussianBlur(gray_1, (5,5) , 0) #가우시간 블러로 블러처리를 한다.
        
        ret,thresh1 = cv2.threshold(blur_1, 123, 255, cv2.THRESH_BINARY_INV) #임계점 처리로, 123보다 크면, 255로 변환
        #123밑의 값은 0으로 처리한다. 흑백으로 색을 명확하게 처리하기 위해서
        
        #이미지를 압축해서 노이즈를 없앤다.
        mask1 = cv2.erode(thresh1, None, iterations=2)  
        mask1 = cv2.dilate(mask1, None, iterations=2)
        cv2.imshow('mask1',mask1)

        gray_2 = cv2.cvtColor(crop_img_2, cv2.COLOR_BGR2GRAY) #이미지를 회색으로 변경
        
        blur_2 = cv2.GaussianBlur(gray_2, (5,5) , 0) #가우시간 블러로 블러처리를 한다.
        
        ret_2,thresh2 = cv2.threshold(blur_2, 123, 255, cv2.THRESH_BINARY_INV) #임계점 처리로, 123보다 크면, 255로 변환
        #123밑의 값은 0으로 처리한다. 흑백으로 색을 명확하게 처리하기 위해서
        
        #이미지를 압축해서 노이즈를 없앤다.
        mask2 = cv2.erode(thresh2, None, iterations=2)  
        mask2 = cv2.dilate(mask2, None, iterations=2)
        cv2.imshow('mask2',mask2)
    

        #이미지의 윤곽선을 검출
        contours1,hierarchy1 = cv2.findContours(mask1.copy(), 1, cv2.CHAIN_APPROX_NONE)
        contours2,hierarchy2 = cv2.findContours(mask2.copy(), 1, cv2.CHAIN_APPROX_NONE)

        #윤곽선이 있다면, max(가장큰값)을 반환, 모멘트를 계산한다.
        if len(contours1) > 0:
            c = max(contours1, key=cv2.contourArea)
            M = cv2.moments(c)
             
            #X축과 Y축의 무게중심을 구한다.
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
           #X축의 무게중심을 출력한다.
            cv2.line(crop_img_1,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img_1,(0,cy),(1280,cy),(255,0,0),1)
        
            cv2.drawContours(crop_img_1, contours1, -1, (0,255,0), 1)
            
            #print(cx,end=" ") #출력값을 print 한다.
            
        if len(contours2) > 0:
            c = max(contours2, key=cv2.contourArea)
            M = cv2.moments(c)
             
            #X축과 Y축의 무게중심을 구한다.
            cx2 = int(M['m10']/M['m00'])
            cy2 = int(M['m01']/M['m00'])
            
           #X축의 무게중심을 출력한다.
            cv2.line(crop_img_2,(cx2,0),(cx2,720),(255,0,0),1)
            cv2.line(crop_img_2,(0,cy2),(1280,cy2),(255,0,0),1)
        
            cv2.drawContours(crop_img_2, contours2, -1, (0,255,0), 1)
            
            #print(cx2) #출력값을 print 한다.

        if cx>=30 and cx<=60:
            if cx2>=110 and cx2<=150:
                print("우회전")

        if cx>=0 and cx<=30:
            if cx2>=20 and cx2<=80:
                print("좌회전") 

        else:
            print("직진")
        
        if cv2.waitKey(1) == ord('q'): #만약 q라는 키보드값을 읽으면 종료합니다.
            break
        
    cv2.destroyAllWindows() #이후 openCV창을 종료합니다.
     
if __name__ == '__main__':
    main()

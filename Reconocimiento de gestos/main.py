import numpy as np
import cv2
import math
import imutils

# Calcula el angulo del defecto de convexidad
def angle(s,e,f):
    v1 = [s[0]-f[0],s[1]-f[1]]
    v2 = [e[0]-f[0],e[1]-f[1]]
    ang1 = math.atan2(v1[1],v1[0])
    ang2 = math.atan2(v2[1],v2[0])
    ang = ang1 - ang2
    if (ang > np.pi):
        ang -= 2*np.pi
    if (ang < -np.pi):
        ang += 2*np.pi
    return ang*180/np.pi

cap = cv2.VideoCapture(0)
backSub = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

if not cap.isOpened:
  print("Unable to open the cam")
  exit(0)

# 2 puntos
pt1 = (400,100) # esquina superior izquierda 
pt2 = (600,300) # esquina inferior derecha

frame_width  = int(cap.get(3))
frame_height = int(cap.get(4))

learningRate = -1
while True:
  ret,frame=cap.read()
  if not ret:
    exit(0)

  frame = cv2.flip(frame, 1)
  # Region de interes
  roi = frame[pt1[1]:pt2[1],pt1[0]:pt2[0],:].copy()
  cv2.rectangle(frame,pt1,pt2,(255, 255, 0))
  fgMask = backSub.apply(roi, None, learningRate)

  kernel = np.ones((5,5),np.uint8)
  opening = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)

  # Deteccion de contornos
  contours, hierarchy = cv2.findContours(opening,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
  if len(contours) > 0:
    max = -1
    for i, cnt in enumerate(contours):
      auxMax = len(cnt)
      if (max < auxMax):
        max = auxMax
        index = i

      #Encontrar centro
      M = cv2.moments(cnt)
      if M["m00"] == 0: M["m00"] = 1
      x = int(M["m10"]/M["m00"])
      y = int(M["m01"]/M["m00"])
      cv2.circle(roi, tuple([x, y]), 5, (0, 255, 0), -1)
    # Malla convexa
      cv2.drawContours(roi, contours, index, (0,255,0))
    cnt = contours[index]
    hull = cv2.convexHull(cnt,returnPoints = False)
    # Defectos de convexidad
    defects = cv2.convexityDefects(cnt, hull)

    if type(defects) != type(None):
      beginning = []
      ending = []
      fingers = 0

      for i in range(len(defects)):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        depth = d / 256.0
        ang = angle(start,end,far)

        if np.linalg.norm(cnt[s][0] - cnt[e][0]) > 20 and d > 12000 and ang < 75:
          beginning.append(start)
          ending.append(end)
          cv2.line(roi,start,end,[255,0,0],2) # linea de la malla convexa
          cv2.circle(roi,far,5,[0,0,255],-1) # circulo del punto mas lejano


      #Cuando se levanta un solo dedo
      if len(beginning) == 0:
        minY = np.linalg.norm(cnt - [x, y])
        if minY >= 850:
          fingers = fingers + 1

      for i in range(len(beginning)):
        fingers = fingers + 1
        if i == len(beginning) - 1:
          fingers = fingers + 1
      cv2.putText(frame, '{}'.format(fingers), (390, 45), 1, 4, (255, 255, 255), 2, cv2.LINE_AA)
      rect = cv2.boundingRect(cnt)
      pt1_ = (rect[0],rect[1])
      pt2_ = (rect[0]+rect[2],rect[1]+rect[3])
      cv2.rectangle(roi,pt1_,pt2_,(0,0,255),3)


# Mostrar ventanas
  cv2.imshow('frame', frame) # ventana frame
  cv2.imshow('ROI', roi) # ventana interes
  cv2.imshow('FgMask', fgMask) # ventana mascara binaria

  keyboard = cv2.waitKey(1) # 1 milesegundo con el "keyboard"
  if keyboard & 0xFF == ord('q'): # q = salir
      break
  elif keyboard == ord('r'): # r = learning rate 0
      learningRate = 0

# Liberar todos los recursos + cámara
cap.release()
cv2.destroyAllWindows()
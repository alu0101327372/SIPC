import numpy as np
import cv2
import math

# Funcion que utilizara cuando busque los defectos de convexidad. 
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

# Abrir la camara con cv2
cap = cv2.VideoCapture(0)
if not cap.isOpened:
    print ("Unable to open cam")
    exit(0)

# Obtener fotograma del fondo inicial del rectangulo de interes para usar como referencia en la eliminacion de fondo
# Se convierte a escala de grises y se le aplica desenfoque gaussiano para eliminar ruido
ret, bgRef = cap.read()
bgRef = cv2.flip(bgRef, 1)

pt1 = (400, 100)
pt2 = (600, 300)
roiBg = bgRef[pt1[1]:pt2[1],pt1[0]:pt2[0], : ].copy()

roiBg_gray = cv2.cvtColor(roiBg, cv2.COLOR_BGR2GRAY)
roiBg_gray = cv2.GaussianBlur(roiBg_gray, (21, 21), 0)

# Variables a inicializar para usar dentro del bucle
isDrawing = False
drawing = []

while (True):

    # Lectura del fotograma actual
    ret,frame = cap.read()
    if not ret:
	    exit(0)

    frame = cv2.flip(frame, 1)

	# Se obtiene el rectangulo de interes del fotograma, se convierte a escala de grises y se le aplica desenfoque gaussiano para eliminar ruido
    roi = frame[pt1[1]:pt2[1],pt1[0]:pt2[0], : ].copy()

    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    roi_gray = cv2.GaussianBlur(roi_gray, (21, 21), 0)

    # En cada iteracion se calcula la diferencia entre el fotograma actual y el de referencia para obtener la imagen sin fondo
    difference = cv2.absdiff(roi_gray, roiBg_gray)

    # Se restringen los colores a blanco y negro estableciendo un umbral para eliminar ruido
    thresh = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=0)

    # Calculo de contornos
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cv2.drawContours(roi, contours, -1, (0,255,0),3)

    # Comprobamos que hayan contornos en la imagen para poder trabajar con ellos
    if (len(contours) > 0):

        # Obtencion de la malla de convexidad
        hull = cv2.convexHull(contours[0])
        cv2.drawContours(roi, [hull], 0, (255,0,0),3)

        # Obtencion de los defectos de convexidad
        cnt = contours[0]
        hull2 = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull2)
          
        # Hallamos el bounding rect y lo dibujamos 
        rect = cv2.boundingRect(cnt)
        p1 = (rect[0], rect[1])
        p2 = (rect[0] + rect[2], rect[1] + rect[3])
        cv2.rectangle(roi, p1, p2, (0, 0, 255), 3)

        ## Hallamos el punto medio del bounding rect, y damos un valor inicial a la variable que almacenara el punto mas alto.
        pmedio = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
        higherPoint = pmedio

        # Comprobamos que hayan defectos de convexidad inicializados para poder trabajar con ellos y los hallamos
        if defects is not None:
            for i in range(len(defects)):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                depth = d/256.0
                ang = angle(start,end,far)
                cv2.line(roi,start,end,[255,0,0],2)
                cv2.circle(roi,far,5,[0,0,255],-1)
                
                # Hallar el punto mas alto
                if start[1] < higherPoint[1]:
                    higherPoint = start
    
        # Calculo del numero de dedos
        # Para ello, dibujamos un circulo desde el centro del bounding rect y hacemos un AND entre la imagen en blanco y negro de
        # la mano y el dibujo del circulo. Por tanto, los trozos de circulo que resultaran de esta imagen indican los dedos. Si se
        # cuentan estos trozos tendremos el numero de dedos, aunque habra que tener en cuenta la muneca y restarla del computo.
        circulo = np.zeros((pt2[0] - pt1[0] , pt2[1] - pt1[1], 1), np.uint8)
        cv2.circle(circulo, pmedio, 65, [255, 255, 255], 1)
        mask = cv2.bitwise_and(thresh, circulo)

        circle_contours, circle_hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
        
        num_fingers = len(circle_contours) - 1
        
        # Restriccion del dominio de num_fingers
        if num_fingers > 5:
            num_fingers = 5
        if num_fingers < 0:
            num_fingers = 0

        # Se indicara el gesto que esta teniendo lugar actualmente
        if isDrawing:
            gesture = "Dibujando"
        elif num_fingers == 0:
            gesture = "Puno cerrado"
        else:
            gesture = "Desconocido"

        # Muestra por pantalla de las variables
        cv2.putText(frame, 'Dedos: ' + str(num_fingers), (460,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,250,0), thickness=4)
        cv2.putText(frame, 'Gesto: ' + gesture, (70,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,250,0), thickness=4)

        # Dibujado
        if isDrawing:
            if higherPoint != pmedio:
                drawing.append(higherPoint)
            for i in range(len(drawing)):
                if (len(drawing) > i + 1):
                    cv2.line(roi, drawing[i], drawing[i + 1], [0, 128, 255], 10)

    # Ventanas a mostrar
    cv2.rectangle(frame, pt1, pt2, (255,0,0))
    cv2.imshow('frame', frame)
    cv2.imshow('ROI', roi)
    
    # Eventos de teclado
    keyboard = cv2.waitKey(1)
    
    # 'r' para recargar el fondo
    if keyboard & 0xFF == ord('r'):
        ret, bgRef = cap.read()
        bgRef = cv2.flip(bgRef, 1)
        roiBg = bgRef[pt1[1]:pt2[1],pt1[0]:pt2[0], : ].copy()
        roiBg_gray = cv2.cvtColor(roiBg, cv2.COLOR_BGR2GRAY)
        roiBg_gray = cv2.GaussianBlur(roiBg_gray, (21, 21), 0)

    # 'd' para activar el dibujado
    if keyboard & 0xFF == ord('d'):
        if not isDrawing:
            isDrawing = True
        else:
            isDrawing = False
            drawing = []
   
    # 'q' para salir del bucle y terminar el programa
    if keyboard & 0xFF == ord('q'):
	    break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
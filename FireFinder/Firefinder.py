import cv2
from ultralytics import YOLO

model = YOLO("models/last.pt")  
confidence_threshold = 0.4     

cam = cv2.VideoCapture(0)  

if not cam.isOpened():
    print("Cannot open camera")
    exit()

fire_frame_count = 0
fire_frame_threshold = 3  

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, (640, 480))

    results = model.predict(frame)[0]  

    fire_detected_in_frame = False

    for box in results.boxes:
        conf = box.conf.item()      
        cls = int(box.cls.item())    

        if conf >= confidence_threshold:
            fire_detected_in_frame = True

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"FIRE {conf:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    if fire_detected_in_frame:
        fire_frame_count += 1
        if fire_frame_count >= fire_frame_threshold:
            cv2.putText(frame, "!!! FIRE DETECTED !!!", (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)
    else:
        fire_frame_count = 0

    cv2.imshow("Fire Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

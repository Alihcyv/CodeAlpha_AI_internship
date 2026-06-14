%%writefile app.py
import cv2
from ultralytics import YOLO

def main():
    model = YOLO('yolov8s.pt')

    video_path = 0 
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Failed to open video stream.")
        return

    print("Press 'q' to exit.")

    while True:
        success, frame = cap.read()
        if not success:
            break
        results = model.track(
            frame, 
            persist=True,
            conf=0.25,
            iou=0.45,
            imgsz=640,
            tracker="botsort.yaml")
        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Object Detection & Tracking", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

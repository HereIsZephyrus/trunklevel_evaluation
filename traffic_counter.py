from ultralytics import YOLO
from datetime import datetime
from datetime import timedelta
import csv
import cv2
import math

model = YOLO('yolov8n.pt')

videoPath = "/windows/Users/Administrator/Videos/traffic/combine-copress.mp4"

cap = cv2.VideoCapture(videoPath)
if not cap.isOpened():
    print("Cannot open video")
    exit()

vehicle_count = 0
next_vehicle_id = 0
vehicle_tracks = {}
distance_threshold = 150
start_time_str = "2024-12-23 17:24:00"
current_time = datetime.strptime(start_time_str, r"%Y-%m-%d %H:%M:%S")
frame_count = 0
frame_speed = 25
time_gap = 5
last_during_count = 0
series_count = []
series_time = []
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame_count  = frame_count + 1
    if frame_count == frame_speed * 60 * time_gap:
        frame_count = 0
        delta_count = vehicle_count - last_during_count
        last_during_count = vehicle_count
        series_count.append(delta_count)
        series_time.append(current_time)
        current_time = current_time + timedelta(minutes=time_gap)
    results = model(frame)
    detections = results[0].boxes.xyxy
    classes = results[0].boxes.cls
    confidences = results[0].boxes.conf
    line_position = int(frame.shape[0] / 4)
    current_frame_tracks = {}
    for index, detection in enumerate(detections):
        if classes[index] in [2,5,7]:
            conf = confidences[index]
            x1, y1, x2, y2 = detection
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            matched_vehicle_id = None
            min_distance = float('inf')
            for vehicle_id, track in vehicle_tracks.items():
                last_x, last_y = track[-1]
                distance = math.sqrt((center_x - last_x) ** 2 + (center_y - last_y) ** 2)

                if distance < distance_threshold and distance < min_distance:
                    matched_vehicle_id = vehicle_id
                    min_distance = distance

            if matched_vehicle_id is not None:
                vehicle_tracks[matched_vehicle_id].append((center_x, center_y))
                current_frame_tracks[matched_vehicle_id] = (center_x, center_y)
                for track_point in vehicle_tracks[matched_vehicle_id]:
                    if track_point[1] < line_position <= center_y:
                        vehicle_count += 1
                        del vehicle_tracks[matched_vehicle_id]
                        break

            else:
                next_vehicle_id += 1
                vehicle_tracks[next_vehicle_id] = [(center_x, center_y)]
                current_frame_tracks[next_vehicle_id] = (center_x, center_y)

            for vehicle_id, (center_x, center_y) in current_frame_tracks.items():
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
                cv2.putText(
                    frame,
                    f"ID: {vehicle_id}",
                    (center_x, center_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )
            #cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            #cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (255, 0, 0), 2)
            #cv2.putText(frame, f"Vehicle {conf:.2f}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame,f"Vehicle Count: {vehicle_count}",(50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),2,)

    cv2.imshow('Traffic Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

delta_count = vehicle_count - last_during_count
last_during_count = vehicle_count
series_count.append(delta_count)
series_time.append(current_time)
current_time = current_time + timedelta(minutes=time_gap)
with open('./count_result.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['time', 'count'])
    for time, count in zip(series_time, series_count):
        writer.writerow([time, count])
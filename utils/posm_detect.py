from ultralytics import YOLOv10

# model = YOLOv10.from_pretrained('yolov10b.pt')
# or
# wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10{n/s/m/b/l/x}.pt
model = YOLOv10('weights/posm.pt')

# result = model(source="billboard_test/3.jpg", imgsz=640, save=True)
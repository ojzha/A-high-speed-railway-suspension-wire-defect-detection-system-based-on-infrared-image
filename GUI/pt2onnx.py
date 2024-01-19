from ultralytics import YOLO

# load model
model = YOLO('./best.pt')

# Export model
success = model.export(format="onnx")

import cv2

from backend.vision.detector import detector

image = cv2.imread("assets/images/bus.jpg")

results = detector.predict(image)

annotated = results[0].plot()

cv2.imwrite(
    "assets/output/result.jpg",
    annotated,
)

print("===================================")
print("Deteksi selesai.")
print("Output:")
print("assets/output/result.jpg")
print("===================================")

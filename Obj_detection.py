import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

###--------------py app---------------------
MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (0, 255, 0)  # red

def visualize(image,detection_result) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ')'
    text_location = (MARGIN + bbox.origin_x,
                     MARGIN + ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

  return image

# STEP 2: Create an ObjectDetector object.
base_options = python.BaseOptions(model_asset_path=r"E:\Route\Projects\Object_Detection\efficientdet_lite0.tflite")
options = vision.ObjectDetectorOptions(base_options=base_options,
                                       score_threshold=0.5)
detector = vision.ObjectDetector.create_from_options(options)


###----GUI------------------------------------------------------
st.title('Object Detection App')
upload_img = st.file_uploader('please , upload an image :', type = ['jpg','png','jepg'])


if upload_img is not None:
    file_bytes = np.asarray(bytearray(upload_img.read()), dtype = np.uint8)
    img = cv2.imdecode(file_bytes,1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    st.image(img, 'Uploaded Image', use_container_width = True)
    
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB , data = img)


    detection_result = detector.detect(mp_image)
    
    annotated_image = visualize(img, detection_result)
    st.image(annotated_image, 'Detected objs Image', use_container_width = True)

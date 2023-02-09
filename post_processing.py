from get_yolo_output import post_process
import cv2

img_to_detect = cv2.imread("TRDG/TextRecognitionDataGenerator/data4/Datafiles/image1.jpg")
class_labels = [x[:-1] for x in open("space1.names").readlines()]
max_value_ids, boxes_list, class_ids_list, confidences_list = post_process(img_to_detect,class_labels)
detection_list = []
for max_valueid in max_value_ids:
    max_class_id = max_valueid
    box = boxes_list[max_class_id]
    start_x_pt = box[0]
    start_y_pt = box[1]
    box_width = box[2]
    box_height = box[3]
    
    predicted_class_id = class_ids_list[max_class_id]
    predicted_class_label = class_labels[predicted_class_id] if class_labels[predicted_class_id] != "Space" else " "
    prediction_confidence = confidences_list[max_class_id]
    print("predicted object {}".format("{}: {:.2f}%".format(predicted_class_label, prediction_confidence * 100)))
    detection_list.append([predicted_class_id,predicted_class_label,prediction_confidence,start_x_pt,start_y_pt,box_width,box_height])

detection_list.sort(key=lambda x:x[3])
res = "".join([x[1] for x in detection_list])
print(res)
cv2.imshow("frame",img_to_detect)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Import required packages
import cv2
# import matplotlib.pyplot as plt

# img = cv2.imread("image0.jpg")
def get_seperator(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
  
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 1))

  dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

  contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_NONE)

  # im2 = img.copy()
  
  
  # Looping through the identified contours
  # Then rectangular part is cropped and passed on
  # to pytesseract for extracting text from it
  # Extracted text is then written into the text file
  boxlist = []
  for cnt in contours:
      x, y, w, h = cv2.boundingRect(cnt)
      boxlist.append([x,y,w,h])
      # Drawing a rectangle on copied image
      # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
      # print(x,y,w,h)
  # plt.imshow(im2)
  # plt.show()
  avgArea = 0
  for ele in boxlist:
    avgArea+=(ele[2]*ele[3])
  avgArea/=len(boxlist)
  boxlist = [x for x in boxlist if x[2]*x[3]>avgArea/1.5]
  min = None
  min1 = None
  uppery = []
  lowery = []
  coords = [[],[]]
  for i in range(len(boxlist)-1):
    if 50<abs(boxlist[i][0] - boxlist[i+1][0]):
      y2 = boxlist[i+1][1]
      y1 = boxlist[i][1]
      diff = abs(y2-y1)
      if min is None or min>=diff:
        min = diff
        uppery.append([(boxlist[i][0],boxlist[i][1]),(boxlist[i+1][0],boxlist[i+1][1])])
    if 100<abs(boxlist[i][0]+boxlist[i][2] - boxlist[i+1][0]+boxlist[i+1][2]):
      y2 = boxlist[i+1][1]+boxlist[i+1][3]
      y1 = boxlist[i][1]+boxlist[i][3]
      diff = abs(y2-y1)
      if min1 is None or min1>=diff:
        min1 = diff
        lowery.append([(boxlist[i][0]+boxlist[i][2],boxlist[i][1]+boxlist[i][3]),(boxlist[i+1][0]+boxlist[i+1][2],boxlist[i+1][1]+boxlist[i+1][3])])
  min = None
  min1 = None
  for ele in uppery:
    if min is None or min[0][1] < ele[0][1]:
      min = ele
  for ele in lowery:
    if min1 is None or min1[0][1] > ele[0][1]:
      min1 = ele
  coords = [min,min1]
  return coords

  # print(coords)
  # cv2.line(img,(0,coords[0][0][1]),(img.shape[1],coords[0][0][1]),(0,0,0),2)
  # cv2.line(img,(0,coords[1][0][1]),(img.shape[1],coords[1][0][1]),(0,0,0),2)
  # cv2.imshow("frame",img)
  # cv2.waitKey(0)
  # plt.imshow(img2)
  # plt.show()
# cv2.imwrite("seperated_img.jpg",img2)
# cv2.imwrite("image_with_boxes.jpg",im2)
# cv2.imwrite("thresh_img.jpg",dilation)
# image = cv2.imread("./latest_dataset1/image3558.jpg")
# get_seperator(image)
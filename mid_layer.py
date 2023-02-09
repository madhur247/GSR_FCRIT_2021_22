import cv2
import numpy as np
import os
from trdg import computer_text_generator_gujarati as computer_text_generator 
from PIL import Image, ImageFilter
from trdg.utils import mask_to_bboxes
vertical_margin = horizontal_margin = 10
size=64
font_path = os.path.join("/home/madhur/.virtualenvs/miniproj6/lib/python3.8/site-packages/trdg", "fonts/gu")
# font = os.path.join(font_path,os.listdir(font_path)[0])
exception = "લ"
# exception1 = "ણ"
exception_list = ["શ","ગ","ણ"]
vowel_symbols = ['ા', 'િ', 'ી', 'ુ', 'ૂ', 'ે', 'ૈ', 'ો', 'ૌ', 'ં', 'ઃ', 'ૃ']
pre_index = [1]
post_index = [0,2,7,8,10]
def mid_bboxes(img,piece,modifier):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgsize = gray.shape
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    # if piece==exception and modifier in [vowel_symbols[i] for i in post_index]:
    #     kernel = (3,1)
    # elif piece==exception and modifier in [vowel_symbols[i] for i in pre_index]:
    #     kernel = (3,1)
    # elif piece==exception1:
        # kernel = (1,2)
        # image, mask = computer_text_generator.generate(
        # text=piece,
        # font=font,
        # text_color="#FFFFFF",
        # font_size=size,
        # orientation=0,
        # space_width=1.0,
        # character_spacing=0,
        # fit=False,
        # word_split=True
        # )
        
        # new_width = int(
        #     image.size[0]
        #     * (float(size - vertical_margin) / float(image.size[1]))
        # )
        # resized_mask = mask.resize((new_width, size - vertical_margin), Image.Resampling.NEAREST)
        # background_width = new_width + horizontal_margin
        # background_height = size
        # background_mask = Image.new("RGB", (background_width, background_height), (0, 0, 0))
        # background_mask.paste(resized_mask, (5,5))
        # background_mask = background_mask.convert("RGB")
        # gaussian_filter = ImageFilter.GaussianBlur(radius=0)
        # final_mask = background_mask.filter(gaussian_filter)
        # bboxes = mask_to_bboxes(final_mask)[0]
        # width_orig = abs(bboxes[2]-bboxes[0])
    # else:
    kernel = (2,1)
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)
    boxlist = []
    for cnt in contours:
      x, y, w, h = cv2.boundingRect(cnt)
      boxlist.append([x,y,w,h])
      # Drawing a rectangle on copied image
    #   cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    coord = None
    if piece == exception and modifier in [vowel_symbols[i] for i in post_index]:
        boxlist = sorted(boxlist,key=lambda x:x[0]+x[2],reverse=True)
        max = boxlist[0]
        min = sorted(boxlist,key=lambda x:x[0],reverse=False)[0]
        max_y = max[3] if max[3]>min[3] else min[3]
        coord = [min[0],max[1],imgsize[1]-max[2]-min[0],max_y]
    
    elif piece == exception and modifier in [vowel_symbols[i] for i in pre_index]:
        boxlist = sorted(boxlist,key=lambda x:x[0]+x[2],reverse=True)
        max = boxlist[0]
        min = sorted(boxlist,key=lambda x:x[0],reverse=False)[0]
        max_y = max[3] if max[3]>min[3] else min[3]
        coord = [min[0]+min[2],max[1],imgsize[1]-min[2]-min[0],max_y]

    # elif piece == exception1 and modifier in [vowel_symbols[i] for i in post_index]:
    #     img_orig = np.asarray(image,"uint8")
    #     gray1 = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
    #     ret, thresh2 = cv2.threshold(gray1, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    #     contours1, hierarchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL,
    #                                                 cv2.CHAIN_APPROX_NONE)
    #     boxlist1 = []
    #     for cnt in contours1:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         boxlist1.append([x,y,w,h])
    #     max_orig = sorted(boxlist1,key=lambda x:x[2],reverse=True)[0]
    #     cv2.rectangle(img_orig, (max_orig[0],max_orig[1]),(max_orig[0]+max_orig[2],max_orig[1]+max_orig[3]), (255, 255, 255), 1)
    #     width_orig = max_orig[2]
    #     print(width_orig)
    #     if len(boxlist)>1:
    #         max = sorted(boxlist,key=lambda x:x[2],reverse=True)[0]
    #     else:
    #         max = boxlist[0]
    #     print(max)
    #     coord = [max[0],max[1],width_orig,max[3]]

    elif piece in exception_list:
        max = None
        boxlist = sorted(boxlist,key=lambda x:x[2],reverse=True)
        max = boxlist[0]
        boxlist = sorted(boxlist,key=lambda x:x[0],reverse=False)
        if piece==exception_list[-1]:
            j=boxlist.index(max)+2
        else:
            j=boxlist.index(max)+1
        max_y = max[3] if max[3]>boxlist[j][3] else boxlist[j][3]
        coord = [max[0],max[1],boxlist[j][0]+boxlist[j][2]-max[0],max_y]

    else:
        for ele in boxlist:
            if imgsize[1]*0.5<=ele[2]<=imgsize[1]*0.95:
                print((ele[2]/imgsize[1]) * 100)
                coord = ele
    # if coord is not None:
    #     cv2.rectangle(img, (coord[0],coord[1]),(coord[0]+coord[2],coord[1]+coord[3]), (0, 255, 0), 1)
    # cv2.imshow("frame",np.asarray(img))
    # cv2.imshow("dilation",img_orig)
    # if cv2.waitKey():
    #     cv2.destroyAllWindows()
    if coord is None:
        cv2.imwrite("problem.jpg",img)
        for ele in boxlist:
            print("bad",(ele[2]/imgsize[1]) * 100)
            cv2.rectangle(img, (ele[0],ele[1]),(ele[0]+ele[2],ele[1]+ele[3]), (0, 255, 0), 1)
        cv2.imshow("frame",img)
        if cv2.waitKey():
            cv2.destroyAllWindows()
    return coord
# print(mid_bboxes(cv2.imread("problem.jpg"),"જ","ો"))

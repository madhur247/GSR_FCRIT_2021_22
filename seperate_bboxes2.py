import os
import cv2
# from trdg import computer_text_generator_gujarati as computer_text_generator 
# from PIL import Image, ImageFilter
from Seperator import get_seperator
from mid_layer import mid_bboxes
# from trdg.utils import mask_to_bboxes
folder = "./latest_dataset4"
folder1 = "./dataset_rectified2"
files = os.listdir(folder)
if not os.path.exists(folder1):
    os.mkdir(folder1)
txtfiles = []
exception_list = ["જા","જી","જો","જૌ","રુ","રૂ","હૃ"]
inclusion_list = ["આ","એ","ઐ","ઓ","ઔ"]
charfile = open("./characters2.txt","r").read()
modfile = open("./modifiers.txt","r").read()
vowelfile = open("./characters1.txt","r").read()
numfile = open("./numbers.txt","r").read()
numbers = numfile.split("\n")[0].split()+numfile.split("\n")[1].split()
vowels = vowelfile.split()[:-6]
vowels.pop(1)
chardict = {}
chars = charfile.split()+modfile.split()+vowels+numbers
charlist = []
size=64
vertical_margin = horizontal_margin = 10
imgfiles = []
vowel_symbols = ['ા', 'િ', 'ી', 'ુ', 'ૂ', 'ે', 'ૈ', 'ો', 'ૌ', 'ં', 'ઃ', 'ૃ']
font_path = os.path.join("/home/madhur/.virtualenvs/miniproj6/lib/python3.8/site-packages/trdg", "fonts/gu")
font = os.path.join(font_path,os.listdir(font_path)[0])
pre_index = [1]
post_index = [0,2,7,8,10]
down_index = [3,4,11]
up_index = [5,6,9]
for i,char in enumerate(chars):
    chardict[char] = str(i)
    charlist.append(char+"\n")
charlist[-1] = charlist[-1].replace("\n","")
# print(len(charlist))
print(chars)
for file in files:
    if file.endswith(".txt"):
        txtfiles.append(file)
    else:
        imgfiles.append(file)
for wcount,txt in enumerate(txtfiles):
    file = open(os.path.join(folder,txt),"r")
    coords = file.readlines()
    value = txt.split("_")[0]
    img_name = value+"_"+txt.split("_")[1]+".jpg"
    img = cv2.imread(os.path.join(folder,img_name))
    imgsize = img.shape
    val = value.replace("\n","")
    print(val)
    writelin = []
    count = 0
    seperator_coords = get_seperator(img)
    wfile = open(os.path.join(folder1, "image" + str(wcount) + ".txt"), "w+")
    for word in val.split(' '):
        i = 0
        while i<len(word):
            ele = word[i]
            splitted_text = False
            if ele in vowel_symbols:
                i+=1
                continue
            piece, j = ele, i + 1
            coord = list(map(int,coords[count].split()))
            width_comp = abs(coord[0]-coord[2])
            if (j<len(word) and word[j] in vowel_symbols) or (j<=len(word) and ele in inclusion_list):
                # print(ele,count)
                if ele in inclusion_list:
                    # print("yes")
                    piece = vowels[0]
                    if ele==inclusion_list[0]:
                        modif = vowel_symbols[0]
                    elif ele==inclusion_list[1]:
                        modif = vowel_symbols[5]
                    elif ele==inclusion_list[2]:
                        modif = vowel_symbols[6]
                    elif ele==inclusion_list[3]:
                        modif = vowel_symbols[7]
                    elif ele==inclusion_list[4]:
                        modif = vowel_symbols[8]
                else:
                    modif = word[j]
                splitted_text = True
                new_bbox1 = []
                new_bbox2 = []
                new_bbox3 = []
                ind1 = -1
                ind2 = -1
                ind3 = -1
                # print("word",piece)
                # piece += ele[j]
                line = ""
                # image, mask = computer_text_generator.generate(
                # text=piece,
                # font=font,
                # text_color="#282828",
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
                
                if (modif in [vowel_symbols[k] for k in post_index]) and (piece+modif not in exception_list):
                    crop = img[seperator_coords[0][0][1]:seperator_coords[1][0][0],coord[0]:coord[2]]
                    bboxes = mid_bboxes(crop,piece,modif)
                    if bboxes is None:
                        print(piece,modif)
                        exit()
                    width_orig = bboxes[2]
                    ind1 = chardict.get(piece)
                    if modif==vowel_symbols[10]:
                        ind2 = chardict.get(vowel_symbols[10])
                    else:
                        ind2 = chardict.get(vowel_symbols[0])
                    if modif in [vowel_symbols[k] for k in [2,7,8]]:
                        new_bbox1 = [coord[0],seperator_coords[0][0][1],coord[0]+width_orig,coord[3]]
                        new_bbox2 = [coord[0]+width_orig,seperator_coords[0][0][1],coord[2]+1,coord[3]]
                        if modif==vowel_symbols[2]:
                            ind3 = chardict.get(modif)
                        elif modif==vowel_symbols[7]:
                            ind3 = chardict.get(vowel_symbols[5])
                        elif modif==vowel_symbols[8]:
                            ind3 = chardict.get(vowel_symbols[6])
                        new_bbox3 = [coord[0],coord[1],coord[2],seperator_coords[0][0][1]]
                    else:
                        new_bbox1 = [coord[0],coord[1],coord[0]+width_orig,coord[3]]
                        new_bbox2 = [coord[0]+width_orig,coord[1],coord[2],coord[3]]
                        if modif==vowel_symbols[10]:
                            new_bbox2 = [coord[0]+width_orig-1,coord[1],coord[2]+1,coord[3]]

                elif modif in [vowel_symbols[k] for k in pre_index] and (piece+modif not in exception_list):
                    crop = img[seperator_coords[0][0][1]:seperator_coords[1][0][0],coord[0]:coord[2]]
                    bboxes = mid_bboxes(crop,piece,modif)
                    if bboxes is None:
                        print(piece,modif)
                        exit()
                    width_orig = bboxes[2]
                    ind1 = chardict.get(piece)
                    ind2 = chardict.get(vowel_symbols[0])
                    new_bbox1 = [coord[2]-width_orig,seperator_coords[0][0][1],coord[2],coord[3]]
                    new_bbox2 = [coord[0],seperator_coords[0][0][1],coord[2]-width_orig,coord[3]]
                    ind3 = chardict.get(modif)
                    new_bbox3 = [coord[0],coord[1],coord[2],seperator_coords[0][0][1]]

                elif modif in [vowel_symbols[k] for k in up_index] and (piece+modif not in exception_list):
                    ind1 = chardict.get(piece)
                    new_bbox1 = [coord[0],seperator_coords[0][0][1],coord[2],coord[3]]
                    ind3 = chardict.get(modif)
                    new_bbox3 = [coord[0],coord[1],coord[2],seperator_coords[0][0][1]]

                elif modif in [vowel_symbols[k] for k in down_index] and (piece+modif not in exception_list):
                    ind1 = chardict.get(piece)
                    new_bbox1 = [coord[0],coord[1],coord[2],seperator_coords[1][0][1]]
                    ind3 = chardict.get(modif)
                    new_bbox3 = [coord[0],seperator_coords[1][0][1],coord[2],coord[3]]

                if len(new_bbox1)>0:
                    xmin = min([new_bbox1[0],new_bbox1[2]])
                    xmax = max([new_bbox1[0],new_bbox1[2]])
                    ymin = min([new_bbox1[1],new_bbox1[3]])
                    ymax = max([new_bbox1[1],new_bbox1[3]])
                    xcen = abs(xmin+xmax)/2/imgsize[1]
                    ycen = abs(ymin+ymax)/2/imgsize[0]
                    w = abs(xmax - xmin)/imgsize[1]
                    h = abs(ymax - ymin)/imgsize[0]
                    line = " ".join([ind1,str(xcen),str(ycen),str(w),str(h)])
                    line += "\n"
                    writelin.append(line)
                    # print(line)

                if len(new_bbox2)>0:
                    xmin = min([new_bbox2[0],new_bbox2[2]])
                    xmax = max([new_bbox2[0],new_bbox2[2]])
                    ymin = min([new_bbox2[1],new_bbox2[3]])
                    ymax = max([new_bbox2[1],new_bbox2[3]])
                    xcen = abs(xmin+xmax)/2/imgsize[1]
                    ycen = abs(ymin+ymax)/2/imgsize[0]
                    w = abs(xmax - xmin)/imgsize[1]
                    h = abs(ymax - ymin)/imgsize[0]
                    line = " ".join([ind2,str(xcen),str(ycen),str(w),str(h)])
                    line += "\n"
                    writelin.append(line)
                    # print(line)

                if len(new_bbox3)>0:
                    xmin = min([new_bbox3[0],new_bbox3[2]])
                    xmax = max([new_bbox3[0],new_bbox3[2]])
                    ymin = min([new_bbox3[1],new_bbox3[3]])
                    ymax = max([new_bbox3[1],new_bbox3[3]])
                    xcen = abs(xmin+xmax)/2/imgsize[1]
                    ycen = abs(ymin+ymax)/2/imgsize[0]
                    w = abs(xmax - xmin)/imgsize[1]
                    h = abs(ymax - ymin)/imgsize[0]
                    line = " ".join([ind3,str(xcen),str(ycen),str(w),str(h)])
                    line += "\n"
                    writelin.append(line)
                    # print(line)
                if ele not in inclusion_list:
                    i = j
                
            if (j<len(word) and word[j] not in vowel_symbols and not splitted_text) or (i==len(word)-1 and not splitted_text) or (j<len(word) and piece+word[j] in exception_list):
                if j<len(word) and piece+word[j] in exception_list:
                    ind = chardict.get(piece+word[j])
                else:
                    ind = chardict.get(word[i])
                # print(word[i])
                xmin = min([coord[0],coord[2]])
                xmax = max([coord[0],coord[2]])
                ymin = min([coord[1],coord[3]])
                ymax = max([coord[1],coord[3]])
                xcen = abs(xmin+xmax)/2/imgsize[1]
                ycen = abs(ymin+ymax)/2/imgsize[0]
                w = abs(xmax - xmin)/imgsize[1]
                h = abs(ymax - ymin)/imgsize[0]
                line = " ".join([ind,str(xcen),str(ycen),str(w),str(h)])
                line+="\n"
                writelin.append(line)
                i=j-1
            count+=1
            i+=1
        if count<len(coords):
            coord = list(map(int,coords[count].split()))
            ind = chardict.get("Space")
            xmin = min([coord[0],coord[2]])
            xmax = max([coord[0],coord[2]])
            ymin = min([coord[1],coord[3]])
            ymax = max([coord[1],coord[3]])
            xcen = abs(xmin+xmax)/2/imgsize[1]
            ycen = abs(ymin+ymax)/2/imgsize[0]
            w = abs(xmax - xmin)/imgsize[1]
            h = abs(ymax - ymin)/imgsize[0]
            line = " ".join([ind,str(xcen),str(ycen),str(w),str(h)])
            line+="\n"
            writelin.append(line)
            count+=1

    wfile.writelines(writelin)
    # print(len(writelin))
    print(wcount)
    cv2.imwrite(os.path.join(folder1, "image" + str(wcount) + ".jpg"),img)
print(len(txtfiles))
spacefile = open("./space.names","w+")
spacefile.writelines(charlist)
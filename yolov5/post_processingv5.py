from yolov5_output import run_yolov5
from IOU import calculate_iou

# img_path = "testing_images/021 ૮૦૧૫ ૫૪૩૮ છૌનુઋઆ ઔઉદ 387 628 ઞનઅઃખ ચઅંપાદો થષઋ_32.jpg"
# spacefile = "space.names"
# weights_path = "./YoloV5_model2/yolov5x_latest_8000/weights/best.pt"
# conf_threshold = 0.55
# iou_threshold = 0.5
def post_process(img_path,weights_path,conf_threshold,iou_threshold,spacefile):
    result = run_yolov5(img_path,weights_path,conf_threshold,iou_threshold,spacefile)
    vowel_symbols = ['ા', 'િ', 'ી', 'ુ', 'ૂ', 'ે', 'ૈ', 'ો', 'ૌ', 'ં', 'ઃ', 'ૃ']
    exception = "અ"
    exceptions = ['આ','એ','ઐ','ઓ','ઔ']
    # pre_index = [1]
    post_index = [0,10]
    down_index = [3,4,11]
    up_index = [5,6,9,2,1]
    upper_region = []
    middle_region = []
    lower_region = []
    root_letters = []
    final_result = {}
    for ele in result:
        if ele[0] in [vowel_symbols[x] for x in up_index]:
            upper_region.append(ele+[None])
        elif ele[0] in [vowel_symbols[x] for x in down_index]:
            lower_region.append(ele+[None])
        elif ele[0] in [vowel_symbols[x] for x in post_index]:
            middle_region.append(ele+[None])
        elif ele[0] not in vowel_symbols:
            root_letters.append(ele+[0])

    upper_region.sort(key=lambda x:x[1][0])
    middle_region.sort(key=lambda x:x[1][0])
    lower_region.sort(key=lambda x:x[1][0])
    root_letters.sort(key=lambda x:x[1][0])

    # print(upper_region)
    # print(lower_region)
    # print(middle_region)
    # print(root_letters)

    for j,ele in enumerate(upper_region):
        min_upper = None
        for i,ele1 in enumerate(root_letters):
            dist = abs(((ele[1][0]+ele[1][2])/2) - ((ele1[1][0]+ele1[1][2])/2))
            if min_upper is None or min_upper[0]>dist:
                min_upper = [dist,ele[0],i,j]
        if root_letters[min_upper[2]][3] != 1:
            if root_letters[min_upper[2]][0] == exception and upper_region[min_upper[-1]][0] in vowel_symbols[5:7]:
                final_letter = ""
                if upper_region[min_upper[-1]][0] == vowel_symbols[5]:
                    final_letter = exceptions[1]
                elif upper_region[min_upper[-1]][0] == vowel_symbols[6]:
                    final_letter = exceptions[2]
                final_result[root_letters[min_upper[2]][1][0]] = final_letter
            else:
                final_result[root_letters[min_upper[2]][1][0]] = root_letters[min_upper[2]][0]+min_upper[1]
            root_letters[min_upper[2]][3] = 1
            upper_region[min_upper[-1]][-1] = min_upper[2]
    # print(final_result)
    # print(upper_region)
    # exit()
    for j,ele in enumerate(lower_region):
        min_lower = None
        for i,ele1 in enumerate(root_letters):
            dist = abs(((ele[1][0]+ele[1][2])/2) - ((ele1[1][0]+ele1[1][2])/2))
            if min_lower is None or min_lower[0]>dist:
                min_lower = [dist,ele[0],i,j]
        if root_letters[min_lower[2]][3] != 1:
            final_result[root_letters[min_lower[2]][1][0]] = root_letters[min_lower[2]][0]+min_lower[1]
            root_letters[min_lower[2]][3] = 1
            lower_region[min_lower[-1]][-1] = min_lower[2]
    # print(final_result)
    # print(lower_region)
    # exit()

    for j,ele in enumerate(middle_region):
        max_iou = None
        if ele[0]==vowel_symbols[0]:
            for i,ele1 in enumerate(upper_region):
                new_middle = ele[1]
                new_middle[1] = 0
                iou = calculate_iou(ele1[1],new_middle)
                if (iou!=0) and (max_iou is None or max_iou[0]<iou):
                    max_iou = [iou,i,j,ele[0]]

        if max_iou is not None:
            # print(max_iou)
            k = vowel_symbols.index(upper_region[max_iou[1]][0])
            if k in [5,6]:
                new_k = k+2
                if final_result.get(root_letters[upper_region[max_iou[1]][-1]][1][0]) is None:
                    raise Exception("Errors!!! Stop right there!!!")
                if root_letters[upper_region[max_iou[1]][-1]][0] == exception:
                    final_letter = ""
                    if k == 5:
                        final_letter = exceptions[3]
                    elif k == 6:
                        final_letter = exceptions[4]
                    final_result[root_letters[upper_region[max_iou[1]][-1]][1][0]] = final_letter
                else:
                    final_result[root_letters[upper_region[max_iou[1]][-1]][1][0]] = root_letters[upper_region[max_iou[1]][-1]][0]+vowel_symbols[new_k]
                middle_region[max_iou[2]][-1] = upper_region[max_iou[1]][-1]
            elif k in [1,2]:
                middle_region[max_iou[2]][-1] = upper_region[max_iou[1]][-1]
        else:
            min_middle = None
            for i,ele1 in enumerate(root_letters):
                dist = ((ele[1][0]+ele[1][2])/2) - ((ele1[1][0]+ele1[1][2])/2)
                if dist<0:
                    break
                if min_middle is None or min_middle[0]>dist:
                    min_middle = [dist,ele[0],i,j]
            if root_letters[min_middle[2]][3] != 1:
                if root_letters[min_middle[2]][0] == exception and middle_region[min_middle[-1]][0] == vowel_symbols[0]:
                    final_letter = exceptions[0]
                    final_result[root_letters[min_middle[2]][1][0]] = final_letter
                else:
                    final_result[root_letters[min_middle[2]][1][0]] = root_letters[min_middle[2]][0]+min_middle[1]
                root_letters[min_middle[2]][3] = 1
                middle_region[min_middle[-1]][-1] = min_middle[2]

    # print(final_result)
    # print(middle_region)
    # exit()
    # print(root_letters)
    for i,ele in enumerate(root_letters):
        if ele[-1]==0 and final_result.get(ele[1][0]) is None:
            if ele[0]!="Space":
                final_result[ele[1][0]] = ele[0]
            else:
                final_result[ele[1][0]] = " "
    # print(final_result)
    # print(sorted(list(final_result.items()),key=lambda x:x[0]))
    return "".join([v for k,v in sorted(list(final_result.items()),key=lambda x:x[0])]).strip()


    
        




import pathlib
import os
import numpy as np
import cv2
import glob


def origin_text_coordiction_map(origin_text, scale):
    '''
    从pdf解析的在pdf上的坐标，映射到图片上的坐标
    :param origin_text:dict
    :param scale: float
    :return: dict
    '''
    maped_origin_text = origin_text.copy()
    text_infos = origin_text["text_infos"]
    maped_text_infos = []
    for text_info in text_infos:
        maped_text_info = {}
        maped_text_rectangle = {}
        text_rectangle = text_info["text_rectangle"]
        text = text_info["text"]
        llx = text_rectangle["llx"]
        lly = text_rectangle["lly"]
        urx = text_rectangle["urx"]
        ury = text_rectangle["ury"]
        maped_llx = int(llx * scale)
        maped_lly = int(lly * scale)
        maped_urx = int(urx * scale)
        maped_ury = int(ury * scale)
        maped_text_rectangle["llx"] = maped_llx
        maped_text_rectangle["lly"] = maped_lly
        maped_text_rectangle["urx"] = maped_urx
        maped_text_rectangle["ury"] = maped_ury
        maped_text_info["text"] = text
        maped_text_info["text_rectangle"] = maped_text_rectangle
        maped_text_infos.append(maped_text_info)
    maped_origin_text["text_infos"] = maped_text_infos
    return maped_origin_text


def coordition_four_map_eight(text_rectangle):
    '''
    从4坐标映射到8坐标
    :param text_rectangle:
    :return: []
    '''
    llx = text_rectangle["llx"]
    lly = text_rectangle["lly"]
    urx = text_rectangle["urx"]
    ury = text_rectangle["ury"]
    x1, y1 = llx, lly
    x2, y2 = urx, lly
    x3, y3 = urx, ury
    x4, y4 = llx, ury
    return [x1, y1, x2, y2, x3, y3, x4, y4]


def generator_data_from_origin_text(origin_text, scale, file_name, page_num, save_dir="/data-hdd/LingYue/ocr_data/txt"):
    '''
    从pdf解析结果 生成ocr训练数据
    :param origin_text:
    :return:
    '''
    origin_text = origin_text_coordiction_map(origin_text, scale)
    text_infos = origin_text["text_infos"]
    write_file_path = os.path.join(save_dir, file_name + "_" + str(page_num) + ".txt")
    if os.path.exists(write_file_path):
        os.remove(write_file_path)
    with open(write_file_path, mode="a+", encoding="utf-8") as f:
        for text_info in text_infos:
            text = text_info["text"]
            text_rectangle = text_info["text_rectangle"]
            text_rectangle = coordition_four_map_eight(text_rectangle)
            text_rectangle = np.array(text_rectangle).astype(str)
            in_file_text = ",".join(text_rectangle) + "," + text
            f.write(in_file_text)
            f.write("\n")


def draw_rect_to_img(origin_text_path, img_path, save_dir="/data-hdd/LingYue/ocr_data"):
    d = pathlib.Path(origin_text_path)
    file_name = d.stem
    bboxes = []
    texts = []
    with open(origin_text_path, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if len(line) > 0:
                splited_line = line.split(",")
                if len(splited_line) > 0:
                    box = list(map(int, splited_line[:8]))
                    bboxes.append(box)
                    text = str(splited_line[8])
                    texts.append(text)
    img = cv2.imread(img_path)
    real_write_file_path = os.path.join(save_dir, "img", file_name + ".jpg")
    cv2.imwrite(real_write_file_path, img)
    for box in bboxes:
        box = np.reshape(box, (4, 2))
        cv2.drawContours(img, [box], -1, (255, 0, 0), 2)
    bboxes_write_file_path = os.path.join(save_dir, "mask", file_name + "_result.jpg")
    print(file_name)
    cv2.imwrite(bboxes_write_file_path, img)


def analysis_bbox_to_img(ocr_text_dir):
    for path in glob.glob(os.path.join(ocr_text_dir, "*.txt"), recursive=True):
        d = pathlib.Path(path)
        file_name = d.stem
        splited_file_name = file_name.split("_")
        ship_company = splited_file_name[0]
        img_name = splited_file_name[1]
        page_num = splited_file_name[2]
        img_dir = os.path.join("/data-hdd/LingYue/booking_confirmation/base_class", ship_company, "doc2img")
        real_img_name = str(page_num) + "#" + str(img_name) + ".jpg"
        img_path = os.path.join(img_dir, real_img_name)
        draw_rect_to_img(path, img_path)
        print("deal end ", path)


def from_file_find_bboxes_and_text(file_path):
    bboxes = []
    texts = []
    with open(file_path, encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if len(line) > 0:
                splited_line = line.split(",")
                if len(splited_line) > 0:
                    box = list(map(int, splited_line[:8]))
                    bboxes.append(box)
                    text = str(splited_line[8]).strip("\n")
                    texts.append(text)
    return bboxes, texts


def generator_crnn_data_from_box_to_img(ocr_data_dir):
    save_lable_path = os.path.join(ocr_data_dir, "crnn_less_20_txt", "gen.txt")
    save_img_dir = os.path.join(ocr_data_dir, "crnn_less_20_img")
    text_dir = os.path.join(ocr_data_dir, "txt")
    img_dir = os.path.join(ocr_data_dir, "img")
    with open(save_lable_path, "a+", encoding="utf-8") as f:
        for path in glob.glob(os.path.join(text_dir, "*.txt"), recursive=True):
            d = pathlib.Path(path)
            file_name = d.stem
            img_path = os.path.join(img_dir, file_name + ".jpg")
            img = cv2.imread(img_path)
            bboxes, texts = from_file_find_bboxes_and_text(path)
            for i in range(len(bboxes)):
                box = bboxes[i]
                text = texts[i]

                img_id = i + 1
                if len(text) <= 71:
                    try:
                        cropped_img, (topleft_x, topleft_y, bot_right_x, bot_right_y) = crop_4(img, box)
                        this_img_path = os.path.join(save_img_dir, file_name + "_croped_" + str(img_id) + ".jpg")
                        cv2.imwrite(this_img_path, cropped_img)
                        f.write(file_name + "_croped_" + str(img_id) + ".jpg★✿★" + text)
                        f.write("\n")
                    except Exception as e:
                        continue
            print("deal end " + path)


def crop_4(img, bbox):
    img_h, img_w = img.shape[:2]
    bbox = np.reshape(bbox, (4, 2))
    topleft_x = np.min(bbox[:, 0])
    topleft_y = np.min(bbox[:, 1])
    bot_right_x = np.max(bbox[:, 0])
    bot_right_y = np.max(bbox[:, 1])
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#测试使用
    topleft_x = topleft_x - 1 if (topleft_x - 1) > 0 else 0
    bot_right_x = bot_right_x + 1 if (bot_right_x + 1) < img_w else img_w
    topleft_y = topleft_y - 3 if (topleft_y - 3) > 0 else 0
    bot_right_y = bot_right_y + 3 if (bot_right_y + 3) < img_h else img_h
    cropped_img = img[topleft_y:bot_right_y, topleft_x:bot_right_x]
    h, w, _ = cropped_img.shape
    # print("h,w",h,w)
    if h > 32.0:
        scale = h / 32.0
        new_w, new_h = int(w / scale), int(h / scale)
        # print(new_w,new_h)
        if new_w > 720:
            cropped_img = cv2.resize(cropped_img, (0, 0), fx=720 / w, fy=new_h / h, interpolation=cv2.INTER_AREA)
        else:
            cropped_img = cv2.resize(cropped_img, (0, 0), fx=new_w / w, fy=new_h / h, interpolation=cv2.INTER_AREA)
            cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, 0, (720 - new_w), cv2.BORDER_CONSTANT,
                                             value=(255, 255, 255))
    else:
        top_dis = int((32 - h) / 2)
        bot_dis = (32 - h) - top_dis
        cropped_img = cv2.copyMakeBorder(cropped_img, top_dis, bot_dis, 0, 0, cv2.BORDER_CONSTANT,
                                         value=(255, 255, 255))
        if w > 720:
            cropped_img = cv2.resize(cropped_img, (0, 0), fx=720 / w, fy=1, interpolation=cv2.INTER_AREA)
        else:
            cropped_img = cv2.copyMakeBorder(cropped_img, 0, 0, 0, (720 - w), cv2.BORDER_CONSTANT,
                                             value=(255, 255, 255))

    return cropped_img, (topleft_x, topleft_y, bot_right_x, bot_right_y)


def remove_no_parse_file(save_dir, no_parse_list):
    img_dir = os.path.join(save_dir, "crnn_img_resize")
    save_path = os.path.join(save_dir, "crnn_txt_resize", "gen_cleared.txt")
    txt_path = os.path.join(save_dir, "crnn_txt_resize", "gen.txt")
    for no_parse_info in no_parse_list:
        img_name = no_parse_info.split("★✿★")[0]
        img_path = os.path.join(img_dir, img_name)
        if os.path.exists(img_path):
            os.remove(img_path)
            print("删除图片:" + img_path)
    cleared_txt = []
    with open(txt_path, encoding="utf-8") as f:
        lines = f.readlines()
        for no_parse_info in no_parse_list:
            if no_parse_info in lines:
                lines.remove(no_parse_info)
                print("删除信息：" + no_parse_info)
        with open(save_path, "a+", encoding="utf-8") as file:
            for line in lines:
                line = line.strip("\n")
                file.write(line)
                file.write("\n")

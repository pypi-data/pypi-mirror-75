'''
    File name: utils.py.py
    Author: [Qoala Ds Team]
    Date created: / /2019
    Date last modified: //2020
    Python Version: >= 3.5
    Qoaladep version: v0.2
    Maintainer: [Qoala Ds Team]
'''
import cv2 
import random
import numpy as np 


def nms(result_detection: [float], 
        confidence_threshold=0.75, 
        overlap_threshold=0.3) -> [float]:
    """[summary]
    
    Arguments:
        result_detection {[type]} -- [description]
    
    Keyword Arguments:
        confidence_threshold {float} -- [description] (default: {0.75})
        overlap_threshold {float} -- [description] (default: {0.3})
    
    Returns:
        [float] -- [description]
    """    

    result_box = []
    result_conf = []
    result_class = []
    final_bbox = []
    final_class_prob = []

    array_shape = result_detection.shape
    class_num = array_shape[2] - 5
    
    for boxes in result_detection:
        mask = boxes[:, 4] > confidence_threshold
        boxes = boxes[mask, :] 
        classes = np.argmax(boxes[:, 5:], axis=-1)
        classes = classes.astype(np.float32).reshape((classes.shape[0], 1))
        classes_prob = np.max(boxes[:, 5:], axis=-1)
        classes_prob = classes_prob.astype(np.float32).reshape((classes_prob.shape[0], 1))
        boxes = np.concatenate((boxes[:, :5], classes, classes_prob), axis=-1)

        boxes_dict = dict()
        for cls in range(class_num):
            mask = (boxes[:, 5] == cls)
            mask_shape = mask.shape
                
            if np.sum(mask.astype(np.int)) != 0:
                class_boxes = boxes[mask, :]
                boxes_coords = class_boxes[:, :4]
                boxes_ = boxes_coords.copy()
                boxes_[:, 2] = (boxes_coords[:, 2] - boxes_coords[:, 0])
                boxes_[:, 3] = (boxes_coords[:, 3] - boxes_coords[:, 1])
                boxes_ = boxes_.astype(np.int)
                    
                boxes_conf_scores = class_boxes[:, 4:5]
                boxes_conf_scores = boxes_conf_scores.reshape((len(boxes_conf_scores)))
                the_class = class_boxes[:, 5:6]
                the_class_prob = class_boxes[:, 6:]

                result_box.extend(boxes_.tolist())
                result_conf.extend(boxes_conf_scores.tolist())
                result_class.extend(the_class.tolist())
                final_class_prob.extend(the_class_prob.tolist())
        
    indices = cv2.dnn.NMSBoxes(result_box, result_conf, confidence_threshold, overlap_threshold)
    for i in indices:
        i = i[0]
        box = result_box[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        conf = result_conf[i]
        the_class = result_class[i][0]
        the_class_prob = final_class_prob[i][0]
        final_bbox.append([left, top, width, height, conf, the_class, the_class_prob])
    return final_bbox


def nms_ml(batch, main_class_num, multilabel_dict, 
            confidence_threshold=0.5,
            overlap_threshold=0.5):
        """[summary]

        Arguments:
            batch {[type]} -- [description]
            main_class_num {[type]} -- [description]
            multilabel_dict {[type]} -- [description]

        Keyword Arguments:
            confidence_threshold {float} -- [description] (default: {0.5})
            overlap_threshold {float} -- [description] (default: {0.5})

        Returns:
            [type] -- [description]
        """        
        result_box = []
        result_conf = []
        result_class = []
        result_class_prob = []
        final_box = []
        result_class_ml = []
        
        for boxes in batch:
            mask = boxes[:, 4] > confidence_threshold
            boxes = boxes[mask, :] 
            classes = np.argmax(boxes[:, 5:5+main_class_num], axis=-1)
            classes = classes.astype(np.float32).reshape((classes.shape[0], 1))
            classes_prob = np.max(boxes[:, 5:5+main_class_num], axis=-1)
            classes_prob = classes_prob.astype(np.float32).reshape((classes_prob.shape[0], 1))
            boxes_new = np.concatenate((boxes[:, :5], classes, classes_prob), axis=-1)

            for i in multilabel_dict: 
                base = 5+main_class_num
                tmp = np.argmax(boxes[:, base:base + multilabel_dict[i]], axis=-1)
                tmp = tmp.astype(np.float32).reshape((tmp.shape[0], 1))
                tmp_prob = np.max(boxes[:, base:base + multilabel_dict[i]], axis=-1)
                tmp_prob = tmp_prob.astype(np.float32).reshape((classes_prob.shape[0], 1))
                boxes_new = np.concatenate((boxes_new, tmp, tmp_prob), axis=-1)
                base = base + multilabel_dict[i]

            boxes_dict = dict()
            for cls in range(main_class_num):
                mask = (boxes_new[:, 5] == cls)
                mask_shape = mask.shape
                
                if np.sum(mask.astype(np.int)) != 0:
                    class_boxes = boxes_new[mask, :]
                    boxes_coords = class_boxes[:, :4]
                    boxes_ = boxes_coords.copy()
                    boxes_[:, 2] = (boxes_coords[:, 2] - boxes_coords[:, 0])
                    boxes_[:, 3] = (boxes_coords[:, 3] - boxes_coords[:, 1])
                    boxes_ = boxes_.astype(np.int)
                    
                    boxes_conf_scores = class_boxes[:, 4:5]
                    boxes_conf_scores = boxes_conf_scores.reshape((len(boxes_conf_scores)))
                    the_class = class_boxes[:, 5:6]
                    the_class_prob = class_boxes[:, 6:7]
                    the_additional_class = class_boxes[:, 7:]

                    result_box.extend(boxes_.tolist())
                    result_conf.extend(boxes_conf_scores.tolist())
                    result_class.extend(the_class.tolist())
                    result_class_prob.extend(the_class_prob.tolist())
                    result_class_ml.extend(the_additional_class.tolist())
        
        indices = cv2.dnn.NMSBoxes(result_box, result_conf, confidence_threshold, overlap_threshold)
        for i in indices:
            i = i[0]
            box = result_box[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            conf = result_conf[i]
            the_class = result_class[i][0]
            the_class_prob = result_class_prob[i][0]
            the_additional_class = result_class_ml[i]
            final_box.append([left, top, width, height, conf, the_class, the_class_prob, the_additional_class])
        return final_box


def crop_image(image, bboxes: [[float]]) -> []:
        """[summary]
        
        Arguments:
            image {[type]} -- [description]
            bboxes {[type]} -- [[x1, y1, w, h, obj prob, class, class_prob], [], ...], Absolute to 416x416 size
        
        Returns:
            [] -- [description]
        """        
        h, w, c = image.shape
        crop_list = []

        for i in bboxes: 
            x1 = max(int(i[0] * w/416), 0) 
            y1 = max(int(i[1] * h/416), 0)
            w1 = int(i[2] * w/416) 
            h1 = int(i[3] * h/416)
            crop = image[y1:y1+h1, x1:x1+w1]
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            crop_list.append(crop)

        return crop_list 


def draw_rectangle(image, bboxes: [[int, int, int, int]]): 
    """[summary]

    Arguments:
        image {[type]} -- [description]
        bboxes {[type]} -- [description]
    """    
    for i in bboxes: 
        start_point = (int(i[0]), int(i[1]))
        end_point = (int(i[0] + i[2]), int(i[1] + i[3]))
        rg = random.randint(100, 255)
        rb = random.randint(0, 255)
        image = cv2.rectangle(image, start_point, end_point, (rg, rb, 125), thickness=2) 
        end_point = (int(i[0]), int(i[1] + i[3]/3.))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=5)
        end_point = (int(i[0] + i[2]/3.), int(i[1]))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=5)
        start_point = (int(i[0] + i[2]), int(i[1] + i[3]))
        end_point =  (int(i[0] + i[2]), int(i[1] + i[3]/1.5))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=5)
        end_point =  (int(i[0] + i[2]/1.5), int(i[1] + i[3]))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=5)

    return image


def resize_bboxes_based_img_size(bboxes: [[float]], 
                                img_shape: (int, int)): 
    """[summary]

    Args:
        bbox ([type]): [description]
        img_shape ([type]): [description]

    Returns:
        [int, int, int, int]: [description]
    """ 
    res = []         
    for i in bboxes:                      
        x = int((i[0]/416)*img_shape[1])
        y = int((i[1]/416)*img_shape[0])
        w = int((i[2]/416)*img_shape[1])
        h = int((i[3]/416)*img_shape[0])
        obj_prob = i[4]
        clss = i[5]
        clss_prob = i[6]
        res.append([x, y, w, h, obj_prob, clss, clss_prob])

    return res


from class_n.net import *
import torch
import cv2
import heapq
from PIL import Image

class model_2(object):
    def __init__(self, model_path, transform):
        self.model_path = model_path
        # 网络
        self.model = resnet50()
        # 加载预训练模型
        net_dict = self.model.state_dict()
        pretrained = torch.load(self.model_path)
        pretrained_dict = {}
        for k in pretrained.keys():
            pretrained_dict.update({k: pretrained[k]})
        net_dict.update(pretrained_dict)
        self.model.load_state_dict(net_dict)
        # 加载到GPU
        self.model.cuda()
        self.model.eval()

        self.transform_data = transform

    def test_img(self, img_path, flag, score_thr):
        if flag == True:
            img_test = cv2.imread(img_path)
        else:
            img_test = img_path
        # img_test = Image.fromarray(img_test)
        img_test = self.transform_data(img_test)
        img_test = torch.unsqueeze(img_test, 0)

        img_test = img_test.cuda()
        output = self.model(img_test)
        if torch.max(torch.softmax(output, 1)) < score_thr:
            doubt = 1
        else:
            doubt = 0
        output3 = output[0].cpu().data.numpy()
        top3 = heapq.nlargest(10, range(len(output3)), output3.take)
        return top3, doubt

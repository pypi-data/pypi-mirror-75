from mmdet.apis import init_detector,inference_detector
import numpy as np
import cv2
from detec.nms_iou import nms_iou

class subway_det(object):
    '''
        1.在任务启动时只需要实例化一次对象，实例化对象时，需要传入config_file,checkpoint_file
        2.之后向detector方法传入img即可返回测试结果
    '''
    def __init__(self,config_file,checkpoint_file,config):
        '''
        :param config_file: 定义网络结构的文件
        :param checkpoint_file: 训练好的网络模型
        '''
        self.net_model=init_detector(config_file,checkpoint_file,device='cuda:0')
        self.config=config

    def detector(self,img):
        '''
        :param img: opencv读取的图片，底层为numpy格式
        :return: result ,size=[n*6]，其中n为检测到的目标数量
                result[:,0]=目标类别
                result[:,1:4]=x_min,y_min,x_max,y_max
                result[:,5]=置信度
        '''
        self.det_result=inference_detector(self.net_model,img)
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(self.det_result)
        ]
        self.labels = np.concatenate(labels)
        self.labels=self.labels.reshape(self.config.num_roi,1)
        self.bboxes = np.vstack(self.det_result)
        self.result=np.hstack((self.labels,self.bboxes))

        # 基于重叠度的筛选
        nms_iou_detec=nms_iou(self.config.miji_thr,self.config.h_thr,self.config.nms_thr,self.config.num_thr)
        self.result=nms_iou_detec.mix_nms(self.result)

        return self.result
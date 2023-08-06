import os
import numpy as np
import glob

class nms_iou(object):
    def __init__(self, miji_thr=0.3, h_thr=0.3, nms_thr=0.05,num_thr=0):
        self.miji_thr=miji_thr
        self.h_thr=h_thr
        self.nms_thr=nms_thr
        # 输出第几个阈值的结果
        self.num_thr=num_thr

    def get_iou(self,bb, bbgt):
        bi = [max(bb[0], bbgt[0]), max(bb[1], bbgt[1]), min(bb[2], bbgt[2]), min(bb[3], bbgt[3])]
        iw = bi[2] - bi[0] + 1
        ih = bi[3] - bi[1] + 1
        if iw > 0 and ih > 0:
            # compute overlap (IoU) = area of intersection / area of union    #计算IOU
            ua = (bb[2] - bb[0] + 1) * (bb[3] - bb[1] + 1) + (bbgt[2] - bbgt[0]
                                                              + 1) * (bbgt[3] - bbgt[1] + 1) - iw * ih
            ov = iw * ih / ua
            return ov
            # 固定iou,小于阈值的直接去掉，后面再统计虚检和漏检
        else:
            return 0

    def nms(self,box_h, box_l, thr):
        box = np.concatenate((box_h, box_l))
        del_number = []
        for i in range(box_h.shape[0]):
            ov = np.zeros((1, box.shape[0]))
            for j in range(0, box.shape[0]):
                if j == i:
                    continue
                else:
                    ov[0, j] = self.get_iou(box[i], box[j])

            # 大于阈值的框
            idx = np.where(ov[0, :] > thr)
            idx = np.asarray(idx)
            for k in idx[0]:
                if k not in del_number and k > i:
                    del_number.append(k)
        box = np.delete(box, np.asarray(del_number), 0)
        return box

    def mix_nms(self,gt_lines_list):
        boxes=gt_lines_list[:,[1,2,3,4,5,0]]
        # 按照confidence大小排序
        boxes = boxes[boxes[:, 4].argsort()[::-1]]
        iou = np.zeros((boxes.shape[0], boxes.shape[0]), dtype=np.float16)
        for i in range(boxes.shape[0]):
            bbgt = boxes[i]
            for j in range(i, boxes.shape[0]):
                bb = boxes[j]
                ov = self.get_iou(bb, bbgt)
                if i == j:
                    ov = 1.5
                iou[i][j] = ov
                iou[j][i] = ov

        # 删除重复度过高的框
        del_list = []
        for i in range(boxes.shape[0]):
            if i in del_list:
                continue
            # 这里主要控制判定预测相同目标的阈值
            '''
                方案一，对于任意的框只要重叠率过高，都要去掉
                对于稍大的置信度较大时，删去其他框，不考虑类别
                置信度较低的则考虑类别
            '''
            iou_on = np.where((iou[:, i] > self.miji_thr) & (iou[:, i] < 1.3))
            for item in iou_on[0]:
                if item not in del_list:
                    del_list.append(item)
            iou_on = np.where((iou[:, i] > self.miji_thr * 0.85) & (iou[:, i] < self.miji_thr ))
            for item in iou_on[0]:
                if boxes[i, 4] > 0.7:
                    if item not in del_list:
                        del_list.append(item)
                else:
                    if boxes[i, 5] == boxes[item, 5] and item not in del_list:
                        del_list.append(item)
        del_list.sort()
        iou[np.asarray(del_list)] = 0

        # 计算每个框的平均iou
        iou_ave = np.zeros((1, 1000), dtype=np.float16)
        for i in range(iou.shape[0]):
            # 为了防止除0，相交面积大于1，所以要设定有效iou来筛选
            true_iou = np.where(iou[i] > 0.01)
            true_iou = np.asarray(list(true_iou))
            iou_ave[0, i] = np.sum(iou[i, true_iou]) / (true_iou.shape[1] + 1)

        # 输出结果
        '''
            整体思路：所有框都参与传统的nms，但是只有高分框会被用作主要的目标框，低分框和高分框都会被删减
        '''
        # 基于重叠率的选择
        iou_ave_idx = np.where(iou_ave[0] > 0.05 * self.num_thr)
        box_output = boxes[iou_ave_idx]

        # 传统nms主要是要控制高分的划分和nms删减iou的控制
        # 选出得分高的框
        box_con_h_idx = np.where(box_output[:, 4] > self.h_thr)
        # 低分框
        boxes_part = np.delete(box_output, box_con_h_idx, 0)

        # 只用高分框进行nms选择，但是删去的是所有的框
        box_con_h = box_output[box_con_h_idx]

        # 进行nms
        keep = self.nms(box_con_h, boxes_part, self.nms_thr)
        return keep



class Config(object):
    def __init__(self):
        # 数据
        self.size=224
        self.mean=[0.5, 0.5 ,0.5]
        self.std=[0.5, 0.5, 0.5]

        # 检测网络
        self.config_file='/home/cbird/work/net/mmdetection-master/configs/pascal_voc/cascade_rcnn_r50_fpn_1x+cascade.py'
        self.checkpoint_file='/home/cbird/work/net/mmdetection-master/work_dir/2020_1000_mix_4000/epoch_5.pth'
        self.num_roi=1000

        # nms_iou
        self.miji_thr=0.3
        self.h_thr=0.3
        self.nms_thr=0.05
        self.num_thr=0

        self.num_class=2
        # 粗粒度分类
        self.model_path_Coarse_grained='/media/cbird/新加卷1/miao/NS2/class/train-data/class-ba-sample/5.pkl'

        # 细粒度分类
        self.model_path_fine_grained='/media/cbird/新加卷1/miao/NS2/class/train-data/class-ba-sample/5.pkl'
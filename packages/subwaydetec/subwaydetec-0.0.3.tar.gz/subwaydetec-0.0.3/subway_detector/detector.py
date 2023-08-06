from detec.dete import subway_det
from class_n.class_n_model import model_n
from class_2.class_2_model import model_2
from data import data_detile
from config import Config
import cv2
import numpy as np
from PIL import Image

class detector(object):
    def __init__(self,config):
        self.config=config
        self.data=data_detile(self.config)
        # 加载检测模块
        self.sud_det=subway_det(self.config.config_file,self.config.checkpoint_file,self.config)

        # 加载粗粒度分类模块
        self.Coarse_grained_class=model_n(self.config.model_path_Coarse_grained,self.data.transforms)

        # 加载细粒度分类模块
        self.fine_grained_class=model_2(self.config.model_path_fine_grained,self.data.transforms)

    def detecte(self,img):
        self.result = []
        # 检测模块
        self.roi_list = self.sud_det.detector(img)
        # 将每一个roi输入分类网络
        for i in range(self.roi_list.shape[0]):
            box=self.roi_list[i,0:4]
            confidence=self.roi_list[i,-2]
            class_name=self.roi_list[i,-1]
            # 这里只对低分框进行在分类
            if float(confidence)>0.05:
                self.result.append(self.roi_list[i])
                continue
            else:
                box=box.astype(np.int)
                img_test=img[box[1]:box[3],box[0]:box[2],:]
                img_test = Image.fromarray(cv2.cvtColor(img_test,cv2.COLOR_BGR2RGB))
                img_test=img_test.resize((self.config.size,self.config.size))

                # 粗粒度分类
                class_name=self.Coarse_grained_class.test_img(img_test,flag=False,score_thr=0.5)
                if class_name[0][0]!=0:
                    continue
                else:
                    # 细粒度分类
                    class_name=self.fine_grained_class.test_img(img_test,flag=False,score_thr=0.5)
                    if class_name[0][0]!=0:
                        continue
                    else:
                        # 将检测结果输出为类别
                        self.roi_list[i, 0]=class_name[0][0]
                        self.result.append(self.roi_list[i])
        return self.result

if __name__ == '__main__':
    img_path='/media/cbird/新加卷1/miao/NS2/mix/1000-3000/all/img/1 (685).png'
    img=cv2.imread(img_path)
    cfg=Config()
    dete=detector(cfg)
    result=dete.detecte(img)
    print (result)

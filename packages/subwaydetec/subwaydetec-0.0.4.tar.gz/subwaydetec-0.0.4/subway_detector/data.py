from torchvision import transforms

class data_detile(object):
    def __init__(self,config):
        # 这个目前只用在测试阶段
        self.transforms=transforms.Compose([
                # transforms.Resize(config.size),
                transforms.ToTensor(),
                transforms.Normalize(config.mean,config.std)])

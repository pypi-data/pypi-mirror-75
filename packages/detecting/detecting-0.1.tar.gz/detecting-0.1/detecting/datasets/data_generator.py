import numpy as np
from tensorflow.keras.utils import Sequence

class DataGenerator(Sequence):
    def __init__(self, dataset, batch_size=1, shuffle=False):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.indices = np.arange(len(self.dataset))
        # 打乱索引
        if self.shuffle:
            np.random.shuffle(self.indices)

    # 获得index位置的批次数据
    def __getitem__(self, index):
        img_list = []
        img_meta_list = []
        bbox_list = []
        label_list = []
        # 循环一个批次的数据
        for i in self.indices[index * self.batch_size: (index + 1) * self.batch_size]:
            # 获取数据
            img, img_meta, bbox, label = self.dataset[i]
            img_list.append(img)
            img_meta_list.append(img_meta)
            bbox_list.append(bbox)
            label_list.append(label)

        if self.batch_size == 1:
            batch_imgs = np.expand_dims(img_list[0], 0)
            batch_metas = np.expand_dims(img_meta_list[0], 0)
            batch_bboxes = np.expand_dims(bbox_list[0], 0)
            batch_labels = np.expand_dims(label_list[0], 0)
        else:
            # 堆叠为一个批次的数据
            batch_imgs = np.stack(img_list,axis=0)
            batch_metas = np.stack(img_meta_list,axis=0)
            # 先填充
            bbox_list = self._pad_batch_data(bbox_list)
            batch_bboxes = np.stack(bbox_list,axis=0)
            # 先填充
            label_list = self._pad_batch_data(label_list)
            batch_labels = np.stack(label_list,axis=0)
        # 返回
        return batch_imgs, batch_metas, batch_bboxes, batch_labels

    def __call__(self):
        for img_idx in self.indices:
            img, img_meta, bbox, label = self.dataset[img_idx]
            yield img, img_meta, bbox, label

    # 返回生成器的长度
    def __len__(self):
        return int(np.ceil(float(len(self.dataset))/self.batch_size))  

    # 用于填充bbox和label，使得一个批次中的bbox和label的数量相等
    def _pad_batch_data(self, data):
        # 计算这个批次中最多的数据量
        max_len = max([d.shape[0] for d in data])
        temp_list = []
        for d in data:
            # 计算需要填充的数据量
            pad_len = max_len - d.shape[0]
            if d.ndim == 1:
                # 填充pad_len个数据0
                d = np.pad(d,(0,pad_len),'constant',constant_values=0)
            elif d.ndim == 2:
                # 填充pad_len行数据0
                d = np.pad(d,((0,pad_len),(0,0)),'constant',constant_values=0)
            temp_list.append(d)
        return temp_list

    # 在epoch末尾
    def on_epoch_end(self):
        # 打乱数据索引
        if self.shuffle: 
            np.random.shuffle(self.indices)
    
    # 获得种类名称
    def get_categories(self):
        return self.dataset.get_categories()

    # 类别数
    def num_classes(self):
        return len(self.get_categories())
    
    # 返回数据集大小
    def size(self):
        return len(self.dataset) 

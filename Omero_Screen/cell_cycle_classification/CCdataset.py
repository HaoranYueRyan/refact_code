import os
import ast
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import torch
from torch.utils.data import Dataset
from PIL import Image
from natsort import natsorted
from torchvision.utils import save_image
import torchvision.transforms as transforms
import skimage
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2

class CCdata(Dataset):
    def __init__(self, csv_file, root_dir,transform=None):
        self.annotations=pd.read_csv(csv_file)
        # print(self.annotations)
        self.root_dir=root_dir

        self.transform = transform
        if '.DS_S' in self.annotations:
            print('yes')
        #     self.images.remove('.DS_Store')
        # for i in self.images:
        #   if i[-5:-1]== ').ti':
        #     self.images.remove(i)

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir,(self.annotations.iloc[index,0]))
        # [: -1]+'.tif'
        # image=Image.open(img_path).convert('L')
        image=skimage.io.imread(img_path)
        # plt.figure(figsize=(10,10))
        # plt.imshow(image)
        # plt.show()

        image=np.float32(image)
        # print(image.shape)

        # plt.figure(figsize=(10,10))
        # plt.imshow(image,cmap='gray')
        # plt.show()
        # print(image.mean())

        # image = image / np.amax(image)
        # image= np.clip(image, 0, 1)
        # image=image[:, :, 1:3]


        # image=np.float32(image)
        # plt.figure(figsize=(10,10))
        # plt.imshow(image[:,:,0])
        # plt.show()





        # y_lable= torch.tensor(int(self.annotations.iloc[index,1])),

        y_lable = torch.tensor(np.array(ast.literal_eval(self.annotations.iloc[index,1]), dtype=np.float32))

        # y_lable=y_lable.view(1, 4)     #  1D convert to 2D tensor
        # y_lable=y_lable.softmax(dim=1)
        # y_lable = y_lable.view(4)




        # print((np.float32(image) / 255)
        if self.transform:
            # image = self.transform(image=image)
            augmentations= self.transform(image=image)
            image=augmentations['image']

            # mean, std = torch.mean(image), torch.std(image)
            # transform_norm=transforms.Normalize(mean, std)
            # img_normalized = transform_norm(image)

            # print(image)
            # plt.Figure(figsize=(10, 10))
            #
            # plt.imshow(image[0])
            # plt.show()
            # plt.imshow(image[1])
            # plt.show()
            # save_image(image[1],'/Users/haoranyue/Documents/master_project/imaaaaage' + str(10000) + '.png'
            #            )
        # print(y_lable[0])
        return (image,y_lable)

if __name__=='__main__':
    transform = A.Compose(
        [
            A.Resize(64, 64, ),
            # # A.CenterCrop(60, 60, ),
            # # A.Resize(32, 32),
            # A.Rotate(limit=20, p=0.8),
            # A.HorizontalFlip(p=0.5),
            # A.RandomBrightnessContrast(p=0.4),
            # # A.VerticalFlip(p=0.1),
            # A.VerticalFlip(p=0.4),
            A.OneOf(
                [
                    # A.Blur(blur_limit=3, p=0.8),
                    # A.Blur(blur_limit=3, p=0.5),
                    # A.ColorJitter(p=0.6),

                ], p=1.0
            ),
            ToTensorV2(),

        ]
    )
    dataset =CCdata(csv_file='/Users/Lab/Documents/RPE-1_10000_Flatfield_Corr_814/df_training.csv',
root_dir = '/Users/Lab/Documents/RPE-1_10000_Flatfield_Corr_814/alpha_tubulins_bolean_mask',transform=transform)
    dataset.__getitem__(-1)

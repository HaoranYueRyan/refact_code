import matplotlib.pyplot as plt

from CNN_model import CNN
from torch.utils.data import DataLoader
import torch.nn as nn
import torch

import torch.optim as optim
from torch.utils.data import DataLoader

from CCdataset import CCdata
from tqdm import tqdm
import albumentations as A
from albumentations.pytorch import ToTensorV2
import pandas as pd
load_model=False



# save weights of model
def save_checkpoint(state,filename='/Users/haoranyue/PycharmProjects/Cell_cycle_classification/my_CNN_original_32_checkpoint_11_25.pth.tar'):
    print('=> Saving checkpoint')
    torch.save(state,filename)
# check the accuracy of model predict with ground truth
def check_accuracy(loader,model,device):
    num_correct=0
    num_samples=0
    model.eval()
    with torch.no_grad():
        for x,y in loader:
            x=x.to(device=device)
            y=y.to(device=device)
            _,y = y.max(1)
            scores = model(x)
            _,predictions= scores.max(1)
            num_correct += (predictions==y).sum()
            num_samples+= predictions.size(0)
    model.train()
    return num_correct.item()/num_samples



def main():
    in_channel = 3
    num_classes = 4
    learning_rate = 0.001
    batch_size = 64
    num_epochs =100
    csv_dir = '/Users/Lab/Documents/RPE-1_10000_Flatfield_Corr_814/df_training.csv'
    root_dir = '/Users/Lab/Documents/RPE-1_10000_Flatfield_Corr_814/alpha_tubulins_bolean_mask/'
    # device using mps
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    # increase the samples by augmentation
    transform = A.Compose(
        [
            A.Resize(64, 64, ),
            # A.CenterCrop(60, 60,),
            # A.Resize(32, 32),
            A.Rotate(limit=40, p=0.6),
            # A.HorizontalFlip(p=0.5),
            # A.RandomBrightnessContrast(p=0.4),
            A.VerticalFlip(p=0.2),
            A.VerticalFlip(p=0.6),
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
    #  load dataset
    datasets = CCdata(csv_file=csv_dir, root_dir=root_dir, transform=transform)
    train_size = int(0.8 * len(datasets))
    print(train_size)
    test_size = len(datasets) - train_size
    print(test_size)
    train_set, test_set = torch.utils.data.random_split(datasets, [train_size, test_size])
    train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(dataset=test_set, batch_size=batch_size, shuffle=True)
    # load model
    model = CNN(in_channels=in_channel, num_classes=num_classes).to(device=device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # record the accuracy on training
    train_accurcy=[]
    test_accuracy=[]
    loss_epoch=[]

    # training the model
    for epoch in range(num_epochs):
        for batch_idx, (data, targets) in enumerate(tqdm(train_loader)):

            data = data.to(device=device)
            targets = targets.to(device=device)


        # forward
            scores= model(data)
        # print(scores)

            loss = criterion(scores, targets)


         # backward
            optimizer.zero_grad()
            loss.backward()
         # gradient descent or adam step
            optimizer.step()

        loss_epoch.append(loss.item())
        print(loss.item())
        train_accurcy.append(check_accuracy(train_loader, model, device))
        print(check_accuracy(train_loader, model, device))
        test_accuracy.append(check_accuracy(test_loader, model, device))
        print(check_accuracy(test_loader, model, device))
        checkpoint = {'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict()}
        save_checkpoint(checkpoint)
    df_loss= pd.DataFrame(loss_epoch, columns=['loss'])
    df_train = pd.DataFrame(train_accurcy, columns=['train_accuracy'])
    df_test = pd.DataFrame(test_accuracy, columns=['test_accuracy'])
    df_train.to_csv('/Users/haoranyue/Documents/master_project/disseration_image/accuracy_epoch/epoch_CNN_25_11_train.csv')
    df_test.to_csv('/Users/haoranyue/Documents/master_project/disseration_image/accuracy_epoch/epoch_CNN_25_11_test.csv')
    df_loss.to_csv('/Users/haoranyue/Documents/master_project/disseration_image/accuracy_epoch/epoch_CNN_25_11_loss.csv')

if __name__=='__main__':
    main()

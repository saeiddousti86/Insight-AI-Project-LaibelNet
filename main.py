import argparse
import pandas as pd
import os
import shutil
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib import rcParams
import numpy as np
from import_images import read_images
from cnn_model import cnn_model
from cluster import clustering
from keras.preprocessing.image import ImageDataGenerator
from sklearn.mixture import GaussianMixture as GMM
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import keras
import time
import tqdm
import pickle
from PIL import Image


# ---------------------------------------------------------------

# predefined variables

def pars_arg():
    parser = argparse.ArgumentParser(description='lAIbelNet: an automatic labeling tool using unsupervised clustering')

    parser.add_argument('--res', type=int, help='Image Resolution', default=150)
    parser.add_argument('--mode', type=int, help='0:Labeled, 1:Unlabeled', default=0)
    parser.add_argument('--data_path', type=str, help='Data Path', default='data')
    parser.add_argument('--n_images', type=int, help='Number of Images to Label', default=None)
    parser.add_argument('--ftr_ext', type=int, help='0:MobileNetV2, 1:ResNet50, 2:InceptionResNetV2', default=0)
    parser.add_argument('--min_clustr', type=int, help='Min Number of Clusters', default=2)
    parser.add_argument('--max_clustr', type=int, help='Max Number of Clusters', default=50)

    args = parser.parse_args()
    return args


Image_Height, Image_width = 250, 250  #
Batch_size = 100
num_classes = 12
class_names = ['Charlock', 'Common Chickweed', 'Black-grass',
               'Fat Hen', 'Loose Silky-bent', 'Sugar beet', 'Maize',
               'Scentless Mayweed', 'Shepherds Purse', 'Cleavers',
               'Small-flowered Cranesbill', 'Common wheat']
feature_space_size = 2048

# this is the path in my google drive
train_path = 'data'


# model_path = '/content/drive/My Drive/Python 3/AI_Seedling_train/Model'

# ---------------------------------------------------------------

# time string
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60
    return f"{h}:{m:>02}:{s:>05.2f}"


def predic_gen(path, batch_size, image_size=None, data_classes=None):
    '''
    this function creates data generator
    :param path:
    :param image_size:
    :param batch_size:
    :param data_classes:
    :return:
    '''

    if data_classes is None:
        data_classes = class_names

    datagen = ImageDataGenerator(
        # set rescaling factor (applied before any other transformation)
        rescale=1. / 255)

    if image_size is None:

        generator = datagen.flow_from_directory(
            directory=path,
            color_mode="rgb",
            batch_size=batch_size,
            class_mode="categorical",
            classes=data_classes,
            shuffle=True,
            subset='training')
    else:

        generator = datagen.flow_from_directory(
            directory=path,
            target_size=image_size,
            color_mode="rgb",
            batch_size=batch_size,
            class_mode="categorical",
            classes=data_classes,
            shuffle=True,
            subset='training')

    return generator


def df_maker(imgs, features, labels):
    '''
    create data frame to store clustering info
    :return: data frame
    '''
    df = pd.DataFrame(df)
    df['img','Real_Labls','img_ftrs'] = imgs
    df['img_ftrs'] = features
    df['Real_Labls'] = labels
    print(df)
    #df['img_ftrs'] = [feature[i, :] for i in range(len(feature[:, 0]))]
    #df['Real_Labls'] = [labels[i].argmax() for i in range(len(feature[:, 0]))]
    df = pd.DataFrame(df)

    df.head()

    return df


def plot_():
    rcParams['figuer.figsize'] = 16, 5
    _ = plt.plot(range(2,10), silhout, "bo-", color='blue', linewith=3, markersize=8,
                 label='Silhoutee curve')
    _ = plt.xlabel("$k$",fontsize=14, family='Arial')
    _ = plt.ylabel("Silhoutte score", fontsize=14, family='Arial')
    _ = plt.grid(which='major', color='#cccccc', linestyle='--')
    _ = plt.title('Silhoutee curve for predict optimal number of clusters',
                  family='Arial', fontsize=14)

    k=np.argmax(silhout) + 2

    _ = plt.axvline(x=k, linestyle='--', c='green', linewith=3,
                    label=f'Optimal number of clusters({k})')
    _ = plt.scatter(k, silhout[k-2], c='red', s= 400)
    _ = plt.legend(shadow=True)
    _ = plt.show()

    print(f'The optimal number of clusters is {k}')

# def main():
args = pars_arg()
print(args)

image_size = (args.res, args.res)

model = cnn_model(args.ftr_ext,image_size)

images, labels = read_images(args.data_path, image_size, args.mode, args.n_images)

features = model.predict(images)

print(images.shape, labels, model, features.shape)

# df_maker(images, features, labels)

silhout, opt_clustr = clustering(features, args.min_clustr, args.max_clustr)

plt.figure()
plt.plot(np.arange(3, 16), silhout['KMeans'], linestyle='-')
plt.plot(np.arange(3, 16), silhout['GMM'], linestyle='--')
plt.show()

# bgmm = BGMM(n_components=12).fit(features)

df['KMN_Labls'] = kmeans.labels_

df['gmm'] = gmm.predict(features)

# df['bgmm'] = bgmm.predict(features)


# if __name__ == '__main__':
#    main()

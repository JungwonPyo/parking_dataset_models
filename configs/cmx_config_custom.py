import os
import os.path as osp
import sys
import time
import numpy as np
from easydict import EasyDict as edict
import argparse

C = edict()
config = C
cfg = C

C.seed = 12345

remoteip = os.popen('pwd').read()
C.root_dir = os.path.abspath(os.path.join(os.getcwd(), './'))
C.abs_dir = osp.realpath(".")

# Dataset config
"""Dataset Path"""
C.dataset_name = 'custom'
C.dataset_path = '/media/kkk/T7_Shield_2'
C.rgb_root_folder = osp.join(C.dataset_path, 'de_front')
C.rgb_format = '.jpg'
C.gt_root_folder = osp.join(C.dataset_path, 'mask_front')
C.gt_format = '.png'
C.gt_transform = False
C.json_root_folder = osp.join(C.dataset_path, 'seg_front')
C.json_format = '.json'
C.use_json = True
# True when label 0 is invalid, you can also modify the function _transform_gt in dataloader.RGBXDataset
# True for most dataset valid, Faslse for MFNet(?)
C.x_root_folder = osp.join(C.dataset_path, 'lidar_front')
C.x_format = '.pcd'
C.x_is_single_channel = False # True for raw depth, thermal and aolp/dolp(not aolp/dolp tri) input
C.train_source = osp.join(C.dataset_path, "train.txt")
C.eval_source = osp.join(C.dataset_path, "val.txt")
C.test_source = osp.join(C.dataset_path, "test.txt")

# Need to resize 
# Note this False if you don't want to change size from original one
C.resize_shape = np.array([1280, 1920])

C.is_test = False
C.num_train_imgs = 10169 # Restricted because of the memory
C.num_eval_imgs = 1000
C.num_classes = 29
C.class_names = [
    'Wall',
    'Driving Area',
    'Non Driving Area',
    'Parking Area',
    'No Parking Area',
    'Big Notice',
    'Pillar',
    'Parking Area Number',
    'Parking Line',
    'Disabled Icon',
    'Women Icon',
    'Compact Car Icon',
    'Speed Bump',
    'Parking Block',
    'Billboard',
    'Toll Bar',
    'Sign',
    'No Parking Sign',
    'Traffic Cone',
    'Fire Extinguisher',
    'Undefined Object',
    'Two-wheeled Vehicle',
    'Vehicle',
    'Wheelchair',
    'Stroller',
    'Shopping Cart',
    'Animal',
    'Human',
    'Undefined Stuff'
]

"""Path Config"""
def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
add_path(osp.join(C.root_dir))

C.log_dir = osp.abspath('cmx_log')

""" Settings for network, this would be different for each kind of model"""
C.backbone = 'mit_b5' # Remember change the path below.
C.pretrained_model = '/home/kkk/data_project/cmx_log/submit/cmx_submit_checkpoint.pth'
C.decoder = 'MLPDecoder'
C.decoder_embed_dim = 512
C.optimizer = 'AdamW'

C.tb_dir = osp.abspath(osp.join(C.log_dir, "tb"))
C.log_dir_link = C.log_dir
C.checkpoint_save_dir = osp.abspath(
    C.log_dir + '_' + C.dataset_name + '_' + C.backbone)
C.checkpoint_dir = osp.abspath(osp.join(C.log_dir, "checkpoint"))

exp_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
C.log_file = C.log_dir + '/log_' + exp_time + '.log'
C.link_log_file = C.log_file + '/log_last.log'
C.val_log_file = C.log_dir + '/val_' + exp_time + '.log'
C.link_val_log_file = C.log_dir + '/val_last.log'

"""Image Config"""
C.background = 255
C.image_height = 480
C.image_width = 640
C.norm_mean = np.array([0.485, 0.456, 0.406])
C.norm_std = np.array([0.229, 0.224, 0.225])

"""Train Config"""
# C.lr = 6e-5
C.lr = 1e-4
C.lr_power = 0.9
C.momentum = 0.9
C.weight_decay = 0.01
C.batch_size = 2
C.nepochs = 100
C.niters_per_epoch = C.num_train_imgs // C.batch_size  + 1
C.num_workers = 8
C.train_scale_array = [0.5, 0.75, 1, 1.25, 1.5, 1.75]
C.warm_up_epoch = 0

C.fix_bias = True
C.bn_eps = 1e-3
C.bn_momentum = 0.1

"""Eval Config"""
C.eval_iter = 2
C.eval_stride_rate = 2 / 3
C.eval_scale_array = [0.75, 1, 1.25] # [0.75, 1, 1.25] # 
C.eval_flip = False # True # 
C.eval_crop_size = [480, 640] # [height weight]

"""Store Config"""
C.checkpoint_start_epoch = 0
C.checkpoint_step = 1

if __name__ == '__main__':
    print(config.nepochs)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-tb', '--tensorboard', default=True, action='store_true')
    args = parser.parse_args()

    if args.tensorboard:
        open_tensorboard()

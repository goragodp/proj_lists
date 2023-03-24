
from scipy.io import loadmat
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split, StratifiedKFold
from scipy.signal import lfilter, butter, filtfilt
import tensorflow as tf


from glob import glob

maps = {'F4': 0, 'C4': 1, 'P4': 2, 'Cz': 3, 'F3': 4, 'C3': 5, 'P3': 6, 'F7': 7, 'T3': 8, 'T5': 9, 
                           'Fp1': 10, 'Fp2': 11, 'T4': 12, 'F8': 13, 'Fz': 14, 'Pz': 15, 'T6': 16, 'O2': 17, 'O1': 18}
# blink_chs = ['C4','F4', 'Fp2','Fp1','F3', 'O1', 'F7', 'F8', 'Fz']
# target_ch = [v for k,v in zip(maps.keys(), maps.values()) if k not in blink_chs]

fs = 500
durations = 2
sample = fs * durations
ch = 19
nyquist = fs * 0.5

def butterworth_bandpass(low, high, fs, order = 4):
    return butter(order, [low, high], fs = fs, btype = 'band', output = 'ba', analog = False)

def butterworth_bpf(data, low, high, fs, order = 4):
    b,a = butterworth_bandpass(low, high, fs, order)
    return filtfilt(b,a, data, axis = 2)

def load_target(fname:str, target:list = None):
    label_keys = {'no':0, 'ball':1, 'box':2, 'pen':3}

    path = fname
    
    info = loadmat(path)
    
    ball_data = np.vstack([
        np.moveaxis(info['ball1'], 2, 0),
        np.moveaxis(info['ball2'], 2, 0),
        np.moveaxis(info['ball3'], 2, 0),
        np.moveaxis(info['ball4'], 2, 0),
        np.moveaxis(info['ball5'], 2, 0)
    ])
    ball_label = np.ones((ball_data.shape[0], 1)) * label_keys['ball']
    
    box_data = np.vstack([
        np.moveaxis(info['box1'], 2, 0),
        np.moveaxis(info['box2'], 2, 0),
        np.moveaxis(info['box3'], 2, 0),
        np.moveaxis(info['box4'], 2, 0),
        np.moveaxis(info['box5'], 2, 0)
    ])
    box_label = np.ones((box_data.shape[0], 1)) * label_keys['box']
    
    pen_data = np.vstack([
        np.moveaxis(info['pen1'], 2, 0),
        np.moveaxis(info['pen2'], 2, 0),
        np.moveaxis(info['pen3'], 2, 0),
        np.moveaxis(info['pen4'], 2, 0),
        np.moveaxis(info['pen5'], 2, 0)
    ])
    pen_label = np.ones((pen_data.shape[0], 1)) * label_keys['pen']
    
    no_data = np.vstack([
        np.moveaxis(info['no1'], 2, 0),
        np.moveaxis(info['no2'], 2, 0),
        np.moveaxis(info['no3'], 2, 0),
        np.moveaxis(info['no4'], 2, 0),
        np.moveaxis(info['no5'], 2, 0)
    ])
    no_label = np.ones((no_data.shape[0], 1)) * label_keys['no']
    # data = np.moveaxis(data, 2, 0)
    
    data = np.vstack([ball_data, box_data, pen_data, no_data])
    label = np.vstack([ball_label, box_label, pen_label, no_label])
    
    nbr_class = len(np.unique(label))
    label = tf.keras.utils.to_categorical(label,num_classes = nbr_class)
    
    return data, label


def load_target_resample(fname:str):
    label_keys = {'no':0, 'ball':1, 'box':2, 'pen':3}

    path = f'Datasets/{fname}.mat'
    info = loadmat(path)
    
    ball = np.vstack([
        np.moveaxis(info['ball1'], 2, 0),
        np.moveaxis(info['ball2'], 2, 0),
        np.moveaxis(info['ball3'], 2, 0),
        np.moveaxis(info['ball4'], 2, 0),
        np.moveaxis(info['ball5'], 2, 0)
    ])
    ball_data = np.vstack([ball[:,:,500:], ball[:,:,:500]])
    ball_label = np.ones((ball_data.shape[0], 1)) * label_keys['ball']
    
    box = np.vstack([
        np.moveaxis(info['box1'], 2, 0),
        np.moveaxis(info['box2'], 2, 0),
        np.moveaxis(info['box3'], 2, 0),
        np.moveaxis(info['box4'], 2, 0),
        np.moveaxis(info['box5'], 2, 0)
    ])
    box_data = np.vstack([box[:,:,500:], box[:,:,:500]])
    box_label = np.ones((box_data.shape[0], 1)) * label_keys['box']
    
    pen = np.vstack([
        np.moveaxis(info['pen1'], 2, 0),
        np.moveaxis(info['pen2'], 2, 0),
        np.moveaxis(info['pen3'], 2, 0),
        np.moveaxis(info['pen4'], 2, 0),
        np.moveaxis(info['pen5'], 2, 0)
    ])
    pen_data = np.vstack([pen[:,:,500:], pen[:,:,:500]])
    pen_label = np.ones((pen_data.shape[0], 1)) * label_keys['pen']
    
    no = np.vstack([
        np.moveaxis(info['no1'], 2, 0),
        np.moveaxis(info['no2'], 2, 0),
        np.moveaxis(info['no3'], 2, 0),
        np.moveaxis(info['no4'], 2, 0),
        np.moveaxis(info['no5'], 2, 0)
    ])
    no_data = np.vstack([no[:,:,500:], no[:,:,:500]])
    no_label = np.ones((no_data.shape[0], 1)) * label_keys['no']
    # data = np.moveaxis(data, 2, 0)
    
    data = np.vstack([ball_data, box_data, pen_data, no_data])
    label = np.vstack([ball_label, box_label, pen_label, no_label])
    
    nbr_class = len(np.unique(label))
    label = tf.keras.utils.to_categorical(label,num_classes = nbr_class)
    
    return data, label


def get_all():
    
    #regular expression for file
    regex = 'Datasets/*_JulyData*'
    target_files = glob(regex)
    
    fs = 500
    duration = 2
    sample = fs * duration
    ch = 19
    hp = 0.5
    lp = 40
    #data1, label1 = capilab_dataset2.load_target('Takahashi_JulyData')
    #data2, label2 = capilab_dataset2.load_target('Suguro_JulyData')
    #data3, label3 = capilab_dataset2.load_target('Lai_JulyData')
    #data4, label4 = capilab_dataset2.load_target('Sugiyama_JulyData')
    #data = np.vstack([data1, data2, data3, data4])
    data, label = capilab_dataset2.load_target(subj + '_JulyData')
    #label = np.vstack([label1, label2, label3, label4])
    try:
        x, x_test,  y, y_test = train_test_split(data, label, test_size = .1, stratify = label, random_state = 1)
        x = capilab_dataset2.butterworth_bpf(x, hp, lp, fs)
        x_test = capilab_dataset2.butterworth_bpf(x_test, hp, lp, fs)
        x = np.expand_dims(x, axis = 3)
        x_test = np.expand_dims(x_test, axis = 3)
        # # swap sample and channels axis
        # x = np.transpose(x, (0,2,1,3))
        # x_test = np.transpose(x_test, (0,2,1,3))
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return None
    else:
        return x, y, x_test, y_test
        
    

if __name__ == "__main__":
    fname = 'Takahashi_JulyData'
    X, y = load_target(fname)
    print(X.shape, y.shape)
    
    X, y = load_target_resample(fname)
    print(X.shape, y.shape)
    


from silence_tensorflow import silence_tensorflow
silence_tensorflow()

import tensorflow as tf
#shut up
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

# import ray
# # from ray.rllib.algorithms import ppo
# from ray.rllib.env.env_context import EnvContext
# from ray.rllib.models.tf.tf_modelv2 import TFModelV2
# from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
# from ray.rllib.utils.framework import try_import_tf
# from ray.rllib.utils.test_utils import check_learning_achieved
# from ray.tune.logger import pretty_print

import gym
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold

from model_set import EEGNet
import capilab_dataset2
from sklearn.model_selection import train_test_split


class EEGChannelOptimze(gym.Env):
    def __init__(self, config):
        super(EEGChannelOptimze, self).__init__()
        self.data = config['data'] #X, y, x_test and y_test
        self.checkpoint_path = config['checkpoint_path']
        self.action_space = gym.spaces.Discrete(config['action_space'])
        self.observation_space = gym.spaces.MultiBinary(config['state_space'])
        self.initial_reward_thresh = config['initial_reward_threshold']
        self.fold = config['fold']
        self.channel_map = config["channel_map"]
        self.max_select =  config['max_select']
        self.initial_channel = config['initial_channels']
        self.base_reward = config['base_reward']
        self.min_channel = config['min_selected_channel']
        self.batch_size = config['batch_size']
        self.epochs = config['epochs']
        
        self.reset()    

    def _step(self, X, y, x_val, y_val, x_test, y_test, verbose = False):
        tf.random.set_seed(1)
        classifier_optimizer = tf.keras.optimizers.Adam()
        classifier_loss = tf.keras.losses.CategoricalCrossentropy()
        
        clf = EEGNet(y.shape[1], Chans = X.shape[1], Samples = X.shape[2], 
                                            dropoutRate = 0.5, kernLength = 512, F1 = 64, 
                                            D = 8, F2 = 128, norm_rate = 0.25, dropoutType = 'Dropout')
        
        clf.compile(optimizer = classifier_optimizer, loss= classifier_loss , metrics=['accuracy'])
        
        checkpointer = tf.keras.callbacks.ModelCheckpoint(filepath='/tmp/checkpoint.h5', verbose=False, save_best_only=True)
        earlystopper = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0.001, patience=4, verbose=0)
        clf.fit(X, y,
                batch_size=self.batch_size, 
                epochs = self.epochs, 
                verbose = verbose, 
                validation_data = (x_val, y_val),
                callbacks = [checkpointer, earlystopper])
        y_preds = clf.predict(x_test, verbose = verbose)
        predicted = np.argmax(y_preds, axis=1)
        ground_truth = np.argmax(y_test, axis=1)
        
        r = accuracy_score(ground_truth, predicted)
        # clf.save('temp_model')
        
        return r
    
    def kfold_eval(self, x,y,x_test, y_test):
        r = np.array([])
        kfold = StratifiedKFold(n_splits = self.fold, shuffle = True, random_state = 420) #fold
        for i , (train, val) in enumerate(kfold.split(x, np.argmax(y, axis = 1))):
            tf.random.set_seed(1)
            res = self._step(x[train], y[train], x[val], y[val],x_test, y_test)
            r = np.append(r, res)
        return r.mean()
    
    def step(self, action):
        
        done = False
        info = {}
        reward = 0
        nbr_selected = len(np.where(self.state == 1)[0])

        #done
        if self.rounds == 1:

            #number of channel less than expect, additional panalties
            if len(self.state) < self.min_channel:
               reward = (len(self.state) - self.min_channel) * 10 

            done = True 
            #eval final f1 score fro all selected channel and get the mean
            self.state[action] = 1 #select the channel
            target_ch = np.where(self.state == 1)[0] 
            X = self.data['X'][:,target_ch,:]
            y = self.data['y']
            x_test = self.data['x_test'][:,target_ch,:]
            y_test = self.data['y_test'] 
                
            final_eval = self.kfold_eval(X, y, x_test, y_test)
            self.score_tracker = final_eval
            
            #improvement percentage
            reward += (final_eval - self.base_reward) * 100 
            
        #not done
        else:
            self.rounds -= 1
            if self.state[action] == 1:
                reward = 0
            else:
                self.state[action] = 1 #select the channel
                target_ch = np.where(self.state == 1)[0] 
                X = self.data['X'][:,target_ch,:]
                y = self.data['y']
                x_test = self.data['x_test'][:,target_ch,:]
                y_test = self.data['y_test'] 
                
                eval_crit =  self._step(X,y, x_test, y_test, x_test, y_test, verbose=False)
                self.score_tracker = eval_crit
                reward = (eval_crit * 100) - (self.reward_threshold * 100)
                if eval_crit - self.reward_threshold > 0:
                    self.reward_threshold = eval_crit
                else:
                    pass


        tf.keras.backend.clear_session()
        return self.state, reward, done, info
    
    def get_current_score(self):
        return self.score_tracker
        
    def reset(self):
        self.state = np.zeros(self.observation_space.n, dtype=int)
        for ch in self.initial_channel:
            self.state[self.channel_map[ch]] = 1
        self.rounds = self.max_select
        self.reward_threshold = self.initial_reward_thresh
        self.tolerance = 2 # nbr of toleranct if the agnet select same chan
        self.score_tracker = self.initial_reward_thresh
        return self.state

if __name__ == "__main__":
    
    def load():
        
        fs = 500
        duration = 2
        sample = fs * duration
        ch = 19
        hp = 0.4
        lp = 30
        data, label = capilab_dataset2.load_target('Takahashi_JulyData')

        #apply fileter
        
        try:
            x, x_test,  y, y_test = train_test_split(data, label, test_size = .1, stratify = label, random_state = 420)
            #filter
            x = capilab_dataset2.butterworth_bpf(x, hp, lp, fs)
            x_test = capilab_dataset2.butterworth_bpf(x_test, hp, lp, fs)
            #add final dim for kernal
            x = np.expand_dims(x, axis = 3)
            x_test = np.expand_dims(x_test, axis = 3)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None
        else:
            return x, y, x_test, y_test
    
    maps = {'F4': 0, 'C4': 1, 'P4': 2, 'Cz': 3, 'F3': 4, 'C3': 5, 'P3': 6, 'F7': 7, 'T3': 8, 'T5': 9, 
                           'Fp1': 10, 'Fp2': 11, 'T4': 12, 'F8': 13, 'Fz': 14, 'Pz': 15, 'T6': 16, 'O2': 17, 'O1': 18}
    X, y, x_test,y_test = load()

    config = {
        "env": "EEGClassiifcationEnvironement",
        "env_config": {
            "data":{
                "X":X,
                "y":y,
                "x_test":x_test,
                "y_test":y_test
                },
            "checkpoint_path":"classifier_ckpt/",
            "action_space":19,
            "state_space":19,
            "initial_reward_threshold":0.4,
            "final_eval_reward":0.80,
            "fold":6,
            "max_selected_channel":13, #number of differnett channel
            "min_selected_channel":8, #number of differnett channel
            "max_select":15, #max decision make
            "initial_channels":['C3', 'C4'],
            "channel_map":maps,
            "batch_size":8,
            "epochs":15,
        },
        "num_worker":1,
    }
    
    stop = {
        "training_iterations": 1000,
        "timestep_total": 6,
        "episode_reward_mean":0.5
    }
    import time
    start_time = time.time()
    
    env = EEGChannelOptimze(config['env_config'])
    x, r, d, _ = env.step(maps['P3'])
    print('Next step', env.get_current_score())
    x, r, d, _ = env.step(maps['Fp1'])
    print('Next step')
    x, r, d, _ = env.step(maps['Fp2'])
    print('Next step')
    x, r, d, _ = env.step(maps['T5'])
    print('Next step')
    x, r, d, _ = env.step(maps['T6'])
    print('Next step')
    x, r, d, _ = env.step(maps['O1'])
    print(env.reward_threshold, r, d, env.state)

    print("Time taken: %.2fs" % (time.time() - start_time))

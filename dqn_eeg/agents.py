import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.metrics import mean_squared_error
from tensorflow.keras.losses import Huber
import numpy as np

class DQNAgent_RANDMEM:
    def __init__(self, state_size, action_size):
        self.n_actions = action_size #nbr of action
        self.lr = 1e-3 #Learning rate for model
        self.gamma = 0.99 #discount factor
        self.exploration_proba = 1.0 #Coolant factor
        # self.exploration_proba_decay = 0.0145 #Decay Rate -> start exploting env at around 60 eps
        self.exploration_proba_decay = 0.009
        self.batch_size = 128 #barch size for memory sampling
        
        self.memory_buffer= list()
        self.max_memory_buffer = 1000
        
        self.train_model = Sequential([
            Flatten(),             
            Dense(units=32,activation = 'relu'),
            Dense(units=64,activation = 'relu'),
            Dense(units=128,activation = 'relu'),
            Dense(self.n_actions, activation = 'softmax')
        ])
        self.train_model.compile(loss="huber", optimizer = Adam(learning_rate = self.lr))
        
        self.target_model = Sequential([
            Flatten(),             
            Dense(units=32,activation = 'relu'),
            Dense(units=64,activation = 'relu'),
            Dense(units=128,activation = 'relu'),
            Dense(self.n_actions, activation = 'softmax')
        ])
        self.target_model.compile(loss="huber", optimizer = Adam(learning_rate = self.lr))
        
    def compute_action(self, current_state):
        if np.random.uniform(0,1) < self.exploration_proba:
            return np.random.choice(range(self.n_actions))
        q_values = tf.reduce_sum(self.target_model.predict(current_state, verbose = False), axis = 0)
        return np.argmax(q_values)

    def update_exploration_probability(self):
        self.exploration_proba = self.exploration_proba * np.exp(-self.exploration_proba_decay)

    def store_episode(self,current_state, action, reward, next_state, done, score, logs = True, flog = "rand_log_mem.txt"):
        if len(self.memory_buffer) > self.max_memory_buffer:
            self.memory_buffer.pop(0)
        self.memory_buffer.append({
            "current_state":current_state,
            "action":action,
            "reward":reward,
            "next_state":next_state,
            "done" :done
        })
        
        if logs:
            #write memory buffer to file as backup
            __w = '{}, {}, {:.3f}, {}, {}, {:.3f}\n'.format(current_state, action, reward, next_state, done, score)
            with open(flog, 'a+') as f:
                f.write(__w)

    def resume_action_approx_training(self, model_path = 'approximator'):
        self.train_model = tf.keras.models.load_model(model_path)

    def train(self, batch_size = 64, model_name = 'randmem'):
        np.random.shuffle(self.memory_buffer)
        batch_sample = self.memory_buffer[0:self.batch_size]
        for experience in batch_sample:
            experience["current_state"] = np.reshape(experience["current_state"], (1,19))
            q_current_state = self.train_model.predict(experience["current_state"], verbose = False)
            #predict Q (reward) of current state eg 
            q_target = experience["reward"]
            if not experience["done"]:
                q_predict = self.train_model.predict(experience["next_state"], verbose = False) #predict q of next state
                q_predict = tf.reduce_sum(q_predict, axis = 0) #flatten output
                q_target = q_target + self.gamma*np.max(q_predict) #apply discount factor
            
            q_current_state[0][experience["action"]] = q_target #set a q value of an action (predicted  by network) to q target
            #[0] because output of network is array of array
        
            # train the model
            hist = self.train_model.fit(experience["current_state"], q_current_state, verbose=False)
        self.train_model.save(model_name)
        return hist.history['loss']

    def update_from_train_nn(self):
        self.target_model.set_weigth(self.train_model.get_weights())
        # arget_model.set_weights(model.get_weights()) 


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.n_actions = action_size #nbr of action
        self.lr = 1e-3 #Learning rate for model
        self.gamma = 0.99 #discount factor
        self.exploration_proba = 1 #Coolant factor
        # self.exploration_proba_decay = 0.0145 #Decay Rate -> start exploting env at around 60 eps
        self.exploration_proba_decay = 0.009
        self.batch_size = 128 #barch size for memory sampling
        
        # self.memory_buffer= list()
        self.good_exp = []
        self.bad_exp = []
        self.max_memory_buffer = 1000
        # self.good_trajectories = 1000
        # self.bad_trajectories = 1000
        
        self.train_model = Sequential([
            Flatten(),             
            Dense(units=32,activation = 'relu'),
            Dense(units=64,activation = 'relu'),
            Dense(units=128,activation = 'relu'),
            Dense(self.n_actions, activation = 'softmax')
        ])
        self.train_model.compile(loss="huber", optimizer = Adam(learning_rate = self.lr))
        
        self.target_model = Sequential([
            Flatten(),             
            Dense(units=32,activation = 'relu'),
            Dense(units=64,activation = 'relu'),
            Dense(units=128,activation = 'relu'),
            Dense(self.n_actions, activation = 'softmax')
        ])
        self.target_model.compile(loss="huber", optimizer = Adam(learning_rate = self.lr))
        
    def compute_action(self, current_state):
        if np.random.uniform(0,1) < self.exploration_proba:
            return np.random.choice(range(self.n_actions))
        q_values = tf.reduce_sum(self.target_model.predict(current_state, verbose = False), axis = 0)
        return np.argmax(q_values)

    def update_exploration_probability(self):
        self.exploration_proba = self.exploration_proba * np.exp(-self.exploration_proba_decay)

    def store_episode(self,current_state, action, reward, next_state, done, score, logs = True, flog = 'log_sep_mem.txt'):
               
        if reward > 0:
            if len(self.good_exp) > self.max_memory_buffer // 2:
                self.good_exp.pop(0)
            self.good_exp.append({
                "current_state":current_state,
                "action":action,
                "reward":reward,
                "next_state":next_state,
                "done" :done
            })
        else:
            if len(self.bad_exp) > self.max_memory_buffer // 2:
                self.bad_exp.pop(0)
            self.bad_exp.append({
                "current_state":current_state,
                "action":action,
                "reward":reward,
                "next_state":next_state,
                "done" :done
            })
        if logs:
            __w = '{}, {}, {:.3f}, {}, {}, {:.3f}\n'.format(current_state, action, reward, next_state, done, score)
            with open(flog, 'a+') as f:
                f.write(__w)

    def resume_action_approx_training(self, model_path = 'approximator'):
        self.train_model = tf.keras.models.load_model(model_path)

    def train(self, batch_size = 64, model_name = 'sepmem'):
        np.random.shuffle(self.good_exp)
        np.random.shuffle(self.bad_exp)
        
        good_batch_sample = self.good_exp[0:self.batch_size // 2]
        bad_batch_sample = self.bad_exp[0:self.batch_size // 2]
        batch_sample = np.append(good_batch_sample, bad_batch_sample)
        np.random.shuffle(batch_sample)
        
        for experience in batch_sample:
            experience["current_state"] = np.reshape(experience["current_state"], (1,19))
            q_current_state = self.train_model.predict(experience["current_state"], verbose = False)
            q_target = experience["reward"]
            if not experience["done"]:
                q_predict = self.train_model.predict(experience["next_state"], verbose = False) #predict q of next state
                q_predict = tf.reduce_sum(q_predict, axis = 0) #flatten output
                q_target = q_target + self.gamma*np.max(q_predict) #apply discount factor
            
            q_current_state[0][experience["action"]] = q_target #set a q value of an action (predicted  by network) to q target
            #[0] because output of network is array of array
        
            # train the model
            hist = self.train_model.fit(experience["current_state"], q_current_state, verbose=False)
        self.train_model.save(model_name)
        return hist.history['loss']
    
    def update_weigths(self):
        self.target_model.set_weights(self.train_model.get_weights())


if __name__ == "__main__":
    a1 = DQNAgent(19, 19)
    a1.target_model.build((1,19))
    a1.train_model.build((1,19))
    a1.update_weigths()
    # a2 = DQNAgent_RANDMEM(19, 19)
    

import capilab_dataset2
from sklearn.model_selection import train_test_split
from custom_env_ga_compare import EEGChannelOptimze
import numpy as np
from agents import DQNAgent
import json
from scipy.io import loadmat


### EXPERIMENT PARAMETER
# RL    : exp_replay length = 1000 (500//each)
#       : alpha = 0.01, gamma = 0.99, decay 0.009, episodes = 1000
# CNN   : batch = 8 epoch 12, adam with lr = 0.001, cce

#HEPLER FUNC ------------------------------------------------------------------------------------------------------------
def json_serialize(e, state, reward_trajectory, current, fname):
    d = {
        'episode' : e,
        'data' :{
        "final_state": state.tolist(),
        "reward_trajectory": reward_trajectory.tolist(),
        "accumulative_reward": reward_trajectory.sum(),
        "final_score": current
        }
    }
    json_object = json.dumps(d, indent=4)
    with open('log/' + fname, "a+") as outfile:
        outfile.write(json_object)
        outfile.write(',\n')

def log(msg, fname = 'log/execution_log.txt'):
    with open(fname, "a+") as outfile:
        outfile.write(msg)
        outfile.write('\n')
    
def load_matlab_data(target_file):
    f = 'Datasets/{}_filtered_data.mat'.format(target_file)
    try:
        contents= loadmat(f)
        X = contents['raw_x']
        Y = contents['raw_y']

        #target shape = (data, 19, 1000, 1), from (1000, 19, data)
        X = np.transpose(X, [2,1,0])
        Y = np.transpose(Y, [1,0])
        X = np.expand_dims(X, axis = 3)
        x, x_test,  y, y_test = train_test_split(X, Y, test_size = .1, stratify = Y, random_state = 1)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return None
    else:
        return x, y, x_test, y_test
    
def load(subj):    
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


def evaluate(subj, base_acc_all_ch):
    
    #PREPARE DATA ------------------------------------------------------------------------------------------------------------
    maps = {'F4': 0, 'C4': 1, 'P4': 2, 'Cz': 3, 'F3': 4, 'C3': 5, 'P3': 6, 'F7': 7, 'T3': 8, 'T5': 9, 
                            'Fp1': 10, 'Fp2': 11, 'T4': 12, 'F8': 13, 'Fz': 14, 'Pz': 15, 'T6': 16, 'O2': 17, 'O1': 18}
    # X, y, x_test,y_test = load(subj) # subj = "Takahashi", "Suguro", "Lai" or "Sugiyama"
    X, y, x_test,y_test = load_matlab_data(subj) # subj = "tkh", "sgym", "lyf" or "sgr"
    config = {
        "env": "EEGClassiifcationEnvironement",
        "env_config": {
            "data":{
                "X":X,
                "y":y,
                "x_test":x_test,
                "y_test":y_test
                },
            "checkpoint_path":subj +"_classifier_ckpt/",
            "action_space":19,
            "state_space":19,
            "initial_reward_threshold":0.55,
            "base_reward":base_acc_all_ch,
            "fold":4,
            "min_selected_channel":7, #number of differnett channel
            "max_select":11, #max decision make
            "initial_channels":['C3', 'C4', 'Cz'],
            "channel_map":maps,
            "batch_size":8,
            "epochs":12,
        },
        "num_worker":1,
    }
    #PREPARE ENVI ------------------------------------------------------------------------------------------------------------
    stop = {
        "training_iterations": 1000,
        "timestep_total": 6,
        "episode_reward_mean":0.5
    }
    env = EEGChannelOptimze(config['env_config'])#ENV
    
    from tqdm import tqdm
    
    
    print(f'---------performing channel optimization on subject {subj} data---------')
    print('started\n\n\n')
    n_episodes = 1000
    state_size = env.observation_space.n
    action_size = env.action_space.n
    agent2 = DQNAgent(state_size, action_size)   
    agent2.batch_size = 128
    batch_size = agent2.batch_size
    total_steps = 0
    with tqdm(total = n_episodes, position = 0, leave = True) as pbar:
        for e in tqdm(range(n_episodes), ncols = 100, position = 0, leave = True, desc ="DQN Training>"):
            current_state = np.array([env.reset()])
            episode_step = 0
            done = False
            r = 0
            episode_reward = np.array([])
            
            while not done:
                total_steps = total_steps + 1
                action = agent2.compute_action(current_state)
                
                next_state, reward, done, _ = env.step(action)
                episode_reward = np.append(episode_reward, reward)
                next_state = np.array([next_state])
                agent2.store_episode(current_state, action, 
                        reward, next_state, 
                        done, env.get_current_score(),
                        subj + '_mem_buffer.txt')
                
                if done:
                    agent2.update_exploration_probability()
                    json_serialize(e, env.state, episode_reward, env.get_current_score(), subj +"_rand_agent_reward.json")
                    break
                current_state = next_state
                episode_step += 1
    
            if len(agent2.good_exp) >= batch_size // 2 and len(agent2.bad_exp) >= batch_size //2:
                loss = agent2.train(batch_size=batch_size,  model_name=subj+ 'model')
                #update weight of target network every 20 episode
                if total_steps % 20 == 0:
                    with open(subj + '_weigth.txt', 'a+') as f:
                        f.write('weigth updated\n')
                    agent2.update_weigths()
                with open(subj + '_loss.txt', 'a+') as f:
                    f.write(str(loss[-1]) + '\n')
            total_steps += 1
            pbar.update()

if __name__ == "__main__":
    # subjs = [('Takahashi', 0.6041), ('Lai',0.5708), ('Sugiyama',0.6458), ('Suguro',0.5708)]
    subjs = [('tkh', 0.6041)]
    for subj, base in subjs:
        evaluate(subj,base)

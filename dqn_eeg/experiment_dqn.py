import capilab_dataset2
from sklearn.model_selection import train_test_split
from custom_env import EEGChannelOptimze
import numpy as np
from agents import DQNAgent, DQNAgent_RANDMEM

#HEPLER FUNC ------------------------------------------------------------------------------------------------------------
def json_serialize(e, state, reward_trajectory, current_f1, fname):
    d = {
        'episode' : e,
        'data' :{
        "final_state": state.tolist(),
        "reward_trajectory": reward_trajectory.tolist(),
        "accumulative_reward": reward_trajectory.sum(),
        "final_f1_score": current_f1
        }
    }
    json_object = json.dumps(d, indent=4)
    with open(fname, "a+") as outfile:
        outfile.write(json_object)
        outfile.write(',\n')

def log(msg, fname = 'execution_log.txt'):
    with open(fname, "a+") as outfile:
        outfile.write(msg)
        outfile.write('\n')
    

def load():    
    fs = 500
    duration = 2
    sample = fs * duration
    ch = 19
    hp = 0.4
    lp = 30
    data1, label1 = capilab_dataset2.load_target('Takahashi_JulyData')
    data2, label2 = capilab_dataset2.load_target('Suguro_JulyData')
    data3, label3 = capilab_dataset2.load_target('Lai_JulyData')
    data4, label4 = capilab_dataset2.load_target('Sugiyama_JulyData')
    data = np.vstack([data1, data2, data3, data4])
    label = np.vstack([label1, label2, label3, label4])
    try:
        x, x_test,  y, y_test = train_test_split(data, label, test_size = .1, stratify = label, random_state = 420)
        x = capilab_dataset2.butterworth_bpf(x, hp, lp, fs)
        x_test = capilab_dataset2.butterworth_bpf(x_test, hp, lp, fs)
        x = np.expand_dims(x, axis = 3)
        x_test = np.expand_dims(x_test, axis = 3)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return None
    else:
        return x, y, x_test, y_test


def evaluate(subj):
    #PREPARE DATA ------------------------------------------------------------------------------------------------------------
    maps = {'F4': 0, 'C4': 1, 'P4': 2, 'Cz': 3, 'F3': 4, 'C3': 5, 'P3': 6, 'F7': 7, 'T3': 8, 'T5': 9, 
                            'Fp1': 10, 'Fp2': 11, 'T4': 12, 'F8': 13, 'Fz': 14, 'Pz': 15, 'T6': 16, 'O2': 17, 'O1': 18}
    X, y, x_test,y_test = load() #DATA
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
            "initial_reward_threshold":0.5,
            "final_eval_reward":0.70,
            "fold":5,
            "max_selected_channel":11, #number of differnett channel
            "min_selected_channel":6, #number of differnett channel
            "max_select":8, #max decision make
            "initial_channels":['C3', 'C4', 'O1', 'T6'],
            "channel_map":maps,
            "batch_size":8,
            "epochs":30,
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

    #_________________________________________________________________ 2ND RAMDOM MEM AGENT __________________________________________________________________________
    n_episodes = 1000
    state_size = env.observation_space.n
    action_size = env.action_space.n
    agent2 = DQNAgent_RANDMEM(state_size, action_size)   
    agent2.batch_size = 128
    batch_size = agent.batch_size
    total_steps = 0
    with tqdm(total = n_episodes, position = 0, leave = True) as pbar:
        for e in tqdm(range(n_episodes, n_episodes + 300), ncols = 100, position = 0, leave = True, desc ="DQN Training>"):
            
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
                agent2.store_episode(current_state, action, reward, next_state, done, env.get_current_score())
                
                if done:
                    agent2.update_exploration_probability()
                    json_serialize(e, env.state, episode_reward, env.get_current_score(), "rand_agent_reward.json")
                    break
                current_state = next_state
                episode_step += 1

            if len(agent2.memory_buffer) >= batch_size:
                loss = agent2.train(batch_size=batch_size)
                with open('rand_log_action_approximator.txt', 'a+') as f:
                    f.write(str(loss[-1]) + '\n')
            pbar.update()
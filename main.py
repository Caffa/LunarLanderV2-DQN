import gym
import os
import argparse
import cv2
import random
from agent import Agent
from constants import *
import json
import pandas as pd
import os
from datetime import datetime

os.environ['KMP_DUPLICATE_LIB_OK']='True'

ENV = "LunarLander-v2"

def run(params):
    env = gym.make(ENV)
    
    agent = Agent(input_dims=env.observation_space.shape, n_actions=env.action_space.n, seed=params['seed'], agent_mode=params['agent_mode'], network_mode=params['network_mode'], test_mode=params['test_mode'], batch_size=params['batch_size'], n_epochs=params['n_epochs'], update_every=params['update_every'], lr=params['lr'], fc1_dims=params['fc1_dims'], fc2_dims=params['fc2_dims'], fc3_dims=params['fc3_dims'], gamma=params['gamma'], epsilon=params['epsilon'], eps_end=params['eps_end'], eps_dec=params['eps_dec'], max_mem_size=params['max_mem_size'], tau=params['tau'])
    
    if not os.path.isdir(f'videos'): os.makedirs(f'videos')
    if params['test_mode']:
        result = cv2.VideoWriter(f'./videos/{agent.agent_name}.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             60, (600,400))
    
    # load_checkpoint = os.path.exists(f'./models/{agent.agent_name}/{agent.agent_name}_EVAL.pth') and os.path.exists(f'./models/{agent.agent_name}/{agent.agent_name}_TARGET.pth')
    
    # if load_checkpoint:
    #     agent.load_model()
        
    average_reward, best_avg = 0, -1000
    scores, eps_history = [], []
    
    n_games = params['n_games']
    n_steps = 0
    limit_steps = params['limit_steps']
    scores_window = params['scores_window']

    unique = 'Log_{}_{}_{}_{}_N{}_{}'.format(params['agent_mode'], params['network_mode'],params['fc1_dims'], params['fc2_dims'],  params['name'],  params['randID'])
    
    for i in range(n_games):
        score = 0
        obs = env.reset()
        done = False
        agent.tensorboard_step = i
        i_step = 0
        while not done:
            action = agent.choose_action(obs)
            next_obs, reward, done, info = env.step(action)
            n_steps += 1
            i_step += 1
            # Reward Punishing for Moving Vertically away from zero
            # Range is [-1.00 to +1.00] with center at zero to maximize efficiency
            reward -= abs(obs[0])*0.05
            score += reward
            
            if not params['test_mode']:
                agent.step(obs, action, reward, next_obs, done)
            else:
                frame_ = env.render(mode="rgb_array")
                frame = cv2.cvtColor(frame_, cv2.COLOR_RGB2BGR) 
                font = cv2.FONT_HERSHEY_SIMPLEX
                frame = cv2.putText(frame,f'{agent.agent_name}',(375,20), font, 0.6, (0,165,255), 2, cv2.LINE_AA)
                frame = cv2.putText(frame,f'Episode: {i}',(10,20), font, 0.75, (0,165,255), 2, cv2.LINE_AA)
                frame = cv2.putText(frame,f'Score: {score:.2f}',(10,60), font, 0.75, (0,165,255), 2, cv2.LINE_AA)
                if len(scores)>0:
                    frame = cv2.putText(frame,f'Average Score: {sum(scores[-5:])/len(scores[-5:]):.2f}',(10,100), font, 0.75, (0,165,255), 2, cv2.LINE_AA)
                result.write(frame)
            obs = next_obs
            print('\rEpisode: {:4n}\tAverage Score: {:.2f}\tEpsilon: {:.4f}\tStep: {:4n}\tScore: {:.2f}'.format(i, average_reward, agent.epsilon, i_step, score), end="")
            if i_step > limit_steps or done: break 

        agent.epsilon_decay()        
        scores.append(score)
        eps_history.append(agent.epsilon)

        average_reward = sum(scores[-scores_window:])/len(scores[-scores_window:])
        min_reward = min(scores[-scores_window:])
        max_reward = max(scores[-scores_window:])

        ## TODO save model during training so can render some progress shots later

        if not params['test_mode']:
            agent.on_epsiode_end(reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward, n_steps=n_steps, i_steps=i_step)

            if best_avg < average_reward and i > 100: 
                agent.save_model()
                oldavv = best_avg
                best_avg = average_reward
                if oldavv + 10 < average_reward: 
                    print('\rEpisode: {:4n}\tAverage Score: {:.2f}\tEpsilon: {:.4f}'.format(i, average_reward, agent.epsilon))

        # my addition, quit and record if the reward is sufficient
        if average_reward >= params['reward'] and i > 100 and not params['test_mode']:
            print('\n won the game for {} at {} eps'.format(unique, i))
            # record the data in a way that won't have two program access issue - params and current episode - 100 which is scores_window
            statement = {
            'episodeLearnt': i - scores_window,
            'episodeEnd': i,
            "averageReward": average_reward,
            'uniqueID':unique

            }

            statement.update(params)

            # save data

            now = datetime.now()
            dt_string = now.strftime("_%m-%d-%H-%M-%S")

            a_file = open(os.path.join("Results", unique + dt_string + ".json") , "w")
            json.dump(statement, a_file)
            a_file.close()

            df = pd.DataFrame.from_records(statement, index=[0])

            try:
                with open("Results.csv", 'a') as f:
                    df.to_csv(f, header=f.tell()==0, index=[0])     
            except Exception as e:
                print(e)
            else:
                with open("Results.csv", 'a') as f:
                    df.to_csv(f, header=f.tell()==0, index=['uniqueID'])          
                        
            # quit
            break


    if not params['test_mode']:
        agent.tensorboard_writer.close()
    env.close()
    
    if params['test_mode']:
        result.release()
        # Closes all the frames
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Solving Lunar Lander using Deep Q Network',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-a','--agent_mode', help='Enter Agent Type: SIMPLE or DOUBLE', 
                        choices=[SIMPLE, DOUBLE], default=SIMPLE, nargs='?', metavar="")
    parser.add_argument('-n','--network_mode', help='Enter Network Type: SIMPLE or DUELING', 
                        choices=[SIMPLE, DUELING], default=SIMPLE, nargs='?', metavar="")
    parser.add_argument('-t','--test_mode', help='Enter Mode Type: TEST or TRAIN', 
                        choices=[TRAIN, TEST], default=TEST, nargs='?', metavar="")

    # Hyperparameters for Main
    parser.add_argument('--seed', help='Initialize the Random Number Generator', 
                        type=int, nargs='?', default=0, metavar="")
    parser.add_argument('--scores_window', help='Lenght of scores window for evaluation', 
                        type=int, nargs='?', default=100, metavar="")
    parser.add_argument('--n_games', help='Number of games to run on', 
                        type=int, nargs='?', default=2000, metavar="")
    parser.add_argument('--limit_steps', help='Number of steps per run', 
                        type=int, nargs='?', default=1000, metavar="")

    # Hyperparameters for Agent
    parser.add_argument('--gamma', help='Discount Factor for Training', 
                        type=float, nargs='?', default=0.99, metavar="")
    parser.add_argument('--epsilon', help='Exploration Parameter Initial Value', 
                        type=float, nargs='?', default=0.90, metavar="")
    parser.add_argument('--eps_end', help='Exploration Parameter Minimum Value', 
                        type=float, nargs='?', default=0.01, metavar="")
    parser.add_argument('--eps_dec', help='Exploration Parameter Decay Value', 
                        type=float, nargs='?', default=0.995, metavar="")
    parser.add_argument('--batch_size', help='Number of samples per learning step', 
                        type=int, nargs='?', default=64, metavar="")
    parser.add_argument('--n_epochs', help='Number of epochs per learning step', 
                        type=int, nargs='?', default=5, metavar="")
    parser.add_argument('--update_every', help='Number of steps to Update the Target Network', 
                        type=int, nargs='?', default=5, metavar="")
    parser.add_argument('--max_mem_size', help='Memory size of Replay Buffer', 
                        type=int, nargs='?', default=1_00_000, metavar="")
    parser.add_argument('--tau', help='Parameter for Soft Update of Target Network', 
                        type=int, nargs='?', default=1e-3, metavar="")

    # Hyperparameters for Model
    parser.add_argument('--lr', help='Learning Rate for Training', 
                        type=float, nargs='?', default=0.0005, metavar="")
    parser.add_argument('--fc1_dims', help='Number of Nodes in First Hidden Layer', 
                        type=int, nargs='?', default=64, metavar="")
    parser.add_argument('--fc2_dims', help='Number of Nodes in Second Hidden Layer', 
                        type=int, nargs='?', default=64, metavar="")
    parser.add_argument('--fc3_dims', help='Number of Nodes in Third Hidden Layer', 
                        type=int, nargs='?', default=64, metavar="")

    parser.add_argument('--name', help='unique save file name', 
                        type=str, nargs='?', default=str(random.randrange(100)), metavar="")
    parser.add_argument('--randID', help='unique save file name', 
                        type=str, nargs='?', default=str(random.randrange(100)), metavar="")
    parser.add_argument('--reward', help='to stop the training', 
                        type=int, nargs='?', default=200, metavar="")    
    args = vars(parser.parse_args())
    print ("{:>5}{:<20} {:<20}".format('','Hyperparameters', 'Value'))
    for k,v in args.items():
        print ("{:>5}{:<20} {:<20}".format('',k, v))
    if args['test_mode'] == TEST:
        args['test_mode'] = True
        args['epsilon'] = 0.0 if args['epsilon'] == 0.90 else args['epsilon']
        args['n_games'] = 5 if args['n_games'] == 2000 else args['n_games']
    elif args['test_mode'] == TRAIN:
        args['test_mode'] = False
        args['epsilon'] = 1.0 if args['epsilon'] == 0.90 else args['epsilon']
        args['n_games'] = 2000 if args['n_games'] == 2000 else args['n_games']
    else:
        raise SystemExit('Test Mode got improper variables')
    
    run(args)
    

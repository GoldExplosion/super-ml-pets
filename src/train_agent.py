from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.evaluation import evaluate_policy
from sb3_contrib.common.maskable.utils import get_action_masks
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.logger import configure
from sapai_gym import SuperAutoPetsEnv
from sapai_gym.opponent_gen.opponent_generators import random_opp_generator, biggest_numbers_horizontal_opp_generator
from tqdm import tqdm
import numpy as np
import os
import sys


def opponent_generator(num_turns):
    # Returns teams to fight against in the gym
    opponents = biggest_numbers_horizontal_opp_generator(25)
    return opponents


def train_with_masks(ret):
    # gamma: int):
    # initialize environment
    env = SuperAutoPetsEnv(opponent_generator, valid_actions_only=True)

    # setup logger
    logger = configure("./history/sb3_log/")

    # create models directory if it does not exist
    if not os.path.exists('./models/'):
        os.makedirs('./models/')

    # setup model checkpoint callback, to save model after a specific #iters
    checkpoint_callback = CheckpointCallback(save_freq=1000, save_path='./models/', name_prefix=ret.model_name)

    if ret.finetune is not None:
        # check if current python version differ from the one the model is trained with
        vals = ret.infer_pversion.split(".")
        newer_python_version = sys.version_info.major != vals[0] or sys.version_info.minor != vals[1]
        custom_objects = {}
        if newer_python_version:
            custom_objects = {
                "learning_rate": 0.0003,  # default value for MaskablePPO
                "clip_range": lambda _: 0.2,  # default value for MaskablePPO
            }

        print("\nfinetuning...")
        model = MaskablePPO.load(ret.finetune, custom_objects=custom_objects)
        model.set_env(env)
    else:
        print("\ntraining from scratch...")
        model = MaskablePPO("MlpPolicy", env, verbose=0)

    # train
    print("\nTraining...")
    training_flag = True
    retry_counter = 0
    while training_flag:
        try:
            # stop training if number of retries reaches user-defined value
            if retry_counter == ret.nb_retries:
                break
            # setup trainer and start learning
            model.set_logger(logger)
            model.learn(total_timesteps=ret.nb_steps, callback=checkpoint_callback)
            evaluate_policy(model, env, n_eval_episodes=20, reward_threshold=0, warn=False)
            obs = env.reset()

            # if we reach 1M iterations, then training can stop, else, restart!
            # training_flag = False
            print("one full iter is done")
            retry_counter += 1
        except AssertionError as e1:
            print("AssertionError:", e1)
            retry_counter += 1
        except TypeError as e2:
            print("TypeError:", e2)
            print("Model stopped training...")
            retry_counter += 1
        except ValueError as e3:
            print("ValueError:", e3)
            retry_counter += 1
        except Exception as e4:
            print("Exception:", e4)
            retry_counter += 1

        # load previous checkpoint
        # model = MaskablePPO.load("./models/model_sap_gym_sb3_070822_checkpoint")
        # model.set_env(env)

    # save best model
    model.save("./models/" + ret.model_name)

    del model

    # load model
    trained_model = MaskablePPO.load("./models/" + ret.model_name)

    print("\nPredicting...")

    # predict
    obs = env.reset()
    rewards = []
    for i in tqdm(range(ret.nb_games), "Games:"):
        # Predict outcome with model
        action_masks = get_action_masks(env)
        action, _states = trained_model.predict(obs, action_masks=action_masks, deterministic=True)

        obs, reward, done, info = env.step(action)
        if done:
            obs = env.reset()
        rewards.append(reward)
    print(sum(rewards), len(rewards), np.mean(rewards))
    env.close()
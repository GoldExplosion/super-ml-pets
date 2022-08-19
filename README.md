<div align="center">
<img src="https://www.gamelivestory.com/images/article/super-auto-pets-how-to-level-up-quickly-main.webp" width="50%" alt='super-auto-pets'>
<h1 align="center">super-ml-pets</h1>
<h3 align="center">Framework for training and deploying AIs for Super Auto Pets</h3>

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
![CI](https://github.com/andreped/super-ml-pets/workflows/CI/badge.svg)
 ![CodeQL](https://github.com/andreped/super-ml-pets/workflows/CodeQL/badge.svg)
 
Train AIs for Super Auto Pets through a simulated environment and test the trained model against real opponents in the actual game! AI is trained using reinforcement learning and a machine vision system is used to capture the screen to give information to the AI.

</div>

_NOTE: Framework supports Python 3.7-3.10 and works cross-platform (Ubuntu, Windows, macOS)._

## Getting started

1. Clone the repo:
```
git clone https://github.com/andreped/super-ml-pets.git
```

2. Setup virtual environment:
```
cd super-ml-pets/
virtualenv -ppython3 venv --clear
source venv/bin/activate
```

3. Install requirements:
```
pip install -r requirements.txt
```

## Usage
This framework currently supports training and deploying RL models for SAP.

<details open>
<summary>

### Training </summary>

For training in simulated environment, using default arguments, simply run:
```
python main.py --task train
```

Given an existing model, it is also possible to finetune it by (with example):
```
python main.py --task train --finetune ./models/model_sap_gym_sb3_180822_checkpoint_2175_steps.zip
```

The script supports other arguments. To see what is possible, run:
```
python main.py --help
```

</details>

<details open>
<summary>

### Testing </summary>

1. To use a trained model in battle, start the game Super Auto Pets.

2. Ensure that the game is in full screen mode, disable all unneccessary prompts, and set speed to 200%.

3. Enter the arena by clicking "Arena mode".

4. Then, simply start the AI by running this command from the terminal:
```
python main.py --task deploy --model_name model_sap_gym_sb3_180822_checkpoint_finetuned
```

5. Go back into the game and press the "Space" keyboard button.

It might take a few seconds, but you should now be able to see the AI start playing. Please, let it play in peace, or else it might get angry and you have accidentally creating [Skynet](https://en.wikipedia.org/wiki/Skynet_(Terminator)).

</details>

<details open>
<summary>

### Training history </summary>

It is possible to plot the training history by running (might require some path adjustments... To be fixed in the future):
```
python src/game_interaction/plot_history.py
```

<p align="left">
  <img src="assets/training_history_example.png" width="80%" alt='super-auto-pets'>
</p>

</details>

<details>
<summary>

### Troubleshoot </summary>

If you are working on Windows, you need to use slightly different commands for setting up the environment. If you do not have virtualenv in the path, you need to do:
```
python -m virtualenv -ppython3 venv --clear
```

To activate virtual env on windows do:
```
./venv/Scripts/activate
```

</details>

## Acknowledgements
This implementation is based on multiple different projects. The core implementation is derived from [GoldExplosion](https://github.com/GoldExplosion/SuperAutoPets-RL-Agent), which further was based upon the super auto pets engine [sapai](https://github.com/manny405/sapai) and RL training through [sapai-gym](https://github.com/alexdriedger/sapai-gym).

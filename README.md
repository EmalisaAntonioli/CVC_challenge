# Deep Learning CVC Project
### By Emalisa Antonioli, Jeffrey Stynen, and Emma Schoofs (Team 1)

This project is our admission for the Computer Vision Challenge for the Deep Learning Course.

This repository contains code and notebooks for training and deploying an autonomous driving simulation in the game Forza Horison 4. Using YOLO for object detection and a custom CNN regression model for control prediction, the project allows for both identifying key objects (e.g., cars, buses, trucks) on the screen and generating simulated game controller inputs based on model predictions.

## Requirements

All required packages are listed in requirements.txt. To install, run:

```bash
pip install -r requirements.txt
```
Refer to init.ipnyb to create a virtual environment to use to run the code, as well as install the requirements.
               
## Usage
Data was not included in this repository. To collect data, run screen_grab.py while playing your game, we optimized the model using Forza Horizon 4.

To train the final regression model the code in model.ipynb was used. This folder also contains the code required to let the model make predictions and play the game. 

classification_model.ipynb contains abandoned code for a classification model, see the report for further elaboration. 

Use the yolo_object_detection.ipynb while playing the game for real=time object detection.

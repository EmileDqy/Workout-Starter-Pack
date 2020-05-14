# Workout Starter Pack (beta v0.1)

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/AlioptK/Workout-Starter-Pack/issues)



<p align="center">
 <img src="./demo_plank.gif" />
</p>

## Table of contents
* [Introduction](#introduction)
* [Content](#content)
* [What if I can't commit to it ?](#forcing-commit)
* [Installation](#installation)
    * [Executable](#installation-exe)
    * [Code source](#installation-source)
* [Add your own exercices!](#add-exercice)
* [Share with the community!](#sharing)
* [TODOs & possible bugs](#todos-bugs)

<a name="introduction"></a>
## Introduction

**Workout Starter Pack (WSPack) is a highly configurable *community driven* workout program!**
Designed with the goal in mind to help its users develop healthier habits, WSPack is the perfect companion for every developper, remote-worker and basically anyone that has to stay in front of a computer all day!

### Each exercice is fully configurable and has its own AI to supervise you! 
> **Want to share your workout plan and your custom exercices to the community ?** Share them on the community's workshop (see bellow)!

Let's be real, I wanted to do some workout in order to have a summer body (for once). But I know myself way too well for that. It's like one of these workout resolutions we have every year, I knew I wouldn't be able to commit to it for more than a couple of days before giving up and finding excuses to myself.

So... I looked at myself and ... well, I'm all day long on my laptop so I might as well use these hours for my workout.
I knew a little bit of python as well as some javascript! 
That was it!  I employed my programming skills to my health and form.

With this program I had the goal to **find time for me for my workout** and **force me to commit to it**. 

**I wanted my program to disable both of my mouse and keyboard during each session so that I have no other choice but to do my workout session**. Thus, I developped it in python (who cares). 

The **AI** was added in order to **monitor me during my workout**. I wanted it to count my pushups or time my planking and **re-enable my peripherics after each session**. I also added **mathematical functions in order to enhance the difficulty of the exercices over time**. 
*By default, the program won't disable your mouse and keyboard but if you want to, you also can activate it in the configuration file*.


<a name="content"></a>
## In this starter pack, you'll find
 - Customizable exercices and workout sessions :
      - **Customize**, for each exercice, **the number of repetitions** you have to do over time
      - **Create a sequence by selecting one or multiple exercices** from the list of the already installed ones
      - **Randomize your sequences** (or not)
      - **Create and import your own exercices**
 - **An AI which analyzes your movements by counting your repetitions or time your position**
 - **Two modes** were added : 
     - One that runs a session every N seconds throughout the whole day
     - Another that works by intervals of hours, allowing you to run N sessions during each interval 
 
### The Starter Pack comes with 2 basic exercices :
  - Pushups : the AI will count your pushups
  - Plank : the AI will time you. As long as you plank, time will be added to the counter. But if you stop planking, time will be deducted.

### The exercice you were looking for isn't on the list ? Add it and let the community use it (see bellow)!

---

<a name="forcing-commit"></a>
## You feel like you won't be able to commit more than a couple of days ?
You can tell the program to obligate you to do your workout!
How? 
By disabling your mouse and keyboard when a session begins! That way, you won't be able to back off when a session begins!

You can find it in the configuration file under [INPUTS]

<a name="installation"></a>
## Installation : 

<a name="installation-exe"></a>
### Installing the executable :
1) **Download the executable** [here](https://bit.ly/WorkoutStarterPack) !
2) **Extract** its content 
3) **Edit the configuration file** situated in ```config/config.ini```
4) **Run** ```Workout Starter Pack.exe``` and you should be good to go!

**An icon should appear on your taskbar** : 


![icon](https://i.imgur.com/k1EBRuW.png)

You should **receive a notification** telling you the number of seconds till the next session.


#### If you want to run it on startup :

1) Right click on the executable -> Create Shortcut
2) Copy or Cut the Shortcut
3) Press ``` WIN + R ```
4) Enter ``` shell:startup ```
5) Press ENTER
5) Paste the shortcut


<a name="installation-source"></a>
### Manual installation (python 3):

1) Download the project, unzip it
2) Go to the folder :
```
cd <path to the project>
```
2) Install the required modules :
```
pip install -r requirements.txt
```
3) If you want to run the program :
```
python main.py 
```

<a name="add-exercice"></a>
## How to create your own exercices

[tutorial coming soon]

<a name="sharing"></a>
## The community's workshop !

[coming soon]

<a name="todos-bugs"></a>
## TODOs & possible bugs
<?php
include 'TODO.md';
?>
<!--#include virtual="TODO.md"-->

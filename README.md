# Project Name
> Recruitment task - backend internship 2022

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [TO DO](#to-do)
* [Contact](#contact)


## General Information
This application gathers from https://www.balldontlie.io/ API's and filtering data about the NBA league, and shows or store results for the user. This is a task for an internship in an IT company. Application created and tested on Ubuntu 20.04.

## Technologies Used
* Python 3.9.5
* Marshmallow 3.14.1
* Pandas 1.4.1
* Requests 2.27.1
* SQLAlchemy 1.4.31

## Features
* List of features:
* Getting all teams and group them by division. The result is printed on the screen.
* Getting players with a specific name (first or surname) who is the tallest and another one who weights the most. Results are printed on the screen in the metric system.
* Getting statistics for a given season, and they are printed on the screen by default, but optionally they can be stored.

## Setup
#### In the beginning, you have to clone the repository from GitHub to your PC.
* Here is a [link](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) explaining how to clone repository.

#### If you want to use this application, you will need to install packages from requirements.txt file to a virtual environment. 
* Here is a [link](https://www.arubacloud.com/tutorial/how-to-create-a-python-virtual-environment-on-ubuntu.aspx) explaining how to create virtual environment on Ubuntu.
* Here is a [link](https://stackoverflow.com/questions/7225900/how-can-i-install-packages-using-pip-according-to-the-requirements-txt-file-from) explaining how to install packages from requriments.txt.

## Usage
* If you want to use this application, write a command from the examples below:

* `python main.py -h`
* `python main.py grouped-teams`
* `python main.py players-stats --name PLAYER NAME`
* `python main.py teams-stats --season SEASON`
* `python main.py teams-stats --season SEASON --output EXTENSION`

## Project Status
* The main features are done, but I have some ideas, and it's a great practise exercise.

## To do:
* I want to create a docstring for each class...
* I want to create unit tests using PyTest...
* I want to upgrade performance, maybe using asynchronous requests or change the way of filtering data....


## Contact
* #### Created by Dariusz Kowalczyk - dariusz_kowalczykk@wp.pl - feel free to contact me!

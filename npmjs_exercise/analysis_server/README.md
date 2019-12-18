# Installation Instructions

## Pre-setup
* Confirm that Python3 is already installed by opening your Ubuntu terminal and entering: `python3 --version`.
 This should return your Python version number. If you need to update your version of Python,
 first update your Ubuntu version by entering: `sudo apt update && sudo apt upgrade`,
 then update Python using `sudo apt upgrade python3`.

* Install pip by entering: `sudo apt install python3-pip`.
 Pip allows you to install and manage additional packages that are not part of the Python standard library.

* (Optional) Install venv by entering: `sudo apt install python3-venv`.

*  Download the zip file from [here](https://github.com/tzahifurmanski/code_games) and extract it

## Setup a venv
Optional - a venv is a very convenient way to manage multiple python projects
 so the requirements can be installed into a venv that can later be removed without leaving any
 leftovers.

* Inside the code folder, create a venv using `python3 -m venv .venv`.
* Active the venv using `source .venv/bin/activate`


## Setup the project

* Browse to the project's main dir using `cd npmjs_exercise/analysis_server/`
* Install the required packages using `pip3 install -r requirements.txt`
* Run the server `python3 manage.py runserver`
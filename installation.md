# Requirements and Installation:

+ pyenv with Python: 3.9.8

## Clone the Repo

First clone the repository using:

    git clone git@github.com:sbuenker/florita.git

Then navigate to the folder using:

    cd florita

## Setup

For installing the virtual environment you can either use the Makefile and run `make setup` or install it manually:

```zsh
make setup

#or

pyenv local 3.9.8
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

The `requirements.txt` file contains the libraries needed to run the EDA and modeling notebooks, including creating the Folium maps.

## Run the Notebooks

Next, head over to notebooks folder and read or run the notebooks that pique your interests.
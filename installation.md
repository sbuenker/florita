# Requirements and Installation:

+ pyenv with Python: 3.9.8

or

+ conda with Python: 3.9.8

## Clone the Repo

First clone the repository using:

    git clone git@github.com:sbuenker/florita.git

Then navigate to the folder using:

    cd florita

## Setup

For installing the virtual environment with pyenv you can either use the Makefile and run `make setup` or install it manually:

```zsh
make setup

#or

pyenv local 3.9.8
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

For setting up the virtual environment with conda:

```
conda env create -f environment.yml
conda activate flood
```

The `requirements.txt` file contains the libraries needed to run the EDA and modeling notebooks, including creating the Folium maps.

## Downloading the Data

Both datasets are available as csv files through Open FEMA. The policies data can be found [here](https://www.fema.gov/openfema-data-page/fima-nfip-redacted-policies-v1) and the claims data [here](https://www.fema.gov/openfema-data-page/fima-nfip-redacted-claims-v1).

## Run the Notebooks

Next, head over to notebooks folder and read or run the notebooks that pique your interest.

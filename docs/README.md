# Mind games
Encapsulates o series of interactive games with the purpose of increasing one's mood.

## Getting started
In order to get started you need to go through these simple steps:

### 1. Prerequisites
+ Make sure you have Python3 installed, it won't work with Python2.
    + If you haven't got Python3 on your system, make sure to download it from [here](https://www.python.org/).
+ Clone or download this repository locally.
+ Create a Python3 virtual environment.
    + The purpose of this virtual environment is to isolate the game's package dependencies.
    + (Since python3.6): ```python3 -m venv /path/to/new/virtual/environment```
    + (Before python3.6): ```Just upgrade to 3.6 or later, the future is now.```
    + Activate the virtual environment by running the following:
        + (Windows): ```/path/to/new/virtual/environment/Lib/Scripts/activate```
        + (Unix systems): ```source /path/to/new/virtual/environment/bin/activate```

### 2. Change directory into the projct root (everything you do will be done from here)

### 3. Install package dependencies
```pip install -r requirements.txt```

### 4. Running the tests
```nosetests``` (This command should show absolutely no errors.)

### 5. Running the game
+ ```python -m bin.webapp```
+ Open your favourite browser and punch in: http://localhost:8080/

## Contributing
This game can benefit from your ideas should you have any, mind you, a new game even.  
Just do your thing and open a pull request and I'll review it.  
Regarding performance, this is just a fun project, however one should not wait like seconds between requests and responses.  
Before opening a pull request read the **Code style** section below.  

### Code style
This project follows [PEP8](https://www.python.org/dev/peps/pep-0008/) **VERY STRICTLY** (don't believe me? skim read throught the sources).

In order for your changes to be pulled into master do the following:
1. Read [PEP8](https://www.python.org/dev/peps/pep-0008/).
2. Read [PEP8](https://www.python.org/dev/peps/pep-0008/) again.
3. Repeat 1 & 2 until everything is flawless.



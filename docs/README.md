# Mind games
Encapsulates o series of interactive games with the purpose of increasing one's mood.

<table>
    <tr>
        <th rowspan="3">Tests</th>
        <th>Branch</th>
        <th>Status</th>
    </tr>
    <tr>
        <td>Master</td>
        <td><img src="https://travis-ci.com/mariusmucenicu/mind-games.svg?branch=master"></td>
    </tr>
    <tr>
        <td>Staging</td>
        <td><img src="https://travis-ci.com/mariusmucenicu/mind-games.svg?branch=staging"</td>
    </tr>
    <tr>
        <th>Issues</th>
        <td colspan="2" align="center">
            <img src="https://img.shields.io/github/issues/mariusmucenicu/mind-games.svg">
        </td>
    </tr>
    <tr>
        <th>State</th>
        <td colspan="2" align="center">
            <img src="https://img.shields.io/github/commits-since/mariusmucenicu/mind-games/0.1.0.svg">
        </td>
    </tr>
</table>

## Contents
+ [Getting started](https://github.com/mariusmucenicu/mind-games#getting-started)
+ [Versioning](https://github.com/mariusmucenicu/mind-games#versioning)
+ [Contributing](https://github.com/mariusmucenicu/mind-games#contributing)
+ [Code style guidelines](https://github.com/mariusmucenicu/mind-games#code-style-guidelines)

## Getting started
In order to get started you need to go through these simple steps:

### Step 1: Prerequisites
+ Make sure you have any version of `Python 3.6.X` installed.
    + If you haven't got a `Python 3.6.X` version on your system, you can download one from [here](https://www.python.org/).
+ Clone or download this repository locally.
+ Create a `Python 3.6.X` virtual environment (to isolate the game's package dependencies) and **activate** it.

### Step 2: Change directory into the projct root (everything you do will be done from here)

### Step 3: Install package dependencies
```pip install -r requirements.txt```

### Step 4: Running the tests
```nosetests``` (This command should show absolutely no errors.)

### Step 5: Running the game
+ ```python -m bin.webapp```
+ Open your favourite browser and punch in: http://localhost:8080/

## Versioning

This project adheres to [SemVer](http://semver.org/) for versioning.
For the versions available, see the [tags on this repository](https://github.com/mariusmucenicu/mind-games/tags).

- New major versions are exceptional and are planned very long in advance.
- New minor versions are feature releases; they get released roughly every 3 months.
- New patch versions are bugfix releases; they get released roughly every month.

## Contributing
This game can benefit from your ideas should you have any, mind you, a new game even.
Just do your thing and open a pull request and I'll review it.
Regarding performance, this is just a fun project, however one should not wait like seconds between requests and responses.
Before opening a pull request read the **Code style guidelines** section below.

## Code style guidelines

### Back-end style guide
+ This project follows [PEP8](https://www.python.org/dev/peps/pep-0008/) **very strictly** enforced with [Google's Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md). Don't believe me? skim read throught the sources.

### Front-end style guide

+ #### HTML/CSS
    + This project follows [Google's HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html) enforced with [W3C's HTML/CSS Style Guide](https://www.w3schools.com/html/html5_syntax.asp).

+ #### JavaScript
    + This project follows [Google's JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html) enforced with [W3C's JavaScript Style Guide](https://www.w3schools.com/js/js_conventions.asp).

In order for your changes to be **pulled into master** do the following:
1. Read the style guides above.
2. Read the style guides above **again**.
3. Repeat 1 & 2 until everything is flawless.



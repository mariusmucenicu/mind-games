# Mind games

Encapsulates o series of interactive games with the purpose of increasing one's mood. **:iphone: :computer: friendly**

<table>
  <tr>
    <th rowspan="3">State</th>
    <th>Branch</th>
    <th>Status</th>
  </tr>
  <tr>
    <td>Master</td>
    <td>
      <a href="https://travis-ci.com/mariusmucenicu/mind-games/branches">
        <img src="https://travis-ci.com/mariusmucenicu/mind-games.svg?branch=master"></a>
    </td>
  </tr>
  <tr>
    <td>Staging</td>
    <td>
      <a href="https://travis-ci.com/mariusmucenicu/mind-games/branches">
        <img src="https://travis-ci.com/mariusmucenicu/mind-games.svg?branch=staging"></a>
    </td>
  </tr>
  <tr>
    <th>Measurements</th>
    <td colspan="2" align="center">
      <a href="https://codecov.io/gh/mariusmucenicu/mind-games">
        <img src="https://codecov.io/gh/mariusmucenicu/mind-games/branch/master/graph/badge.svg"></a>
    </td>
  </tr>
  <tr>
    <th>To do</th>
    <td colspan="2" align="center">
      <a href="https://github.com/mariusmucenicu/mind-games/issues">
        <img src="https://img.shields.io/github/issues/mariusmucenicu/mind-games.svg"></a>
    </td>
  </tr>
  <tr>
    <th>Progress</th>
    <td colspan="2" align="center">
      <a href="https://github.com/mariusmucenicu/mind-games/compare/0.1.0...master">
        <img src="https://img.shields.io/github/commits-since/mariusmucenicu/mind-games/0.1.0.svg"></a>
    </td>
  </tr>
</table>

## Contents
+ [Development](https://github.com/mariusmucenicu/mind-games#development)
+ [Versioning](https://github.com/mariusmucenicu/mind-games#versioning)
+ [Code of conduct](https://github.com/mariusmucenicu/mind-games#code-of-conduct)
+ [Contributing](https://github.com/mariusmucenicu/mind-games#how-can-i-contribute)

## Development
In order to get started you need to go through these simple steps:

### Step 1: Prerequisites
+ Make sure you have any version of `Python 3.5.X, 3.6.X` installed.
    + If you **haven't got** any of the supported `Python` versions (mentioned above), you can download one from [here](https://www.python.org/).
+ Clone or download this repository locally.
+ (OPTIONAL) Create a `Python` virtual environment (to isolate the game's package dependencies) and **activate** it.

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

## Code of conduct
This project adheres to the Contributor Covenant [code of conduct](https://github.com/mariusmucenicu/mind-games/blob/master/docs/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How can I contribute?
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.  

- Before filing an **issue** or submitting a **pull request** please make sure you read the [project's contribution guidelines](https://github.com/mariusmucenicu/mind-games/blob/master/docs/CONTRIBUTING.md).
- **Performance-wise**:
    - This is just a fun project, however, one shouldn't wait like seconds between requests and responses.  

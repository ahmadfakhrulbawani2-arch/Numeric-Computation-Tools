# Numeric-Computation-Tool

## About

Numeric Computation Tool is a numerical approximation calculator that applies numerical computation methods.
This project is a continuation of a Linear Algebra course project that I developed last year.<br />

## Feature

1. Newton-Raphson
2. Coming soon...
<div align="center">
  <p>Overview:</p>
  <img src="/docs/Programs.jpeg">
</div>

## Get Started

### Prerequisites

1. You need to install Python 3 interpreter. You can choose any version, me personally using older Python 3 with version v3.12.0. You can install python [here](https://python.org)
2. Check using `python --version` if not showing the version then you need to adjust your OS environment variables.
3. You need to install version control like git bash. You can choose any version you wants. You can install it [here](https://git-scm.com)
4. Check again using `git --verison`

## How to Run

1. Clone this repo by copying this repo https URL like this:

```bash
git clone https://github.com/ahmadfakhrulbawani2-arch/Numeric-Computation-CLI.git <your_folder_name>
# you can put your_folder_name as you want. If you want to clone it in current folder, put '.' there
```

2. Go to root folder and find `requirements.txt`. Then you want to make Virtual Environment (venv). You can use any venv, but me personally use default venv like this:

```bash
# WARNING: if you are Linux/Mac OS make sure you install this first
sudo apt update
sudo apt-get install python3-venv
# Check venv
python -m venv --help
# make sure it show help info
# Then create venv
python -m venv .venv
# Then activate it using its scripts
cd ".venv/Scripts"
./activate
# back to root dir
cd ../../
```

3. You will see new folder of `.venv/` are created and the venv is turned on by seeing the left of your terminal have `(.venv)` (It may not shown on some terminal). Then you can install dependencies like this:

```bash
pip install -r requirements.txt
```

4. After the installation, you can run all program like this:

```bash
python main.py
```

5. Leave an issue of this repo [here](https://github.com/ahmadfakhrulbawani2-arch/Numeric-Computation-CLI/issues) if you find any error or bugs

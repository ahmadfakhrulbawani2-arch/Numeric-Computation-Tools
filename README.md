# Numeric-Computation-Tool

## ℹ️ About

<div align="center">
  <p>Overview:</p>
  <img src="/docs/main.png">
  <br /><br />
</div>

Numeric Computation Tool is a numerical approximation calculator that applies numerical computation methods.
This project is a continuation of a Linear Algebra course project that I developed last year.<br />

## Feature

1. Newton-Raphson
2. Coming soon...
<div align="center">
  <p>Overview:</p>
  <img src="/docs/Programs.jpeg">
</div>

## 📂 Project Directory Structure

TDOO

## ⚒️ Get Started

### Prerequisites

1. You need to install Python 3 interpreter. You can choose any version, me personally using older Python 3 with version v3.12.0. You can install python [here](https://python.org)
2. Check using `python --version` if not showing the version then you need to adjust your OS environment variables.
3. You need to install version control like git bash. You can choose any version you wants. You can install it [here](https://git-scm.com)
4. Check again using `git --verison`

### 🏃‍➡️ How to Run

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

## 🛠️ How to Contribute and Develop

This is complete step by step to contribute in this repo:

1. Clone this repo first. Step specified above.
2. Install all dependencies.
3. Create new branch in your local git like this:

```bash
git checkout -b <your_branch_name>
```

4. Now you can work to contribute in this repo
5. After changing spesific file and want to commit push, you need to sync your git main branch with this repo/remote main branch:

```bash
# go to your main branch
git checkout main

# pull changes. Usually the remote name is origin, but if you change it to anything else, please use that
git pull origin main
```

6. Go back to your branch and rebase with main. You can use merge but I highly recommend using rebase because it does not create new unnecessary commit

```bash
# go to your branch
git checkout -b <your_branch_name>

# save the tracked & untracked file
git stash -u

# rebase with main
git rebase main

# restore the stash
git stash pop
```

7. In case of any conflict you need to resolve it yourself. Ask AI or google it.
8. Commit and push as usual. But before that, format and lint your code:

```bash
# to lint your code in GNU
./scripts/lint.sh
# to lint your code in pwsh
./scripts/lint.ps1
```

```bash
git pull <your_remote_name> <your_branch_name>
git add .
git commit -m "your_commit_message"
git push <your_remote_name> <your_branch_name>
```

9. To merge it with main branch, open [pull request](https://github.com/ahmadfakhrulbawani2-arch/Numeric-Computation-CLI/pulls) and click new pull request. Select to compare main with your branch and merge it. No review needed btw.

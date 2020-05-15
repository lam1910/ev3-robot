# GLOBAL SOFTWARE PRODUCT DEVELOPMENT - TEAM 5 - COURSE PROJECT

**Get The Repository**

```bash
    git clone https://github.com/TimSvensson/gsdp2018-team5.git
```

---

## RULES FOR CODE COLLABORATION

* A simple branching work-flow will be adopted.

* Users will create a new branch with master as a base and will name it appropriately with the user story they are currently working on.

**WHEN THE HEAD IS AT MASTER**

```bash
    git branch
```

*OUTPUT :*

```bash
    * master
```

```bash
    git checkout -b <NAME OF THE USER STORY>
```

**USER WILL WORK IN THEIR RESPECTIVE BRANCHES BRANCH**

* Users will always add proper commit messages.

*EX :*
```bash
    git commit README.md -m "Updated README file with rules for code collaboration"
```

* Users will always push to their respective branches

```bash
    git push origin <NAME OF THE USER STORY>
```

* A minor code review will be employed before a pull request can be opened.

* Finally the user can create a pull request via github, which will be approved by the project owner.

---

# SETUP A BLUETOOTH PERSONAL AREA NETWORK

## REQUIREMENTS

    * GNU/Linux OS - (Debian, Fedora, LinuxMint, Ubuntu)
    * Python3

**USE THE FOLLOWING COMMAND IN EV3DEV TO SETUP CONNECTION**

```bash
    sudo apt-get install bluetooth libbluetooth-dev python3-pip

    sudo python3 -m pip install pybluez
```

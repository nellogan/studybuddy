[![CI](https://github.com/nellogan/studybuddy/actions/workflows/CI.yml/badge.svg)](https://github.com/nellogan/studybuddy/actions/workflows/CI.yml)

# Description
Optimize Leetcode study sessions by scraping provided URLs to local files with preconfigured imports/includes and supporting build files.

What studybuddy does:

    1. Creates a directory for current session.
    2. Each question will have its own sub-directory created.
    3. Each sub-directory will contain a solution file. This file will automatically import/include 
       commonly used data structures for the selected language. For C++, the file will have a main function as well as
       a make file generated. Run the C++ solution file by simply calling 'make' or 'make run'
    4. Creates a session log, 'log.txt', that will note the difficulty and suggested time limit based on the difficulty
       rating. Allows the user to take notes per question such as start time, end time, link to a discussion post
       with a clean answer for comparison or review. This log header will also be included in the solution file so
       that it can be seamlessly copy pasted back into the log.txt file.
    5. The log file can be omitted by passing the -n commandline option.

For example, passing URL: https://leetcode.com/problems/two-sum/ will produce a file called 'TwoSum.py' (if 
Python selected). Since the question is marked Easy, the suggested time limit will be set to 20 minutes 
(Easy: 20 minutes, Easy: 30 minutes, Hard: 40 minutes).


Studybuddy increases study efficiency by:
    
    1. Eliminating boilerplate associated with copying question information to a local IDE or file, rather than relying 
        on Leetcode's brower editor and test cases.
    2. Automatically generating a study journal to keep track of progress. Very useful for spaced repitition of problem
       sets. Enabling the user to waste less time managing a study journal.
    3. Neatly consolidating the study session into one directory.


# Installation
Requires Python3, chromium, and the chromedriver to be installed. The only supported operating system is Linux.

Both the chromium and chromium-driver packages are required to interface with Selenium. For C++ problems,
makefile is assumed to be installed. If using a debian based distribution:

    sudo apt install chromium chromium-driver

## Install From Source:

    git clone https://github.com/nellogan/studybuddy.git
    python3 -m venv ./.venv
    source ./.venv/bin/activate
    pip install .

### Option 1: venv will need to be activated every time before directly calling studybuddy, for example:
    
    source ./.venv/bin/activate
    studybuddy [args]

### Option 2 (cleaner method): Create a symlink to /usr/local/bin so that venv does NOT need to be activated beforehand

    sudo ln -s $PWD/.venv/bin/studybuddy /usr/local/bin/studybuddy
    # Now studybuddy will persist in $PATH
    studybuddy [args]

## Uninstall
    
    cd $INSTALL_DIR
    source ./.venv/bin/activate
    pip uninstall studybuddy
    #If used Option 2 of 'Install from source': sudo rm /usr/local/bin/studybuddy

# How To Use

    studybuddy -h
    usage: studybuddy [-h] [-l LANGUAGE] [-n] (-q QUESTION | -f QUESTIONS_FILE) DESTINATION_DIR
        
    Optimize Leetcode study sessions by scraping provided URLs code data to local files with preconfigured imports/includes and supporting build files. Generates a log header per file and a
    consolidated log file in the destination directory.
    
    positional arguments:
      DESTINATION_DIR       (Required) destination directory (will recursively create directories if they do not exist)
    
    options:
      -h, --help            show this help message and exit
      -l, --language LANGUAGE
                            (Optional) specify language, only Python3 and C++ are supported. Defaults to Python3 if omitted
      -n, --no_log          (Optional) turn off logging
      -q, --question QUESTION
                            (Required, mutually exclusive to -f) URL of question
      -f, --questions_file QUESTIONS_FILE
                            (Required, mutually exclusive to -q) path to file that contains question urls that are newline separated
    
    For suggestions or bug reports, raise an issue at 'https://github.com/nellogan/studybuddy/issues'

Python3 is the default language. Currently only Python3 and C++ are supported.

For a single question, let URL=https://leetcode.com/problems/two-sum:

    studybuddy /path/to/destination -q $URL
    #Solve the question and validate solution with any test cases developed with (optionally fill out header/log):
    python3 /path/to/destination/TwoSum.py

For multiple questions, create a file that contains a question url on each line, for example: "URLS_FILE=./questions_file"
where the file contains https://leetcode.com/problems/two-sum/description and https://leetcode.com/problems/add-two-numbers.

    studybuddy /path/to/destination -f $URLS_FILE -l C++
    #Solve TwoSum and validate solution with any test cases developed with (optionally fill out header/log):
    cd /path/to/destination/TwoSum && make
    #Solve AddTwoNumbers and validate solution with any test cases developed with (optionally fill out header/log) 
    cd /path/to/destination/AddTwoNumbers && make


# License Information
This project uses Selenium, which is licensed under the Apache 2.0 License. See the `selenium_license` directory for the 
Selenium LICENSE and NOTICE files.

studybuddy is licensed under the Apache 2.0 License, see files LICENSE and NOTICE in the root directory.


# Suggestions or Issues
For any suggestions such as support for a new language or any bugs are found, raise an issue at: https://github.com/nellogan/studybuddy/issues

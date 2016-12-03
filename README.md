# Snipped
## Snippet client for glot.io written in Python!

## Description:

##### This is a simple program written in Python that can be used as a basic snippet client for [glot.io](https://glot.io).
##### You can use it to post, download, delete and update snippets from glot.io, serving as a good CLI client.

##### To delete or update snippets, you'll be required to input your [Authorization Token (API Token)](https://glot.io/account/token) when prompted, or put it on the AUTH_TOKEN variable on the source code, in case you don't want to show it on the terminal or don't want to type it everytime.

##### To post a snippet, the Authorization Token is optional. Not using it means you'll post it anonymously. 

##### The program will ask for the programming language of the snippet, a name for the snippet, the optional Token in case you want to save it on your account (this prompt will not appear if you insert your Token in the AUTH_TOKEN variable) and the availability of the snippet (public or secret). These same steps will happen when updating a snippet and the program will ask for the URL of the snippet to be updated.

##### Downloading snippets doesn't require the Token. It will ask for the URL of the snippet and will create a directory for it, inside the 'Snippets' directory (the program will create one if it doesn't exists) in your home directory.

##### When deleting snippets, you'll need the Token and the URL of the snippet to be deleted. Keep in mind that once this is done, you cannot revert it! Anonymous snippets, even the one's written or uploaded by you, cannot be deleted.

## [Check the CHANGELOG for more informations about newer versions](https://raw.github.com/Wolfterro/Snipped/master/CHANGELOG.txt)

## Options:

#### These are the available options of the program:

    -h || --help      Show the help menu.
    -p || --post      Select files to be posted. At least one file is required!
    -d || --delete    Delete snippet from the website. Cannot be undone!!
    -g || --get       Download the snippet files to your computer.
    -u || --update    Update the snippet files from the website. At least one file is required!

#### Usage:

    Help:
    -----
    ./Snipped.py [-h / --help]
    
    Post Snippets (Authorization Token is optional):
    ------------------------------------------------
    ./Snipped.py [-p / --post] [FILE 1] [FILE 2] ... [FILE 6]
    
    Delete Snippets (Requires Authorization Token):
    -----------------------------------------------
    ./Snipped.py [-d / --delete] [URL]
    
    Update Snippets (Requires Authorization Token):
    -----------------------------------------------
    ./Snipped.py [-u / --update] [FILE 1] [FILE 2] ... [FILE 6]
    
    Download Snippets:
    ------------------
    ./Snipped.py [-g / --get] [URL]

## Requirements:

- Python 2.7
- PycURL + libcURL

#### You can install PycURL by using python-pip:

    sudo pip install pycurl

##### cURL and it's libraries normally comes preinstalled in various distros, but in case you don't have it, it's recommended to install it just in case.

#### Ubuntu/Debian/Linux Mint:

    sudo apt-get install curl libcurl-dev

## Download:

#### You can download Snipped by cloning this repo with git:

    git clone https://github.com/Wolfterro/Snipped.git
    cd Snipped/
    chmod +x Snipped.py
    ./Snipped.py --help

#### In case you don't have git installed on your system, you can download this repo by clicking on the "Clone or download" button ontop of the page and download the zip file, or by clicking [here!](https://github.com/Wolfterro/Snipped/archive/master.zip)

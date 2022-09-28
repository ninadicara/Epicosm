
  ![release](https://img.shields.io/badge/release-1.0.0-brightgreen)
  [![GPLv3 license](https://img.shields.io/badge/licence-GPL_v3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
  [![DOI](https://zenodo.org/badge/405694270.svg)](https://zenodo.org/badge/latestdoi/405694270)


## Overview
Epicosm: a framework for linking online social media in epidemiological cohorts.
Epicosm is a suite of tools for working with social media data in the context of
epidemiological research. It is aimed for use by epidemiologists who wish to gather, analyse
and integrate social media data with existing longitudinal and cohort-study research.
The tools can:
* Harvest ongoing and retrospective Tweets from a list of users.
* Harvest a "pseudofeed" of users - the recent tweets of the accounts being followed.
* Sentiment analysis of Tweets using labMT, Vader and LIWC (dictionary required for LIWC).

## Instructions in a nutshell
#### 1. [Download the Epicosm repository](https://github.com/DynamicGenetics/Epicosm/archive/refs/heads/main.zip), or clone the repo to your local machine.

#### 2. Install [MongoDB](https://www.mongodb.com/) version 4 or higher:
  * In a Mac terminal `brew install mongodb`
  * In a Linux terminal `apt install mongodb`

#### 3. Provide your Twitter API authorisation token:
  * Complete the `bearer_token.py` file with your own bearer token. You will need to acquire a Twitter developer account, so please search for the current details on how to do that. Epicosm functions best with an approved academic developer account, which grants access to the `full archive` v2API, allowing complete timelines to be recovered. Search for current documentation on how to do this on the [Twitter Developer Portal](https://developer.twitter.com/en).

#### 4. Install the required Python packages:
  * We recommend running Epicosm in a clean python virtual environment. On the command line you can create a new virtual environment with

`python -m venv ./venv`

then activate this clean environment with

`source ./venv/bin/activate`

and finally install the required dependencies with

`pip install -r requirements.txt`

You are now ready to run Epicosm. To leave your Python virtual environment, type `deactivate`.

#### 5. Run Epicosm from your command line, including your run flags
  * Epicosm will provide some help if it doesn't understand you, or just type `python epicosm.py` for usage and documentation. See below for more details, but for example a typical harvest can be started with

`python epicosm.py --harvest`

<p align="center"> ••• </p>

## More detail
#### 1 What does it do?  
#### 2 Running the Python scripts
#### 3 Optional parameters
#### 4 Natural Language Processing (Sentiment analysis)
#### 5 Data and other outputs
#### 6 Licence

<p align="center"> ••• </p>

### 1 What does it do?

Epicosm is a social media harvester, data manager and sentiment analyser. Currently, the platform uses Twitter as the data source and the sentiment analysis methods available are VADER, labMT and LIWC (you will need an LIWC dictionary for this). You provide a list of users, and it will gather and store all tweets and metadata for each user. If you have a standard developer account, Epicosm can only retrieve the most 3,200 tweets from each user. With an approved academic researcher account, it can gather complete timeline histories from users. Images, videos and other attachments are stored as URLs. All information is stored by MongoDB. Harvesting can be iterated, for example once a week it can gather new tweets and add them to the database. As well as the full database, output includes a comma-separated-values (.csv) file, with the default fields being the user id number, the tweet id number, time and date, and the tweet content. Epicosm can also harvest the "following" list of users, but only to a depth of the last seven days (ie, *this approximates a users feed, or at least the pool of accounts from which the feed is built.*).

You will need Twitter API credentials by having a developer account authorised by Twitter. Please see our [guide to getting an authorised account](https://github.com/DynamicGenetics/Epicosm/blob/master/Twitter_Authorisation.pdf), and there are further details on [Twitter documentation](developer.twitter.com/en/apply-for-access.html) for how to do this. As of summer 2021, Twitter are more stringent when issuing academic research accounts and you will need to clearly describe the research purposes and institutional backing of your work, but these provide significantly elevated API access rights. **You may find many guides for getting authorisation which are out of date!**

Epicosm uses [MongoDB](https://www.mongodb.com/) for data management, and this must be installed before being running Epicosm. This can be done through downloading and installing from the MongoDB website, or it can be done in a Terminal window with the commands
`brew install mongodb` on a Mac
`apt install mongodb` on Linux (Debian-based systems like Ubuntu).

<p align="center"> ••• </p>

### 2 Running the Python scripts

`epicosm.py` is the harvesting program.
`python epicosm.py [your run flags]`

You must provide 2 files:
1. a list of user screen names in a file called `user_list`. The user list must be a plain text file, with a single username (twitter screen name) per line. You can have the `@` symbol included or not, Epicosm with recognise either.
2. Twitter API credentials will need to be supplied, by editing the file `bearer_token.py` (further instructions inside file). You will need your own Twitter API token by having a developer account authorised by Twitter, and generating the required codes. Please see [our guide](https://github.com/DynamicGenetics/Epicosm/blob/master/Twitter_Authorisation.pdf), and there are further details on [Twitter documentation](developer.twitter.com/en/apply-for-access.html) on how to do this.

Please also see these further requirements.

1. Put all repository files and your user list into their own folder. The python script must be run from the folder it is in.
2. MongoDB version 4 or higher will need to be installed. It does not need to be running, the script will check MongoDB's status, and start it if it is not running. The working database will be stored in the folder where you place your local copy of this repository (not the default location of /data/db). For Linux and MacOS, use your package manager (eg. apt, yum, yast), for example:

`apt install mongodb` (or `yum`, `brew` or other package manager as appropriate)

3. The file `requirements.txt` contains the names of all the dependencies, and these can be simply installed with the command

`pip3 install -r requirements.txt`

<p align="center"> ••• </p>

### 3 Optional parameters
When running the harvester, please specify what you want Epicosm to do:

```
  --harvest      Harvest tweets from all users from a file called user_list (provided by you) with a single user per line.
  --get_follows  Create a database of the users that are being followed by the accounts in your user_list. (This process can be very slow, especially if your
                 users are prolific followers.)
  --pseudofeed   Harvest recent tweets from the users being followed by a user. (This process can be very slow and take up a lot of storage, especially if
                 your users are prolific followers.)
  --repeat       Repeat the harvest every . This process will need to be put to the background to free your terminal prompt.
  --refresh      If you have a new user_list, this will tell Epicosm to switch to this list.
  --start_db     Start the MongoDB daemon in this folder, but don't run any Epicosm processes.
  --stop         Stop all Epicosm processes.
  --shutdown_db  Stop all Epicosm processes and shut down MongoDB.
  --log          Create a logfile rather than printing progress to terminal.
```

Examples
A single harvest:
`python epicosm.py --harvest`

Harvest once a week, with a renewed user_list:
`python epicosm.py --harvest --refresh --repeat 7`

Harvests can take a few hours per thousand users - connection and traffic dependent. In order to run processes in the background, we recommend starting a `tmux` session, starting the process appended with an ampersand `&` to put it into the background, and detaching the `tmux` session. Putting the process into `tmux` is required if you are running a repeated session.

<p align="center"> ••• </p>

### 4 Natural Language Processing (Sentiment analysis)

Once you have a database with tweets, you can apply sentiment analysis to each document and insert the result into MongoDB with `python epicosm_nlp.py`.

To run, specify from the following flags:

`--insert_groundtruth` Provide a file of groundtruth values called 'groundtruth.csv' and insert these into the local database.

`--liwc` Apply LIWC (Pennebaker et al 2015) analysis and append values to the local database. You must have a LIWC dictionary in therun folder, named "LIWC.dic". LIWC has around 70 categories (including posemo and negemo), but many of these will return no value because tweets are too short to provide information. Empty categories are not appended to the database. **Note: the LIWC package is broken and cannot deal with its own dictionary. If it comes across phrasal entries it throws a key error. In LIWC 2015, most of these are variations on the word 'like' ('we like', 'they like', 'not like'), but the words 'like', 'not' 'we' are already in categories, and the phrasal categories have the same metrics anyway! You will need to clean your dictionary with the script in src called `cleanLIWC.sh`.

`--labmt` Apply labMT (Dodds & Danforth 2011) analysis and append values to the local database. LabMT provides a single positive - negative metric, ranging from -1 to 1 (1 being positive sentiment, 0 being neutral, -1 being negative).

`--vader` Apply VADER (Hutto & Gilbert 2014) analysis and append values to the local database. VADER returns 4 metrics: positive, neutral, negative and compound. See their documentation for details.

`--textblob` Apply TextBlob (github: @sloria) analysis and append values to the local database. TextBlob provides a single positive - negative metric, ranging from -1 to 1 (1 being positive sentiment, 0 being neutral, -1 being negative).

The results of these analyses will be appended to each tweet's record, under the field "epicosm", and stored in MongoDB.

<p align="center"> ••• </p>

### 5 Data and other outputs
The primary data is the database stored in MongoDB. Epicosm will create a DB called `twitter_db`, and collections called `tweets`, `follows` and `pseudofeed`. You can interact with MongoDB on the command line with `mongo`. To view and interact with the database using a GUI we find that [Robo 3T](https://robomongo.org/) works very well.

Log files are stored in `/epicosm_logs/`.

A backup of the entire database is stored in `/output/twitter_db/`. If you have MongoDB installed, this can be restored with the command

`mongorestore [your name given to the database] [the path to the mongodump bson file]`

for example:

`mongorestore -d twitter_db ./output/twitter_db/tweets.bson`

(However, please check [MongoDB documentation](https://docs.mongodb.com/manual/) as commands can change)

<p align="center"> ••• </p>

### 6 Licence
DynamicGenetics/Epicosm is licensed under the GNU General Public License v3.0. For full details, please see our [license](https://github.com/DynamicGenetics/Epicosm/blob/master/LICENSE) file.

Epicosm is written and maintained by [Alastair Tanner](https://github.com/altanner), University of Bristol, Integrative Epidemiology Unit.

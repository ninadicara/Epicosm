## Overview
As we go about our daily lives, each of us lays down digital footprints, such as through our interactions on social media, our search behaviour, and the things we buy. This vast repository of data on real life behaviour has huge potential to inform the research carried out by epidemiological cohorts into the causes of poor health.

Although it is straightforward to collect social media data from consenting study participants via the application programming interfaces (APIs) that social media sites make available, there are challenges specific to linking these data in birth cohorts. For example, cohorts have a responsibility to protect the identity of their participants. To do this, they maintain data safe havens certified by the International Organization for Standardisation (ISO) and the International Electrotechnical Commission (IEC), and ensure that participants’ personal and identifiable data remain inside these havens. This means that instead of providing a centralised service to cohorts, it is easier for cohorts to run social media linking software themselves, within their own data safe havens.

We designed the Epicosm software to make it as straightforward as possible for epidemiological cohorts to run ongoing social media linkage themselves, keeping all participant data within their data safe havens. We collaborated with cohort leaders and participants to make sure the software was as useful as possible while meeting the expectations of the people donating their data for research.

Epicosm can:
* collect previous and ongoing Twitter updates from a list of participants
* collect Tweets from accounts those participants are following to give a sample of the updates they are likely to see when browsing Twitter
* infer the mood of the collected Tweets using some of the most widely used approaches:  LabMT, Vader and (with a separate licence from the publisher) LIWC

## Accessing the Twitter API
To run Epicosm, you will need to [apply for an authorisation token (bearer token) from Twitter itself](https://developer.twitter.com/en/use-cases/do-research/academic-research) by registering for a Developer Account. Academic researchers are then able to apply for free access to the full Twitter archive.

You will need to install the Epicosm software on an appropriate server (currently Linux or MacOS) that will run long-term to download participants’ Tweets and update a data base:

## Installation and quick start
#### 1. Download Epicosm using one of the links above.
#### 2. [Install MongoDB](https://www.mongodb.com/docs/manual/administration/install-community/) version 4 or higher, following the instructions for your platform.
#### 3. Add your own Twitter API authorisation token
When you applied for a Twitter Developer account, you should have received a code called a `bearer token`. Add this to the `bearer_token.py` file in Epicosm’s top level directory.
#### 4. Install the required Python packages
Epicosm is written in the Python programming language (version 3), and it requires certain Python packages to work. We suggest setting up a new virtual Python environment to run Epicosm, like this (in a terminal window):

`python -m venv ./venv`

then activate this clean environment with

`source ./venv/bin/activate`

and finally install the required dependencies with

`pip install -r requirements.txt`

You are now ready to run Epicosm.
#### 5. Run Epicosm
You can see the options for running Epicosm by typing `python epicosm.py` while in the software’s top level directory. There are some more detailed guidelines below, but you can start a typical data collection by typing:

`python epicosm.py --harvest`

<p align="center"> ••• </p>

## Detailed guidelines
#### 1 What does Epicosm do?  
#### 2 Running the Python scripts
#### 3 Optional parameters
#### 4 Natural Language Processing (Sentiment analysis)
#### 5 Data and other outputs
#### 6 Licence

<p align="center"> ••• </p>

### 1 What does Epicosm do?
Epicosm is a social media harvester, data manager and sentiment analyser. Currently, the platform uses Twitter as the data source and the sentiment analysis methods available are VADER, labMT and LIWC (you will need a licenced LIWC dictionary for this). You provide a list of users, and it will gather and store all tweets and metadata for each user. If you have a standard developer account, Epicosm can only retrieve at most 3,200 tweets from each user. With an approved academic researcher account, however, it can gather complete timeline histories from users. Images, videos and other attachments are stored as URLs. All information is stored in a MongoDB data base. Harvesting can be repeated, for example once a week it can gather new tweets and add them to the data base. As well as the full database, output includes a comma delimited (.csv) file with, by default, the user id number, the tweet id number, time and date, and the tweet content. Epicosm can also harvest Tweets from accounts users are following, but only the last seven days. This is the pool of Tweets from which a user’s Twitter feed is built, although the actual Tweets seen are governed by Twitter’s own algorithms.

To use Epicosm, you will need to get Twitter API credentials by [applying for a Twitter developer account](developer.twitter.com/en/apply-for-access.html). Academic users can apply for elevated access rights by providing a description of their research project, providing it meets Twitter’s criteria.

Epicosm uses [MongoDB](https://www.mongodb.com/) for data management, and you will need to [install this](https://www.mongodb.com/docs/manual/administration/install-community/) before running the software.

<p align="center"> ••• </p>

### 2 Running the Python scripts
`epicosm.py` is the harvesting program. You can run it like this:

`python epicosm.py [your run flags]`

Before running Epicosm, you must:
1. Provide a list of user screen names in a file called `user_list` at the top level of the Epicosm directory. The user list must be a plain text file, with a single user name (twitter screen name) per line. You can start each name with the `@` symbol or not; Epicosm will recognise either.
2. You will also need to supply Twitter API credentials by editing the `bearer_token.py` file in the top level of the Epicosm directory (there are further instructions inside the file). This needs to be your own bearer token from your Twitter developer account.
3. Install MongoDB version 4 or higher. It does not need to be running when you start Epicosm: the script will check MongoDB's status, and start it if it is not already running. The working data base will be stored in Epicosm’s top level directory.
4. Install Epicosm’s Python dependencies. They are listed in the  `requirements.txt` file, and these can be installed with a command such as

`pip3 install -r requirements.txt`

<p align="center"> ••• </p>

### 3 Optional parameters
When running the harvester, you can use these options to tell Epicosm what to do:

```
  --harvest      Harvest tweets from all user names in a file called user_list (with a single user per line)
  --get_follows  Create a database of the users that are being followed by the accounts in your user_list. (This process can be very slow, especially if your users are each following a lot of accounts)
  --pseudofeed   Harvest recent tweets from accounts followed by those in your user_list. (This process can be very slow and take up a lot of storage, especially if your users are following a lot of accounts.)
  --repeat       Specify how often to repeat the harvest e.g. “—repeat 7” means repeat every seven days
  --refresh      If you have a new user_list, this will tell Epicosm to switch to this list
  --start_db     Start the MongoDB daemon in this folder, but don't run any Epicosm processes
  --stop         Stop all Epicosm processes
  --shutdown_db  Stop all Epicosm processes and shut down MongoDB
  --log          Create a log file rather than printing progress to terminal
```

For example:

A single harvest:
`python epicosm.py --harvest`

Harvest once a week, with a refreshed user_list:
`python epicosm.py --harvest --refresh --repeat 7`

Harvests can take a few hours per thousand users, depending on connection speed and network traffic. To run the Epicosm processes in the background, freeing up your terminal, we recommend starting a `tmux` session, starting the process appended with an ampersand `&` to put it into the background, and detaching the `tmux` session. Putting the process into `tmux` is required if you are running a repeated session.

<p align="center"> ••• </p>

### 4 Sentiment analysis

Once you have a database with tweets, you can apply sentiment analysis to each document and add the result to each Tweet’s MongoDB record with `python epicosm_nlp.py`.

To run, choose from the following options:

`--insert_groundtruth` Provide ground truth values (estimates of sentiment from a different source) in a file called 'groundtruth.csv' and add these to the local database

`--liwc` Apply LIWC (Pennebaker et al 2015) analysis and append the results to the local database. You must have a LIWC dictionary (named “LIWC.dic”) in the directory you are running Epicosm in. LIWC has around 70 categories, including positive emotion (posemo) and negative emotion (negemo), but many of these will return no value because the short Tweets do not include words in these categories. Empty categories are not appended to the database.

`--labmt` Apply labMT (Dodds & Danforth 2011) analysis and append values to the local database. LabMT provides a single score, ranging from -1 to 1 (1 being most positive sentiment, 0 being neutral, -1 being most negative).

`--vader` Apply VADER (Hutto & Gilbert 2014) analysis and append values to the local database. VADER returns 4 metrics: positive, neutral, negative and compound. See the VADER documentation for details.

`--textblob` Apply TextBlob (github: @sloria) analysis and append values to the local database. TextBlob provides a single score, ranging from -1 to 1 (1 being most positive sentiment, 0 being neutral, -1 being most negative).

The results of these analyses will be appended to each tweet's record, under the field "epicosm", and stored in MongoDB.

<p align="center"> ••• </p>

### 5 Data and other outputs
The primary data are stored in the MongoDB database. Epicosm will create a data base called `twitter_db`, and collections called `tweets`, `follows` and `pseudofeed`. You can interact with MongoDB on the command line with `mongo`. To view and interact with the database using a graphical user interface, we find that [Robo 3T](https://robomongo.org/) works very well.

Log files are stored in `/epicosm_logs/`.

A backup of the entire database is stored in `/output/twitter_db/`. If you have MongoDB installed, this can be restored with the command

`mongorestore -d [your name given to the database] [the path to the mongodump bson file]`

for example:

`mongorestore -d twitter_db ./output/twitter_db/tweets.bson`

Please check the [MongoDB documentation](https://docs.mongodb.com/manual/) for the most up-to-date version of the commands.

<p align="center"> ••• </p>

### 6 Licence
DynamicGenetics/Epicosm is licensed under the GNU General Public License v3.0. For details, please see the [license file](https://github.com/DynamicGenetics/Epicosm/blob/master/LICENSE).

Epicosm is written and maintained by [Dr Alastair Tanner](https://github.com/altanner) in the University of Bristol Research Software Engineering team.

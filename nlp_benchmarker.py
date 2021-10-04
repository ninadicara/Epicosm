
#~ Standard library imports
import time
import csv
import sys
import os
import re
from collections import namedtuple, Counter

#~ 3rd party imports
import pymongo
from alive_progress import alive_bar
import liwc
from textblob import TextBlob

#~ Local application imports
sys.path.append("./modules")
from modules import (
    mongo_ops,
    epicosm_meta,
    twitter_ops,
    nlp_ops,
    env_config,
    mongodb_config,
    vader_sentiment,
    labmt)


def vader_runner(text):

    # print(f"Vader sentiment, analysing...")

    #~ initialise analyser
    analyser = vader_sentiment.SentimentIntensityAnalyzer()

    #~ vader process
    vader_negative = analyser.polarity_scores(text)["neg"]
    vader_neutral = analyser.polarity_scores(text)["neu"]
    vader_positive = analyser.polarity_scores(text)["pos"]
    vader_compound = analyser.polarity_scores(text)["compound"]

    # print(f"Vader positive:     {vader_positive}")
    # print(f"Vader negative:     {vader_negative}")
    # print(f"Vader neutral:      {vader_neutral}")
    # print(f"Vader compound:     {vader_compound}")


def labmt_runner(text):

    # print(f"labMT sentiment, analysing...")

    lang = "english"
    labMT, labMTvector, labMTwordList = labmt.emotionFileReader(stopval=0.0, lang=lang, returnVector=True)

    #~ compute valence score and return frequency vector for generating wordshift
    valence, frequency_vector = labmt.emotion(
        text,
        labMT,
        shift=True,
        happsList=labMTvector)

    #~ assign a stop vector
    stop_vector = labmt.stopper(
        frequency_vector,
        labMTvector,
        labMTwordList,
        stopVal=1.0)

    #~ get the emotional valence
    output_valence = labmt.emotionV(stop_vector, labMTvector)

    # print(f"LabMT:      {output_valence}")


def textblob_runner(text):

    # print(f"TextBlob sentiment, analysing...")

    #~ we want textblob to ignore sentences and take tweets as a whole
    text_clean = text.replace(".", " ")

    blob = TextBlob(text_clean)
    blob.tags
    blob.noun_phrases

    for sentence in blob.sentences:

        tb = float(format(sentence.sentiment.polarity, '.4f'))
        # print(f"Textblob:       {tb}")


def liwc_runner(text):

    #~ Look for an LIWC dictionary
    if os.path.isfile('./LIWC.dic'):
        dictionary = "LIWC.dic"
    else:
        print(f"Please have your dictionary here, named LIWC.dic")
        return #~ abort LIWC if not dictionary

    def tokenize(text):

        """Split each text entry into words (tokens)"""

        for match in re.finditer(r"\w+", text, re.UNICODE):
            yield match.group(0)

    # print(f"LIWC sentiment, analysing...")

    parse, category_names = liwc.load_token_parser(dictionary)

    word_count = len(re.findall(r'\w+', text))
    text_tokens = tokenize(text)
    text_counts = Counter(category for token in text_tokens for category in parse(token))

    for count_category in text_counts:  #~ insert the LIWC values as proportion of word_count

        result = float(format((text_counts[count_category] / word_count), '.4f'))
        # print(f"{count_category}:       {result}")


def main():

    with open("65k_random_words", "r") as infile:

        text = infile.read()

        words1000 = " ".join(text.split()[:1000])
        words2000 = " ".join(text.split()[:2000])
        words3000 = " ".join(text.split()[:3000])
        words4000 = " ".join(text.split()[:4000])
        words5000 = " ".join(text.split()[:5000])
        words6000 = " ".join(text.split()[:6000])
        words7000 = " ".join(text.split()[:7000])
        words8000 = " ".join(text.split()[:8000])
        words9000 = " ".join(text.split()[:9000])
        words10000 = " ".join(text.split()[:10000])
        words15000 = " ".join(text.split()[:15000])
        words100 = " ".join(text.split()[:100])
        # words200 = " ".join(text.split()[:200])
        # words400 = " ".join(text.split()[:400])
        # words800 = " ".join(text.split()[:800])
        # words1600 = " ".join(text.split()[:1600])
        # words3200 = " ".join(text.split()[:3200])
        # words6400 = " ".join(text.split()[:6400])
        # words12800 = " ".join(text.split()[:12800])
        # words25600 = " ".join(text.split()[:25600])
        # words51200 = " ".join(text.split()[:51200])

        testset_list = [
            words1000,
            words2000,
            words3000,
            words4000,
            words5000,
            words6000,
            words7000,
            words8000,
            words9000,
            words10000,
            words15000]

        # testset_list = [
        #     words100,
        #     words200,
        #     words400,
        #     words800,
        #     words1600,
        #     words3200,
        #     words6400,
        #     words12800,
        #     words25600,
        #     words51200]

        method_list = [
            vader_runner,
            liwc_runner,
            textblob_runner,
            labmt_runner]

        for method in method_list:

            print(method.__name__)

            start_time = time.time()

            for x in range(0, 100):

                # print(f"{len(testset.split())} words")

                method(words100)

            print(time.time() - start_time)

            start_time = time.time()
            method(words10000)
            print(time.time() - start_time)

        # for method in method_list:

        #     print(method)

        #     for testset in testset_list:

        #         # print(f"{len(testset.split())} words")
        #         start_time = time.time()

        #         method(testset)

        #         print(time.time() - start_time)



if __name__ == "__main__":

    main()
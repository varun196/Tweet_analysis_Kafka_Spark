from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import matplotlib.pyplot as plt

def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")

    sc.setLogLevel("WARN")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")
   
    counts = stream(ssc, pwords, nwords,100)
    make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    """
    l_pos = []
    l_neg = []
    for list_ele in counts:
        f_pos,f_neg=0,0
        for tup in list_ele:
            if "positive" in tup:
                l_pos.append(tup[1])
                f_pos=1
            if "negative" in tup:
                l_neg.append(tup[1])
                f_neg=1
        if f_pos == 0:
            l_pos.append(0)
        if f_neg == 0:
            l_neg.append(0)
    plt.plot(l_pos,label="positive",marker='.',color="blue")
    plt.plot(l_neg,label="negative",marker='.',c="green")
    plt.legend(loc="upper left")
    plt.xlabel("Time step")
    plt.ylabel("Word count")
    plt.show()
   


def load_wordlist(filename):
    """ 
    Returns a list or set of words from the given filename.
    """
    word_list = open(filename,"r").readlines()
    word_set = set()
    for word in word_list:
        word_set.add(word[:-1])		# remove trailing \n
    return word_set


def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    # Each element of tweets is the text of a tweet.
    tweets = kstream.map(lambda x: x[1])

    def word_key(word):
        if word in pwords:       # O(1) as set
            return ("positive",1)
        elif word in nwords:
            return ("negative",1)
        else:
            return ("neutral",1) 

    def update_via_add(new,old):
        return sum(new,old or 0)    

    # Can be chained, avoided for understanding.
    words = tweets.flatMap(lambda line: line.split(" "))  # words in tweet
    words_to_keys = words.map(word_key) # Assign positive/negative/neutral to words
    this_timeframe_pair_counts = words_to_keys.reduceByKey(lambda x,y: x+y) # Aggregate words by type
    # running count - adds prev time step's counts to current ones
    running_count = this_timeframe_pair_counts.updateStateByKey(update_via_add) 
    
    running_count.pprint(2)
   
    # Counts variable holds the word counts for all time steps
    counts = []
    this_timeframe_pair_counts.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))   

    ssc.start()                         # Start the computation
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)

    return counts


if __name__=="__main__":
    main()

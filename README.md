# Intro

The project analyzes a twitter stream and plots the sentiments present in the stream. Sentiments are simple counts of positive and negative words. For simplicity and ease of testing, a pre-downloaded dataset of 16 Million tweets is used to generate the tweet stream (twitter_to_kafka.py).

Kafka is used to read the tweets present in text file and provide them as a stream to the program. Program uses spark streaming to receive the stream of tweets, and analyzes them in batches of 10 seconds to find out the number of positive and negative words present in tweets in the batch.

The time it runs for can be set by changing the timeout duration. At 100, program analyzes data for 120 seconds.

### Run :

6. To stream tweets, read tweets from a file and push them to the twitterstream topic in Kafka. Do this by running:

$ python twitter_to_kafka.py


8. Run the Program:
 
Note: 6. must be runnnig for the program to receive the stream and consequently process it.

$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 twitterStream.py 

###Setup
1. unzip 16M.txt.zip

2. Start zookeeper service:
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties &

3. Start kafka service:
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties &

4. Create a topic named twitterstream in kafka:
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitterstream

5. Check what topics you have with:
$KAFKA_HOME/bin/kafka-topics.sh --list --zookeeper localhost:2181  

6. To stream tweets, read tweets from a file and push them to the twitterstream topic in Kafka. Do this by running:

$ python twitter_to_kafka.py

7. To check if the data is landing in Kafka:
$KAFKA_HOME/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic twitterstream --frombeginning

8. Run the Program:
 
Note: 6. must be runnnig for the program to receive the stream and consequently process it.

$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 twitterStream.py 

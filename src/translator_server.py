#!/usr/bin/env python

"""
Server for the gRPC example. See readme.
"""

from concurrent import futures
from collections import defaultdict
import time
import grpc
import translator_pb2


# Implement the service defined in the .proto file and its functions
class Translator(translator_pb2.TranslatorServicer):
    delay_s = 0.5
    
    # Dog to English dictionary
    dog_dict = defaultdict(lambda: "Unknown word -- is it really dogspeak?")
    dog_dict["wof"] = "o hai there"
    dog_dict["wuf"] = "naice to meet u"
    dog_dict["waf"] = "am hungry"
    dog_dict["wef"] = "am so fluffey"
    dog_dict["bork"] = "heck"
    dog_dict["kai"] = "u r doin me a frighten"
    
    # Single request, single response:
    # Translate one word to one expression
    def Translate(self, request, context):
        print("Client requested a direct translation")
        word = request.word.lower()
        translation = Translator.dog_dict[word]
        return translator_pb2.EnglishExpression(exp=translation)
            
    # Single request, stream response:
    # Get all dog words in the dictionary
    def GetAllWords(self, request, context):
        print("Client requested a dictionary summary")
        for w in Translator.dog_dict:
            time.sleep(Translator.delay_s)
            yield translator_pb2.DogWord(word=w)
            
    # Stream request, single response:
    # Of the received words, count how many are less than 4 characters long
    def CountShortWords(self, request_iterator, context):
        print("Client requested a word count")
        i = 0
        for dog_word in request_iterator:
            if len(dog_word.word) < 4:
                i += 1
        return translator_pb2.WordCount(total=i)
            
    # Stream request, stream response:
    # Translate words on the fly
    def TranslateOnTheFly(self, request_iterator, context):
        print("Client requested an on-the-fly translation")
        for dog_word in request_iterator:
            time.sleep(Translator.delay_s)
            word = dog_word.word.lower()
            translation = Translator.dog_dict[word]
            yield translator_pb2.EnglishExpression(exp=translation)
            
            
def run():
    # Run the server in a separate thread
    thread = futures.ThreadPoolExecutor(max_workers=1)
    server = grpc.server(thread)
    translator_pb2.add_TranslatorServicer_to_server(Translator(), server)
    # I don't get the port syntax
    server.add_insecure_port("[::]:50051")
    server.start()
    
    # Infinite loop, waiting for requests
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run()

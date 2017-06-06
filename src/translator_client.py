#!/usr/bin/env python

"""
Client for the gRPC example. See readme.
"""

import time
import grpc
import translator_pb2


def run():
    # Open channel to server
    channel = grpc.insecure_channel("localhost:50051")
    stub = translator_pb2.TranslatorStub(channel)
    
    # Example parameters
    dog_word = "wuf"
    word_list = ["bark", "bork", "woof", "waf", "wef"]
    
    # Client-server communication
    translate(stub, dog_word)               # Single request, single response
    get_all_words(stub)                     # Single request, stream response
    count_short_words(stub, word_list)      # Stream request, single response
    translate_on_the_fly(stub, word_list)   # Stream request, stream response
    
    
def translate(stub, dog_word):
    # Translate one word to one expression
    request = translator_pb2.DogWord(word=dog_word)
    response = stub.Translate(request)
    print("Single request, single response")
    print("Client sends \"" + dog_word + "\"")
    print("Server answers \"" + response.exp + "\"")
    print("\n")
    
    
def get_all_words(stub):
    # Get all dog words in the dictionary
    request = translator_pb2.Empty()
    responses = stub.GetAllWords(request)
    print("Single request, stream response")
    print("Client asks for all dog words in the dictionary")
    print("Server answers:")
    for response in responses:
        print(response.word)
    print("\n")
        
        
def count_short_words(stub, word_list):
    # Of the transmitted words, count how many less than 4 characters long
    requests = make_generator(word_list)
    response = stub.CountShortWords(requests)
    print("Stream request, single response")
    print("Client streams this list to server:")
    print(", ".join(word_list))
    print("How many of these words are less than 4 characters long?")
    print("Server answers: {} words".format(response.total))
    print("\n")
    
    
def translate_on_the_fly(stub, word_list):
    # Translate words on the fly
    requests = make_generator(word_list)
    responses = stub.TranslateOnTheFly(requests)
    print("Stream request, stream response")
    print("Client streams this list to server:")
    print(", ".join(word_list))
    for response in responses:
        print("Server answers \"" + response.exp + "\"")
    print("\n")
    
    
def make_generator(word_list):
    # Create a generator for streaming requests
    for i in range(len(word_list)):
        yield translator_pb2.DogWord(word=word_list[i])
    
    
if __name__ == '__main__':
    run()

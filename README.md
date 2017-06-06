# gRPC-dog-translator

A simple example to understand how gRPC/protobuf work. The code is based on
the Python tutorial for gRPC:

http://www.grpc.io/docs/tutorials/basic/python.html

Before use, follow the installation steps for grpcio and grpcio-tools at:

http://www.grpc.io/docs/quickstart/python.html

The project runs a server and a client as two separate processes and makes them
communicate via TCP. The four possible communications are used:
1. Single request, single response
2. Single request, stream response
3. Stream request, single response
4. Stream request, stream response

The build_protobuf.sh script translates the proto file into Python.

The example program is a Dog/English translator, very useful to understand
what your doggo is telling you without having to carry a dictionary around. 
The dictionary is on the server and the client can make four different requests
that correspond to the four communication methods:
1. Translate one Dog word into English
2. Get a stream of all Dog words that are in the dictionary
3. Stream a list of Dog words and get how many are less than 4 characters long
4. Stream Dog words and get a stream of translations into English

A response latency is simulated on the server side. To run the example, just
run translator_server.py in a terminal and translator_client.py in another.

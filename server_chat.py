
import grpc
import snitch_pb2_grpc as pb2_grpc
import snitch_pb2 as pb2

import socketio

import linsimpy

class SnitchClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 8080

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.SnitchStub(self.channel)

    def SnitchUser(self, message):
        message = pb2.Message(message=message)
        print(f'{message}')
        return self.stub.SnitchUser(message)

grpc = SnitchClient()

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)

tse = linsimpy.TupleSpaceEnvironment()
sids = tse.out(("SIDS", tuple([])))
watched_words = tse.out(("WATCHED_WORDS", tuple([])))

client_count = 0

@sio.event
async def connect(sid, env, payload):
    global client_count
    client_count += 1
    username = payload["username"]
    print('user ' + username + ' (' + sid + ') ' + 'connected\nclient_count ' + str(client_count))
    await sio.emit("client_count", username + ' connected')
    save_username_for_sid(sid, username)

@sio.event
async def disconnect(sid):
    global client_count
    client_count -= 1
    username = get_username_from_sid(sid)
    print('user ' + username + ' (' + sid + ') ' + ' disconnected\nclient_count ' + str(client_count))
    await sio.emit("client_count",  username + ' disconnected')
    remove_sid(sid)

@sio.event
async def broadcast_chat_message(sid, payload):
    print(payload)
    if is_there_watched_words_on(payload):
        await print(grpc.SnitchUser(message = payload))
    await sio.emit('broadcast_chat_message', payload)

@sio.event
async def register_watched_word(sid, word):
    add_watched_word(word)
    print('new registered watched word: ' + word)

def save_username_for_sid(sid, username):
    tse.out(("SID", sid, tuple(username)))

    temp = list(tse.inp(("SIDS", object))[1])
    temp.append(sid)
    tse.out(("SIDS", tuple(temp)))

def get_username_from_sid(sid):
    username = ''.join(tse.inp(("SID", sid, object))[2])
    tse.out(("SID", sid, tuple(username)))
    return username

def remove_sid(sid):
    sid = tse.inp(("SID", sid, object))
    temp = list(tse.inp(("SIDS", object))[1])
    temp.remove(sid[1])
    tse.out(("SIDS", tuple(temp)))

def add_watched_word(word):
    temp = list(tse.inp(("WATCHED_WORDS", object))[1])
    temp.append(word)
    tse.out(("WATCHED_WORDS", tuple(temp)))

def get_watched_words():
    temp = list(tse.inp(("WATCHED_WORDS", object))[1])
    tse.out(("WATCHED_WORDS", tuple(temp)))
    print(temp)
    words = []
    for word in temp:
        words.append(''.join(word))
    return words

def is_there_watched_words_on(message):
    words = get_watched_words()
    shouldSnitch = False
    for word in words:
        if word in message:
            shouldSnitch = True
    return shouldSnitch
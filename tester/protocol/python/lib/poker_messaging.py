import time

LENGTH_BYTES = 4

def receive_message(f, message_class):
    # get a message of the specified type from the input stream, return true
    # on success, false on failure
    length = f.read(LENGTH_BYTES)
    if len(length) < LENGTH_BYTES:
        raise Exception("Unexpected end of stream while reading length")
        
    bytes = 0
    for c in length:
        bytes <<= 8
        bytes |= ord(c)
    
    message_str = f.read(bytes)
    if len(message_str) < bytes:
        raise Exception("Unexpected end of stream while reading message")
    
    message = message_class()
    message.ParseFromString(message_str)
    return message
        
def send_message(f, message):
    # write a message to the output stream
    s = message.SerializeToString()
    bytes = len(s)
    for i in reversed(range(LENGTH_BYTES)):
        byte = (bytes >> 8*i) & 0xFF
        f.write(chr(byte))
    f.write(s)
    f.flush()
    
def send_terminator(f):
    # terminate a stream
    for i in range(LENGTH_BYTES):
      f.write(chr(0))
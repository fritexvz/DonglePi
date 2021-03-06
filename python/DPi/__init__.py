import donglepi_pb2
import threading
import serial
import logging
from google.protobuf.message import DecodeError
from google.protobuf.internal.decoder import _DecodeVarint32 as DecodeVarint32 
from serial.tools import list_ports

logging.basicConfig(level=logging.DEBUG)

def hexdump(s):
  return " ".join("{:02x}".format(ord(c)) for c in s)

def delimitedMessage(message):
  serializedMessage = message.SerializeToString()
  delimiter = donglepi_pb2.Transport()
  delimiter.message_length = len(serializedMessage)
  return delimiter.SerializeToString() + serializedMessage

pending_request = donglepi_pb2.DonglePiRequest()
request_lock = threading.Lock()

last_response = donglepi_pb2.DonglePiResponse()
response_lock = threading.Lock()


def find_donglepi():
  try:
     # TODO(gbin): fix me it broke, dunno why
     return '/dev/ttyACM0'
     # return next(list_ports.grep("DonglePI"))[0]
  except StopIteration:
     return None

def main_loop(cb):
  global pending_request
  global last_response
  port_name = find_donglepi()
  if not port_name:
    logging.error("Could not find a plugged DonglePi.")
    return
  port = serial.Serial(port=port_name, baudrate=115200, timeout=0.5) #0.0002)
  logging.debug("DonglePi found on [%s]" % port_name)
  rcv_buffer = ""
  pending_request.message_nb = 314
  while True:
    with request_lock:
      request_number = pending_request.message_nb
      msg = delimitedMessage(pending_request)
      pending_request = donglepi_pb2.DonglePiRequest()
      pending_request.message_nb = (request_number + 1) % 65536

    logging.debug("Write message #%d" % request_number)
    port.write(msg)
    print(hexdump(msg))
    logging.debug("Write message #%d OK" % request_number)

    
    delimiter = donglepi_pb2.Transport()
    while True:
      rcv_buffer += port.read(1024)
      print(hexdump(rcv_buffer))
      try:
        (msg_length, offset) = DecodeVarint32(rcv_buffer, 0)
        logging.debug("expected message len = %s" % msg_length)
      except DecodeError:
        logging.debug("not enough for the init len")
        continue
      if len(rcv_buffer) - offset == msg_length:
        break

    response = donglepi_pb2.DonglePiResponse()
    response.ParseFromString(
        rcv_buffer[offset:offset + msg_length])
    logging.debug("Response parsed #%d" % response.message_nb)
    rcv_buffer = rcv_buffer[msg_length + offset:]
    if response.message_nb != request_number:
      logging.warn("Donglepi desynchronized req nb = %d but resp nb = %d" %
                   (response.message_nb, pending_request.message_nb))

    # assert response.message_nb == request_number
    with response_lock:
      last_response = response
    cb(response)


#req = donglepi_pb2.DonglePiRequest()
#req.message_nb = 1
#req.data.gpio.mask = 0xDEADBEEF
#req.data.gpio.values = 0x13333331
#print(hexdump(delimitedMessage(req)))

#req2 = donglepi_pb2.DonglePiRequest()
#req2.message_nb = 9
#print(hexdump(delimitedMessage(req2)))



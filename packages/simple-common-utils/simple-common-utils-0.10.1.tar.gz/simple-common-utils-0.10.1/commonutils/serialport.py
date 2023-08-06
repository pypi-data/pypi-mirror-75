from dataxmissionprotocol import Parser
from serial import serial_for_url
from serial.serialutil import SerialException, portNotOpenError

class SerialPort:
   __debugRead = False
   __debugWrite = False
   __port = None
   __errorProcessor = lambda e: e
   
   @staticmethod
   def close():
      if SerialPort.__port and SerialPort.__port.isOpen():
         SerialPort.__port.close()
         SerialPort.__port = None
   
   @staticmethod
   def getPacketType():
      return SerialPort.__packetType
   
   @staticmethod
   def open(path, **kw):
      SerialPort.close()
      
      try:
         SerialPort.__port = serial_for_url(path, **kw)
         
         return True
      
      except SerialException as e:
         SerialPort.__errorProcessor(e)
   
   @staticmethod
   def read(size):
      try:
         if not SerialPort.__port:
            raise portNotOpenError
         
         size = SerialPort.__packetType.getFormat().getTotalPacketSize(size)
         
         if SerialPort.__debugRead:
            print(f"reading {size} bytes...")
         
         buf = SerialPort.__port.read(size)
         
         if SerialPort.__debugRead:
            print("bytes read:", list(buf))
         
         return SerialPort.__parser.parse(buf)
      
      except SerialException as e:
         SerialPort.__errorProcessor(e)
   
   @staticmethod
   def setDebug(debugRead = False, debugWrite = False):
      SerialPort.__debugRead = debugRead
      SerialPort.__debugWrite = debugWrite
   
   @staticmethod
   def setErrorProcessor(processor):
      SerialPort.__errorProcessor = processor
   
   @staticmethod
   def setPacketType(packetType):
      SerialPort.__packetType = packetType
      SerialPort.__parser = Parser(packetType.getFormat())
   
   @staticmethod
   def write(**kw):
      throw = kw.pop("throw", False)
      
      return SerialPort.writePacket(SerialPort.__packetType(**kw), throw)
   
   @staticmethod
   def writePacket(packet, throw = False):
      if SerialPort.__debugWrite:
         print(list(packet.rawBuffer))
         return True
      
      try:
         if not SerialPort.__port:
            raise portNotOpenError
         
         SerialPort.__port.write(packet.rawBuffer)
         
         return True
      
      except SerialException as e:
         if throw:
            raise
         
         SerialPort.__errorProcessor(e)

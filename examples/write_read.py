import pickle
from io import BytesIO
from pprint import pprint

from pb2nano.protocol import *
from pb2nano.reader import *
from pb2nano.writer import *


# A totally random example on how to use pb2nano


# Specify the protocol like this:

Object = Pb2Message("Object")\
         .field("required", "uint64", "id", 1)\
         .field("optional", "uint32", "some_val", 2)\
         .field("required", "bool", "is_important", 3)\
         .field("optional", "string", "name", 4)\
         .field("optional", "bytes", "object", 5,
                filter = (pickle.loads, pickle.dumps))


Type = Pb2Enum("Type")\
       .define("DO_THAT", 1)\
       .define("DO_THIS", 2)


Command = Pb2Message("Command")\
          .field("required", "Type", "type", 1)\
          .field("repeated", "Object", "arg", 2)


TestProtocol = Pb2Protocol()\
               .enum(Type)\
               .message(Object)\
               .message(Command)


# Some test data:

class AnyPickableClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def xor(self):
        return self.a ^ self.b

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b


my_python_object = AnyPickableClass(42, 1337)

obj = {
    "type": "DO_THAT",
    "arg": [{        # <-- arg is repeated, therefore it must be an iterable
        "id": 12345,
        "is_important": False,
        "name": "awesome_name",
        "object": my_python_object
    },
    {
        "id": 54321,
        "is_important": True,
    }]
}


# Let's serialize that:

buf = BytesIO()
w = Pb2Writer(Pb2WireWriter(buf), TestProtocol, Command)
w.write(obj)



print("Serialized data:")
print(buf.getvalue())
print()


# And now unserialize it again

buf.seek(0)
r = Pb2Reader(Pb2WireReader(buf), TestProtocol, Command)
obj2 = r.read()


# Let's see

assert obj == obj2

print("Read object:")
pprint(obj2)
print()
print("xor:", obj2["arg"][0]["object"].xor())


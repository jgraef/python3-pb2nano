# python3-pb2nano

python3-pb2nano is a **minimal** [protobuf2](https://developers.google.com/protocol-buffers/) reader and writer.

Currently it doesn't have a protocol parser, so you have to specify your protocols with python objects. Furthermore it
only supports unsigned varints, string, bytes and top-level enums and messages.

It was created for [python3-ipfs-api](https://github.com/ipfs/py-ipfs) to parse very simple protobuf2 messages and is
meant as a replacement until Google adds proper Python3 support for Protocol Buffers.

Sorry, but no documentation currently available.


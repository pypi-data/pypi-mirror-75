# python-simpleprotocol
A small socket wrapper

Used for sending code, subcode, parameters.
Code: Integer
Subcode: Integer
Params: Array of strings


Only has basic use, as shown in this example:


Server:

```

import simpleprotocol

server = simpleprotocol.SimpleServer(port=8080)

while True:
    handler = server.accept()
    handler.send(0)
    print(handler.get())
    handler.send(1)
    print(handler.get())


```

Client:

```

import simpleprotocol

socket = simpleprotocol.SimpleProtocol()

if socket.get().code:
    socket.send(1, 0, ["That sounds good!"])
else:
    socket.send(1, 1, ["Oh dear, that's not right..."])

```

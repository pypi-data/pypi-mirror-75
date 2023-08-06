# simple-message-channels

[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/simple-message-channels/status.svg)](https://drone.autonomic.zone/hyperpy/simple-message-channels)

## Sans I/O wire protocol for Hypercore

## Install

```sh
$ pip install simple-message-channels
```

## Example

```python
from simple_message_channels import SimpleMessageChannel

smc_a = SimpleMessageChannel()
smc_b = SimpleMessageChannel()

payload = smc_b.send(0, 1, b"foo")
print(f"sent: {payload}")

for idx in range(0, len(payload)):
    smc_a.recv(payload[idx : idx + 1])

for msg in smc_a.messages:
    print(f"received: {msg}")
```

Output:

```sh
sent: b'\x04\x01foo'
received: (0, 1, b'foo')
```

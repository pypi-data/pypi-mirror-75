# pandas-zmq

Communicate [Pandas](https://pypi.org/project/pandas/) DataFrame over [ZeroMQ](https://pypi.org/project/pyzmq/) connection

## API

```
send_dataframe(socket, dataframe, secret='', alg='sha256', flags=0)
```

```
recv_dataframe(socket, secret='', alg='sha256', flags=0)
```

### Server

```
import pandas_zmq

# ...
pandas_zmq.send_dataframe(socket, df)
```


### Client

```
import pandas_zmq

# ...
df = pandas_zmq.recv_dataframe(socket)
```


## Security

WARNING: There are reported security issues with pickle, which is the backend serialization for this feature. A signature using a shared secret and a configurable hash algorithm has been added to mitigate this risk which will attempt to verify the data has not been altered. [See pickle documentation](https://docs.python.org/3/library/pickle.html).

# oh_my_env

### example
***
```python
from oh_my_env import Env

env = Env('hydra')
env.read_envfile()
# env.read_envfile('/tmp/.env')
env.bool('debug', default=True) # HYDRA_DEBUG
env.int('port', default=8080) # HYDRA_PORT
env.secret('password', default="3VpavryXEro5CUWph41NGA==") # HYDRA_PASSWORD aes encryption, oh_my_env/utils.py里有encrypt方法
```


### backend
***
oh_my_env默认是从环境变量里读取配置，也支持其他形式的存储介质作为backend，只需要实现`__call__`方法，`DummyBackend`可以作为参考。


### test
***
```
pip install tox pytest
make test
```

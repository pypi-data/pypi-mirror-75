from proxypool_framework.contrib.proxy_client import ProxyClient
from proxypool_framework.proxy_pool_config import REDIS_URL

ProxyClient(redis_url=REDIS_URL).statistic_rate_of_sucess()
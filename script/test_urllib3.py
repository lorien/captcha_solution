from urllib3 import PoolManager


def main(**kwargs):
    pool = PoolManager()
    res = pool.request(
        'POST', 'https://google.com/',
        fields={'foo': 'bar'},
        body=None,
    )
    print(res.status, res.data[:100])

import asyncio
import concurrent.futures
import requests
import json
import socket
import pycurl
from urllib.parse import urlparse
from haversine import haversine
from io import BytesIO


def _ipToGeoloc(ipaddr):
    res = requests.get("http://api.ipstack.com/"\
                        + ipaddr\
                        + "?access_key=1e7beb7517ccc392c760dd63e3fa0917")

    if res.status_code == 200:
        result = json.loads(res.text)
        return result['latitude'], result['longitude']
    else:
        raise Exception(res.status_code)


def _getMyGeoloc():
    return _ipToGeoloc('check')


def _urlToIp(url):
    o = urlparse(url)
    hostname = o.hostname
    port = o.port or (443 if o.scheme == 'https' else 80)
    ip_addr = socket.getaddrinfo(hostname, port)[0][4][0]
    return ip_addr


def getMirrorUrls(country='mirrors'):
    res = requests.get('http://mirrors.ubuntu.com/' + country + '.txt')

    if res.status_code == 200:
        return res.text.split("\n")
    else:
        raise Exception(res.status_code)
        

def getMirrorsWithLocation(sorted=True):
    mirrors = []
    
    for url in getMirrorUrls():
        try:
            ip_addr = _urlToIp(url)
            geoloc = _ipToGeoloc(ip_addr)
            mirrors.append((url, geoloc))
        except Exception as e:
            # current mirror is unreachable
            pass

    if sorted:
        myloc = _getMyGeoloc()
        mirrors.sort(key=lambda x: haversine(x[1], myloc))

    return mirrors


def getCandidates():
    mirrors = getMirrorsWithLocation()
    return [url for url, loc in mirrors]


def __getServerStat(url):
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, BytesIO())
    c.setopt(c.TIMEOUT, 1)
    try:
        c.perform()
        stat = {
            "time_namelookup": c.getinfo(pycurl.NAMELOOKUP_TIME),
            "time_connect": c.getinfo(pycurl.CONNECT_TIME),
            "time_appconnect": c.getinfo(pycurl.APPCONNECT_TIME),
            "time_pretransfer": c.getinfo(pycurl.PRETRANSFER_TIME),
            "time_redirect": c.getinfo(pycurl.REDIRECT_TIME),
            "time_starttransfer": c.getinfo(pycurl.STARTTRANSFER_TIME),
            "time_total": c.getinfo(pycurl.TOTAL_TIME),
            "speed_download": c.getinfo(pycurl.SPEED_DOWNLOAD),
            "speed_upload": c.getinfo(pycurl.SPEED_UPLOAD),
            "local_ip": c.getinfo(pycurl.LOCAL_IP),
            "local_port": c.getinfo(pycurl.LOCAL_PORT)
        }
    except Exception as e:
        stat = {
            "time_total": 999999
        }
    c.close()

    return stat


async def __getAvgLatency(pool, url, trial=3):
    loop = asyncio.get_running_loop()
    times = await asyncio.gather(*[loop.run_in_executor(pool, lambda : __getServerStat(url)) for _ in range(trial)])
    return url, sum(map(lambda x: x['time_total'], times)) * 1000 // trial


async def _testLatencies(urls):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        wait_target = {__getAvgLatency(pool, url) for url in urls}
        done, pending = await asyncio.wait(wait_target) #, return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()

        responseTimes = list(map(lambda x: x.result(), done))
        responseTimes.sort(key=lambda x: x[1])
    return responseTimes


def testLatencies(urls):
    return asyncio.run(_testLatencies(urls))


def findOptimalMirror(urls):
    latencies = testLatencies(urls)
    return latencies[0][0]
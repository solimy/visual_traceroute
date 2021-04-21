import multiprocessing
import subprocess
import requests
import gmplot
import sys
import os
import re


def traceroute(host):
    p = subprocess.run(
        ['traceroute', host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return p.stdout.strip().decode('utf-8')

def get_ip_latlong(ip):
    result = requests.get(f'http://api.ipstack.com/{ip}?access_key={os.environ["IPSTACK_KEY"]}')
    result = result.json()
    lat = result['latitude']
    long = result['longitude']
    latlong = (lat, long) if lat and long else None
    return latlong


def plot(ip_list, latlong_list):
    gmap = gmplot.GoogleMapPlotter(*(latlong_list[0]), 14, apikey=os.environ['GMPLOT_KEY'])

    gmap.plot(*zip(*latlong_list),
        color='cornflowerblue',
        edge_width=5,
        precision=14,
    )
    gmap.scatter(*zip(*latlong_list[1:-1]), precision=14, color='black')
    gmap.scatter(*zip(*latlong_list[:1]), precision=14, color='red')
    gmap.scatter(*zip(*latlong_list[-1:]), precision=14, color='red')
    for (i, ip), (lat, long) in zip(ip_list, latlong_list):
        gmap.text(lat, long, f'{i}: {ip}', precision=14)

    gmap.draw('traceroute.html')

if __name__ == '__main__':
    if sys.stdin.isatty():
        if len(sys.argv) != 2:
            print('''
                Usage:

                1) $>python traceroute.py host

                2) $>traceroute host | python traceroute.py

                3) $>traceroute host > route.txt
                   $>python traceroute.py < route.txt
            ''')
            exit(-1)
        host = sys.argv[1]
        traceroute_output = traceroute(host)
    else:
        traceroute_output = sys.stdin.read().strip()
    ip_list = [
        result.groups()[0]
        for line in traceroute_output.split('\n')
        if (result := re.search(r'\((\d+\.\d+\.\d+\.\d+)\)', line))
    ]
    count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=count)
    latlong_list = pool.map(get_ip_latlong, ip_list)
    ip_list, latlong_list = zip(*[(ip, latlong) for ip, latlong in zip(enumerate(ip_list), latlong_list) if latlong])
    plot(ip_list, latlong_list)

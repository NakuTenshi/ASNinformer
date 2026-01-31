#!/usr/bin/env python3

import os 
import re
import sys
import json
import requests
from bs4 import BeautifulSoup
import argparse
from rich import print as pprint



parser = argparse.ArgumentParser()
parser.add_argument("-p", "--proxy", help="proxy ip for using")
parser.add_argument('-v', action="store_true", help="prints result")
parser.add_argument('-o', help="file name for saving results", default="./asn-result.txt")

args, _ = parser.parse_known_args()
proxy_ip = args.proxy
verbose = args.v
outputFileName = args.o

proxies = {
    "http": proxy_ip,
    "https": proxy_ip
}

ASNs = {}

ip_regex = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)


def cleanLine():
    sys.stdout.write("\033[F")  # move cursor up one line
    sys.stdout.write("\033[K")  # clear line

def checkASN(ip):
    if ip_regex.match(ip):
        cleanLine()
        print(ip)
        base_url = f"http://ip2asn.ipinfo.app/lookup/{ip}"

        try:
            response = requests.get(base_url, verify=False)

        except requests.exceptions.ConnectionError:
            checkASN(ip)
        else:
            if response.status_code == 200:
                data = response.json()

                if data["announcedBy"]: # has data
                  company_name = data["announcedBy"][0]["name"]
                  asn_name = f'AS{data["announcedBy"][0]["asn"]}'
                  cidr = data["announcedBy"][0]["subnet"]

                  if not asn_name in ASNs.keys():
                      ASNs[asn_name] = {
                          "ASN": asn_name,
                          "ASN url": f"https://bgp.he.net/{asn_name}",
                          "CIDR": cidr,
                          "company's name": company_name,
                          "IPs": [ip]
                      }
                  else:
                      ASNs[asn_name]["IPs"].append(ip)

            else:
                print(response.status_code)
                print(response.content)
                print('[ERROR] the connection is not ok')
                exit()

if __name__ == "__main__":
  # take ips
  try:
      
    if not sys.stdin.isatty():
        for line in sys.stdin:
            ip = line.strip()
            checkASN(ip)
    elif len(sys.argv) > 1:
        lines = sys.argv[1:]
        for line in lines:
            ip = line.strip()
            checkASN(ip)
    else:
        file_name = __file__.split('/')[-1]
        print("no input provided")
        print("Usage:")

        print(f'    echo 1.1.1.1 | {file_name}')
        print(f'    cat ips.txt | {file_name}')
        print(f'    {file_name} 1.1.1.1')
        print(f'    {file_name} 1.1.1.1 8.8.8.8')

        exit()

    cleanLine()
    if verbose:
        pprint(ASNs)
    else:
        print("Done.")
        print(f"the result saved at {outputFileName}")

    with open(outputFileName, "w") as f:
        json.dump(ASNs, f, indent=2)
    
  except KeyboardInterrupt:
    print("\nBye :)")
    exit()




#!/usr/bin/env python3

import re
import sys
import json
import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--proxy", help="proxy ip for using")
parser.add_argument('-o', help="file name for saving results", default="./asn-result.json")

args, _ = parser.parse_known_args()
proxy_ip = args.proxy
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

def checkASN(line_input):
    global ASNs

    if ip_regex.match(line_input): # it was an ip
        base_url = f"http://ip2asn.ipinfo.app/lookup/{line_input}"
        try:
            response = requests.get(base_url, verify=False)

        except requests.exceptions.ConnectionError:
            checkASN(line_input)
        else:
            if response.status_code == 200:
                data = response.json()

                if data["announcedBy"]: # has data
                  company_name = data["announcedBy"][0]["name"]
                  asn_name = f'AS{data["announcedBy"][0]["asn"]}'
                  bgp_url = f"https://bgp.he.net/{asn_name}"                  
                  ip_range = data["announcedBy"][0]["subnet"]

                  if not asn_name in ASNs.keys():
                      ASNs[asn_name] = {
                          "company's name": company_name,
                          "ASN": asn_name,
                          "ASN url": bgp_url,
                          "Provided IP Ranges": [ip_range],
                          "Provided IP": [line_input]
                      }
                  else:
                    ASNs[asn_name]["Provided IP"].append(line_input)
                    if ip_range not in ASNs[asn_name]["Provided IP Ranges"]: 
                        ASNs[asn_name]["Provided IP Ranges"].append(ip_range)

    elif line_input.lower().startswith("as"): # it's ASN
        if line_input not in ASNs.keys():
            asn_details_url = f"https://asn.ipinfo.app/api/json/details/{line_input}"
            asn_ranges_url = f"https://asn.ipinfo.app/api/json/list/{line_input}"

            asn_details_response = requests.get(asn_details_url)
            asn_ranges_reponse = requests.get(asn_ranges_url)

            if asn_details_response.status_code == 200 and asn_details_response.status_code == 200:
                details_data = asn_details_response.json()
                ranges_data = asn_ranges_reponse.json()

                company_name = details_data["name"]
                asn_name = f'AS{details_data["asn"]}'
                bgp_url = f"https://bgp.he.net/{asn_name}"                  
                ip_ranges = ranges_data["list"]

                ASNs[asn_name] = {
                    "Company's Name": company_name,
                    "ASN": asn_name,
                    "ASN Url": bgp_url,
                    "IP Ranges": ip_ranges,
                }


if __name__ == "__main__":
  # take input
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
        print(f'    {file_name} -h')

        print(f'Get ip\'s information:')
        print(f'    echo 1.1.1.1 | {file_name}')
        print(f'    cat ips.txt | {file_name}')
        print(f'    {file_name} 1.1.1.1')
        print(f'    {file_name} 1.1.1.1 8.8.8.8')
        
        print(f'Get ASN\'s information: ')
        print(f'    echo AS13335 | {file_name}')
        print(f'    cat ASNs.txt | {file_name}')
        print(f'    {file_name} AS13335')
        print(f'    {file_name} AS13335 AS15169')
        exit()

    print(json.dumps(ASNs))
    with open(outputFileName, "w") as f:
        json.dump(ASNs, f)
        
  except KeyboardInterrupt:
    print("\nBye :)")
    exit()




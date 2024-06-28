#!/usr/bin/env python3

# Python version
# Bruf0x script 1.0!
# This script is based on crtndstry by https://www.youtube.com/@NahamSec

import requests
import subprocess
import argparse
import json

def print_ascii_art():
    ascii_art = """
           _         _                  __ 
          | |       | |                / _|
 ___ _   _| |__   __| | ___  _ __ ___ | |_ 
/ __| | | | '_ \ / _` |/ _ \| '_ ` _ \|  _|
\__ \ |_| | |_) | (_| | (_) | | | | | | |  
|___/\__,_|_.__/ \__,_|\___/|_| |_| |_|_|  by: Bruf0x                                           
    """
    print(ascii_art)

# Function to add custom patterns
def add_patterns(custom_patterns_string):
    global patterns
    custom_patterns = custom_patterns_string.split(',')
    patterns.extend(custom_patterns)

def query_crtsh(domain):
    print("[+] Searching in crt.sh...")
    crtsh_domains = set()
    for pattern in patterns:
        url = f"https://crt.sh/?q={pattern}.{domain}&output=json"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                for entry in data:
                    crtsh_domains.update(entry["name_value"].replace("*.", "").replace("www.", "").split())
            except json.JSONDecodeError:
                print(f"[-] Invalid JSON response from crt.sh for pattern {pattern}")
        else:
            print(f"[-] Failed to fetch data from crt.sh for pattern {pattern}")
    return crtsh_domains

def query_certspotter(domain):
    print("[+] Searching in certspotter...")
    certspotter_domains = set()
    url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names&expand=issuer&expand=issuer.caa_domains"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            for entry in data:
                certspotter_domains.update(d.replace("*.", "").replace("www.", "") for d in entry["dns_names"])
        except json.JSONDecodeError:
            print("[-] Invalid JSON response from certspotter")
    else:
        print("[-] Failed to fetch data from certspotter")
    return certspotter_domains

def combine_and_probe(domain, crtsh_domains, certspotter_domains):
    all_domains = crtsh_domains.union(certspotter_domains)
    with open(f"./{domain}-subdomains.txt", "w") as f:
        for d in sorted(all_domains):
            f.write(d.lower() + "\n")

    # Run httprobe to find live domains
    print("[+] Searching live domains in httprobe...")
    with open(f"./{domain}-subdomains.txt", "r") as f:
        result = subprocess.run(["httprobe"], input=f.read().encode(), capture_output=True)
        live_domains = result.stdout.decode().splitlines()

    with open(f"./{domain}-live-subdomains.txt", "w") as f:
        for d in sorted(live_domains):
            f.write(d + "\n")

    # Count the number of unique domains and subdomains
    print("[+] Number of subdomains found:", len(live_domains))

def gather_domains(domain):
    crtsh_domains = query_crtsh(domain)
    certspotter_domains = query_certspotter(domain)
    combine_and_probe(domain, crtsh_domains, certspotter_domains)

if __name__ == "__main__":
    # Default patterns
    patterns = ["api", "corp", "dev", "uat", "test", "stag", "sandbox", "prod", "hom"]

    # Help
    parser = argparse.ArgumentParser(description='subdomf script 1.0!')
    parser.add_argument('-p', '--patterns', help='Custom patterns separated by comma')
    parser.add_argument('domain', help='Domain to search for subdomains')
    args = parser.parse_args()

    # ASCII Art
    print_ascii_art()

    if args.patterns:
        add_patterns(args.patterns)

    if not args.domain:
        print("Usage: subdomf.py [-p pattern1,pattern2,...] domain")
        exit(1)

    gather_domains(args.domain)

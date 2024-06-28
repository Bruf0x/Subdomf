#!/usr/bin/env bash

# Bruf0x script 1.0!
# This script is based on crtndstry by https://www.youtube.com/@NahamSec

echo '           _         _                  __ '
echo '          | |       | |                / _|'
echo ' ___ _   _| |__   __| | ___  _ __ ___ | |_ '
echo '/ __| | | | '"'"'_ \ / _` |/ _ \| '"'"'_ ` _ \|  _|'
echo '\__ \ |_| | |_) | (_| | (_) | | | | | | |  '
echo '|___/\__,_|_.__/ \__,_|\___/|_| |_| |_|_|  by: Bruf0x'
echo '                                           '
echo '                                           '

# Default patterns
patterns=("api" "corp" "dev" "uat" "test" "stag" "sandbox" "prod" "internal" "hom" "prd" "intranet" "mail")

# Function to add custom patterns
add_patterns() {
    local custom_patterns_string=$1
    IFS=',' read -r -a custom_patterns <<< "$custom_patterns_string"
    patterns+=("${custom_patterns[@]}")
}

gather_domains(){
    local domain=$1

    # Get domains from crt.sh based on patterns
    for pattern in "${patterns[@]}"; do
        response=$(curl -s "https://crt.sh/?q=$pattern.$domain&output=json")
        if echo "$response" | jq -e . >/dev/null 2>&1; then
            echo "$response" | jq -r '.[].name_value' | sed 's/\*\.//g' | sed 's/^www\.//' | sort -u >> ./$domain-crtsh.txt
        else
            echo "[-] Invalid JSON response from crt.sh for pattern $pattern"
        fi
    done

    # Get domains from certspotter
    response=$(curl -s "https://api.certspotter.com/v1/issuances?domain=$domain&include_subdomains=true&expand=dns_names&expand=issuer&expand=issuer.caa_domains")
    if echo "$response" | jq -e . >/dev/null 2>&1; then
        echo "$response" | jq '.[].dns_names[]' | sed 's/\"//g' | sed 's/\*\.//g' | sed 's/^www\.//' | sort -u >> ./$domain-certspotter.txt
    else
        echo "[-] Invalid JSON response from certspotter"
        echo "$response"
    fi

    # Combine, sort, and remove duplicates
    sort -u ./$domain-crtsh.txt ./$domain-certspotter.txt > ./$domain-temp.txt
    
    # Final sorting, removing duplicates, and saving
    sort -u ./$domain-temp.txt | tr '[:upper:]' '[:lower:]' | sort -u > ./$domain-subdomains.txt
    rm ./$domain-temp.txt ./$domain-crtsh.txt ./$domain-certspotter.txt

    # Count the number of unique domains and subdomains
    cat "./$domain-subdomains.txt"
    echo "[+] Number of subdomains found: $(wc -l < ./$domain-subdomains.txt)"
}

# Parse arguments and add custom patterns
while [ $# -gt 0 ]; do
    case $1 in
        -p)
            shift
            add_patterns "$1"
            ;;
        *)
            domain="$1"
            ;;
    esac
    shift
done

# Ensure the domain argument is provided
if [ -z "$domain" ]; then
    echo "Usage: $0 [-p pattern1,pattern2,...] domain"
    exit 1
fi

# Call the function with the domain
gather_domains "$domain"

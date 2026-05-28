# ASNinformer

<div align="center">
  <img src="src/logo.png" alt="ASNinformer Logo"  height="90"/>
  <p>ASNinformer -- a lightweight tool that takes IPs as input, looks up their ASN information, and groups results by ASN in a JSON file.</p>
</div>

---

**ASNinformer** is a simple Python script that takes IP addresses as
input, queries their ASN (Autonomous System Number) information via
`ip2asn.ipinfo.app`, groups IPs by ASN, and saves the results as a JSON
file.

It is designed to work with **stdin (piping)** or direct command-line
arguments.

------------------------------------------------------------------------

## Features

-   Accepts IPs from:
    -   Standard input (`stdin`)
    -   Command-line arguments\
-   Automatically groups IPs by ASN\
-   Saves results in JSON format\
-   Optional verbose output\
-   Optional proxy support\
-   Uses a simple regex-based IPv4 validator



<br>

## Installation

Clone the repository:

``` bash
git clone https://github.com/NakuTenshi/ASNinformer.git
cd ASNinformer
```

Make the script executable:

``` bash
chmod +x ASNinformer.py
```

then install the script:
```bash
sudo ./install
```


------------------------------------------------------------------------

## Usage

### 1️⃣ Using stdin (recommended)

``` bash
echo 1.1.1.1 | ASNinformer
```

``` bash
cat ips.txt | ASNinformer
```

Example `ips.txt`:

    1.1.1.1
    8.8.8.8
    9.9.9.9

------------------------------------------------------------------------

### 2️⃣ Passing IPs as arguments

``` bash
ASNinformer 1.1.1.1
```

``` bash
ASNinformer 1.1.1.1 8.8.8.8
```

------------------------------------------------------------------------

## Options

| Flag | Description |
|------|-------------|
| `-p, --proxy` | Use an HTTP/HTTPS proxy |
| `-v` | Print detailed ASN results to the terminal |
| `-o` | Output file name (default: `./asn-result.txt`) |

### Examples

#### Save results to custom file

``` bash
echo 8.8.8.8 | ASNinformer -o results.json
```

#### Use a proxy

``` bash
echo 8.8.8.8 | ASNinformer -p http://127.0.0.1:8080
```

#### Print results in terminal (verbose mode)

``` bash
echo 1.1.1.1 | ASNinformer -v
```

------------------------------------------------------------------------

## Output Format

The script outputs a JSON file structured like this:

``` json
{
  "AS15169": {
    "ASN": "AS15169",
    "ASN url": "https://bgp.he.net/AS15169",
    "CIDR": "8.8.8.0/24",
    "company's name": "Google LLC",
    "IPs": [
      "8.8.8.8"
    ]
  }
}
```

Each ASN entry contains: - ASN number\
- Link to BGP info (`bgp.he.net`)\
- Announced CIDR\
- Company name\
- List of IPs belonging to that ASN (that given as input to code)


---
created by: **NakuTenshi**

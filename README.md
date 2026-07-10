# ASNinformer

<div align="center">
  <img src="src/logo.png" alt="ASNinformer Logo"  height="90"/>
  <p>ASNinformer -- a lightweight tool that takes IPs or ASNs as input, looks up their ASN information, and groups results in a JSON file.</p>
</div>

---

**ASNinformer** is a simple Python script that takes IP addresses or ASNs as input, queries their ASN (Autonomous System Number) information via `ip2asn.ipinfo.app` and `asn.ipinfo.app`, groups IPs by ASN, and saves the results as a JSON file.

It is designed to work with **stdin (piping)** or direct command-line arguments.

------------------------------------------------------------------------

## Features

-   Accepts input from:
    -   Standard input (`stdin`)
    -   Command-line arguments
-   **IP to ASN lookup** - Queries IP to ASN information via `ip2asn.ipinfo.app`
-   **ASN to details lookup** - Queries ASN details (company name, IP ranges) via `asn.ipinfo.app`
-   Automatically groups IPs by ASN
-   Saves results in JSON format
-   Optional proxy support
-   Uses a simple regex-based IPv4 validator
-   ASN input support (e.g., `AS13335`)

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
./install
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

### 3️⃣ ASN lookup (NEW)

``` bash
echo AS13335 | ASNinformer
```

``` bash
cat ASNs.txt | ASNinformer
```

``` bash
ASNinformer AS13335
```

``` bash
ASNinformer AS13335 AS15169
```

Example `ASNs.txt`:

    AS13335
    AS15169

------------------------------------------------------------------------

## Options

| Flag | Description |
|------|-------------|
| `-p, --proxy` | Use an HTTP/HTTPS proxy |
| `-o` | Output file name (default: `./asn-result.json`) |

### Examples

#### Save results to custom file

``` bash
echo 8.8.8.8 | ASNinformer -o results.json
```

#### Use a proxy

``` bash
echo 8.8.8.8 | ASNinformer -p http://127.0.0.1:8080
```

#### ASN lookup with custom output

``` bash
echo AS13335 | ASNinformer -o asn-details.json
```

------------------------------------------------------------------------

## Output Format

### IP Lookup Output

The script outputs a JSON file structured like this:

``` json
{
  "AS15169": {
    "company's name": "Google LLC",
    "ASN": "AS15169",
    "ASN url": "https://bgp.he.net/AS15169",
    "Provided IP Ranges": [
      "8.8.8.0/24"
    ],
    "Provided IP": [
      "8.8.8.8"
    ]
  }
}
```

Each ASN entry contains:
- **ASN** - ASN number
- **ASN url** - Link to BGP info (`bgp.he.net`)
- **Provided IP Ranges** - Announced CIDR ranges for the input IPs
- **Company's Name** - Organization name
- **Provided IP** - List of input IPs belonging to that ASN

### ASN Lookup Output (NEW)

When you provide an ASN as input, the output includes IP ranges:

``` json
{
  "AS13335": {
    "Company's Name": "Cloudflare, Inc.",
    "ASN": "AS13335",
    "ASN Url": "https://bgp.he.net/AS13335",
    "IP Ranges": [
      "1.1.1.0/24",
      "1.0.0.0/24",
      ...
    ]
  }
}
```

Each ASN entry contains:
- **Company's Name** - Organization name
- **ASN** - ASN number
- **ASN Url** - Link to BGP info (`bgp.he.net`)
- **IP Ranges** - All announced IP ranges for that ASN

------------------------------------------------------------------------

## Requirements

- Python 3.x
- `requests` library
- `certifi`, `charset-normalizer`, `idna`, `urllib3` (dependencies of requests)

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

created by: **NakuTenshi**

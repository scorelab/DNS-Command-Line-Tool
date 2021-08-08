# DNS-Command-Line-Tool

DNSTool-CLI is an extension of the DNSTool, which is designed to monitor the given set of internet resources like domains, IP, SOA, etc.  DNSTool-CLI allows the user to download the DNS scan feed(s) automatically by integrating the CLI to their corn jobs or Airflow automation. This project is to develop high throughput and low latency data transferring pipeline with authentication for transferring the data from the system’s file store to the consumer environment.

<div align="center">
    <a href="https://drive.google.com/uc?export=view&id=1mqz8ZL-7_ja3Z8dwKhhDqwtoqyMUtpL_"><img src="https://drive.google.com/uc?export=view&id=1mqz8ZL-7_ja3Z8dwKhhDqwtoqyMUtpL_" style="max-width: 100%; height: auto;" title="Click to enlarge picture"></a>
</div>
    
    
    
The command line tool can be found in pypi as [DNS-Command-Line-Tool 1.0.0](https://pypi.org/project/DNS-Command-Line-Tool)

 The commandline tool can be accessed by **dnsip**

   ```
usage: dnsip [-h] [--size] [--list] [--download file_to_download] [--download_bucket Local_location_of_files]
             [--schedule Local_location_of_files]

Check, download and update the local DNS IP dataset location.

optional arguments:
  -h, --help            show this help message and exit
  --size                The size of the downloadable blob
  --list                List the available data for downloading
  --download file_to_download
                        Download a single file
  --download_bucket Local_location_of_files
                        One-time download of the complete DNSIP dataset
  --schedule Local_location_of_files
                        Update the DNSIP dataset every 24 hours

```

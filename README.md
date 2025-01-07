# IOC List Creator & Lookup

The IoC List Creator downloads IoCs (“Indicator of Compromise”, i.e., malicious domains, IP-addresses, or URLs) from different blocklists and unites them into three CSV files (one for each type). 
The information of this files is served via a REST-API and can be used by Graylog to enrich logs.

## How does it work?

The main script (`ioc-lists.py`) downloads all given blocklists in `downloads.json` and saves them temporarily for aggregation. 
After completing all downloads, it reads every file and separates the containing IoCs into three categories, IP, domain, URL. 
IoCs of each type are written to seperate CSV-files.


The IoC data can be queried through a lightweight Flask REST-API (`ioc-server.py`). The API serves an endpoint (`/lookup`) which expects a get-request with the lookup value (IP, domain, URL) and an authorization token. 
If the given lookup value is known as an IoC and the source of the IoC blocklist is found it will be returned, otherwise the request returns false. 

The API endpoint is used with an Graylog HTTP JSONPath Data Adapter to serve a Lookup Table. This Lookup Table can be used in different Pipelines to check different logs containing IPs, domains and URLs. If the check about being IoCs turns out true the respective log can be marked as such. 

## Installation

### Requirements

- Python 3.6
- requests
- validators
- Flask
- gunicorn

You can install the requirements with the following command `pip3 install -r requirements.txt`.
Gunicorn can be installed with `sudo apt install gunicorn3` or `pip3 install gunicorn`.

### Configuration

The scripts are configured by a ini-style configuration file with the following content:

```
[ioc]
token=<random string e.g.: pwgen -s 10>
download_list=<absolute path to the json file with blocklists to download>
output_dir=<absolute path to the directory in which the CSV files are stored>
```

### Running the IOC Server

The following systemd-service file can be used to run the ioc-server. Make sure to replace `CONFIG_FILE` and the `WorkingDirectory` with appropiate values.

```
[Unit]
Description=IOC server
After=network.target

[Service]
# the specific user that our service will run as
Environment=CONFIG_FILE=<absolute path to the config file>
User=<user to run the server>
Group=<group of the user>
# another option for an even more restricted service is
# DynamicUser=yes
# see http://0pointer.net/blog/dynamic-users-with-systemd.html
RuntimeDirectory=gunicorn
WorkingDirectory=<absolute path to the working directory>
ExecStart=<absolute path to gunicorn> -b 0.0.0.0:<port to run the server on> ioc-server:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

To start and enable the service, follow these steps:

1. Place the file `ioc-server.service` in `/etc/sytemd/system`
2. Start the server with `systemctl start ioc-server`
3. Enable automatic start on boot: `systemctl enable ioc-server`

## Running the IOC List Creator 

The script can be run with the following command:

`python3 ioc-lists.py [-h] [-c CONFIG]`

Following command line arguments can optionally be passed to the script:

| Argument | Funktion |
| :-------------: |-------------|
| --help / -h | Shows the help function |
| --config / -c | Allows using a custom config file |

## Cron Job

The creation of a cron job is recommended to regularly execute IoC Lookup and update its lists and the server. 
The execution interval depends on your conditions.
The crontab for IoC lookup should follow the following scheme:

```
python3 <absolute-path>/ioc-lists.py --config <absolute-path>/ioc-lists.conf && curl -XPOST -s --show-error "http://<ip:port>/reload?token=<token>" > /dev/null
```

## Blocklists Configuration

The blocklists to download are documented in the json file `downloads.json`.
IoC Lookup currently supports the download of text, CSV or JSON files.
An entry in the download file is constructed with the following schema:

```
{
    "url": <absolute uri to the file (online or local)>,
    "source": <source of the blocklist>,
    "type": <type of file ("text/plain", "text/csv" or "text/json")>,
    "content": <content of the file (ip/domain/url)>,
    "parser": <parser to be used>
}
```

## Adding a new parser

For parsing the blocklists an abstract factory pattern (see https://en.wikipedia.org/wiki/Abstract_factory_pattern for more information) is used. All code regarding the parsers can be found in the folder `ioc`. The folder `ioc` contains a folder `parsers` which contains subfolders for the supported file types (text, CSV, JSON). The structure of relevant folders/files is as following:

```bash
ioc/parsers
├── __init__.py
├── csv
│   ├── __init__.py
│   ├── factory.py
│   └── parser.py
├── json
│   ├── __init__.py
│   ├── factory.py
│   └── parser.py
├── parser_factory.py
└── text
    ├── __init__.py
    ├── factory.py
    └── parser.py
```

### Writing a new parser for an existing file type

If you need a new parser for an existing file type, you need to edit the files `factory.py` and `parser.py` inside the corresponding subfolder.
1.	First step is to write a create a new class inside the `parser.py` file. The class needs to implement the static method `parse(text_file, source)` which returns the IoC data. 
2.	Afterwards you need to edit the file `factory.py` to register the new class. Add a new `elif`-case for the parser and call the `parse` function of the parser. 

For further guidance look at the other parsers’ implementations and how they are registered in both files.

### Writing a parser for a new file type

If you need to parse a new file type you need to add a new subfolder for that type and create three files `__init__.py`, `factory.py` and `parser.py`inside this subfolder.
1.	First step is to create the needed parser inside `parser.py` (see description in Writing a new parser for an existing file type). 
2.	After that you need to import the parser in the file `factory.py`, this can be done with 
`from .parser import *`. This imports all parsers from their file. 
3.	Now you need to create the factory class for that file type in `factory.py` and define the static method `create_<file-type>_parser(file)`. Substitute `<file-type>` with your corresponding file type. This function is used to call the parsers of the file type.
4.	Export the newly created factory in the `__init__.py` file. 
This can be done with `from .factory import <factory-name>`.
5.	Import the new factory in `parser_factory.py`. Look at how the other factories are imported for guidance.
6.	Register the new factory and file type in the method `create_parser(file)` of the file `parser_factory.py`.

For more guidance and information look at how the other factories and parsers are implemented and repeat the same process.

## Rest-API Endpoints

The following endpoints are provided by the API:

| Endpoint | Type | Parameter | Return | Description |
| --- | --- | --- | --- | --- |
| `lookup` | GET | `token`: Auth token<br>`value`: Domain/IP/URL | 200: `False` or source of IoC<br>403: Invalid token or wrong parameter | Fetch the result of an IoC Lookup |
| `reload` | POST | `token`: Auth token | 200<br>403: Invalid token or wrong parameter | Reload the server to serve new information |

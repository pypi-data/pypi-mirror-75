# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['witnessme',
 'witnessme.api',
 'witnessme.api.routers',
 'witnessme.commands',
 'witnessme.console']

package_data = \
{'': ['*'], 'witnessme': ['signatures/*', 'templates/*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiosqlite>=0.13.0,<0.14.0',
 'fastapi>=0.55.1,<0.56.0',
 'imgcat>=0.5.0,<0.6.0',
 'jinja2>=2.11.2,<3.0.0',
 'lxml>=4.5.2,<5.0.0',
 'prompt-toolkit>=3.0.5,<4.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'pyppeteer>=0.2.2,<0.3.0',
 'python-multipart>=0.0.5,<0.0.6',
 'pyyaml>=5.3.1,<6.0.0',
 'terminaltables>=3.1.0,<4.0.0',
 'uvicorn>=0.11.5,<0.12.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['witnessme = witnessme.console.witnessme:run',
                     'wmapi = witnessme.console.wmapi:run',
                     'wmdb = witnessme.console.wmdb:run']}

setup_kwargs = {
    'name': 'witnessme',
    'version': '1.5.0',
    'description': 'Web Inventory tool that uses Pyppeteer (headless Chrome/Chromium) and provides some extra bells & whistles to make life easier.',
    'long_description': '# WitnessMe\n\n<p align="center">\n  <img src="https://user-images.githubusercontent.com/5151193/60783062-1f637c00-a106-11e9-83de-83ef88115f74.gif" alt="WitnessMe"/>\n</p>\n\nWitnessMe is primarily a Web Inventory tool inspired by [Eyewitness](https://github.com/FortyNorthSecurity/EyeWitness), its also written to be extensible allowing you to create custom functionality that can take advantage of the headless browser it drives in the back-end.\n\nWitnessMe uses the [Pyppeteer](https://github.com/pyppeteer/pyppeteer) library to drive Headless Chromium.\n\n## Sponsors\n[<img src="https://www.blackhillsinfosec.com/wp-content/uploads/2016/03/BHIS-logo-L-300x300.png" width="130" height="130"/>](https://www.blackhillsinfosec.com/)\n[<img src="https://handbook.volkis.com.au/assets/img/Volkis_Logo_Brandpack.svg" width="130" hspace="10"/>](https://volkis.com.au)\n[<img src="https://user-images.githubusercontent.com/5151193/85817125-875e0880-b743-11ea-83e9-764cd55a29c5.png" width="200" vspace="21"/>](https://qomplx.com/blog/cyber/)\n[<img src="https://user-images.githubusercontent.com/5151193/86521020-9f0f4e00-be21-11ea-9256-836bc28e9d14.png" width="250" hspace="20"/>](https://ledgerops.com)\n[<img src="https://user-images.githubusercontent.com/5151193/87607538-ede79e00-c6d3-11ea-9fcf-a32d314eb65e.png" width="170" hspace="20"/>](https://www.guidepointsecurity.com/)\n\n## Table of Contents\n\n- [WitnessMe](#witnessme)\n  * [Motivation](#motivation)\n  * [Installation](#Installation)\n    + [Docker](#docker)\n    + [Python Package](#python-package)\n    + [Development Install](#development-install)\n  * [Quick starts](#quick-starts)\n    + [Finding F5 Load Balancers Vulnerable to CVE-2020-5902](#finding-f5-load-balancers-vulnerable-to-cve-2020-5902)\n    + [Scraping Javascript Heavy Webpages](#scraping-javascript-heavy-webpages)\n  * [RESTful API](#restful-api)\n  * [Deploying to the Cloud](#deploying-to-the-cloud-)\n    + [GCP Cloud Run](#gcp-cloud-run)\n    + [AWS ElasticBeanstalk](#aws-elasticbeanstalk)\n  * [Usage and Examples](#usage-and-examples)\n    + [Modes of Operation](#modes-of-operation)\n      * [Screenshot Mode](#screenshot-mode)\n      * [Grab Mode](#grab-mode)\n    + [Interacting with the Scan Database](#interacting-with-the-scan-database)\n    + [Generating Reports](#generating-reports)\n    + [Previewing Screenshots Directly in the Terminal](#preview-screenshots-directly-in-the-terminal)\n  * [Creating Signatures](#call-for-signatures)\n\n## Motivation\n\nAre there are a bunch of other tools that do this? Absolutely. See the following projects for alternatives (I\'m sure there are more, these are the ones I\'ve personally tried):\n\n- [Eyewitness](https://github.com/FortyNorthSecurity/EyeWitness)\n- [GoWitness](https://github.com/sensepost/gowitness)\n- [Aquatone](https://github.com/michenriksen/aquatone)\n\nThe reason why I wrote WitnessMe was that none of these projects had all of the features I wanted/needed in order for them to work well within my workflow. Additionally, some of them are prone to a decent amount of installation/dependency hell.\n\nHere are some of the main features that make WitnessMe "stand out":\n\n- Written in Python 3.7+\n- Ability to parse extremely large Nessus and NMap XML files\n- Docker compatible\n- No installation/dependency hell\n- Full test suite! Everything is less prone to bugs\n- CSV & HTML reporting\n- Provides a RESTful API! Scan stuff remotely!\n- CLI interface to view and search scan results without having to view the reports.\n- Signature scanning (Signatures use YAML files)\n- Preview screenshots directly in the terminal (On MacOSX/ITerm2 and some Nix terminals)\n- Extensibly written, allowing you to add functionality that can take advantage of headless chromium.\n- Built to be deployed to the Clouds (e.g. GCP Cloud Run , AWS ElasticBeanstalk etc...)\n\n## Installation\n\n### Docker\n\nRunning WitnessMe from a Docker container is fully supported and is the easiest/recommended way of using the tool.\n\n**Note: it is highly recommended to give the Docker container at least 4GB of RAM during large scans as Chromium can be a resource hog. If you keep running into "Page Crash" errors, it\'s because your container does not have enough memory. On Mac/Windows you can change this by clicking the Docker Task Bar Icon -> Preferences -> Resources. For Linux, refer to Docker\'s documentation**\n\nPull the image from Docker Hub:\n\n```console\ndocker pull byt3bl33d3r/witnessme\n```\n\nYou can then spin up a docker container, run it like the main `witnessme` script and pass it the same arguments:\n\n```console\ndocker run --rm -ti $IMAGE_ID screenshot https://google.com 192.168.0.1/24\n```\n\nAlternatively, you can drop into a shell within the container and run the tools that way. This also allows you to execute the `wmdb` and `wmapi` scripts.\n\n```console\ndocker run --rm -ti --entrypoint=/bin/sh $IMAGE_ID\n```\n\n### Python Package\n\nWitnessMe is also available as a Python package (Python 3.7 or above is required). If you do install it this way it is extremely recommended to use [pipx](https://github.com/pipxproject/pipx) as it takes care of installing everything in isolated environments for you in a seamless manner.\n\nRun the following commands:\n\n```console\npython3 -m pip install --user pipx\npipx install witnessme\n```\n\nAll of the WitnessMe scripts should now be in your PATH and ready to go.\n\n### Development Install\n\nYou really should only install WitnessMe this way if you intend to hack on the source code. You\'re going to Python 3.7+ and [Poetry](https://python-poetry.org/): please refer to the Poetry installation documentation in order to install it.\n\n```console\ngit clone https://github.com/byt3bl33d3r/WitnessMe && cd WitnessMe\npoetry install\n```\n\n## Quick Starts\n\n### Finding F5 Load Balancers Vulnerable to CVE-2020-5902\n\nInstall WitnessMe using Docker:\n\n```console\ndocker pull byt3bl33d3r/witnessme\n```\n\nGet the `$IMAGE_ID` from the `docker images` command output, then run the following command to drop into a shell inside the container. Additionally, specify the `-v` flag to mount the current directory inside the container at the path `/transfer` in order to copy the scan results back to your host machine (if so desired):\n\n```console\ndocker run -it --entrypoint=/bin/sh -v $(pwd):/transfer $IMAGE_ID\n```\n\nScan your network using WitnessMe, it can accept multiple .Nessus files, Nmap XMLs, IP ranges/CIDRs. Example:\n\n```console\nwitnessme screenshot 10.0.1.0/24 192.168.0.1-20 ~/my_nessus_scan.nessus ~/my_nmap_scan.xml\n```\n\nAfter the scan is finished, a folder will have been created in the current directory with the results. Access the results using the `wmdb` command line utility:\n\n```console\nwmdb scan_2020_$TIME/\n```\n\nTo quickly identify F5 load balancers, first perform a signature scan using the `scan` command. Then search for "BIG-IP" or "F5" using the `servers` command (this will search for the "BIG-IP" and "F5" string in the signature name, page title and server header):\n\n![image](https://user-images.githubusercontent.com/5151193/86619581-43fc6900-bf91-11ea-9a01-ba8ce09c3f3b.png)\n\nAdditionally, you can generate an HTML or CSV report using the following commands:\n```console\nWMDB ≫ generate_report html\n```\n```console\nWMDB ≫ generate_report csv\n```\n\nYou can then copy the entire scan folder which will contain all of the reports and results to your host machine by copying it to the `/transfer` folder.\n\n### Scraping Javascript Heavy Webpages\n\nAs of v1.5.0, WitnessMe has a `grab` command which allows you to quickly scrape Javascript heavy webpages by rendering the page first with Headless Chromium and then parsing the resulting HTML using the specified XPath (see [here](https://devhints.io/xpath) for an XPath cheatsheet).\n\nBelow are a few examples to get your started.\n\nThis grabs a list of all advertised domains on the `144.161.160.0/23` subnet from [Hurricane Electric\'s BGP Toolkit](https://bgp.he.net/):\n```console\nwitnessme -d grab -x \'//div[@id="dns"]/table//tr/td[2]/a/text()\' https://bgp.he.net/net/144.161.160.0/23#_dns\n```\n\n## RESTful API\n\nAs of version 1.0, WitnessMe has a RESTful API which allows you to interact with the tool remotely.\n\n**Note: Currently, the API does not implement any authentication mechanisms. Make sure to allow/deny access at the transport level**\n\nTo start the RESTful API for testing/development purposes run :\n```console\nwmapi\n```\n\nThe API documentation will then be available at http://127.0.0.1:8000/docs\n\n[Uvicorn](https://www.uvicorn.org/) should be used to enable SSL and run the API in production. See [this dockerfile](https://github.com/byt3bl33d3r/WitnessMe/blob/master/dockerfiles/Dockerfile.selfhosted) for an example.\n\n## Deploying to the Cloud (™)\n\nSince WitnessMe has a RESTful API now, you can deploy it to the magical cloud and perform scanning from there. This would have a number of benefits, including giving you a fresh external IP on every scan (More OPSEC safe when assessing attack surface on Red Teams).\n\nThere are a number of ways of doing this, you can obviously do it the traditional way (e.g. spin up a machine, install docker etc..).\n\nRecently cloud service providers started offering ways of running Docker containers directly in a fully managed environment. Think of it as serverless functions (e.g. AWS Lambdas) only with Docker containers.\n\nThis would technically allow you to really quickly deploy and run WitnessMe (or really anything in a Docker container) without having to worry about underlying infrastructure and removes a lot of the security concerns that come with that.\n\nBelow are some of the ones I\'ve tried along with the steps necessary to get it going and any issues I encountered.\n\n### GCP Cloud Run\n\n**Unfortunately, it seems like Cloud Run doesn\'t allow outbound internet access to containers, if anybody knows of a way to get around this please get in touch**\n\nCloud Run is by far the easiest of these services to work with.\n\nThis repository includes the `cloudbuild.yaml` file necessary to get this setup and running.\n\nFrom the repositories root folder (after you authenticated and setup a project), these two commands will automatically build the Docker image, publish it to the Gcloud Container Registry and deploy a working container to Cloud Run:\n\n```bash\ngcloud builds submit --config cloudbuild.yaml\ngcloud run deploy --image gcr.io/$PROJECT_ID/witnessme --platform managed\n```\n\nThe output will give you a HTTPS url to invoke the WitnessMe RESTful API from :)\n\nWhen you\'re done:\n\n```bash\ngcloud run services delete witnessme\ngcloud container images delete gcr.io/$PROJECT_ID/witnessme\n```\n\n### AWS ElasticBeanstalk\n\nTO DO\n\n## Usage\n\nThere are 3 main utilities:\n\n- `witnessme`: is the main CLI interface.\n- `wmdb`: allows you to browse the database (created on each scan) to view results and generate reports.\n- `wmapi`: provides a RESTful API to schedule, start, stop and monitor scans.\n\n### Modes of Operations\n\nAs of v1.5.0 there are two main modes (commands) that the `witnessme` utility Supports:\n\n- The `screenshot` command, you guessed it, screenshots webpages. This is the main functionality.\n- The `grab` command allows you to scrape pages and quickly grab server headers.\n\n```\nusage: witnessme [-h] [--threads THREADS] [--timeout TIMEOUT] [-d] [-v] {screenshot,grab} ...\n\nWitnessMe!\n\npositional arguments:\n  {screenshot,grab}\n\noptional arguments:\n  -h, --help         show this help message and exit\n  --threads THREADS  Number of concurrent browser tab(s) to open\n                     [WARNING: This can cause huge RAM consumption if set to high values] (default: 15)\n  --timeout TIMEOUT  Timeout for each connection attempt in seconds (default: 15)\n  -d, --debug        Enable debug output (default: False)\n  -v, --version      show program\'s version number and exit\n```\n\n#### Screenshot Mode\n\n```console\n$ witnessme screenshot --help\nusage: witnessme screenshot [-h] [-p PORTS [PORTS ...]] target [target ...]\n\npositional arguments:\n  target                The target IP(s), range(s), CIDR(s) or hostname(s), NMap XML file(s), .Nessus file(s)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PORTS [PORTS ...], --ports PORTS [PORTS ...]\n                        Ports to scan if IP Range/CIDR is provided\n```\n\nCan accept a mix of .Nessus file(s), Nmap XML file(s), files containing URLs and/or IPs, IP addresses/ranges/CIDRs and URLs or alternatively read from stdin.\n\n*Note: WitnessMe detects .Nessus and NMap files by their extension so make sure Nessus files have a `.nessus` extension and NMap scans have a `.xml` extension*\n\nLong story short, should be able to handle anything you throw at it:\n\n```console\nwitnessme screenshot 192.168.1.0/24 192.168.1.10-20 https://bing.com ~/my_nessus_scan.nessus ~/my_nmap_scan.xml ~/myfilewithURLSandIPs\n```\n\n```console\n$ cat my_domain_list.txt | witnessme screenshot -\n```\n\nIf an IP address/range/CIDR is specified as a target, WitnessMe will attempt to screenshot HTTP & HTTPS pages on ports 80, 8080, 443, 8443 by default. This is customizable with the `--port` argument.\n\nOnce a scan is completed, a folder with all the screenshots and a database will be in the current directory, point `wmdb` to the folder in order to see the results.\n\n```console\nwmdb scan_2019_11_05_021237/\n```\n#### Grab Mode\n\n```console\n$ witnessme grab --help\nusage: witnessme grab [-h] [-x XPATH | -l] target [target ...]\n\npositional arguments:\n  target                The target IP(s), range(s), CIDR(s) or hostname(s), NMap XML file(s), .Nessus file(s)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -x XPATH, --xpath XPATH\n                        XPath to use\n  -l, --links           Get all links\n```\n\nThe `grab` subcommand allows you to render Javascript heavy webpages and scrape their content using XPaths. See this [section](#scraping-javascript-heavy-webpages) for some examples.\n\n### Interacting with the Scan Database\n\nOnce a scan is completed (using the `screenshot` mode), a folder with all the screenshots and a database will be in the current directory, point `wmdb` to the folder in order to see the results.\n\n```console\nwmdb scan_2019_11_05_021237/\n```\nThis will drop you into the WMDB CLI menu.\n\nPressing tab will show you the available commands and a help menu:\n\n<p align="center">\n  <img src="https://user-images.githubusercontent.com/5151193/88490790-725bdb80-cf74-11ea-8ecd-1300cf1ad534.png" alt="Tab "/>\n</p>\n\nThe `servers` and `hosts` commands in the `wmdb` CLI accept 1 argument. WMCLI is smart enough to know what you\'re trying to do with that argument\n\n#### Server Command\n\nNo arguments will show all discovered servers. Passing it an argument will search the `title` and `server` columns for that pattern (it\'s case insensitive).\n\nFor example if you wanted to search for all discovered Apache Tomcat servers:\n- `servers tomcat` or `servers \'apache tomcat\'`\n\nSimilarly if you wanted to find servers with a \'login\' in the title:\n- `servers login`\n\n#### Hosts Command\n\nNo arguments will show all discovered hosts. Passing it an argument will search the `IP` and `Hostname` columns for that pattern (it\'s case insensitive). If the value corresponds to a Host ID it will show you the host information and all of the servers discovered on that host which is extremely useful for reporting purposes and/or when targeting specific hosts.\n\n#### Signature Scan\n\nYou can perform a signature scan on all discovered services using the `scan` command.\n\n### Generating Reports\n\nYou can use the `generate_report` command in the `wmdb` cli to generate reports in HTML or CSV format. To generate a HTML report simply run `generate_report` without any arguments. Here\'s an example of what it\'ll look like:\n\n![image](https://user-images.githubusercontent.com/5151193/86676611-2c44d500-bfd1-11ea-87fd-faf874a2dcf2.png)\n\nTo generate a CSV report:\n\n```console\nWMDB ≫ generate_report csv\n```\n\nThe reports will then be available in the scan folder.\n\n### Preview Screenshots Directly in the Terminal\n\n**Note: this feature will only work if you\'re on MacOSX and using ITerm2**\n\nYou can preview screenshots directly in the terminal using the `show` command:\n\n<p align="center">\n  <img src="https://user-images.githubusercontent.com/5151193/68194496-5e012a00-ff72-11e9-9ccd-6a50aa384f3e.png" alt="ScreenPreview"/>\n</p>\n\n## Writing Signatures\n\nIf you run into a new webapp write a signature for it! It\'s beyond simple and they\'re all in YAML!\n\nDon\'t believe me? Here\'s the AirOS signature (you can find them all in the [signatures directory](https://github.com/byt3bl33d3r/WitnessMe/tree/master/witnessme/signatures)):\n\n```yaml\ncredentials:\n- password: ubnt\n  username: ubnt\nname: AirOS\nsignatures:\n- airos_logo.png\n- form enctype="multipart/form-data" id="loginform" method="post"\n- align="center" class="loginsubtable"\n- function onLangChange()\n# AirOS ubnt/ubnt\n```\n\nYup that\'s it. Just plop it in the signatures folder and POW! Done.',
    'author': 'Marcello Salvati',
    'author_email': 'byt3bl33d3r@pm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/byt3bl33d3r/WitnessMe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)

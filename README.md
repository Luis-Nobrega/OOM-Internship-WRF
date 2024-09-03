# Weather Research & Forecasting Model (WRF) 
## Processing of forecasts with docker containers in Azure cloud environment
Running WRF simulation on a local or Virtual Machine takes up a **lot** of resources and requires above-average computers. Using docker allows a reduction in resources as well as the possibility of migrating containers into cloud environments, like *MS AZURE CLOUD*.

## Motivation
Reduction of computation costs associated with large CORE and RAM usage for *OOM*.

## Screenshots
![OOM logo](https://oom.arditi.pt/assets/OOM_Logo.png)

## Tech/framework used

<b>Built with</b>
- [WRF](https://www.mmm.ucar.edu/models/wrf)
- [Docker](https://www.docker.com/)
- [Pyhton](https://www.python.org/)
- [Bash](https://pt.wikipedia.org/wiki/Bash)

## Features
Allows automation of simulations for multiple domains. Performs verifications on input files. Kills container in case of **MPI ABORT**.

## Installation
<b>After downloading `reduced_wrf_image.tar.gz` *(3.3GB)* or `wrf_image.tar.gz` *(22.3 GB)* from SSD:</b>

- `docker load` -i /path/to/`reduced_wrf_image.tar.gz` -> This normally takes *15 minutes* for `reduced_wrf_image.tar.gz` and over an hour for `wrf_image.tar.gz`;
- On your **WDIR** install: `core_calc`;
- Provide the necessary input files: `instructions.txt`, `wps_input.txt` and `wrf_input.txt`;
- Example files are listed below. Change `instructions.txt` *processors* value for an adequate value;
- In main folder `./run.sh -e START_DATE=2024-09-01 -e END_DATE=2024-09-01_03:00:00`. Date format is either **%Y-%m-%d** or **%Y-%m-%d_%H:00:00** -> Time intervals must be multiples of 3h for *forecast mode* and 6h for *historic mode*;
- Validate output given in console with *y* or *n*;
- Data will be output in `data` folder if no errors occur. 

## Input file example

## API Reference

Depending on the size of the project, if it is small and simple enough the reference docs can be added to the README. For medium size to larger projects it is important to at least provide a link to where the API reference docs live.

## Tests
Describe and show how to run the tests with code examples.

## How to use?
If people like your project they’ll want to learn how they can use it. To do so include step by step guide to use your project.

## Contribute

Let people know how they can contribute into your project. A [contributing guideline](https://github.com/zulip/zulip-electron/blob/master/CONTRIBUTING.md) will be a big plus.

## Credits
Give proper credits. This could be a link to any repo which inspired you to build this project, any blogposts or links to people who contrbuted in this project. 

#### Anything else that seems useful

## License
A short snippet describing the license (MIT, Apache etc)

MIT © [Yourname]()

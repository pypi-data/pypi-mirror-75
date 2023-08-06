# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proxmox_hetzner_autoconfigure',
 'proxmox_hetzner_autoconfigure.configurators',
 'proxmox_hetzner_autoconfigure.configurators.lvm_thin_storage',
 'proxmox_hetzner_autoconfigure.configurators.network',
 'proxmox_hetzner_autoconfigure.configurators.network.topologies',
 'proxmox_hetzner_autoconfigure.configurators.storage_box',
 'proxmox_hetzner_autoconfigure.configurators.tls',
 'proxmox_hetzner_autoconfigure.util']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0', 'pythondialog>=3.5.1,<4.0.0']

entry_points = \
{'console_scripts': ['proxmox-hetzner-autoconfigure = '
                     'proxmox_hetzner_autoconfigure.main:run']}

setup_kwargs = {
    'name': 'proxmox-hetzner-autoconfigure',
    'version': '0.1.6',
    'description': 'Helps to configure Proxmox on Hetzner. Takes over where Hetzner installimage left off',
    'long_description': '<!-- PROJECT LOGO -->\n<br />\n<p align="center">\n  <h1 align="center">Proxmox Hetzner Autoconfigure</h1>\n  <p align="center">\n    Takes over where the Hetzner installimage left off\n  </p>\n</p>\n\n<!-- ABOUT THE PROJECT -->\n\n## About This Project\n\nThis is a command line `dialog` based tool to help configure a freshly installed Proxmox host node on a Hetzner dedicated server.\n\nThe application will ask you a series of questions to ascertain how you\'d like your server to be setup, and output a neat, well documented `boostrap.sh` script you can execute on your Proxmox host to configure things like Networking, Storage, and TLS.\n\nThings this project will help configure and whether they are implemented yet:\n\n- [x] Setting up the Network\n  - [x] Routed topology where you have purchased an additional subnet\n  - [x] Routed topology where you have purchased separate IPs\n  - [ ] Bridged topology where you have purchased an additional subnet\n  - [ ] Bridged topology where you have purchased separate IPs\n  - [ ] Single IP (port forwarding, SNI)\n- [x] TLS with LetsEncrypt / ACME\n- [x] Mounting a Hetzner Storage Box\n- [x] Setting up LMV-Thin\n- [ ] DNS and DHCP (DNSMasq)\n- [ ] Wireguard\n\nHopefully this script saves some people some time. I\'ll try and update it as I learn new and better ways to do things with Proxmox.\n\n![Screenshot](https://raw.githubusercontent.com/johnknott/proxmox-hetzner-autoconfigure/master/images/screenshot.png)\n\n<!-- GETTING STARTED -->\n\n## Getting Started\n\nTo install the binary locally follow these steps:\n\n### Prerequisites\n\nNeeds a [dialog](https://linux.die.net/man/1/dialog) like program in your search path.\nThis is available on most Linux operating systems through the native package managers and on MacOS through `brew`.\nWindows users might have more trouble, although running through WSL or a VM would work.\n\nYou also need [Python 3.6 or above](https://www.python.org/) and pip, if they\'re not already installed.\n\nFor example, on Debian:\n\n```sh\n$ apt install dialog python3-pip\n```\n\n### Installation\n\n1. Install the package using the python3 version of pip.\n\n```sh\n$ pip3 install proxmox_hetzner_autoconfigure\n```\n\n<!-- USAGE EXAMPLES -->\n\n## Usage\n\n```sh\n$ proxmox_hetzner_autoconfigure\n```\n\nThen follow the instructions. The application does not need to be run as root and will not make any changes to your system. It also does not need to be run on your Proxmox host node. It\'s better to run it locally and not pollute your host node with unnecessary dependencies.\n\nIt will ask you a series of questions using the venerable `dialog` application to ascertain how you would like your Proxmox system setup, and then output a simple shell (Bash) script `boostrap.sh` that can be run on your Proxmox host node.\n\n`bootstrap.sh` has no dependencies and can easily be added to source control to document your system setup and for disaster recovery scenarios.\n\n### Development Setup\n\n- Requires a working installation of [Python 3.6 or above](https://www.python.org/), [dialog](https://linux.die.net/man/1/dialog) and [Poetry](https://python-poetry.org/).\n- Checkout the source code using `git`\n\n```sh\n$ git clone https://github.com/johnknott/proxmox-hetzner-autoconfigure.git\n```\n\n- From within the project directory, fetch the dependencies using `poetry`.\n\n```sh\n$ poetry install\n```\n\n- From within the project directory, run the application using `poetry`.\n\n```sh\n$ poetry run main\n```\n\n- From within the project directory, run the test-suite using `poetry`.\n\n```sh\n$ poetry run pytest\n```\n\n<!-- ROADMAP -->\n\n## Roadmap\n\nSee the [open issues](https://github.com/johnknott/proxmox-hetzner-autoconfigure/issues) for a list of proposed features (and known issues).\n\n<!-- CONTRIBUTING -->\n\n## Contributing\n\nContributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n<!-- LICENSE -->\n\n## License\n\nDistributed under the MIT License. See `LICENSE` for more information.\n\n<!-- CONTACT -->\n\n## Contact\n\nJohn Knott - [@johndknott](https://twitter.com/johndknott) - john.knott@gmail.com\n\nProject Link: [https://github.com/johnknott/proxmox-hetzner-autoconfigure](https://github.com/johnknott/proxmox-hetzner-autoconfigure)\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n\n[product-screenshot]: images/screenshot.png\n',
    'author': 'John Knott',
    'author_email': 'john.knott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['black_mamba',
 'black_mamba.auth',
 'black_mamba.contract',
 'black_mamba.deploy',
 'black_mamba.epm',
 'black_mamba.mnemonic',
 'black_mamba.testlib']

package_data = \
{'': ['*'],
 'black_mamba': ['compilation/*',
                 'compilation/compiled_files/migration_sample.py',
                 'initialization/*',
                 'initialization/init_files/*',
                 'server/*',
                 'server/server_files/*']}

install_requires = \
['eth-tester==0.5.0b1',
 'mypy>=0.782,<0.783',
 'py-evm==0.3.0a18',
 'pytest-mock==3.1.0',
 'pytest==6.0.1',
 'vyper==0.2.3',
 'web3==5.12.0']

entry_points = \
{'console_scripts': ['mamba = black_mamba.mamba_cli:parse_cli_args']}

setup_kwargs = {
    'name': 'black-mamba',
    'version': '0.4.3',
    'description': 'Development framework to write, test and deploy smart contracts written in Vyper. It has integrated web3.py support.',
    'long_description': '# Mamba\n\nMamba is a framework to write, compile, and deploy smart contracts\nwritten in Vyper language. On top of that, it has supports for writing\nand testing decentralized applications using Web3.py and Pytest.\n\n## Dependencies\n\n* [Ganache](https://www.trufflesuite.com/ganache)\n* [Pip](https://pypi.org/project/pip/)\n* [Python3](https://www.python.org/downloads/) version 3.6 or greater\n* [Go Ethereum](https://geth.ethereum.org/downloads/)\n* [Vyper](https://github.com/ethereum/vyper)\n\n## Installation\n\nYou can install the latest release via ``pip``:\n\n```bash\n$ pip install black-mamba\n```\n\n## Quick Usage\n\nTo set up the the structure of Mamba project directory:\n\n```bash\n$ mamba init\n$ edit contracts/HelloWorld.vy\n$ mamba compile\n```\n\n## Documentation\n\nMamba documentation can be found at [Mamba website](https://mamba.black/documentation).\n\n\n## Contributing\n\nI invite you to join Mamba squad! You can contribute to Mamba by\nwriting documentation, finding bugs, and creating pull requests.\n',
    'author': 'Arjuna Sky Kok',
    'author_email': 'arjuna@mamba.black',
    'url': 'https://mamba.black',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

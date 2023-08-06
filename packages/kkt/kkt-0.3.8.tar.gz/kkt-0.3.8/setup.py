# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kkt', 'kkt.builders', 'kkt.builders.kernels', 'kkt.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'gitpython>=3.1,<4.0',
 'kaggle>=1.5,<2.0',
 'lockfile>=0.12.2,<0.13.0',
 'poetry==1.0.0',
 'tomlkit>=0.5.8,<0.6.0']

entry_points = \
{'console_scripts': ['kkt = kkt.cli:main']}

setup_kwargs = {
    'name': 'kkt',
    'version': '0.3.8',
    'description': 'A tool for kaggle kernel',
    'long_description': '# kkt\nkkt is a tool for kaggle kernel management.\n\n[![Actions Status](https://github.com/ar90n/kkt/workflows/Python%20package/badge.svg)](https://github.com/ar90n/kkt/actions)\n[![PyPI](https://img.shields.io/pypi/v/kkt.svg)](https://pypi.python.org/pypi/kkt)\n[![PythonVersions](https://img.shields.io/pypi/pyversions/kkt.svg)](https://pypi.python.org/pypi/kkt)\n\n## Feature\n* Show the status of the latest version\n* Push your script or notebook to the Kaggle Kernels\n* Pack and emmbedded your library codes into the generated bootstrap codes\n* Create a dataset containing your dependent packages\n* Add bootstrap codes into the head of your script or notebook automatically\n* Add git tags whose name is corresponding kernel version\n* Set environment variable for your kernels\n\n## Installation\nFor now, kkt is designed to be used with poetry. So kkt can be installed by the following.\n\n```bash\n$ poetry add kkt --dev\n```\n\n## Usage\n\n### Set username and token of kaggle-api\nPlease setup your kaggle-api credentials as following this [article](https://github.com/Kaggle/kaggle-api#api-credentials)\n\n### Setup kkt in your project\nSetup this project for [digit-recognizer competition](https://www.kaggle.com/c/digit-recognizer).\nIn this configuration, we use script.py. If you want to use notebook, kkt also support it.\n\n```bash\n$ poetry run kkt init\nAppending Kkt section into your pyproject.toml config.\ncompetition: digit\n0 digit-recognizer\n> 0\nslug: kkt-example\ncode_file [script.py]: script.py\nkernel_type [script]: script\nis_private [Y/n]: n\nenable_gpu [y/N]: n\nenable_internet [y/N]: y\nWould you like to add dataset sources? [y/N]: n\nenable_git_tag [y/N]: n\n```\n\n### Create kkt_example package and its driver code.\nkkt_example provides random choice solver for digit-recognizer competition.\n```bash\n$ tree\n.\n├── kkt_example\n│\xa0\xa0 └── __init__.py\n├── poetry.lock\n├── pyproject.toml\n└── script.py\n\n1 directory, 4 files\n```\n\n__init__.py\n```python\nfrom pathlib import Path\nimport random\n\nimport pandas as pd\n\ndef choice():\n    return random.randint(0, 9)\n\ndef load_sample_submission():\n    path = Path("..") / "input" / "digit-recognizer" / "sample_submission.csv"\n    return pd.read_csv(path,  index_col="ImageId")\n```\n\nscript.py\n```python\nimport kkt_example\n\nsubmission = kkt_example.load_sample_submission()\nfor _, row in submission.iterrows():\n    row["Label"] = kkt_example.choice()\n\n    submission.to_csv("submission.csv")\n```\n\npyproject.toml\n```toml\n[tool.poetry]\nname = "kkt-example"\nversion = "0.1.0"\ndescription = ""\nauthors = ["Masahiro Wada <argon.argon.argon@gmail.com>"]\n\n[tool.poetry.dependencies]\npython = "^3.7"\npandas = "^1.0.0"\n\n[tool.poetry.dev-dependencies]\nkkt = "^0.3.1"\n\n\n[tool.kkt]\nenable_git_tag = false\n\n[tool.kkt.meta_data]\ncode_file = "script.py"\ncompetition = "digit-recognizer"\ncompetition_sources = ["digit-recognizer"]\ndataset_sources = []\nenable_gpu = false\nenable_internet = true\nis_private = false\nkernel_type = "script"\nslug = "kkt-example"\n\n[build-system]\nrequires = ["poetry>=0.12"]\nbuild-backend = "poetry.masonry.api"\n```\n\nIf you want run script.py in local environmet, please run the following.\n\n```bash\n$ poetry run python script.py\n$ head submission.csv\nImageId,Label\n1,1\n2,1\n3,0\n4,2\n5,4\n6,8\n7,5\n8,3\n9,2\n```\n\n### Create a dataset containing dependent packages if need\nIn this example, there aren\'t extra required packages. So `kkt install` displays the following. And this step is not mandatory.\n\n```bash\n$ poetry run kkt install\nref: /ar90ngas/kkt-example-install\nurl: https://www.kaggle.com/ar90ngas/kkt-example-install\nversion: 1\nPushing install kernel successed.\nWait for install kernel completion...\nWait for install kernel completion...\nWait for install kernel completion...\nExtra required packages are nothing.\n```\n\nBut in the little complicated project such as mnist_efficientnet example, `kkt install` displays the following. This means that a new dataset whose slug is `ar90ngas/mnist-efficientnet-requirements` is created. And it contains an extra package which is required by this example. And this package will be installed automatically in the bootstrap code.\n\n```bash\n$ poetry run kkt install\nref: /ar90ngas/mnist-efficientnet-install\nurl: https://www.kaggle.com/ar90ngas/mnist-efficientnet-install\nversion: 1\nPushing install kernel successed.\nWait for install kernel completion...\nWait for install kernel completion...\nWait for install kernel completion...\nOutput file downloaded to /tmp/tmpq6m9iq9p/timm-0.1.30-py3-none-any.whl\nStarting upload for file timm-0.1.30-py3-none-any.whl\n100%|█████████████████████████████████████████████████████████| 203k/203k [00:03<00:00, 53.7kB/s]\nUpload successful: timm-0.1.30-py3-none-any.whl (203KB)\nref: ar90ngas/mnist-efficientnet-requirements\nurl: https://www.kaggle.com/ar90ngas/mnist-efficientnet-requirements\n```\n\n### Push notebook to Kaggle Kernels\n```bash\n$ poetry run kkt push\nref: /ar90ngas/kkt-example\nurl: https://www.kaggle.com/ar90ngas/kkt-example\nversion: 1\n```\nPlease visit [the result](https://www.kaggle.com/ar90ngas/kkt-example).\n\n### Show the status\n```bash\n$ poetry run kkt status\nstatus: complete\n```\n\n## Configuration\nPlease see [examples](https://github.com/ar90n/kkt/tree/master/examples)\n\n\n## License\nThis software is released under the Apache License, see [LICENSE](LICENSE).\n',
    'author': 'Masahiro Wada',
    'author_email': 'argon.argon.argon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ar90n/kkt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

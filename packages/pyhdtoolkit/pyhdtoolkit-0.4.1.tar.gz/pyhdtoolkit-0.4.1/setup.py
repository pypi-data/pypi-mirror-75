# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyhdtoolkit',
 'pyhdtoolkit.beamphysics',
 'pyhdtoolkit.cpymadtools',
 'pyhdtoolkit.maths',
 'pyhdtoolkit.plotting',
 'pyhdtoolkit.scripts',
 'pyhdtoolkit.scripts.ac_dipole',
 'pyhdtoolkit.scripts.triplet_errors',
 'pyhdtoolkit.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.4.1,<0.5.0',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.18.2,<2.0.0',
 'pandas<1.0',
 'scipy>=1.4.1,<2.0.0',
 'tfs-pandas>=1.0.3,<2.0.0']

extras_require = \
{'madx': ['cpymad>=1.4.1,<2.0.0'], 'tqdm': ['tqdm>=4.45.0,<5.0.0']}

entry_points = \
{'console_scripts': ['ac_dipole = '
                     'pyhdtoolkit.scripts.ac_dipole.sext_ac_dipole_tracking:main',
                     'triplet_errors = '
                     'pyhdtoolkit.scripts.triplet_errors.algo:main']}

setup_kwargs = {
    'name': 'pyhdtoolkit',
    'version': '0.4.1',
    'description': 'An all-in-one toolkit package to easy my Python work in my PhD.',
    'long_description': '<h1 align="center">\n  <b>pyhdtoolkit</b>\n</h1>\n\n<p align="center">\n  <!-- PyPi Version -->\n  <a href="https://pypi.org/project/pyhdtoolkit">\n    <img alt="PyPI Version" src="https://img.shields.io/pypi/v/pyhdtoolkit?label=PyPI&logo=PyPI">\n  </a>\n\n  <!-- Github Release -->\n  <a href="https://github.com/fsoubelet/PyhDToolkit/releases">\n    <img alt="Github Release" src="https://img.shields.io/github/v/release/fsoubelet/PyhDToolkit?color=orange&label=Release&logo=Github">\n  </a>\n\n  <br/>\n\n  <!-- Travis Build -->\n  <a href="https://travis-ci.org/github/fsoubelet/PyhDToolkit">\n    <img alt="Travis Build" src="https://img.shields.io/travis/fsoubelet/pyhdtoolkit?label=Travis%20CI&logo=Travis">\n  </a>\n\n  <!-- Code Coverage -->\n  <a href="https://codeclimate.com/github/fsoubelet/PyhDToolkit/maintainability">\n    <img alt="Code Coverage" src="https://img.shields.io/codeclimate/maintainability/fsoubelet/PyhDToolkit?label=Maintainability&logo=Code%20Climate">\n  </a>\n\n  <!-- Docker Build -->\n  <a href="https://hub.docker.com/r/fsoubelet/simenv">\n    <img alt="Docker Build" src="https://img.shields.io/docker/cloud/build/fsoubelet/simenv?label=Docker%20Build&logo=Docker">\n  </a>\n\n  <br/>\n\n  <!-- Code style -->\n  <a href="https://github.com/psf/Black">\n    <img alt="Code Style" src="https://img.shields.io/badge/Code%20Style-Black-9cf.svg">\n  </a>\n\n  <!-- Linter -->\n  <a href="https://github.com/PyCQA/pylint">\n    <img alt="Linter" src="https://img.shields.io/badge/Linter-Pylint-ce963f.svg">\n  </a>\n\n  <!-- Build tool -->\n  <a href="https://github.com/python-poetry/poetry">\n    <img alt="Build tool" src="https://img.shields.io/badge/Build%20Tool-Poetry-4e5dc8.svg">\n  </a>\n\n  <!-- Test runner -->\n  <a href="https://github.com/pytest-dev/pytest">\n    <img alt="Test runner" src="https://img.shields.io/badge/Test%20Runner-Pytest-ce963f.svg">\n  </a>\n\n  <!-- License -->\n  <a href="https://github.com/fsoubelet/PyhDToolkit/blob/master/LICENSE">\n    <img alt="License" src="https://img.shields.io/github/license/fsoubelet/PyhDToolkit?color=9cf&label=License">\n  </a>\n</p>\n\n<p align="center">\n  ♻️ An all-in-one package for Python work in my PhD\n</p>\n\n<p align="center">\n  <a href="https://www.python.org/">\n    <img alt="Made With Python" src="https://forthebadge.com/images/badges/made-with-python.svg">\n  </a>\n</p>\n\n## Installation\n\nThis code is compatible with `Python 3.6+`.\nIf for some reason you have a need for it, create & activate a virtual enrivonment, then install with pip:\n```bash\n> pip install pyhdtoolkit\n```\n\nThis repository respects the [PEP 518][pep_518_ref] development and build recommandations, and [Poetry][poetry_ref] as a tool to do so.\nIf you intend on making changes, clone this repository through VCS and set yourself up with:\n```bash\n> git clone https://github.com/fsoubelet/PyhDToolkit.git\n> cd PyhDToolkit\n> poetry install\n```\n\n## Standards, Testing, Tools and VCS\n\nThis repository follows the `Google` docstring format, uses [Black][black_formatter] as a code formatter with a default enforced line length of 100 characters, and [Pylint][pylint_ref] as a linter.\nYou can format the code with `make format` and lint it (which will format first) with `make lint`.\n\nTesting builds are ensured after each commit through Travis-CI.\nYou can run tests locally with the predefined `make tests`, or through `poetry run pytest <options>` for customized options.\n\nVCS is done through [git][git_ref] and follows the [Gitflow][gitflow_ref] workflow.\nAs a consequence, make sure to always install from `master`.\n\n## Miscellaneous\n\nFeel free to explore the `Makefile` for sensible defaults commands.\nYou will get an idea of what functionality is available by running `make help`.\n\n### Python Environment\n\nThis repository currently comes with an `environment.yml` file to reproduce my work `conda` environment.\nYou can install this environment and add it to your ipython kernel by running `make condaenv`.\n\n### Container\n\nYou can directly pull a pre-built image - tag `latest` is an automated build - from `Dockerhub` with:\n```bash\n> docker pull fsoubelet/simenv\n```\n\nYou can then run the container in interactive mode, and make use of the already activated `conda` environment.\nIt is highly advised to run with `--init` for zombie processes protection (see [Tini][tini_ref] for details).\nAssuming you pulled the provided image from Dockerhub, the command is then (remove the `--rm` flag if you wish to preserve it after running):\n```bash\n> docker run -it --rm --init fsoubelet/simenv\n```\n\nIf you want to do some exploration through `jupyter` you will need to install it first as it is not bundled in the image, then add the custom environment kernelspec.\nRun the following command before heading over to `localhost:8888`:\n```bash\n> docker run -it --rm --init -p 8888:8888 fsoubelet/simenv /bin/bash -c "/opt/conda/bin/conda install -c conda-forge jupyterlab -y --quiet > /dev/null && mkdir /opt/notebooks && /opt/conda/envs/PHD/bin/ipython kernel install --user --name=PHD && /opt/conda/bin/jupyter lab --notebook-dir=/opt/notebooks --ip=\'*\' --port=8888 --no-browser --allow-root"\n```\n\n## License\n\nCopyright &copy; 2019-2020 Felix Soubelet. [MIT License][license]\n\n[black_formatter]: https://github.com/psf/black\n[docker_cp_doc]: https://docs.docker.com/engine/reference/commandline/cp/\n[gitflow_ref]: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow\n[git_ref]: https://git-scm.com/\n[license]: https://github.com/fsoubelet/PyhDToolkit/blob/master/LICENSE\n[oci_ref]: https://www.opencontainers.org/\n[pep_518_ref]: https://www.python.org/dev/peps/pep-0518/\n[poetry_ref]: https://github.com/python-poetry/poetry\n[pylint_ref]: https://www.pylint.org/\n[tini_ref]: https://github.com/krallin/tini\n',
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@cern.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/PyhDToolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

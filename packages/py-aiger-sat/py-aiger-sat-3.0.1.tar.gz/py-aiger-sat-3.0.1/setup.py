# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_sat']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0',
 'py-aiger-cnf>=5.0.0,<6.0.0',
 'py-aiger>=6.0.0,<7.0.0',
 'python-sat>=0.1.5,<0.2.0']

extras_require = \
{'bitvector': ['py-aiger-bv>=4.0.0,<5.0.0']}

setup_kwargs = {
    'name': 'py-aiger-sat',
    'version': '3.0.1',
    'description': 'Pythonic interface between AIGs and SAT solvers.',
    'long_description': "# py-aiger-sat\nPythonic interface between AIGs and SAT solvers.\n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-sat/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-sat)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-sat/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-sat)\n[![PyPI version](https://badge.fury.io/py/py-aiger-sat.svg)](https://badge.fury.io/py/py-aiger-sat)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->\n**Table of Contents**\n\n- [Installation](#installation)\n- [Usage](#usage)\n\n<!-- markdown-toc end -->\n\n\n# Installation\n\nIf you just need to use `aiger_sat`, you can just run:\n\n`$ pip install py-aiger-sat`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\n`aiger_sat` has two seperate API's. The first, called the Object API,\ncenters around the `SolverWrapper` object - a thin wrapper around a\n`pysat` solver. The second is a Function API which exposes 4 functions\n`solve`, `is_sat`, `is_valid`, and `are_equiv`. The function API is\nprimarily useful for simple 1-off SAT instances, where as the object\nAPI is more useful when incremental solves are needed, or the\nunderlying `pysat` solver must be exposed.\n\n## Object API\n\n```python\nfrom aiger_sat import SolverWrapper\n\nsolver = SolverWrapper()  # defaults to Glucose4\n\nfrom pysat.solvers import Glucose3\nsolver2 = SolverWrapper(solver=Glucose3)\n```\n\n`solver` operate on boolean expressions in the form of `aiger`\ncircuits with a single output. For example,\n\n\n```python\nimport aiger\n\nx, y, z = map(aiger.atom, ['x', 'y', 'z'])\n\nexpr = (x & y) | ~z\nsolver.add_expr(expr)\nassert solver.is_sat()\nmodel = solver.get_model()\nprint(model)  # {'x': True, 'y': False, 'z': False}\nassert expr(model)\n```\n\nFurther, `aiger_sat` supports making assumptions and computing\nunsat_cores.\n\n```python\n# Make invalid assumption.\nassert not solver.is_sat(assumptions={\n    'x': False,\n    'z': True,\n})\nassert not solver.unsolved\n\ncore = solver.get_unsat_core()\nassert core == {'x': False, 'z': True}\n```\n\n## Function API\n\n```python\nimport aiger\nimport aiger_sat\n\nx, y, z = map(aiger.atom, ['x', 'y', 'z'])\nassert aiger_sat.is_sat(x & y & z)\n\nmodel = aiger_sat.solve(x & y & z)\nassert model == {'x': True, 'y': True, 'z': True}\n\nassert aiger_sat.is_valid(aiger.atom(True))\n\nexpr1 = x & y\nexpr2 = x & y & (z | ~z)\nassert aiger_sat.are_equiv(expr1, expr2)\n```\n\n## BitVector Support\n\n`py-aiger-sat` also natively supports the `py-aiger-bv` bitvector\nlibrary.\n\nTo enable this support, make sure that `py-aiger-bv` is installed,\neither manually:\n\n`$ pip install py-aiger-bv`\n\nor by installing `py-aiger-sat` with the `bitvector` option:\n\n`$ pip install py-aiger-sat[bitvector]` or `$ poetry install --extras=bitvector`\n\nUsage is analogous to the non-bitvector usage.\n\n```python\nfrom aiger_bv import atom\nfrom aiger_sat import sat_bv\n\n# Object API\nexpr = atom(4, 'x') & atom(4, 'y') < 2\nf = sat_bv.SolverBVWrapper()\nf.add_expr(expr)\n\nmodel = f.get_model()\n\n# Function API.\nmodel = sat_bv.solve(expr)\n\nprint(model)\n# {'x': (False, False, True, True), 'y': (False, False, True, True)}\n```\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-aiger-sat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

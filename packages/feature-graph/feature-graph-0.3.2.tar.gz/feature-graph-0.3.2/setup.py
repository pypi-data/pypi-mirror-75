# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feature_graph']

package_data = \
{'': ['*']}

install_requires = \
['SqliteDict>=1.6.0,<2.0.0',
 'google-cloud-bigquery>=1.25.0,<2.0.0',
 'graphviz>=0.14.1,<0.15.0',
 'loguru>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'feature-graph',
    'version': '0.3.2',
    'description': 'A simple DAG orchestrator built specifically for machine learning feature generation',
    'long_description': '<h1 align="center" style="background-color:#f64e8b;">\n  <a href="https://https://github.com/mvanwyk/feature_graph"><img src="./logo.png" title="Feature Graph" alt="Feature Graph"></a>\n</h1>\n\n\n# Feature Graph\n\n## A simple DAG orchestrator built specifically for machine learning feature generation\n\n\n\n[![Build Status](https://travis-ci.org/mvanwyk/feature_graph.svg?branch=master)](https://travis-ci.org/mvanwyk/feature_graph)[![Coverage Status](https://coveralls.io/repos/github/mvanwyk/feature_graph/badge.svg?branch=master)](https://coveralls.io/github/mvanwyk/feature_graph?branch=master)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![Linter: flake8](https://img.shields.io/badge/linter-flake8-yellow)](https://gitlab.com/pycqa/flake8)[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)\n\n\nFeature Graph is an easy to use feature generation framework\n\n- **Only orchestration** - Simplifies code by separating orchestration from the heavy lifting of data processing\n- **No cluster required** - No complex and expensive to run infrastructure\n- **Compose features as a graph (DAG)** - Creating features atomically is inefficient. Creating them in a single step is complex and fragile. Feature Graph simplifies things by allowing you to break feature creation into steps (or nodes) and composable graph. The execution engine will then execute the graph taking in account any dependencies.\n- **Intelligent graph execution** - Re-running a DAG will only re-run those which have changed\n\n<!-- **Recordit**\n\n![Recordit GIF](http://g.recordit.co/iLN6A0vSD8.gif) -->\n\n<!-- ## Back story\n\n- Orchestrator and processing infrastructure tightly coupled so complex to setup\n- A lot of data pipelines tailored around flexibility for things like image processing but more business data is still in good old fashion databases\n- Tried moving feature creation to pandas and pyspark but after countless hours of tuning and tinkering BigQuery was able to process the data much more quickly, at a lower cost and with a lot less code - the only problem is that SQL isn\'t the nicest language to build complex data pipelines with\n- There are tools to do this but I wanted something simple and efficient\n- Don\'t need heavy weight orchestrator when using managed services -->\n\n---\n\n## Table of Contents\n\n- [Installation](#installation)\n- [Features](#features)\n- [Documentation](#documentation)\n- Contributing (coming soon)\n- FAQ (coming soon)\n- [License](#license)\n- [Acknowledgements](#acknowledgements)\n\n\n---\n\n## Installation\n\n- Required python >=3.7\n- To render the DAG diagrams you will also need graphviz installed ([download page](https://www.graphviz.org/download/))\n\n```shell\n$ pip install feature-graph\n```\n\n---\n\n## Features\n\n### Basic example\n\n```python\nwith FeatureDAG(dag_params={"project": "my_project"}) as dag:\n\n  base_query = BigQueryNode(name="Base Query", query_file="base_query.sql")\n  feat_query_1 = BigQueryNode(name="Feat Query 1", query_file="feat_query_1.sql")\n  final_query = BigQueryNode(name="Final Query", query_file="final_query.sql")\n\n  base_query >> feat_query_1\n  [feat_query_1, base_query] >> final_query\n\ndag.run_feature_graph()\n```\n\n\n### Display a DAG diagram\n\n```python\n\nwith FeatureDAG():\n\n  base_query = BigQueryNode(\n    name="Base Query", query_file="base_query.sql", project="my-project"\n  )\n  ...\n\n  dag.print_graph()\n```\n\n![Sample of graph image generated](sample_graph.png)\n\n### Save/load DAG state\n\n```python\n\nwith FeatureDAG(state_db="my_state.db") as dag:\n\n  base_query = BigQueryNode(\n    name="Base Query", query_file="base_query.sql", project="my-project"\n  )\n  ...\n\ndag.run_feature_graph()\n```\n\n### Intelligently re-run a graph\n\n```python\n\nwith FeatureDAG(state_db="my_state.db") as dag:\n\n  base_query = BigQueryNode(\n    name="Base Query",\n    query_file="base_query.sql",\n    project="my-project",\n    # The tables base_query.sql relies upon\n    input_tables = ["my_dataset.my_table", "my_dataset.my_other_table"]\n  )\n  ...\n\n# The next The node base_query will re-run if the contents of `base_query.sql` change\n# or if one or more of the input tables have been modified since the last time the DAG\n# was run.\ndag.run_feature_graph()\n\n```\n\n## Documentation\n\n> Better documentation coming. Check the docstrings for now\n\n---\n\n## Roadmap\n\nv0.3.0\n\n- [x] Improved safety checks to avoid loops in DAGs\n- [x] Stateful DAG running - Store the state of the last run in the DAG and only re-run those parts that have changes\n- [x] BigQueryNode load query from file\n- [x] Improved docstrings\n- [x] Complete README.md\n\nv0.4.0\n\n- [ ] Docstring coverage monitoring w/badge\n- [ ] Image of nodes that were run in when calling `run_feature_graph()`\n- [ ] Image of node cache state (stale/fresh)\n- [ ] Load/export DAG to yaml file\n- [ ] Create nodes outside of a FeatureDAG context manager\n\nv0.5.0\n\n- [ ] CLI\n- [ ] More node types\n- [ ] Template node example\n- [ ] Read the docs\n\nv0.6.0\n\n- [ ] Streaming feature generation support\n\n---\n\n## License\n\n[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)\n\n- **[MIT license](http://opensource.org/licenses/mit-license.php)**\n- Copyright 2019 © <a href="https://github.com/mvanwyk/" target="_blank">Murray Vanwyk</a>.\n\n---\n\n## Acknowledgements\n- Readme template - https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46\n- Implementation style - https://diagrams.mingrammer.com/\n',
    'author': 'Murray Vanwyk',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvanwyk/feature_graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

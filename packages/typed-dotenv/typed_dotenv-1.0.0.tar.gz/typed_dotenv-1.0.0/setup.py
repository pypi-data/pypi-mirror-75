# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_dotenv']

package_data = \
{'': ['*']}

install_requires = \
['parse>=1.16.0,<2.0.0', 'python-dotenv>=0.14.0,<0.15.0']

extras_require = \
{'all': ['ruamel.yaml>=0.16.10,<0.17.0',
         'pydantic>=1.6.1,<2.0.0',
         'toml>=0.10.1,<0.11.0'],
 'pydantic': ['pydantic>=1.6.1,<2.0.0'],
 'toml': ['toml>=0.10.1,<0.11.0'],
 'yaml': ['ruamel.yaml>=0.16.10,<0.17.0']}

setup_kwargs = {
    'name': 'typed-dotenv',
    'version': '1.0.0',
    'description': 'Handle .env files with types',
    'long_description': '# typed_dotenv\n\nParse .env files with types\n\n## Installation\n\n```shell\npip install typed_dotenv\n```\n\nTo use...\n\n- **[`load_into`](#the-recommended-way-using-pydantics-basemodel-with-load_into)**: `pip install typed_dotenv[pydantic]`\n- **YAML literals**: `pip install typed_dotenv[yaml]`\n- **TOML literals**: `pip install typed_dotenv[toml]`\n\n## Usage\n\nWith the following `.env` file:\n\n```bash\nGITHUB_TOKEN="jkjkimnotputtinmygithubpersonaltokeninamodulesexamples"\nDEBUG_IN_PRODUCTION=False\n```\n\n```python\nimport typed_dotenv\n\nsecrets = typed_dotenv.load(".env")\n```\n\nYou\'ll see here that nothing has changed much: `secrets[\'DEBUG_IN_PRODUCTION\']` is still a `str`.\n\nThat\'s because you need to explicitly define what syntax your .env uses.\nAdd the following at the top of your `.env`:\n\n```bash\n# values: python\nGITHUB_TOKEN="jkjkimnotputtinmygithubpersonaltokeninamodulesexamples"\nDEBUG_IN_PRODUCTION=False\n```\n\nNow the following will not raise an assertion error:\n```python\nimport typed_dotenv\n\nsecrets = typed_dotenv.load() # ".env" is the default value\nassert type(secrets["DEBUG_IN_PRODUCTION"]) is bool\n```\n\nWe used python-style values, but other syntaxes are available:\n\n- `values: yaml 1.2` to use YAML 1.2 literals<sup>`pip install typed_dotenv[yaml]`</sup>\n- `values: yaml 1.1` to use YAML 1.1 literals ([differences from YAML 1.2](https://yaml.readthedocs.io/en/latest/pyyaml.html#defaulting-to-yaml-1-2-support)). **For now, this has the same effect as `values: yaml 1.2`**<sup>`pip install typed_dotenv[yaml]`</sup>\n- `values: toml` to use TOML literals: `12:35:24` resolves to a `datetime.time`, etc.<sup>`pip install typed_dotenv[toml]`</sup>\n- `values: json` to use JSON literals\n\nNow, up until now, we\'ve only seen how to get those variables into a `dict`.\n\n### The recommended way: using Pydantic\'s `BaseModel` with `load_into`\n\nThis way, you have IDE autcompletion and type checking, and pydantic will raise errors if the value is not of the right type:\n\n```python\nfrom pydantic import BaseModel\nimport typed_dotenv\n\nclass Secrets(BaseModel):\n    GITHUB_TOKEN: str\n    DEBUG_IN_PRODUCTION: bool\n\nsecrets = typed_dotenv.load_into(Secrets, filename="my_dotenv.env")\n```\n\n### Using with `os.getenv`\n\nYou might still want to load these values as environment variables, but need to get type coersion. This time, since the value is gotten via `os.getenv`, _typed_dotenv_ does not know the file\'s contents. The syntax used is thus declared when coercing types:\n\n```python\nfrom os import getenv\nimport typed_dotenv\n\nprint(os.getenv("MY_ENV_VARIABLE"))\nprint(\n    typed_dotenv.coerce(\n        os.getenv("MY_ENV_VARIABLE"),\n        typed_dotenv.VALUE_FORMATS.python_literal\n    )\n)\n```\n\nYou can also make yourself a function to avoid declaring the values\' format each time:\n\n```python\ndef env_coerce(key: str) -> Any:\n    return typed_dotenv.coerce(\n        os.getenv(key),\n        typed_dotenv.VALUE_FORMATS.python_literal\n    )\n```\n\nAnd use it like so:\n\n```python\nprint(env_coerce("MY_ENV_VARIABLE"))\n```\n',
    'author': 'Ewen Le Bihan',
    'author_email': 'hey@ewen.works',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ewen-lbh/python-typed-dotenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

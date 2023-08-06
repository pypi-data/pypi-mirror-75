# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cloudauth']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.60.1,<0.61.0',
 'python-jose>=3.2.0,<4.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'fastapi-cloudauth',
    'version': '0.1.0',
    'description': 'fastapi-cloudauth supports simple integration between FastAPI and cloud authentication services (AWS Cognito, Auth0).',
    'long_description': '# FastAPI Cloud Auth\n\n![Tests](https://github.com/tokusumi/fastapi-cloudauth/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/tokusumi/fastapi-cloudauth/branch/master/graph/badge.svg)](https://codecov.io/gh/tokusumi/fastapi-cloudauth)\n\nfastapi-cloudauth supports simple integration between FastAPI and cloud authentication services (AWS Cognito, Auth0). This standardize the interface for some authentication services.\n\n## Features\n\n* [X] Verify access/id token\n* [X] Authenticate permission based on scope (or groups) within access token \n* [X] Get login user info (name, email, etc.) within ID token\n* [X] Dependency injection for verification/getting user, powered by [FastAPI](https://github.com/tiangolo/fastapi)\n* [X] Support for:\n    * [X] [AWS Cognito](https://aws.amazon.com/jp/cognito/)\n    * [X] [Auth0](https://auth0.com/jp/)\n    * [ ] [Firebase Auth]()\n\n## Requirements\n\nPython 3.6+\n\n## Example (AWS Cognito)\n\n### Pre-requirement\n\n* Check `region` and `userPoolID` of AWS Cognito that you manage to\n* Create a user assigned `read:users` permission in AWS Cognito \n* Get Access/ID token for the created user\n\nNOTE: access token is valid for verification and scope-based authentication. ID token is valid for verification and getting user info.\n\n### Create it\n\nCreate a file main.py with:\n\n```python3\nimport os\nfrom fastapi import FastAPI, Depends\nfrom fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims\n\napp = FastAPI()\nauth = Cognito(region=os.environ["REGION"], userPoolId=os.environ["USERPOOLID"])\n\n\n@app.get("/", dependencies=[Depends(auth.scope("read:users"))])\ndef secure():\n    # access token is valid\n    return "Hello"\n\n\nget_current_user = CognitoCurrentUser(\n    region=os.environ["REGION"], userPoolId=os.environ["USERPOOLID"]\n)\n\n\n@app.get("/user/")\ndef secure_user(current_user: CognitoClaims = Depends(get_current_user)):\n    # ID token is valid\n    return f"Hello, {current_user.username}"\n```\n\nRun the server with:\n\n```console\n$ uvicorn main:app\n\nINFO:     Started server process [15332]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\nINFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)\n```\n\n### Interactive API Doc\n\nGo to http://127.0.0.1:8000/docs.\n\nYou will see the automatic interactive API documentation (provided by Swagger UI).\n\n`Authorize` :unlock: button can be available at the endpoints injected dependency.\n\nYou can put token and try endpoint interactively.\n\n![Swagger UI](https://raw.githubusercontent.com/tokusumi/fastapi-cloudauth/master/docs/src/authorize_in_doc.jpg)\n\n',
    'author': 'tokusumi',
    'author_email': 'tksmtoms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tokusumi/fastapi-cloudauth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

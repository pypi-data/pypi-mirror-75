# Panoramic Auth SDK

## Getting Started

This SDK handles the access token generation using client_credentials flow against Panoramic. To install the SDK in your app, add it to your requirements.txt:

    panoramic-auth==1.0.0

All you then need to do is subclass the OAuth2Client Python class from the SDK, pass your client_id and client_secret, and use the session attribute from your subclass when making HTTP requests:

```py
# Import the class as usual
from panoramic.auth import OAuth2Client

# Note subclassing OAuth2Client below
class PanoramicApiClient(OAuth2Client):
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        super().__init__(client_id, client_secret)
        self.base_url = base_url
   
    def async_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        url = urljoin('https://platform.panoramichq.com/api/example')
        # Note self.session below
        response = self.session.post(url=url, json=data)
        response.raise_for_status()
        return response.json()
```

## Development

This repository does not have a dedicated docker image. At the moment, we create python virtual environment using command (in directory `.venv` inside current directory):

```
> python3 -m venv .venv
```

If you use pyenv and pyenv-virtualenv, you can create it using:

```
> pyenv virtualenv panoramic-auth
```

Then, you can switch to it from command-line using following command:

```
> source .venv/bin/activate
```

Or if using pyenv-virtualenv:

```
pyenv local panoramic-auth
```

Lastly, use following command to install dependencies (make sure you have correct python environment active):

```
> make install
```

Install pre-commit - useful to avoid commiting code that doesn't pass the linter:

```
> make pre-commit-install
```

This installs git hooks that run pre-commit.

## Tests

Use following command to run all tests:

```
> make tests
```

## Release process

To release a new version of the library, follow these steps:

* In your PR, update version in [setup.py](setup.py) and add entry to [CHANGELOG.md](CHANGELOG.md)
* After merge, tag the commit with version number from setup.py. For example `git tag v0.1.1`. You can also do this by creating a new [release](https://github.com/panoramichq/panoramic-auth-py/releases).
* This triggers a Travis pipeline which runs tests, linters and uploads the package to [PyPI]()

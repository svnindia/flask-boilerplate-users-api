# flask-boilerplate-users-api

Flask Based API implementation for User Register, login, Profile View, Profile update

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash

pip3 install -r requirements.txt

```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to maintain requirements.
```bash

pip3 freeze > requirements.txt

```
## Usage

```
[POST]
http://127.0.0.1:5000/register
{
	"username": "user1",
	"email":"user1@xyz.com",
	"password": "12345678"
}

[POST/GET]
http://127.0.0.1:5000/me
{
	"username": "user1",
	"password": "12345678",
	"email": "user1@xyz.com",
	"firstName": "a",
	"lastName": "abcde",
	"mobile": "12345678",
	"activated": 1
}

[POST]
http://127.0.0.1:5000/login
{
	"username": "user1",
	"password": "12345678"
}

```

## Contributing
This can be used as a base code for flask [python framework] based api implementation

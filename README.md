# falcon
`Python 3.6.4`

## Installation
`$ pip install -r requirements.txt`

## Run server
`$ gunicorn api_v2:api --reload`

## Usage
#### Persons
```
# Valid requrests
http GET 0.0.0.0:8000/persons
http POST 0.0.0.0:8000/persons id=6 name='Kate'

# Bad request
http POST 0.0.0.0:8000/persons name='Kate'
```

#### Person with ID
```
# Valid requrests
http GET 0.0.0.0:8000/persons/1
http PUT 0.0.0.0:8000/persons/1 name='Alan'
http DELETE 0.0.0.0:8000/persons/4

# Bad request
http PUT 0.0.0.0:8000/persons/1 nothing='Nothing'

# Not found requests
http GET 0.0.0.0:8000/persons/9999
http PUT 0.0.0.0:8000/persons/9999 name='Alan'
```

#### Person hobbies
```
# Valid requests
http GET 0.0.0.0:8000/persons/1/hobbies
http DELETE 0.0.0.0:8000/persons/1/hobbies hobby='diving'
http POST 0.0.0.0:8000/persons/1/hobbies hobby='haxball'
http POST 0.0.0.0:8000/persons/4/hobbies hobby='haxball'

# Bad requests
http GET 0.0.0.0:8000/persons/4/hobbies

# Not found requests
http GET 0.0.0.0:8000/persons/9999/hobbies
http DELETE 0.0.0.0:8000/persons/1/hobbies hobby='non existing hobby'
http DELETE 0.0.0.0:8000/persons/9999/hobbies hobby='diving'
```
<a name="lcs_client"></a>
# lcs\_client

This is intended to be a server-side client to help with HackRU services that piggyback on lcs login and user data

<a name="lcs_client.set_root_url"></a>
#### set\_root\_url

```python
set_root_url(url: str) -> None
```

Sets root url. defaults to `https://api.hackru.org`

<a name="lcs_client.set_testing"></a>
#### set\_testing

```python
set_testing(testing: bool) -> None
```

Whether or not to use test endpoint, defaults to `False`

<a name="lcs_client.User"></a>
## User Objects

```python
class User()
```

A user object to easily call other endpoints on behalf of a user

<a name="lcs_client.User.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(email: str = None, password: str = None, token: str = None) -> None
```

Constructor logs the user and gets a handle. Requires you to pass a token OR an email and password

<a name="lcs_client.User.profile"></a>
#### profile

```python
 | profile() -> Dict
```

Call lcs to get the user's profile

<a name="lcs_client.User.create_dm_link_to"></a>
#### create\_dm\_link\_to

```python
 | create_dm_link_to(other_user_email: str)
```

Get a link to a slack DM between this User and another user identified by `other_user_email`

<a name="lcs_client.ResponseError"></a>
## ResponseError Objects

```python
class ResponseError(Exception)
```

Error with an attached HTTP Response

<a name="lcs_client.InternalServerError"></a>
## InternalServerError Objects

```python
class InternalServerError(ResponseError)
```

An error occurred which prevented LCS from servicing the request

<a name="lcs_client.RequestError"></a>
## RequestError Objects

```python
class RequestError(ResponseError)
```

Ideally you shouldn't receive this. There was an issue with the input to the API

<a name="lcs_client.CredentialError"></a>
## CredentialError Objects

```python
class CredentialError(RequestError)
```

There was an issue login in with that credential, or a token is invalid

<a name="lcs_client.on_login"></a>
#### on\_login

```python
on_login(fn: Callable)
```

Decorator. Call the decorated function whenever we find a new user
Use case: get their profile and update local db.
Function should take in the user object as the first param

```python
@lcs_client.on_login
def your_func(user_profile):
    # updating the user profile or something
```

<a name="lcs_client.login"></a>
#### login

```python
login(email: str, password: str) -> str
```

Gets an authentication token by calling the `authorize` LCS endpoint

<a name="lcs_client.validate_token"></a>
#### validate\_token

```python
validate_token(token: str) -> Dict
```

Validates a lcs token

<a name="lcs_client.get_profile"></a>
#### get\_profile

```python
get_profile(auth_token: str, user_email: str = None) -> Dict
```

Gets the profile of a user associated with user_email. The permissions associated with the auth_token user are used.
If no user_email is specified or the user doesn't have enough privilege to view someone else's profile,
the profile associated with the auth_token is fetched

<a name="lcs_client.create_dm_link_between"></a>
#### create\_dm\_link\_between

```python
create_dm_link_between(token: str, other_user_email: str) -> str
```

Get a dm link to talk with another user on slack

<a name="lcs_client.get_base_url"></a>
#### get\_base\_url

```python
get_base_url() -> str
```

Get the LCS base url

<a name="lcs_client.get"></a>
#### get

```python
get(endpoint: str, *args, **kwargs) -> requests.models.Response
```

Performs a GET request to a LCS endpoint

<a name="lcs_client.post"></a>
#### post

```python
post(endpoint: str, *args, **kwargs) -> requests.models.Response
```

Performs a POST request to a LCS endpoint


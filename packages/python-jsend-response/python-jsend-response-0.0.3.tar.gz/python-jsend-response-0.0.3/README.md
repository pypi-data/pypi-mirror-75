# Description

python-jsend-response is a simple implementation of [JSend](https://github.com/omniti-labs/jsend).

JSend is a specification that lays down some rules for how JSON responses from web servers should be formatted. JSend focuses on application-level (as opposed to protocol- or transport-level) messaging which makes it ideal for use in REST-style applications and APIs.:

You'll have all kinds of different types of calls and responses. JSend separates responses into some basic types, and defines required and optional keys for each type:

<table>
<tr><th>Type</td><th>Description</th><th>Required Keys</th></tr>
<tr><td>success</td><td>All went well, and (usually) some data was returned.</td><td>status, data</td></tr>
<tr><td>failure</td><td>There was a problem with the data submitted, or some pre-condition of the API call wasn't satisfied</td><td>status, data</td></tr>
<tr><td>error</td><td>An error occurred in processing the request, i.e. an exception was thrown</td><td>status, message</td></tr>
</table>

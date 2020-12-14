# List Events

One of the simplest examples of using ReadyUp's DataAPI is listing the events of your organization.  There are two examples here of how to do that - one with Python and one with cURL.

Both examples require a API Token for your organzation.  That token can be obtained through the ReadyUp Admin UI.

### Python

The example makes use of Python 3.7 with the [Poetry](https://python-poetry.org/) package manager.  Before you run the example the first time you will want to install dependendcies using

```bash
poetry install
```

After that you can inspect the code in `list_events.py` and run with with:

```bash
READYUP_TOKEN=[token] poetry run list-events
```

### cURL

To retrieve the first page of 25 events using cURL, and then output the result in a 'pretty' format you can run:

```bash
curl -H "Authorization: readyup [token]" -X GET https://api.readyup.com/v1/events | json_pp
```

To get additional pages (or use a larger page size) you can provide query parameters to the request.  For example, to retieve the
first 51 events using cURL you can run:

```bash
curl -H "Authorization: readyup [token]" -X GET https://api.readyup.com/v1/events?pageSize=51 | json_pp
```

# Python Examples

The example makes use of Python 3.7+ with the [Poetry](https://python-poetry.org/) package manager.  Before you run the example the first time you will want to install dependencies using

```bash
poetry install
```

_All examples require an API Token for your organization._

Details about how to acquire an API Token can be found in our [quick start guide](https://web-dev.readyup.engineering/developer/documentation/#section/Quickstart-Guide)

## List Events

One of the simplest examples of using the ReadyUp API is listing the events of your organization.  The code is in `list_events.py` and it can be run like:

```bash
READYUP_TOKEN=[token] poetry run list-events
```

The same thing can be accomplished with cURL commands.

To retrieve the first page of 25 events using cURL, and then output the result in a 'pretty' format you can run:

```bash
curl -H "Authorization: readyup [token]" -X GET https://api.readyup.com/v1/events | json_pp
```

To get additional pages (or use a larger page size) you can provide query parameters to the request.  For example, to retieve the
first 51 events using cURL you can run:

```bash
curl -H "Authorization: readyup [token]" -X GET https://api.readyup.com/v1/events?pageSize=51 | json_pp
```

## Create Events

The code in `create_events.py` demonstrates how to create events with the ReadyUp API.  It makes use of a CSV file under the `data` folder to define the events to create in the system.  It can be run like:

```bash
READYUP_TOKEN=[token] poetry run create-events
```

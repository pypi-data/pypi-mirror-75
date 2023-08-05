# Crono API Client

Python client for the 🔮 Crono API: https://crono.com/

```python
>>> import crono_api_client as crono
>>> crono.request('POST', https://your.app/').after(hours=42)
```

## How to

Install package:
```console
$ pip install crono_api_client
```

Configure `.env` variables:
```
CRONO_API_URL=… 
CRONO_API_KEY=…
```

Get all jobs:
```python
>>> job_uuids = crono.jobs()
```

Get a job:
```python
>>> job_json = crono.job(<string:job_uuid>)
```

Schedule a job:
```python
>>> job_uuid = crono.<task>(<args>, <kwargs>).<trigger>(<args>, <kwargs>)
>>> # or
>>> job_uuid = crono.<trigger>(<args>, <kwargs>).<task>(<args>, <kwargs>)
```

Delete a job:
```python
>>> job_uuid = crono.delete(<string:job_uuid>)
```

## Development

Packaging

```console
# Generating distribution archives
$ python setup.py sdist bdist_wheel

# Uploading the distribution archives
$ twine upload --skip-existing dist/*
```

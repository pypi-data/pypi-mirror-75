# django-db-queue-exports

**An extension to [django-db-queue](https://github.com/dabapps/django-db-queue) for monitoring long running task statuses.
The aim of this extension is to simplify the execution of long running tasks, and allow for polling of tasks statuses during execution.**

[![Build Status](https://travis-ci.com/dabapps/django-db-queue-exports.svg?token=gFw2G3a8PohgNBo8f8Nm&branch=master)](https://travis-ci.com/dabapps/django-db-queue-exports)
[![pypi release](https://img.shields.io/pypi/v/django-db-queue-exports.svg)](https://pypi.python.org/pypi/django-db-queue-exports)

Supported and tested against:
- Django 2.2
- django-db-queue 1.3.0
- Python 3.6, 3.7 and 3.8

## What and why?
Have you ever been in a position where you need to run a report, or email several thousand users without blocking your main process? `django-db-queue` can handle this perfectly for you through the use of a seperate `worker` process and a queue of `tasks`. However, it's difficult to determine the state of your task. This package aims to address this. Through the use of a pre-configured view, url and generic task, you can use a single endpoint to create new exports and query their statuses.

## Getting started
### Installation
```
pip install django-db-queue-exports
```
Add `django_dbq_exports` to the installed apps, found inside your settings.py
```
INSTALLED_APPS = (
    ...
    'django_dbq_exports',
)
```
Add `django_dbq_exports.tasks.export_task` to django-dbq JOBS list in settings.py
```
JOBS = {
    ...
    'export': {
        'tasks': ['django_dbq_exports.tasks.export_task'],
    },
}
```
Configure the url, something like this:
```
urlpatterns = [
    ...
    url(r'^export/', include("django_dbq_exports.urls")),
]
```
Remember to run your migrations
```
python manage.py migrate
```
## Usage
### Describing your export
An `export` is a standard python function. It must take an `export_params` dictionary parameter. This can be utilised for any parameters required within your export.
The export can also optionally return a string value which will be stored in `Export.result_reference`. This is best used for file paths or URLs when you need to download or access the results of the export.
Here's an example task:
```
import random

def generate_example_report(export_params):
    output_file = 'myfile.csv'
    array_length = export_params.get("length", None)
    x = []

    for i in range(array_length if array_length else 99):
        x.append(random.randint(1, 10))

    x.sort()
    with open(output_file, 'w') as f:
        f.write(",".join(str(y) for y in x))

    return output_file
```

Configure your task in settings.py
```
EXPORTS = {
    "my_export": "my_project.tasks.generate_example_report",
}
```

### Running the task
Simply `POST` to the pre-configured endpoint with the following json.
The `export_type` should map to a configured key within the `settings.EXPORTS` dictionary.
```
{
    "export_type" : "my_export"
} 
```
With optional parameters to be received by your previously created export task
```
{
    "export_type" : "my_export",
    "export_params" : {
        "length": 256
    }
}
```
### Querying the task status
`GET` the same endpoint with a url parameter = to the export `id` field returned from the POST request.
Or `GET` the same endpoint with no parameters to return a list of all exports.


### Creating a custom view
If you don't wish to use the built in views and urls to trigger exports, create your own! To trigger an export yourself simply create an export object like so:
```
Export.objects.create(export_type="my_export")
```
The newly created export object will handle the `django-db-queue` job creation. 

### Overriding priority
By default all exports will be created with a priority of 1. This is passed through to `django-db-queue`. If you wish to override this you can do so via the POST method.
```
{
    "export_type" : "my_export",
    "priority" : 3
} 
```
Or through the Export creation directly.
```
Export.objects.create(export_type="my_export", priority=3)
```

## Code of conduct

For guidelines regarding the code of conduct when contributing to this repository please review [https://www.dabapps.com/open-source/code-of-conduct/](https://www.dabapps.com/open-source/code-of-conduct/)
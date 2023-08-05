# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amplitude']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.1', 'httpx>=0.13.2,<0.14.0', 'user-agents>=2.1,<3.0']

setup_kwargs = {
    'name': 'django-amplitude',
    'version': '0.5.0',
    'description': 'Integration between Django and Amplitude',
    'long_description': "# Django Amplitude\n\nIntegration between Django and [Amplitude.com](https://amplitude.com/) to help send events via the [Amplitude HTTP API (v2)](https://developers.amplitude.com/docs/http-api-v2)\n\n\n## Quick start\n\n### Installation\n\n```bash\npip install django-amplitude\n```\n\nAdd `amplitude` to your `INSTALLED_APPS`. If they are not already the Django `sessions` app must also be added:\n\n```python\nINSTALLED_APPS = [\n    ...\n    'django.contrib.sessions',\n    ...\n    'amplitude',\n]\n```\n\nIf you do not have it already you must also add the Django `django.contrib.sessions.middleware.SessionMiddleware`. Then add the ampliturde `SessionInfo` middleware after the `SessionMiddleware`:\n```python\nMIDDLEWARE = [\n    ...\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    ...\n    'amplitude.middleware.SessionInfo',\n]\n```\n\nNow set your Amplitude API key and user / group options in your `settings.py`:\n```python\n# Settings > Projects > <Your project> > General > API Key\nAMPLITUDE_API_KEY = '<amplitude-project-api-key>'\n\n# You can also choose if you want to include user and group data (Default False)\nAMPLITUDE_INCLUDE_USER_DATA = False\nAMPLITUDE_INCLUDE_GROUP_DATA = False\n```\n\n*Note: If you want to include user or group data you must ensure the [Django auth is setup correctly](https://docs.djangoproject.com/en/3.0/topics/auth/#installation). This includes adding `django.contrib.auth` and `django.contrib.contenttypes` to `INSTALLED_APPS` and `django.contrib.auth.middleware.AuthenticationMiddleware` to `MIDDLEWARE`*.\n\n\n## Usage\n\n### Page view events\n\nIf you want to send an event to Amplitude on every page view you can use the django-amplitude `SendPageViewEvent` middleware to your `MIDDLEWARE` in your Django settings.\n\nThis will automatically create an event called `Page view` with all the information it's possible to pull from the Django request object such as URL path and parameters, user agent info, IP info, user info etc.\n\nIt must be placed after the `amplitude.middleware.SessionInfo` middleware:\n\n```python\nMIDDLEWARE = [\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    ...\n    'amplitude.middleware.SessionInfo',\n    'amplitude.middleware.SendPageViewEvent',\n]\n```\n\n\n### Sending events manually\n\nIf you want to send your own events:\n```python\nfrom amplitude import Amplitude\n\namplitude = Amplitude()\nevent_data = amplitude.build_event_data(\n    event_type='Some event type',\n    request=request,\n)\namplitude.send_events([event_data])\n```\n\nThe above request will include URL and HTTP header info in the `event_properties`. If you want to override the event properties you can pass them through to `build_event_data`:\n\n```python\nevent_data = amplitude.build_event_data(\n    event_type='User purchase',\n    request=request,\n    event_properties={'products': ['laptop', 'phone']}\n)\n```\n\n### build_event_data missing event data keys\n\nThe `build_event_data` method (and in extension the `SendPageViewEvent` middleware) currently does not send the following keys from `UploadRequestBody` type in [Amplitude HTTP API (v2)](https://developers.amplitude.com/docs/http-api-v2):\n\n* event_id\n* app_version\n* carrier\n* price\n* quantity\n* revenue\n* productId\n* revenueType\n* idfa\n* idfv\n* adid\n* android_id\n* dma\n* insert_id\n\nIf you want to record an event in Amplitude with any of these keys you must use build and send your own event data using `amplitude.build_event_data` where you can pass any of the above as kwargs:\n\n```python\namplitude = Amplitude()\nevent_data = amplitude.build_event_data(\n    event_type='Some event type',\n    request=request,\n    app_version='1.0.0',\n)\namplitude.send_events([event_data])\n```\n\n\n### Building you own event\n\nIf you are not happy with the data from `build_event_data` you can build you own event data based on the `UploadRequestBody` type in [Amplitude HTTP API (v2)](https://developers.amplitude.com/docs/http-api-v2). If you want to do this There are a few helper functions to build different parts of the event data from the Django request object:\n\n```python\namplitude.event_properties_from_request(request)  # Gets URL and HTTP header data\namplitude.device_data_from_request(request)  # Gets device info from user agent\namplitude.user_properties_from_request(request)  # Gets info from user model\namplitude.group_from_request(request)  # Gets the list of groups a user is in\n\namplitude.location_data_from_ip_address(ip_address)  # Gets location data from IP if GeoIP2 is setup\n```\n\n* `user_properties_from_request` will return an empty dict if `AMPLITUDE_INCLUDE_USER_DATA` is `False`\n* `group_from_request` will return an empty dict if `AMPLITUDE_INCLUDE_GROUP_DATA` is `False`\n",
    'author': 'Matt Pye',
    'author_email': 'pyematt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyepye/django-amplitude',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_payments_paybox']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'django-payments-paybox',
    'version': '0.1.0',
    'description': 'django-payments provider for PayBox.money',
    'long_description': '# django-payments-paybox\n\n> ⚠️⚠️⚠️ Not Ready\n> This package in development. Do not use it.\n\nThis is [django-payments](https://github.com/mirumee/django-payments) provider for [PayBox.money](https://paybox.money/).\n\n# Installation\n\n```bash\npip install django-payments-paybox\n```\n\nOr with [poetry](https://python-poetry.org/)\n\n```bash\npoetry add django-payments-paybox\n```\n\n## Dependencies\n\nThis package require next deps:\n\n- `django-payments`\n\n# Configuration example\n\nIn `settings.py` you must connect this provider\n\n```python\nPAYMENT_VARIANTS = {\n    "default": (\n        "django_payments_provider.PayboxProvider",\n        {\n            "secret": "your_secret",\n            "merchant_id": 1000000, # your merchant_id\n            "site_url": "https://your_site.dev",\n            "testing_mode": 1, # enabled by default\n        },\n    )\n}\n```\n\n# Required methods in payment model\n\n```python\nfrom payments.models import BasePayment\n\n\nclass Payment(BasePayment):\n    def get_failure_url(self):\n        return "https://your_site.dev/failure/"\n\n    def get_success_url(self):\n        return "https://your_site.dev/success/"\n\n    def get_process_url(self):\n        path = super().get_process_url()\n        return f"https://your_site.dev{path}"\n\n```\n',
    'author': 'vlzh',
    'author_email': 'vlzh@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vlzh/django-payments-paybox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

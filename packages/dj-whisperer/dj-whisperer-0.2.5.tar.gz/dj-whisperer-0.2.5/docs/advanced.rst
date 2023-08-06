Advanced Usage
==============

Django Whisperer app is highly extensible.

Callback Function
-----------------

When a callback function specified, it can be called after informing
subscribed user with response, event_type, instance and request payload.

.. code-block:: python

    import logging

    logger = logging.getLogger(__name__)

    def callback(response, event_type, instance, payload):
        logger.info('this is a sweety callback function.')
        # some other codes


Subscribing to an event with callback function is as follows:

.. code-block:: python

    import requests

    requests.post(
        url='https://your-app.com/whisperer/hooks/',
        headers={
            'Authorization': 'Token <secret-login-token>',
        },
        json={
            'event_type': 'package-created',
            'secret_key': '<secret>',
            'target_url': 'https://example.com/',
            'callback': 'foo.bar.app.callback'
        }
    )

Deliver Event Optional Parameters
---------------------------------

``deliver_event`` function optional parameters:

_async
~~~~~~

default: True

Set ``_async=False`` if you want the code to run sync

.. code-block:: python

    deliver_event(instance, 'package-created', _async=False)

event_uuid
~~~~~~~~~~

default: None

Set ``event_uuid=uuid`` if you want process with spesific WebhookEvent

.. code-block:: python

    deliver_event(
        instance,
        'package-created',
        event_uuid='d960acbe-4193-44b8-b254-df115cf6d2e7'
    )



Settings Paramaters
-------------------

    WHISPERER_REQUEST_TIMEOUT

Default: 10

If you specify a single value for the timeout, like this:

.. code-block:: python

    WHISPERER_REQUEST_TIMEOUT = 5


The timeout value will be applied to both the ``connect`` and the ``read`` timeouts.
Specify a tuple if you would like to set the values separately:

.. code-block:: python

    WHISPERER_REQUEST_TIMEOUT = (5 , 10)



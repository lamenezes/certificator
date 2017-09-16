============
Certificator
============

Event certificate generator. Currently supports CSV/JSON + Meetup integration.

--------------------
How to install (TBD)
--------------------

TBD

----------
How to use
----------

With CSV files and JSON metadata:

Certificate data (CSV):

::

    name;email
    John Doe;john@doe.com
    Jane Doe;jane@doe.com


Metdata (JSON):

::

    {
      "event_title": "Eventful event for event-driven events",
      "organizer": "Eveorg",
      "place": "Event square",
      "date": "06/06/06",
      "full_date": "June 6, 2006",
      "city": "Eventville",
      "workload": "16 hours",
      "responsible": "Eve Ent Eventson",
      "responsible_title": "Event Organizer"
    }


Generating the certificate:

.. code:: python

    from certificator import CSVCertificator

    certificator = CSVCertificator(delimiter=';', filename_format='eventful-event-{name}.pdf')
    certificator.generate()

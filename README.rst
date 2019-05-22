============
Certificator
============

Event certificate generator. Currently supports CSV/JSON + Meetup integration.

--------------
How to install
--------------

::

    pip install certificator


------------------------------------
How to use (using CLI interface)
------------------------------------

From local CSV file:

.. code:: bash

    certificator csv \
    --meta-file <your_meta_json_file.json> \
    --data-file <your_data_file.csv> \
    --template-path <your_template.html_folder_path>

From MEETUP events:

.. code:: bash

    certificator meetup <destination_path> \
    --urlname <your-meetup-urlname> \
    --event-id <meetup_event_id> \
    --meetup-api-key <your_MEETUP_API_KEY> \
    --template-path <your_template.html_folder_path>

For more options, type certificator --help


------------------------------------
Examples
------------------------------------

Inside the folder examples/ are some files to be used as examples.
To generate certificates using the data in data.csv, you can run the command

.. code:: bash

    certificator csv \
    --meta-file meta.json \
    --data-file data.csv

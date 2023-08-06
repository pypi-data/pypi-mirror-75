Yandex-Tracker-Import
========================

Description
-----------
*Yandex-Tracker-Import* -- allow you to move all your data (tickets,queues,boards,sprints, e.t.c) to another organization.

What will be imported:
 - queues
 - queue workflows
 - boards
 - sprints
 - queue components
 - issues
 - issue checklists
 - issue links
 - issue comments
 - issue files
 - comment files

Installation
------------
To install, simply run:

.. code:: bash

    pip install yandex-tracker-import


Usage
------------

.. code:: bash

    yandex-tracker-import --src_org_id <org_id_from> --src_token <token_from> --dst_org_id <org_id_to> --dst_token <token_to> --user_mapping path/to/file --default_uid <default_user_uid>

Where:
    - src_org_id - organization from which content will be copied
    - src_token - token from first organization obtained `here <https://yandex.ru/dev/connect/tracker/api/concepts/access-docpage/>`_
    - dst_org_id - organization to which content will be copied
    - dst_token - token from first organization obtained `here <https://yandex.ru/dev/connect/tracker/api/concepts/access-docpage/>`_
    - user_mapping - path to local file with following format:

        uid_from_first_org uid_from_second_org

    - default_uid - user uid to use if no match could be found in file

Note about user mapping - if default_uid provided it will be used if where is no
match for current uid in file, if default uid not provided and where is no match - uid from
source org will be used.

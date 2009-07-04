Overview
========

This module provides a simple Pythonic interface to the PivotalTracker API.
It also provides both a simple commandline interface to Pivotal.

Quickstart
==========

This is the primary API for using Pivotal.  First you simply create a client::

    import pivotaltracker
    client = pivotaltracker.Client(token="YOUR API TOKEN")
    
Now you can execute any of the API methods on that client.  All method calls will return Python dictionaries.
You can find detailed documentation in the docstrings for now, until I get the API docs created.
Here's a quick rundown in the meantime:

* **get_project** (project_id)
* **get_all_projects** (self)
* **get_story** (project_id, story_id)
* **get_stories** (project_id, query=None, limit=None, offset=None)
* **get_iterations** (project_id, limit=None, offset=None)
* **get_done_iterations** (project_id, limit=None, offset=None)
* **get_current_iterations** (project_id, limit=None, offset=None)
* **get_backlog_iterations** (project_id, limit=None, offset=None)
* **add_story** (project_id, name, description, story_type, requested_by=None, estimate=None, current_state=None, labels=None)
* **update_story** (project_id, story_id, name=None, description=None, requested_by=None, story_type=None, estimate=None, current_state=None, labels=None)
* **delete_story** (project_id, story_id)
* **add_comment** (project_id, story_id, text, author=None)
* **deliver_all_finished_stories** (project_id)

Release Notes
=============

* **0.0.3** added feature submission to the tool
* **0.0.2** added bug submission to the tool
* **0.0.1** original Client API object, very basic commandline tool (only submits chores)

Advanced
========

Commandline Tool
----------------
Simply run ``pt help`` on the commandline to see options.  The first time you run the tool,
it will walk you through creating your API key and setting up your configuration.

More documentation to come, later.

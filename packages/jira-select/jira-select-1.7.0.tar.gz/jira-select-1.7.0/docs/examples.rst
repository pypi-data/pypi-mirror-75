Examples
========

Finding all issues assigned to a particular user
------------------------------------------------

.. code-block:: yaml

   select:
   - "*"
   from: issues
   where:
   - assignee = "some-user@some-company.com"


Summing the number of story points assigned in a particular sprint
------------------------------------------------------------------

.. code-block:: yaml

   select:
   - sum({Story Points}) as "Total Story Points"
   from: issues
   where:
   - project = "MYPROJECT"
   group_by:
   - True
   having:
   - '"My Sprint Name" in sprint_name({Sprint}[-1])'

In Jira, your "Story Points" and "Sprint" fields may have any number of names
since they're "Custom Fields"
-- their real names are things like
``customfield10024`` and ``customfield10428``,
but may vary instance to instance.
You can use the field name directly in your query,
but if you know only the "human-readable" name
for your field, you can provide it in brackets
as shown above with -- `{Story Points}` and `{Sprint}`.

The ``where`` limitation here is used solely for reducing the number of records needing to be downloaded,
and can be omitted if you are willing to wait.

The ``group_by`` expression here is to make all of your rows be grouped together
so the ``sum`` operation in your ``select`` block will operate over all of the returned rows.
``True`` is used because that expression will evaluate to the same value for every row.

In the ``having`` section, you can see a fairly complicated expression
that takes the last sprint associated with each returned issue,
looks up that sprint's name and compares it with the sprint name you are looking for.
We're using the ``in`` python expression here because I can't remember the full name,
but I can remember part of it.
You'll notice that the line is quoted;
that's necessary only because the yaml parser interprets
a line starting with a double-quote
a little differently from one that does not.
Try running the query without quoting the string to see what I mean.

Summing the total estimated size of issues per-person for a given sprint
------------------------------------------------------------------------

.. code-block:: yaml

   select:
   - assignee
   - sum(map(estimate_to_days, extract(timeestimate, "originalEstimate")))
   from: issues
   where:
   - project = "MYPROJECT"
   group_by:
   - assignee
   having:
   - '"My Sprint Name" in sprint_name({Sprint}[-1])'

See :ref:`Summing the number of story points assigned in a particular sprint` for
an explanation of the ``having`` section here.

In Jira, estimations are stored in the ``timeestimate.originalEstimate`` field,
but since we've grouped our rows by assignee,
``timeestimate`` represents an array of objects
instead of a single object holding the ``originalEstimate`` we want.
To get an array of ``originalEstimate`` objects,
we will use the ``extract`` function;
you can read more about what this function does at :ref:`Data Traversal` .

If we were to stop here, we would receive an array of strings
looking something like::

   ["1d", "4h", "2d", "30m"]

but, we want to be able to sum these estimates,
so we'll ``map`` each of those through the ``estimate_to_days`` function.
This will create an array like this::

   [1, 0.5, 2, 0.625]

An array isn't quite what we want
-- we want the total number of days --
so we use the ``sum`` function to get that.

See :ref:`Query Functions` for more information.

# TestRailYak

A Python library for interacting with the TestRail REST API.

Essentially, another layer on top of gurock's Python interface: https://github.com/gurock/testrail-api.git

Install:

`pip install testrail_yak`

Use:

```
from testrail_yak import TestRailYak

testrail = TestRailYak()
projects = testrail.project.get_projects(<testrail_url>, <username>, <password>)
```

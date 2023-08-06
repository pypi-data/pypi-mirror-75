# corva-worker-python

A repository for integrated python data app development.

![develop](https://github.com/corva-ai/corva-worker-python/workflows/CI/badge.svg?branch=master)

## Publishing to PYPI

Follow these steps to publish the distribution to PYPI:
1. Check out "master" branch
2. Update the version (with v1.2.3 format) in setup.py, commit the change, and push
3. Tag the master branch the same as the above and push

## Included Modules
### API
### State Handlers
### Task Handler
Task handler class allows triggering lambda functions whenever a task is submitted to the `/v2/tasks` endpoint.
Refer to [Task Handler Documentation](docs/TASK_HANDLER.md) 
### Logging
### Rollbar
### APP and Modules
### Wellbore

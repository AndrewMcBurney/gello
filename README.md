# Gello
:octocat: A self-hosted server for managing Trello cards based on GitHub webhook-events
___

Gello, was developed to help Datadog manage GitHub Issues and Pull Requests open by community members, and incorporate them into our biweekly sprints.

## Features
### GitHub Events
Gello responds to GitHub events on repositories you subscribe to.

**GitHub Pull Request Event**

If a pull request is created by a person outside of the members of a GitHub organization on a subscribing repository, a Trello card will be submitted to a board list (or a number of lists), configurable in the Gello web-UI.

**GitHub Issue Creation Event**

Likewise, if an issue is created by a person outside of the members of a GitHub organization on a subscribed repository, a Trello card will be submitted to a board list (or a number of lists), configurable in the Gello web-UI.

## Configuration
### Configure the Server

Gello requires certain environment variables to be set for the server to be run correctly.

```bash
# Admin user configuration
ADMIN_EMAIL='an_email_account@gmail.com'
ADMIN_PASSWORD='an_admin_password'

# Database configuration
DATABASE_URL='the_url_for_a_postgresql_database'

# Redis configuration
REDIS_URL='the_url_for_a_redis_client' # defaults to 'redis://localhost:6379/0'

# GitHub configuration values
GITHUB_API_TOKEN='An API token for a user with access to your GitHub organization'
GITHUB_ORG_LOGIN='The login for your GitHub organization'

# Trello configuration values
TRELLO_ORG_NAME='The name for your Trello organization'
TRELLO_API_KEY='A user's public trello API key'
TRELLO_API_TOKEN='An API token generated by the corresponding user'
```

#### GitHub API Token

The GitHub API token you provide should have the following permissions set:

* `public_repo`
* `read:org`
* `write:repo_hook`

![GitHub API Token Permissions](/images/permissions.png)

#### Trello Configuration

Gello requires two environment variables be set to properly configure the Trello integration.

1. `TRELLO_API_KEY`

This is the key found in the [Trello Developer API Keys page](https://trello.com/app-key):

![Trello API Key](/images/developer_api_key.png)

2. `TRELLO_API_TOKEN`

This is a token generated by from the same [Trello Developer API Keys page](https://trello.com/app-key):

![Trello API Token](/images/trello_api_token.png)

### macOS Development Setup

```bash
# Configure the python virtual environment
pyenv virtualenv 3.6.4 v-3.6.4
pyenv activate v-3.6.4

# Install the dependencies
pip install pipenv
pipenv install

# Create a PostgreSQL database
createdb your_postgresql_database_name

# Run database migrations
python manage.py db upgrade

# In one terminal, start the worker
pyenv activate v-3.6.4
celery worker -A celery_worker.celery --loglevel=info

# In another terminal, run the server
pyenv activate v-3.6.4
python run.py

# Visit localhost:5000
open http://localhost:5000
```

## Deployment to Heroku

```bash
# Login with your heroku credentials
heroku login

# Create your application
heroku apps:create --buildpack heroku/python

# Add redis add-on for celery worker
heroku addons:create heroku-redis -a your_app_name

# Add postgresql add-on for database
heroku addons:create heroku-postgresql

# Verify REDIS and DATABASE exist
heroku addons

# Push the code to heroku
git push heroku master

# Configure your environment variables
#
# NOTE: for heroku, you do not need to set the `DATABASE_URL` or `REDIS_URL`
# environment variables, since they are set automatically with the addons
heroku config:set ADMIN_EMAIL=email@email.com
heroku config:set ADMIN_PASSWORD=some_password
heroku config:set GITHUB_API_TOKEN=your_github_api_token
heroku config:set GITHUB_ORG_LOGIN=the_name_of_your_organization
heroku config:set TRELLO_ORG_NAME=your_trello_organization_name
heroku config:set TRELLO_API_KEY=your_trello_public_key
heroku config:set TRELLO_API_TOKEN=a_trello_token_you_generate

# Start the celery worker on a dyno
heroku ps:scale worker=1

# Open the application
heroku open
```

## Why _Gello_?
Gello was named because it bridges the gap between the GitHub API and the Trello API.

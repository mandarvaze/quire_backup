# Requirements #

* python
* poetry

# Getting Started #

* Install packages with `poetry install`
* Start dev server as :

``` shell
export CLIENT_ID=...
export CLIENT_SECRET=...
export CSRF_TOKEN=.... 
make dev
```

# Make backup #

* Open this URL in the browser
https://quire.io/oauth?client_id=CLIENT_ID&redirect_uri=http://localhost:3000/quire_callback&state=CSRF_TOKEN
* Grant permissions.
* Get list of projects : http://localhost:3000/quire_projects
* Note the *id* of the project you wish to backup
* Get project backup [WIP] : http://localhost:3000/quire_backup/{project_id}



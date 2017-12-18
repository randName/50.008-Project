# Decisions and practices used for this project

This excludes generic good practices like linting.

## Schema
Even though there was no requirement for data to be stored about the entities,
they were brought out into their own tables as referring to an entity by ID is
the only future-proof method.

## JSON Backend & Vue Frontend
To decouple the frontend from the backend, we chose to make a RESTful JSON API.
We used Vue for the frontend, which makes Single-Page Applications (SPAs) easy.
The Django views are just JSON endpoints, with one template for the main page.

## SQL to JSON
From a query to the output of the endpoint, it usually involves:
- Connection to the server
- Executing the query
- Pagination
- Packing into objects
- Outputting JSON

Thus a few helper functions were created, stored in [db](common/db.py) and [utils](common/utils.py).
A general purpose [decorator](common/decorators.py) helps to emit JSON from the usual Python types.

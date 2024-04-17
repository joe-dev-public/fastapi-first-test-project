Working through some of the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) to learn a bit about it and build some kind of test project.

To start:

- In the Postgres Docker repo dir: `make up`
  - (`fastapi-first-test-project-postgres-docker`)
- In this repo dir: `make up`
  - (Likewise, to stop: `make down`)
- In the frontend repo dir: `npm run dev`
  - (`vite-typescript-frontend-test-project`)
- Visit whatever that tells you (probably http://localhost:5173)

(See `Makefile` for more.)

## File structure

```
├── Dockerfile
├── Makefile
├── README.md
├── app
│   ├── main.py - setup & endpoints/routes (for now)
│   └── sql_app
│       ├── crud.py - functions to interact with db[0]
│       ├── database.py - db connection stuff
│       ├── models.py - db/SQLAlchemy models
│       └── schemas.py - Pydantic models[1]
└── requirements.txt

```

[0] Create x, delete y, update z, etc.

[1] For "data validation, conversion, and documentation" ([source](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-sqlalchemy-models-from-the-base-class))


<details>
  <summary>
    Old starting instructions
  </summary>
  Start the server with:

  `uvicorn main:app --reload`

  Where:

  - `main` is the filename of the Python module (i.e. `main.py`)
  - `app` is the FastAPI class instance (i.e. `app = FastAPI()`).
</details>
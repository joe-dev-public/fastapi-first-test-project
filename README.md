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
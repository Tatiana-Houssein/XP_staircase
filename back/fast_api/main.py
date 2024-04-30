from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from back.src.controller import (
    call_back_answer,
    call_back_next_stimulus,
    create_new_experiment,
    get_dict_tache_interferente,
    save_form_data,
)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/first-stimulus")
def first_stimulus():  # noqa: ANN201
    create_new_experiment()
    return call_back_next_stimulus()


@app.post("/next-stimulus")
def next_stimulus(request: Request):  # noqa: ANN201
    payload = request.json()
    call_back_answer(payload)
    return call_back_next_stimulus()


@app.post("/submit")
def submit_form(request: Request):  # noqa: ANN201
    form_data = request.json()
    # Process form data here
    save_form_data(form_data=form_data)
    print("Received form data:", form_data)
    return {"message": "Form submitted successfully"}


@app.get("/tache-interferente")
def get_tache_interferente_parameters():  # noqa: ANN201
    return get_dict_tache_interferente()
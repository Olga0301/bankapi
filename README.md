CREATING VIRTUAL ENVIRONMENT
python -m venv venv

ACTIVATE VENV
venv\Scripts\activate - Windows source venv/bin/activate - Unix

INSTALLING PACKAGES
pip install -r requrements.txt

INITIALIZE ALEMBIC
alimbic init alimbic

alembic revision --autogenerate

alembic upgrade head

RUN
uvicorn app:app --reload
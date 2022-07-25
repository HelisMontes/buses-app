```bash
rm -rf .venv/
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements
cd app/
python3 manage.py runserver
```
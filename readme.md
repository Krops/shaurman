# Install guide

```bash
git clone git@github.com:Krops/shaurman.git
cd /path/to/shaurman
virtualenv venv
source venv/bin/activate
pip install -r req.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## for email sending support change following string into shaurman/settings.py file:
```python
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
```

## home page 
```javascript
http://127.0.0.1:8000/
```
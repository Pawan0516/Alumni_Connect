### Project Setup Guide
```
git clone git@github.com:Pawan0516/Alumni_Connect.git -b dev backend
```

###### Step 1
```
cd backend
```

###### Step 2
```
python -m venv env
```

###### Step 3
```
pip install -r requirements.txt
```
###### Step 4
- Rename `.env.example` -> `.env` and provide environment variables
  
###### Step 5
```
python manage.py makemigrations
python manage.py migrate
```

###### Step 6
```
python manage.py createsuperuser
```

##### Start Dev Server
```
python manage.py runserver
```

###### Dev URL's
[backend](http://localhost:8000)
[frontend](http://localhost:5173)

- Frontend Repo [URL](https://github.com/preeti-khachne/Alumni-Connect)

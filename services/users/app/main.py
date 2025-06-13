from fastapi import FastAPI


app = FastAPI()


@app.get('/api/users/')
def home_page():
    return {'message': 'Привет мир!'}

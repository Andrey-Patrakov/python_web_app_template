from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def gateway_service():
    return {'message': 'Gateway service'}

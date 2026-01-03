from fastapi import FastAPI


print('hello world')


app = FastAPI()


@app.get("/normal/")
def normalTest():
    print("summa")
    return "All good"

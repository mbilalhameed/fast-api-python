from fastapi import FastAPI, Body

app = FastAPI()


@app.get('/')
async def root():
    return {'message': "Hello world!"}


@app.get('/posts')
def get_posts():
    return {'data': ['post1', 'post2', 'post3']}


@app.post('/createpost')
def create_post(pay_load: dict = Body(...)):
    print(pay_load)
    return {
        'message': "post created successfully",
        "post_title": f"{pay_load['title']}",
        "post_content": f"{pay_load['content']}"
    }

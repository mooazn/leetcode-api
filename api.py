from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from tinydb import table, TinyDB, Query

app = FastAPI()
leetcode_problems_db = TinyDB('algorithm_problems.json')
leetcode_problems_db_query = Query()
leetcode_problems_content_db = TinyDB('algorithm_problems_content.json')
leetcode_problems_content_db_query = Query()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/api/v1/{problem_slug}')
async def get_leetcode_problem(problem_slug: str):
    problem = problem_slug.lower()
    basic_details = leetcode_problems_db.search(leetcode_problems_db_query.slug == problem)
    if len(basic_details) == 0:
        return {'status_code': 404, 'message': 'Requested problem does not exist.'}
    else:
        problem_content = leetcode_problems_content_db.search(leetcode_problems_content_db_query.name == problem)
        document_content = [table.Document({'content': problem_content[0]['content']}, doc_id=0)]
        return {'status_code': 200, 'message': basic_details + document_content}

from typing import Optional

from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

import modal

stub = modal.Stub()
stub.image = modal.image.DebianSlim().pip_install(["pygsheets", "jinja2"])

web_app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    user: str
    item: str
    screenshot: str
    price: float

def page(rows):
    row_strings = ["<tr>" + "".join(["<td>" + column + "</td>" for column in row]) + "</tr>\n" for row in rows[1:]]

    return """
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    #purchases {
                        font-family: Arial, Helvetica, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                    }

                    #purchases td, #purchases th { border: 1px solid #ddd; padding: 8px; }

                    #purchases tr:nth-child(even){ background-color: #f2f2f2; }

                    #purchases tr:hover { background-color: #ddd; }

                    #purchases th {
                        padding-top: 12px;
                        padding-bottom: 12px;
                        text-align: left;
                        background-color: #04AA6D;
                        color: white;
                    }
                </style>
            </head>
            <body>
                <h1 href="https://docs.google.com/spreadsheets/d/1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M">
                    93 Leonard Purchases
                </h1>
                <table id="purchases">
                    <tr>
                        <th>Name</th>
                        <th>Item</th>
                        <th>Screenshot</th>
                        <th>Price</th>
                    </tr>
                    """ + "\n".join(row_strings) + """
                </table>
            </body>
        </html>
    """


@web_app.get("/", response_class=HTMLResponse)
async def handle_root(user_agent: Optional[str] = Header(None)):
    print(f"GET /     - received user_agent={user_agent}")
    rows = get_sheet().get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
    return page(rows)

@web_app.post("/add")
async def handle_foo(item: Item, user_agent: Optional[str] = Header(None)):
    print(f"POST /add - received user_agent={user_agent},\
        item.user={item.user}, item.item={item.item}, item.price={item.price}, item.screenshot={item.screenshot}")

    get_sheet().append_table([str(item.name), str(item.item), str(item.screenshot), float(item.price)])

    return True

@stub.function(secret=modal.ref("my-gsheets-secret"))
def get_sheet():
    import pygsheets
    doc = "1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M"
    gc = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_JSON")
    return gc.open_by_key(doc).sheet1

@stub.asgi()
def fastapi_app():
    return web_app


if __name__ == "__main__":
    stub.deploy("93-test")

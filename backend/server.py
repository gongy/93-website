import modal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

stub = modal.Stub()
stub.image = modal.image.DebianSlim().pip_install(["pygsheets"])

web_app = FastAPI()

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://93-website.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@web_app.get("/expenses")
def get_sheet():
    from fastapi.responses import JSONResponse
    import pygsheets

    doc = "1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M"
    gc = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_JSON")
    sheet = gc.open_by_key(doc).sheet1
    rows = sheet.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
    return rows

@stub.asgi(secret=modal.ref("my-gsheets-secret"))
def fastapi():
    return web_app

if __name__ == "__main__":
    stub.deploy("93")

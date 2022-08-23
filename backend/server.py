import modal

stub = modal.Stub()
stub.image = modal.image.DebianSlim().pip_install(["pygsheets", "jinja2"])

def get_sheet():
    import pygsheets
    doc = "1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M"
    gc = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_JSON")
    return gc.open_by_key(doc).sheet1

@stub.asgi()
def fastapi_app():
    return web_app

if __name__ == "__main__":
    stub.deploy("93")

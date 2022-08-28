"""
Backend for 93-website
deploy using `modal app deploy --name 93 server.py::stub`
"""

import modal
from datetime import datetime, timezone
import pandas as pd
import os

def utc_ts():
    return datetime.now(tz=timezone.utc).timestamp()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

stub = modal.Stub()
stub.image = modal.image.DebianSlim().pip_install(["pygsheets", "pandas"])
volume = modal.SharedVolume().persist("93-db")

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

@stub.asgi(
    secret=modal.ref("my-gsheets-secret"),
    shared_volumes={"/root/db": modal.SharedVolume()}
)
def fastapi():
    return web_app

@stub.function(
    secret=modal.ref("my-gsheets-secret"),
    shared_volumes={"/root/db": volume}
)
def reset_db():
    # bump this version after making changes to the database
    db_version = 1

    with open("/root/db/v", "w+") as f:
        x = f.read()
        print(x)
        if x and int(x) == db_version:
            return

    import pygsheets
    doc = "1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M"
    gc = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_JSON")
    sheet = gc.open_by_key(doc).sheet1
    rows = sheet.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)

    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS expenses")
    cur.execute("CREATE TABLE expenses(name, item, screenshot, price)")
    cur.executemany("INSERT INTO expenses VALUES(?, ?, ?, ?)", rows)
    con.commit()

    cur.execute("DROP TABLE IF EXISTS laundry")
    cur.execute("CREATE TABLE laundry(name, washer_end, dryer_end)")
    people = [
        (name, 0.0, 0.0)
        for name in ["ak", "dansun", "cjs", "rgong", "jlee", "bwu"]
    ]
    cur.executemany("INSERT INTO laundry VALUES(?, ?, ?)", people)
    con.commit()


@stub.function(shared_volumes={"/root/db": volume})
def update_laundry(machine, person):
    if machine not in ["washer", "dryer"]:
        return

    # todo: make this a context manager
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    df = pd.read_sql_query("SELECT * from laundry", con)
    df.loc[df['name'] == person, machine + "_end"] = utc_ts()
    df.to_sql("laundry", con, if_exists="replace")
    con.close()

@stub.function(shared_volumes={"/root/db": volume})
def laundry_state():
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM laundry")
    return res.fetchall()

@stub.function(shared_volumes={"/root/db": volume})
def read_all_db():
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    cur = con.cursor()

    res = cur.execute("SELECT * FROM expenses")
    print("expenses table")
    print(res.fetchall())

    print("laundry table")
    res = cur.execute("SELECT * FROM laundry")
    print(res.fetchall())

if __name__ == "__main__":
    with stub.run():
        # reset_db()
        read_all_db()
        update_laundry(machine="washer", person="rgong")
        read_all_db()

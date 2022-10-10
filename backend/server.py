"""
Backend for 93-website
deploy using `modal app deploy --name 93 server.py::stub`
"""

from audioop import add
import modal
from datetime import datetime, timezone
import pandas as pd
import os
import json

def utc_ts():
    return datetime.now(tz=timezone.utc).timestamp()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class LaundryUpdate(BaseModel):
    machine: str
    person: str
    offset: float

class HomeUpdate(BaseModel):
    nmapResult: str

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

@web_app.get("/laundry")
def query_laundry():
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    df = pd.read_sql_query("SELECT * from laundry", con)
    print(df.to_dict("records"))
    return df.to_dict("records")

def modify_home_df(df, person):
    if person in list(df['name']):
        print("person exists")
        df.loc[df['name'] == person, "time"] = utc_ts()
    else:
        print("person doesn't exist")
        new_df = pd.DataFrame([{"name": person, "time": utc_ts()}])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)
    print(df)

    return df

@web_app.post("/localpost")
def local_update(update: HomeUpdate):
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    df = pd.read_sql_query("SELECT * from home", con)

    addresses = json.loads(os.environ["MAC_ADDRESSES"])
    for person, mac in addresses.items():
        if mac in update.nmapResult.lower():
            df = modify_home_df(df, person)

    df = modify_home_df(df, "updated_at")

    df.to_sql("home", con, if_exists="replace", index=False)
    con.close()

    read_all_db()

@web_app.get("/home")
def who_is_home():
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    df = pd.read_sql_query("SELECT * from home", con)

    res = []
    for _, row in df.iterrows():
        res.append({'name': row['name'], 'time': row['time']})
    
    s = sorted(res, key=lambda x:-x['time'])

    return s

@web_app.post("/claim")
def claim_laundry(update: LaundryUpdate):
    print(update)

    if update.machine not in ["washer", "dryer"]:
        return

    # todo: make this a context manager
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    df = pd.read_sql_query("SELECT * from laundry", con)
    print(df)
    print(update.machine, update.offset, update.person)
    df.loc[df['name'] == update.person, update.machine + "_end"] = utc_ts() + update.offset
    print(df)
    df.to_sql("laundry", con, if_exists="replace", index=False)
    con.close()
    
@web_app.get("/expenses")
def query_expenses():
    from fastapi.responses import JSONResponse
    import pygsheets

    doc = "1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M"
    gc = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_JSON")
    sheet = gc.open_by_key(doc).sheet1
    rows = sheet.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
    return rows

@stub.asgi(
    secrets=[
        modal.Secret.from_name("my-gsheets-secret"),
        modal.Secret.from_name("local-macs"),
    ],
    shared_volumes={"/root/db": volume}
)
def fastapi():
    return web_app

@stub.function(
    secret=modal.Secret.from_name("my-gsheets-secret"),
    shared_volumes={"/root/db": volume}
)
def reset_db():
    import sqlite3
    con = sqlite3.connect("/root/db/sqlite.db")
    cur = con.cursor()

    # import pygsheets
    # doc = "1988nYIzBAVzhjlSWTuJ___uQb610KfLLpGZh-xvpd2M"
    # gc = pygsheets.authorize(service_account_env_var="SERVICE_ACCOUNT_JSON")
    # sheet = gc.open_by_key(doc).sheet1
    # rows = sheet.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)

    # cur.execute("DROP TABLE IF EXISTS expenses")
    # cur.execute("CREATE TABLE expenses(name, item, screenshot, price)")
    # cur.executemany("INSERT INTO expenses VALUES(?, ?, ?, ?)", rows)
    # con.commit()

    cur.execute("DROP TABLE IF EXISTS laundry")
    cur.execute("CREATE TABLE laundry(name, washer_end, dryer_end)")
    people = [
        (name, 0.0, 0.0)
        for name in ["ak", "dansun", "cjs", "rgong", "jlee", "bwu"]
    ]
    cur.executemany("INSERT INTO laundry VALUES(?, ?, ?)", people)
    con.commit()

    cur.execute("DROP TABLE IF EXISTS home")
    cur.execute("CREATE TABLE home(name, time)")
    cur.execute("INSERT INTO home VALUES(?, ?)", ["updated_at", 0])
    con.commit()


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

    print("home table")
    res = cur.execute("SELECT * FROM home")
    print(res.fetchall())

if __name__ == "__main__":
    with stub.run():
        reset_db()
        read_all_db()

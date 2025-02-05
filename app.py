# haafai asset management app backend api

# database connection string
# postgresql://postgres:#44F41_$3CR3T@db.ijqlcwhexydftvfwwejg.supabase.co:5432/postgres

from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client
from flask import Flask, request, jsonify
from flask_cors import CORS
from time import sleep

app = Flask(__name__)
CORS(app)

url = os.getenv("DATABASE_URL")
key = os.getenv("DATABASE_KEY")
supabase = create_client(url, key)

# data = supabase.table("staff").select("*").execute()
# print(data)

def fetch(table, eq=False, column=None, value=None): # function to query db, retry 3 times if query fails
    for each in range(3): 
        try:
            if eq == True:
                query = supabase.table(table).select("*").eq(column, value).execute()
                return query.data
            else:
                query = supabase.table(table).select("*").execute()
                return query.data
        except Exception as err:
            print(err)
            sleep(2)

@app.get("/staff")
def Staff():
    return jsonify(
        fetch(table="staff", eq=False)
        )

@app.get("/staff/<staffID>/current")
def staffCurrentAssignments(staffID):
    data = fetch(table="assets", eq=True, column="assigned_staff", value=staffID)
    #query = supabase.table("assets").select("*").eq("assigned_staff", staffID).execute()

    currentlyAssigned = []
    #history = []

    for asset in data:
        if asset["status"] == "Assigned":
            currentlyAssigned.append(asset)
            #print(asset["status"])
        #else:
            #history.append(asset)
    #print(data)
    return jsonify(currentlyAssigned)


@app.get("/assets")
def Assets():
    return jsonify(
        fetch(table="assets", eq=False)
    )

if __name__ == "__main__":
    app.run(debug=True)
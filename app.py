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
from datetime import datetime

app = Flask(__name__)
CORS(app)

url = os.getenv("DATABASE_URL")
key = os.getenv("DATABASE_KEY")
supabase = create_client(url, key)

class Asset:
    def __init__(
        self,
        type,
        status,
        purchasedDate,
        location = None,
        assignedStaff = None,
        assignedDate = None,
        discardedDate = None,
        lastReturnedDate = None,
    ):
        self.type = type
        self.status = status
        self.purchasedDate = purchasedDate
        self.location = location
        self.assignedStaff = assignedStaff
        self.assignedDate = assignedDate
        self.discardedDate = discardedDate
        self.lastReturnedDate = lastReturnedDate

    def getData(self):
        # form validation, ignore specific values based on status
        if self.status == "Not Assigned":
            self.location = None
            self.assignedStaff = None
            self.assignedDate = None
            self.discardedDate = None

        elif self.status == "Assigned":
            self.discardedDate = None

        elif self.status == "Discarded":
            self.location = None
            self.assignedStaff = None
            self.assignedDate = None

        return {
            "type": self.type,
            "status": self.status,
            "location": self.location,
            "assigned_staff": self.assignedStaff,
            **self.getTimestamp()
        }
    
    def getTimestamp(self):
        dates = {
            "purchased_date": self.purchasedDate,
            "assigned_date": self.assignedDate,
            "discarded_date": self.discardedDate,
            "last_returned_date": self.lastReturnedDate,
        }

        for key, value in dates.items():
            if value:
                dates[key] = datetime.strptime(value, "%Y-%m-%d").isoformat()
            else:
                dates[key] = None
    
        return {
            "purchased_date": dates["purchased_date"],
            "assigned_date": dates["assigned_date"],
            "discarded_date": dates["discarded_date"],
            "last_returned_date": dates["last_returned_date"],
        }



# GET routes

@app.get("/")
def Base():
    return """
    <h1>API urls</h1>
    <p>(GET) /staff</p>
    <p>(GET) /staff/{national_id}/current</p>
    <p>(GET) /assets</p>
    """

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


# POST routes

@app.post("/assets/create")
def CreateAsset():
    form = request.get_json()

    asset = Asset(
        type = form.get("type"),
        status = form.get("status"),
        purchasedDate = form.get("purchasedDate"),
        location = form.get("location"),
        assignedStaff = form.get("assignedStaff"),
        assignedDate = form.get("assignedDate"),
        discardedDate = form.get("discardedDate"),
    )

    print(asset.getData())
    try:
        supabase.table("assets").insert(
            asset.getData()
        ).execute()

        return jsonify({
            "success": True
        })
    except Exception as err:
        print(f"ERROR: {err}")
    
        return jsonify({
            "success": False,
            "message": err
        })


# helper functions

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

# def convertDate(asset): # if date exists then convert date str to date obj, else null
#     dates = ["purchasedDate", "assignedDate", "discardedDate"]

#     for i in range(len(dates)):
#         date = asset.get(dates[i])

#         if date:
#             dates[i] = datetime.strptime(date, "%Y-%m-%d")
#         else:
#             dates[i] = None
    
#     return {
#         "purchased_date": dates[0],
#         "assigned_date": dates[1],
#         "discarded_date": dates[2],
#         "last_returned_date": None
#     }

if __name__ == "__main__":
    app.run()
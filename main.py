from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

# Load patient data from patient.json file
def load_data():
    with open("patient.json", "r") as f:
        data = json.load(f)
    return data

# Home route
@app.get("/")
def hello():
    return {"message": "Patient management system API"}

# About route
@app.get("/about")
def about():
    return {"message": "Fully functional API to manage your records"}

# View all patient data
@app.get("/view")
def view():
    data = load_data()
    return data

# View a specific patient using patient_id
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")
):
    data = load_data()

    # Loop through all patients
    for patient in data["patients"]:
        if patient["id"] == patient_id:
            return patient

    # If no patient matches
    raise HTTPException(status_code=404, detail="Patient not found")

# Sort patients by height, weight, or BMI
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight or BMI"),
    order: str = Query("ascending", description="Sort in ascending or descending order")
):
    valid_fields = ["height", "weight", "BMI"]

    # Validate sort field
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose from {valid_fields}"
        )

    # Validate order
    if order not in ["ascending", "descending"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Choose ascending or descending"
        )

    data = load_data()

    # Decide sorting direction
    reverse = True if order == "descending" else False

    # Sort patient list
    sorted_patients = sorted(
        data["patients"],
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )

    return {
        "sorted_by": sort_by,
        "order": order,
        "patients": sorted_patients
    }

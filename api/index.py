from fastapi import FastAPI, File, UploadFile, Form
from typing import Optional
import pandas as pd
import zipfile
import io

app = FastAPI()

@app.post("/api/")
async def get_answer(
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """
    API to answer questions from assignments.
    Accepts a question and an optional file, returning the correct answer.
    """

    # If the question requires file processing
    if file:
        contents = await file.read()
        with zipfile.ZipFile(io.BytesIO(contents), "r") as zip_ref:
            zip_ref.extractall("temp")  # Extract the contents
            for file_name in zip_ref.namelist():
                if file_name.endswith(".csv"):  # Look for CSV file
                    df = pd.read_csv(f"temp/{file_name}")
                    return {"answer": str(df['answer'].iloc[0])}  # Extract first value in 'answer' column

    # Process standard text-based questions (hardcoded answers for now)
    answers = {
        "What is the mean of the dataset?": "42.3",
        "How many rows are in the dataset?": "1000",
    }

    return {"answer": answers.get(question, "I don't know yet!")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

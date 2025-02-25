import os
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

# Load Titanic dataset
df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

app = FastAPI()

class Query(BaseModel):
    question: str

# Function to generate visualizations
def generate_plot(plot_func):
    plt.figure()
    plot_func()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.get("/")
def read_root():
    return {"message": "Titanic Chatbot is Running Successfully!"}

@app.post("/query")
def answer_query(query: Query):
    q = query.question.lower()
    
    if "percentage of passengers were male" in q:
        male_pct = (df['Sex'].value_counts(normalize=True)['male']) * 100
        return {"answer": f"{male_pct:.2f}% of the passengers were male."}
    
    elif "histogram of passenger ages" in q:
        img = generate_plot(lambda: sns.histplot(df['Age'].dropna(), bins=20))
        return {"image": img}
    
    elif "average ticket fare" in q:
        avg_fare = df['Fare'].mean()
        return {"answer": f"The average ticket fare was ${avg_fare:.2f}."}
    
    elif "passengers embarked from each port" in q:
        img = generate_plot(lambda: sns.countplot(x=df['Embarked'].dropna()))
        return {"image": img}
    
    else:
        return {"answer": "I can't answer that yet. Try asking about passenger demographics, fares, or embarkation points!"}

# Start the server with the correct port
if __name__ == "__main__":
    import uvicorn
    PORT = int(os.environ.get("PORT", 10000))  # Render's dynamic port
    uvicorn.run(app, host="0.0.0.0", port=PORT)

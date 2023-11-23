#import nesesary module 
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from io import BytesIO
from pdfminer.high_level import extract_text
import re
import os
import datetime  
from collections import defaultdict
#Set up fastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates") 

#Create directory for downloading and uploaded file
storage_directory = "C:\\Users\Few92\OneDrive\Desktop\AlgoProject(ng)\storage"

#Create list to store applicant data
applicant_data = []

#Create score range list for the 3rd table(sort by score range)
score_ranges = {
    "25-29":[[], 0],
    "20-24":[[], 0],
    "15-19":[[], 0],
    "10-14":[[], 0],
    "5-9":[[], 0],
    "0-4":[[], 0],    
}

#define fucntion for parsing resume 
def parse_and_score_resume(file):

    #Extract texts from the pdf.
    text = extract_text(file)
    
    #Choose satified keywords
    keyword1 = re.compile(r"Python|python")
    keyword2 = re.compile(r"Data Analysis|data analysis")
    keyword3 = re.compile(r"MATLAB")
    keyword4 = re.compile(r"Deep Learning")
    keyword5 = re.compile(r"Statistic")
    keyword6 = re.compile(r"Data Visualization")
    keyword7 = re.compile(r"Machine Learning")
    keyword8 = re.compile(r"Pandas")
    keyword9 = re.compile(r"SQL")
    keyword10 = re.compile(r"TensorFlow")
    keyword11 = re.compile(r"Jupyter Notebook")
    keyword12 = re.compile(r"Oracle")
    keyword13 = re.compile(r"MySQL")
    keyword14 = re.compile(r"SQLite")
    keyword15 = re.compile(r"Keras")
    keyword16 = re.compile(r"PyTorch")
    keyword17 = re.compile(r"Hadoop")
    keyword18 = re.compile(r"Flask")
    keyword19 = re.compile(r"NoSQL")
    keyword20 = re.compile(r"NLP")
    keyword21 = re.compile(r"Excel")
    keyword22 = re.compile(r"NumPy")
    
    #Find keyword from extracts pdf texts
    findk1 = keyword1.findall(text)
    findk2 = keyword2.findall(text)
    findk3 = keyword3.findall(text)
    findk4 = keyword4.findall(text)
    findk5 = keyword5.findall(text)
    findk6 = keyword6.findall(text)
    findk7 = keyword7.findall(text)
    findk8 = keyword8.findall(text)
    findk9 = keyword9.findall(text)
    findk10 = keyword10.findall(text)
    findk11 = keyword11.findall(text)
    findk12 = keyword12.findall(text)
    findk13 = keyword13.findall(text)
    findk14 = keyword14.findall(text)
    findk15 = keyword15.findall(text)
    findk16 = keyword16.findall(text)
    findk17 = keyword17.findall(text)
    findk18 = keyword18.findall(text)
    findk19 = keyword19.findall(text)
    findk20 = keyword20.findall(text)
    findk21 = keyword21.findall(text)
    findk22 = keyword22.findall(text)

    #Put keyword into list and and make it to smaller letter
    findk1 = list(set(map(str.lower, findk1)))
    findk2 = list(set(map(str.lower, findk2)))
    findk3 = list(set(map(str.lower, findk3)))
    findk4 = list(set(map(str.lower, findk4)))
    findk5 = list(set(map(str.lower, findk5)))
    findk6 = list(set(map(str.lower, findk6)))
    findk7 = list(set(map(str.lower, findk7)))
    findk8 = list(set(map(str.lower, findk8)))
    findk9 = list(set(map(str.lower, findk9)))
    findk10 = list(set(map(str.lower, findk10)))
    findk11 = list(set(map(str.lower, findk11)))
    findk12 = list(set(map(str.lower, findk12)))
    findk13 = list(set(map(str.lower, findk13)))
    findk14 = list(set(map(str.lower, findk14)))
    findk15 = list(set(map(str.lower, findk15)))
    findk16 = list(set(map(str.lower, findk16)))
    findk17 = list(set(map(str.lower, findk17)))
    findk18 = list(set(map(str.lower, findk18)))
    findk19 = list(set(map(str.lower, findk19)))
    findk20 = list(set(map(str.lower, findk20)))
    findk21 = list(set(map(str.lower, findk21)))
    findk22 = list(set(map(str.lower, findk22)))

    #Append keywords into the allskills list
    allskills = findk1 + findk2 + findk3 + findk4 + findk5 + findk8 + findk9 + findk10 + findk11 + findk12 + findk13 + findk14 + findk15 + findk16 + findk17+ findk18 + findk19 + findk20 + findk21 + findk22

    #Grading satisfied keywords 
    score = 0
    for i in allskills:
        if i == 'python':
            score += 3
        elif i == 'data analysis':
            score += 3
        elif i == 'matlab':
            score += 3
        elif i == 'machine learning':
            score += 3
        elif i == 'deep Learning':
            score += 3
        elif i == 'statistic':
            score += 3
        elif i == 'data visualization':
            score += 3
        elif i == 'pandas':
            score += 3
        elif i == 'sql':
            score += 3
        elif i == 'tensorflow':
            score += 3
        elif i == 'jupyter notebook':
            score += 3
        elif i == 'oracle':
            score += 3
        elif i == 'mysql':
            score += 3
        elif i == 'sqlite':
            score += 3
        elif i == 'keras':
            score += 3
        elif i == 'pytorch':
            score += 3
        elif i == 'hadoop':
            score += 3
        elif i == 'flask':
            score += 3
        elif i == 'nosql':
            score += 3
        elif i == 'nlp':
            score += 3
        elif i == 'excel':
            score += 3
        elif i == 'numpy':
            score += 3

    return allskills, score
#Create endpoint to root and pass the data which are request, applicant data, sorted data, score ranges to the Applicantdata.html which is our frontend
@app.get("/")
async def root(request: Request):
    # Sort the applicant data by score in descending order
    sorted_data = sorted(applicant_data, key=lambda x: x["score"], reverse=True)
    for k, data in score_ranges.items():
        feq = len(data[0])
        data[1] = feq
    
    return templates.TemplateResponse("Applicantdata.html", {"request": request, "applicant_data": applicant_data, "sorted_data": sorted_data, "score_ranges": score_ranges})

#Create enpoint after we press upload button 
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        #Extract text from the uploaded PDF
        file_data = BytesIO(file.file.read())
        skills, score = parse_and_score_resume(file_data)

        #Get file name without the path
        filename = os.path.basename(file.filename)

        #Build the full file path
        file_path = os.path.join(storage_directory, filename)

        #Save the uploaded file to the given directory
        with open(file_path, "wb") as new_file:
            new_file.write(file_data.read())

        #Output the data that will be display on the html table
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        applicant_data.append({"filename": filename, "Matched_skills": ", ".join(skills), "score": score, "date": date})

        #Finding score ranges for each file uploaded
        score_range = f"{score // 5 * 5}-{score // 5 * 5 + 4}"
        score_ranges[score_range][0].append(filename)
        
        #Create html after the file is uploaded
        result_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
            body {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: 'Roboto', sans-serif;
                background-image: linear-gradient(-225deg, #290B3D 0%, #19173E 52%, #0A223C 100%);
                background-size: cover;
                background-attachment: fixed;
            }}
            h1 {{
                font-size: 65px;
                color: white;
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                gap: 10px;
            }}
            .backbutton {{
                font-size: 18px;
                padding: 1.0rem 2.0rem;
                background-color: #C16FE0;
                color: #000000;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .appbutton{{
                font-size: 18px;
                padding: 1.0rem 2.0rem;
                background-color: #24AE6C;
                color: #000000;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
        </style>
        </head>
        <body>
            <h1 align='center'>Your PDF file is uploaded successfully!<br>❤️❤️❤️</br></h1>
            <div class="button-container">
                <button class="backbutton" onclick="window.open('http://127.0.0.1:5500/img/import.html', '_blank')">Back to import page</button>
                <button class="appbutton" onclick="window.open('http://127.0.0.1:8000/', '_blank')">Applicant data</button>
            </div>
        </body>
        </html>
        """
        #return HTML response to navigates to the HTML page
        return HTMLResponse(content=result_html)

    #If there is no file uploaded the server will return "Upload error"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload Error: {str(e)}")
        
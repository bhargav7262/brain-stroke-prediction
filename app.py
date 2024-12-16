from flask import Flask, render_template, request,session
import pickle
import os 
# Initialize Flask app 
app = Flask(__name__)

app.secret_key = os.urandom(24)
# Load the trained model
with open('model/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    try:
        # Extract features directly from the form without scaling
        features = [
            1 if data['gender'] == 'Male' else 0,
            float(data['age']),
            int(data['hypertension']),
            int(data['heart_disease']),
            1 if data['ever_married'] == 'Yes' else 0,
            int(data['work_type']),
            int(data['Residence_type']),
            float(data['avg_glucose_level']),
            float(data['bmi']),
            int(data['smoking_status']),
        ]

    except ValueError:
        return "Invalid input. Please check the form data."

    # Make prediction
    prediction = model.predict([features])[0]
    # my code
    session['prediction']=int(prediction)

    if prediction == 1:
        return render_template('symptom_input.html', prediction="Brain Stroke Risk Detected.")
    else:
        return render_template('result.html', prediction="No Stroke Risk Detected.")

@app.route('/classify_stroke', methods=['POST'])
def classify_stroke():
    symptoms = request.form.getlist('symptoms')  # Get selected symptoms from checkboxes

    # Classify stroke based on the symptoms
    stroke_type = "Unknown"
    
    # Basic symptom-based classification (you can use a model or rule-based system)
    if 'sudden confusion' in symptoms and 'troubling speech' in symptoms and 'toungue motion' in symptoms:
        stroke_type = "Ischemic Stroke"
    elif 'nausea or vomitimg' in symptoms and 'dizziness' in symptoms:
        stroke_type = "Hemorrhagic Stroke"
    elif 'unable walking' in symptoms and 'difficulty in eyes' in symptoms and 'unable to understand speech' in symptoms:
        stroke_type = "Transient Ischemic Attack (TIA)"
    elif 'Sudden confusion' in symptoms and 'weakness in the arms or legs' in symptoms:
        stroke_type="Cryptogenic Stroke"
    elif 'Double vision' in symptoms and 'Difficulty swallowing' in symptoms and 'Trouble breathing ' in symptoms:
        stroke_type="Brain Stem Stroke"
    elif 'ataxia' in symptoms and 'vertigo' in symptoms:
        stroke_type="Cerebellar Stroke"
    elif 'nausea or vomiting' in symptoms and 'severe headache' in symptoms:
        stroke_type="Stroke Due to Aneurysm"
    
    # Returning stroke type and details
    #return render_template('result.html', prediction=f"Stroke Type: {stroke_type}", details=get_stroke_details(stroke_type))
    # Map prediction result
    #result = "Brain Stroke Risk" if prediction == 1 else "No Brain Stroke Risk"
    #return render_template('result.html', prediction=result)
    details, treatment = get_stroke_details_and_treatment(stroke_type)

    # Return the result with prediction, details, and treatment
    return render_template(
        'result.html',
        prediction=f"Stroke Type: {stroke_type}",
        details=details,
        treatment=treatment
    )

def get_stroke_details_and_treatment(stroke_type):
    if stroke_type == "Ischemic Stroke":
        details = (
            "An ischemic stroke occurs when a blood clot blocks blood flow to the brain. "
            "Fatty deposits in arteries or other obstructions often cause this condition."
        )
        treatment = (
            "Treatment includes clot-dissolving medications like tPA and blood thinners. "
            "Lifestyle changes are vital to prevent recurrence."
        )
    elif stroke_type == "Hemorrhagic Stroke":
        details = (
            "A hemorrhagic stroke happens when a blood vessel bursts, leading to brain bleeding. "
            "High blood pressure or aneurysms are common causes."
        )
        treatment = (
            "Medications control bleeding and brain pressure, or surgery repairs vessels. "
            "Immediate medical care is essential to prevent complications."
        )
    elif stroke_type == "Transient Ischemic Attack (TIA)":
        details = (
            "TIA, or mini-stroke, is a temporary blockage of blood flow to the brain. "
            "Symptoms resolve quickly but signal future stroke risk."
        )
        treatment = (
            "Management includes lifestyle changes, medications, and addressing risk factors. "
            "Early medical evaluation can prevent a full stroke."
        )
    elif stroke_type == "Cryptogenic Stroke":
        details = (
            "A cryptogenic stroke has no identifiable cause despite thorough testing. "
            "It is common in younger individuals and may involve genetic factors."
        )
        treatment = (
            "Long-term monitoring and anticoagulants are used to reduce recurrence risks. "
            "Healthy habits and regular checkups are essential."
        )
    elif stroke_type == "Brain Stem Stroke":
        details = (
            "Brain stem strokes impact vital functions like breathing and heartbeat. "
            "They can severely impair movement, speech, and coordination."
        )
        treatment = (
            "Rehabilitation and specialized care are key to recovery. "
            "Timely intervention minimizes lasting damage."
        )
    elif stroke_type == "Cerebellar Stroke":
        details = (
            "A cerebellar stroke affects the part of the brain controlling balance. "
            "Symptoms include dizziness, coordination loss, and difficulty walking."
        )
        treatment = (
            "Treatment may involve clot removal and managing brain swelling. "
            "Prompt care ensures better recovery outcomes."
        )
    elif stroke_type == "Stroke Due to Aneurysm":
        details = (
            "This stroke occurs when an aneurysm bursts, causing brain bleeding. "
            "Symptoms include a sudden severe headache, nausea, and fainting."
        )
        treatment = (
            "Emergency surgery or coiling can stop bleeding and repair vessels. "
            "Quick action is critical to saving life and reducing damage."
        )
    else:
        details = "Unknown stroke type. Consult a healthcare professional for an accurate diagnosis."
        treatment = "No treatment information available. Seek immediate medical care."
    
    return details, treatment





if __name__ == '__main__':
    app.run(debug=True)

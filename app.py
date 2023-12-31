from flask import Flask,render_template,request
import pandas as pd
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
import os

app = Flask(__name__)
df = pd.read_csv(os.path.join('notebook', 'data', 'Bengaluru_House_Data.csv'))
locations = df['location'].unique().tolist()
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/form',methods = ['GET','POST'])
def predict():
    if request.method == "GET":
        return render_template('predict.html',locations = locations)

    else:
        balcony = int(request.form.get('balcony'))
        bath = int(request.form.get('bath'))
        size = int(request.form.get('size'))
        location = request.form.get('location')
        area_type = request.form.get('area_type')
        total_sqft = float(request.form.get('total_sqft'))

        data = CustomData(location,total_sqft,size,area_type,balcony,bath)

        df = data.get_data_as_dataframe()

        predict_pipeline = PredictPipeline()

        score = predict_pipeline.predict_price(df)

        print(score)

        
        return render_template('predict.html',locations = locations,result=score[0])
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
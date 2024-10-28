from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

from keras.models import load_model

model=load_model("models/fingerprint_classifier_4.h5")
main_model=load_model("models/lenet_model_4.h5")


from predict import model_predict_fc, predict_image
from compatibility import compatiblity_checking
from nutrition import nutritions_recommend

import json 


with open("secret-files.json",'r') as f:
    json_data=json.load(f)


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.secret_key = json_data["secretkey"]


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload_image():
    return render_template('predict.html')

@app.route('/predict_input', methods=['GET', 'POST'])
def predict():
    if 'file' not in request.files:
        flash('No file part')
        return render_template('predict.html')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return render_template('predict.html')
    if file :
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Here you can add your prediction code
        is_valid= is_valid_fingerprint(file_path)
        if is_valid:
            blood_group = get_blood_group(file_path)
            return render_template('prediction.html', image_url=url_for('static', filename=f'uploads/{filename}'), blood_group=blood_group)
        else:
            flash('Unable to classify the image. Please upload a correct fingerprint image.')
            return render_template('predict.html')
    else:
        flash('Allowed file types are png, jpg, jpeg, gif')
        return render_template('predict.html')

@app.route('/predict_result/<filename>',methods=['GET','POST'])
def prediction(filename):
    return render_template('prediction.html', filename=filename)

#predict_transfusion
@app.route('/predict_transfusion',methods=['GET','POST'])
def predict_transfusion():
    
    # if request.method == 'POST':
    #     blood_group = request.form['blood_group']
    #     session['donor_blood_group'] = blood_group
    #     return redirect(url_for('transfusion'))
    # else:
    #     blood_group=request.args.get('blood_group')
    #     session['donor_blood_group'] = blood_group
    #     return redirect(url_for('transfusion'))
    blood_group=request.args.get('blood_group')
    session['donor_blood_group'] = blood_group
    return redirect(url_for('transfusion'))
#predict_nutrition
@app.route('/predict_nutrition',methods=['GET','POST'])
def predict_nutrition():
    blood_group = request.args.get('blood_group')
    session['blood_group']=blood_group
    return redirect(url_for('nutrition'))


@app.route('/transfusion', methods=['GET', 'POST'])
def transfusion():
    donor_blood_group = session.get('donor_blood_group')
    recipient_blood_group = session.get('recipient_blood_group')
    return render_template('transfusion.html', donor_blood_group=donor_blood_group, recipient_blood_group=recipient_blood_group)


@app.route('/handle_donor', methods=['POST'])
def handle_donor():
    blood_group = request.form.get('donor_blood_group')
    fingerprint = request.files.get('donor_fingerprint')
    
    if blood_group:
        session['donor_blood_group']=blood_group
        return redirect(url_for('transfusion'))
    
    if fingerprint:
        filename = secure_filename(fingerprint.filename)
        if filename == "":
            flash('No selected file')
            return redirect(url_for('transfusion'))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        fingerprint.save(file_path)
        is_valid=is_valid_fingerprint(file_path)
        if is_valid:
            blood_group = get_blood_group(file_path)
            session['donor_blood_group']=blood_group
            return redirect(url_for('transfusion'))
        else:
            flash('Unable to classify the image. Please upload a correct fingerprint image.')
            return redirect(url_for('transfusion'))
    flash('Please provide either a blood group or a fingerprint image.')
    return redirect(url_for('transfusion'))

@app.route('/handle_recipient', methods=['POST'])
def handle_recipient():
    blood_group = request.form.get('recipient_blood_group')
    fingerprint = request.files.get('recipient_fingerprint')
    
    if blood_group:
        session['recipient_blood_group']=blood_group
        return redirect(url_for('transfusion'))
    
    if fingerprint:
        filename = secure_filename(fingerprint.filename)
        if filename == "":
            flash('No selected file')
            return redirect(url_for('transfusion'))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        fingerprint.save(file_path)
        is_valid=is_valid_fingerprint(file_path)
        if is_valid:
            blood_group = get_blood_group(file_path)
            session['recipient_blood_group']=blood_group
            return redirect(url_for('transfusion'))
        else:
            flash('Unable to classify the image. Please upload a correct fingerprint image.')
            return redirect(url_for('transfusion'))
    flash('Please provide either a blood group or a fingerprint image.')
    return redirect(url_for('transfusion'))

@app.route('/reset_donor', methods=['POST'])
def reset_donor():
    session.pop('donor_blood_group',None)
    return redirect(url_for('transfusion'))

@app.route('/reset_recipient', methods=['POST'])
def reset_recipient():
    session.pop('recipient_blood_group',None)
    return redirect(url_for('transfusion'))

@app.route('/check_compatibility', methods=['POST'])
def check_compatibility():
    donor_blood_group = session.get('donor_blood_group')
    recipient_blood_group = session.get('recipient_blood_group')
    if donor_blood_group is None or recipient_blood_group is None:
        return redirect(url_for('transfusion'))
    lst=compatiblity_checking(donor_blood_group,recipient_blood_group)
    
    if len(lst) == 2:
        return render_template('compatibility.html',result="Compatible", description=lst[1])
    else:
        return render_template("compatibility.html",result="Not Compatible")

    
@app.route("/compatibility")
def transfusion1():
    return render_template('compatibility.html')


# Nutrition recommendation
@app.route("/nutrition",methods=['GET','POSt'])
def nutrition():
    # blood_group=request.args.get('blood_group')
    blood_group = session.get('blood_group')
    return render_template("nutrition.html",blood_group=blood_group)

@app.route('/handle_input', methods=['POST'])
def handle_input():
    blood_group = request.form.get('blood_group')
    fingerprint = request.files.get('fingerprint')
    
    if fingerprint:
        filename = secure_filename(fingerprint.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        fingerprint.save(file_path)
        is_valid=is_valid_fingerprint(file_path)
        if is_valid:
            blood_group = get_blood_group(file_path)
        else:
            return redirect(url_for('nutrition'))
    
    if blood_group:
        session['blood_group'] = blood_group
        return redirect(url_for('nutrition'))
    
    flash('Please provide a valid input.')
    return redirect(url_for('nutrition'))


@app.route('/reset_input', methods=['POST'])
def reset_input():
    session.pop('blood_group', None)
    return redirect(url_for('nutrition'))

@app.route('/nutrition_recommendation', methods=['POST'])
def nutrition_recommendation():
    blood_group = session.get('blood_group')
    if blood_group is None:
        return redirect('nutrition')
    
    recommendations = nutritions_recommend(blood_group)
    if recommendations is None:
        return render_template('recommendation.html') 
    blood_group=blood_group.upper()
    return render_template('recommendation.html', blood_group=blood_group, foods_to_take=recommendations[0].split(','),foods_to_avoid=recommendations[1].split(','))



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')


def is_valid_fingerprint(image_path):
    if model_predict_fc(image_path,model) == 0:
        return 0
    return 1


def get_blood_group(image_path):
    return predict_image(main_model,image_path)

if __name__ == '__main__':
    app.run(debug=True)

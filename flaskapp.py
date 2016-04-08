import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

from freqest import process_names, get_not_popular_names

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def get_denorm_params(request):
    '''
    To maintain our sanities we allowed the interface to be agnostic of the
    mechanics of firstname and lastname db filtering. This was, to be specific,
    achieved by allowing normalized params to the API. If this is too confusing 
    check out the demo cod ein test.py and expose 
    '''
    
    first_name_start = int(request.form['first_name_start'])
    first_name_end = int(request.form['first_name_end'])
    last_name_start = int(request.form['last_name_start'])
    last_name_end = int(request.form['last_name_end'])
    first_name_threshold = float(request.form['first_name_threshold'])
    last_name_threshold = float(request.form['last_name_threshold'])

    first_name_range = (first_name_end - first_name_start)
    first_name_threshold_denorm = int(first_name_start + first_name_threshold * first_name_range)

    last_name_range = (last_name_end - last_name_start)
    last_name_threshold_denorm = int(last_name_start + float(1 - last_name_threshold) * last_name_range)
    
    params = {'first_name_threshold_denorm': first_name_threshold_denorm,
              'last_name_threshold_denorm': last_name_threshold_denorm}
    print params
    return params
    

    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route('/extract/difficult_names', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        params = get_denorm_params(request) 
        print params
        #print file.read()
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
	    not_popular_names = process_names(filepath, params)
	    os.remove(filepath)
            return str(not_popular_names)
        else:
            return 'This may not be a allowed file !'
            
@app.route('/extract/difficult_name/<name>', methods=['GET', 'POST'])
def is_the_name_not_popular(name):
    if request.method == 'POST':
        params = get_denorm_params(request) 
        firstname_count_threshold = params['first_name_threshold_denorm']
        lastname_rank_threshold = params['last_name_threshold_denorm']
        not_popular_names = get_not_popular_names([name], int(firstname_count_threshold),
                                              int(lastname_rank_threshold),
                                              write_to_file=False)
        if not_popular_names:
            return 'True'
        else:
            return 'False'
            
if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
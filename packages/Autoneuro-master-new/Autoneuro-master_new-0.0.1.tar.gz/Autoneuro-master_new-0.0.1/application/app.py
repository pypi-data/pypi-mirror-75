# test line added
# test demo team
from flask import Flask, render_template, request
from dataLoad.data_loader import DataGetter
from dataPreprocessing.preProcess import Preprocessor
from dataVisualization.visualization import DataVisualization
from modelTraining.classificationModels import ClassificationModelTuner
from prediction.predict import Prediction

app = Flask(__name__)

# All class instantiation
data_getter = DataGetter()
preprocessor = Preprocessor()
visuals = DataVisualization()
classification_model = ClassificationModelTuner()
prediction = Prediction()

@app.route('/', methods=['GET'])
def index():
    """
                              Method Name: index
                              Description: starting point of app.py code which redirect you to the index.html page
                              where you can select the format of data and upload it for further process
                              Output: index html page.
                              On Failure: Raise Exception

                              Written By: iNeuron Intelligence
                              Revisions: None

                              """
    return render_template('index.html')


@app.route('/load_data', methods=['POST'])
def load_data_from_source():
    """
                                Method Name: load_data_from_source
                                Description: describes data frame infomation as below:
                                             	The number of rows
                                             	The number of columns
                                             	Number of missing values per column and their percentage
                                             	Total missing values and it’s percentage
                                             	Number of categorical columns and their list
                                             	Number of numerical columns and their list
                                             	Number of duplicate rows
                                             	Number of columns with zero standard deviation and their list
                                                 Size occupied in RAM

                                Output: tables.html page
                                On Failure: Raise Exception

                                Written By: iNeuron Intelligence
                                Revisions: None

                                """
    file = request.files['filename'] #File can be obtained from request.files
    file_type = request.form['source'] #File Source can be obtained here
    data_getter = DataGetter()  #Class DataGetter object created
    global dataset    #Declare global variable
    data_getter = DataGetter()  # instantiation for genrating preprocessing logs
    dataset = data_getter.get_data(file_type, file)   #call get_data method, it will load the dataset into dataframe
    preprocessor = Preprocessor()  # instantiation for genrating preprocessing logs
    data_profile = preprocessor.get_data_profile(dataset)  #call get_data_profile
    # print(data.head())
    # render template tables.html with the respective dataset
    return render_template('tables.html', tables=[dataset.head(10).to_html(classes='data', header="True")],
                           columns=dataset.columns, profile=data_profile)


@app.route('/start_processing', methods=['POST'])
def start_processing():
    """
                                  Method Name: start_processing
                                  Description: receive the problem type and target column and unwanted columns from tables
                                  html page,generates the correlation table and different types of plots
                                  Output: charts.html page
                                  On Failure: Raise Exception

                                  Written By: iNeuron Intelligence
                                  Revisions: None

                                  """
    global problem_type,target_column
    problem_type = request.form.get('problem_type') #get problem_type, that can be classification or regression
    target_column = request.form['target_column']   #get target column name
    unwanted_cols = request.form['unwanted_cols']   #get unwanted columns
    global x, y
    preprocessor = Preprocessor()  # instantiation for genrating prediction logs
    x, y = preprocessor.preprocess(dataset, target_column,unwanted_cols)  #Calling preprocess method of preprocessor class
    hmap = visuals.correlation_heatmap(x)
    # problem_type = 'classification'
    return render_template('charts.html', hmap=hmap)


@app.route('/build_model', methods=['POST'])
def build_model():
    """
                                       Method Name: build_midel
                                       Description:generates the performance report of both the test and train data
                                       for both the classification and regression problems
                                       Output: model_report.html page in case if any thing fails inside the if condition
                                       then index.html age is returned
                                       On Failure: Raise Exception

                                       Written By: iNeuron Intelligence
                                       Revisions: None

                                       """
    #if problem type is classification, then get the best model with the classification report, else render index.html
    if problem_type == 'Classification':
        classification_model = ClassificationModelTuner()  # instantiation for genrating prediction log
        model_name, train_classification_report, test_classification_report = classification_model.get_best_model(x, y)
        return render_template('model_report.html', model_name=model_name,
                               train_report=train_classification_report[:len(train_classification_report) - 1],
                               test_report=test_classification_report[:len(test_classification_report) - 1])
    else:
        return render_template('index.html')


@app.route('/try_prediction', methods=['POST'])
def try_predict():
    """
                                       Method Name: try_predict
                                       Description: provides the html page for providing the data for prediction,give your prediction data here.
                                       Output: prediction.html page
                                       On Failure: Raise Exception

                                       Written By: iNeuron Intelligence
                                       Revisions: None

                                       """
    return render_template('prediction.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
                                       Method Name: predict
                                       Description: takes the prediction data from prediction.html page
                                       and perform same kind of transformation as the train  and test data set
                                       and provides prediction result
                                       Output: prediction_results.html page
                                       On Failure: Raise Exception

                                       Written By: iNeuron Intelligence
                                       Revisions: None

                                       """
    file = request.files['prediction_filename'] #get prediction file
    file_type = request.form['source']  #get file type
    data_getter = DataGetter() #declare object for DataGetter class
    global prediction_dataset
    prediction = Prediction()  # instantiation for genrating prediction log
    prediction_dataset = data_getter.get_data(file_type, file) #load file from get_data method
    preds = prediction.predict_results(prediction_dataset,target_column,dataset.columns)  #predict the result for the data loaded
    #render prediction_results.html with the prediction result
    return render_template('prediction_results.html', tables=[preds.to_html(classes='data', header="True")],
                           columns=preds.columns)


if __name__ == '__main__':
    app.run(debug=True)

import json
import argparse
from pathlib import Path
from sklearn.metrics import f1_score, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from joblib import dump

def _naive_bayes(args):
    """
    Executes Naive-Bayes classification based on the provided arguments.

    Args:
        args (argparse.Namespace): Command-line arguments containing the paths to the input data and the output accuracy
                                   file.

    Returns:
        None

    The function reads input data from a JSON file specified by the 'args.data' parameter. The data is expected to
    contain training and validation sets ('x_train', 'y_train', 'x_test', 'y_test'). It then trains a Gaussian NB
    model on the training data and evaluates its performance on the testing data. The accuracy score is calculated using
    the 'f1_score' function from the scikit-learn library.
    Finally, the accuracy score is written to an output file specified by 'args.f1-score'.

    Notes:
        - Ensure that the input data file is in JSON format and follows the expected structure.
        - The output accuracy file will be overwritten if it already exists.
    """
    with open(args.data) as data_file:
        data = json.load(data_file)

    data = json.loads(data)
    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']

    model = GaussianNB()

    param_grid = {'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]}

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='f1_weighted')

    grid_search.fit(x_train, y_train)
    best_model = grid_search.best_estimator_
    predictions = best_model.predict(x_test)
    f1 = f1_score(y_test, predictions, average='weighted')
    report = classification_report(y_test, predictions)
    best_params = grid_search.best_params_
    dump(best_model, args.model)

    with open(args.f1_score, 'w') as f1_score_file:
        f1_score_file.write(str(f1))

    with open(args.classification_report, 'w') as classification_report_file:
        classification_report_file.write(str(report))

    with open(args.best_params, 'w') as best_params_file:
        best_params_file.write(str(best_params))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Training of a NaiveBayes model for malicious '
                                                 'URL detection.')
    parser.add_argument('--data', type=str)
    parser.add_argument('--f1_score', type=str)
    parser.add_argument('--classification_report', type=str)
    parser.add_argument('--best_params', type=str)
    parser.add_argument('--model', type=str)

    args = parser.parse_args()

    Path(args.f1_score).parent.mkdir(parents=True, exist_ok=True)
    Path(args.classification_report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.best_params).parent.mkdir(parents=True, exist_ok=True)
    Path(args.model).parent.mkdir(parents=True, exist_ok=True)

    _naive_bayes(args)

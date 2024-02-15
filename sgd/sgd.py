import json
import argparse
from pathlib import Path
from sklearn.metrics import f1_score, classification_report
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from joblib import dump

def _sgd(args):
    """
    Executes Stochastic Gradient Descent (SGD) classification based on the provided arguments.

    Args:
        args (argparse.Namespace): Command-line arguments containing the paths to the input data, the output F1-score
                                   file, the classification report file and the best params file.

    Returns:
        None

    The function reads input data from a JSON file specified by the 'args.data' parameter. The data is expected to
    contain training and testing sets ('x_train', 'y_train', 'x_test', 'y_test'). It then trains an SGDClassifier on the
    training data and evaluates its performance on the testing data. The F1-score is calculated using the
    'f1_score' function from the scikit-learn library.
    Finally, the F1-score is written to an output file specified by 'args.f1-score', the best parameters are written
    in an output file specified by 'args.best_params' and the classification report is written in an output file 
    specified by 'args.classification_report.

    Notes:
        - Ensure that the input data file is in JSON format and follows the expected structure.
        - The output files will be overwritten if they already exists.
    """

    with open(args.data) as data_file:
        data = json.load(data_file)

    data = json.loads(data)
    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']

    model = SGDClassifier()
    param_grid = {
        'loss': ['hinge', 'log', 'perceptron'],
        'penalty': ['l1', 'l2', 'elasticnet'],
        'alpha': [0.0001, 0.001, 0.01],
        'learning_rate': ['constant', 'optimal', 'invscaling', 'adaptive'],
        'eta0': [0.01, 0.1, 1],
        'max_iter': [4000, 5000, 6000],  # Reducing the range for faster computation
        'n_jobs': [-1],
    }

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
    parser = argparse.ArgumentParser(description='Training of a Stochastic Gradient Descent classifier for malicious '
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

    _sgd(args)

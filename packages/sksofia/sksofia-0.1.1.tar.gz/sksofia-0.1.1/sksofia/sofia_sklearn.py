import sys
import logging
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from tempfile import NamedTemporaryFile
from subprocess import call
from sklearn.datasets import dump_svmlight_file
from sklearn.metrics import accuracy_score
from enum import Enum


class LearnerType(Enum):
    pegasos = "pegasos"
    passive_aggressive = "passive-aggressive"
    margin_perceptron = "margin-perceptron"
    romma = "romma"
    sgd_svm = "sgd-svm"
    least_mean_squares = "least-mean-squares"
    logreg = "logreg"
    logreg_pegasos = "logreg-pegasos"


class LoopType(Enum):
    stochastic = "stochastic"
    balanced_stochastic = "balanced-stochastic"
    roc = "roc"
    combined_ranking = "combined-ranking"
    combined_roc = "combined-roc"


class EtaType(Enum):
    basic = "basic"
    constant = "constant"
    pegasos = "pegasos"


def sofia_writer(X, y, file):
    def _add_ending_space(file):
        with open(file, 'r') as source:
            lines = [line.replace("\n", " \n") for line in source.readlines()]
        with open(file, "w") as target:
            target.writelines(lines)

    dump_svmlight_file(X, y, file, zero_based=False)
    # for some reason, we need a space at the end of the lines
    _add_ending_space(file)


def safe_sigmoid(x):
    "Numerically-stable sigmoid function."
    if x >= 0:
        z = np.exp(-x)
        return 1.0 / (1.0 + z)
    else:
        z = np.exp(x)
        return z / (1.0 + z)


def get_argument_string():
    arguments = [
        [
            "learner_type",
            "which linear model, loss function and optimization to use",
            ", ".join([e.value for e in LearnerType]),
            "logreg-pegasos"
        ],
        [
            "loop_type",
            "how to sample examples when training",
            ", ".join([e.value for e in LoopType]),
            "combined-roc"
        ],
        [
            "eta_type",
            "type of update for learning rate",
            ", ".join([e.value for e in EtaType]),
            "pegasos"
        ],
        [
            "lambda_reg",
            "value of lambda used for SVM regularization (for pegasos and sgd-svm)",
            "float >= 0",
            "0.1"
        ],
        [
            "passive_aggressive_c",
            "max step size for a single update with passive_aggressive algorithm",
            "float > 0",
            "0.1"
        ],
        [
            "passive_aggressive_lambda",
            "lambda for pegasos projection with passive_aggressive algorithm update",
            "float >= 0",
            "0 (no projection)"
        ],
        [
            "perceptron_margin_size",
            "width of margin for for peceptron with margins 1 is unregularized svm loss",
            "float",
            "1"
        ],
        [
            "iterations",
            "number of sgd steps to take",
            "int > 0",
            "100000",
        ],
        [
            "dimensionality",
            "the largest feature index + 1; max dimensionality of the model",
            "int > 0",
            "2^18"
        ],
    ]

    arg_labels = [
        "name: ",
        "description: ",
        "type: ",
        "default: "
    ]

    def arg_formatter(arg_info):
        zipped = zip(arg_labels, arg_info)
        return "\n".join(["%s %s" % (z[0], z[1]) for z in zipped])

    return "\n\n\n".join([arg_formatter(arg) for arg in arguments])
            
class SKSofia(BaseEstimator, ClassifierMixin):
    """
      a scikit-learn classifier wrapper for d. sculley's sofia-ml c++ library.
      supports all the options of sofia-ml and is compatible with any kind of
      python serialization. 

      see sofia-ml documentation for more information on the particular options
      `sofia-ml --help` or https://code.google.com/archive/p/sofia-ml/

      arguments: 
      %s
    """ % get_argument_string()
    
    def __init__(
        self,
        learner_type="logreg-pegasos",
        loop_type="combined-roc",
        lambda_reg=0.1,
        passive_aggressive_c=0.1,
        passive_aggressive_lambda=0,
        no_bias_term=False,
        iterations=100000,
        eta_type="pegasos",
        dimensionality=2 ** 18,
        perceptron_margin_size=1,
    ):
        """
          initialize a sksofia classifier
          arguments:
          %s
        """ % get_argument_string()

        self.learner_type = learner_type
        self.loop_type = loop_type
        self.lambda_reg = 0.1
        self.passive_aggressive_c = passive_aggressive_c
        self.passive_aggressive_lambda = passive_aggressive_lambda
        self.no_bias_term = no_bias_term
        self.iterations = iterations
        self.eta_type = eta_type
        self.dimensionality = dimensionality
        self.perceptron_margin_size = perceptron_margin_size

        self.model_params = None

    def _build_train_command(self, training_file, model_file):
        cmd = [
            "sofia-ml",
            f"--learner_type {self.learner_type}",
            f"--loop_type {self.loop_type}",
            f"--lambda {self.lambda_reg} ",
            f"--iterations {self.iterations}",
            f"--passive_aggressive_c {self.passive_aggressive_c}",
            f"--passive_aggressive_lambda {self.passive_aggressive_lambda}",
            f"--eta_type {self.eta_type}",
            f"--dimensionality {self.dimensionality}",
            f"--perceptron_margin_size {self.perceptron_margin_size}",
            f"--training_file {training_file}",
            f"--model_out {model_file}",
            "--no_bias_term" if self.no_bias_term else "",
        ]

        training_command = " ".join(cmd)
        logging.info("training sofia model with: %s" % training_command)

        return training_command

    def fit(self, X, y):
        with NamedTemporaryFile() as training_file:
            sofia_writer(X, y, training_file.name)

            with NamedTemporaryFile() as model_file:
                training_command = self._build_train_command(training_file.name, model_file.name)
                call(training_command, shell=True)

                with open(model_file.name, mode='rb') as file:
                    self.model_params = file.read()

        return self

    def _build_predict_command(self, predict_file, model_file, results_file):
        cmd = [
            "sofia-ml",
            f"--test_file {predict_file}",
            f"--results_file {results_file}",
            f"--model_in {model_file}",
        ]

        predict_command = " ".join(cmd)
        logging.info("predicting using sofia model using command: %s" % predict_command)

        return predict_command

    def _predict(self, X, y=None):

        with NamedTemporaryFile() as predict_file:
            sofia_writer(X, np.zeros(X.shape[0]), predict_file.name)

            with NamedTemporaryFile() as model_params_file:
                with open(model_params_file.name, mode="wb") as file:
                    file.write(self.model_params)

                with NamedTemporaryFile() as results_file:
                    predict_command = self._build_predict_command(
                        predict_file.name, model_params_file.name, results_file.name
                    )
                    call(predict_command, shell=True)

                    pred_prob = pd.read_csv(results_file.name, sep="\t", names=["pred", "true"])
                    logging.debug(pred_prob)

                    return np.nan_to_num(
                        np.array([safe_sigmoid(x) for x in pred_prob["pred"].values])
                    )

    def predict(self, X, y=None):
        preds = self._predict(X, y)
        return np.array([1 if x >= 0.5 else 0 for x in preds])

    def predict_proba(self, X, y=None):
        probs = self._predict(X, y)
        return np.array([[1.0 - p, p] for p in probs])

    def decision_function(self, X, y=None):
        return self._predict(X, y)

    def score(self, X, y, sample_weight=None):
        y_preds = self.predict(X)
        return accuracy_score(y, y_preds, normalized=True)
    
def main():
    from sklearn.datasets import load_iris, fetch_20newsgroups_vectorized
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_auc_score
    import pprint

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
        level="INFO",
    )

    X, yt = fetch_20newsgroups_vectorized(return_X_y=True)
    y = np.array([1 if y == 1 else 0 for y in yt])

    skf = StratifiedKFold(n_splits=3)

    methods = {}

    for learner in LearnerType:
        for loop in LoopType:
            aucs = []
            for train, test in skf.split(X, y):
                clf = SKSofia(loop_type=loop.value, learner_type=learner.value)
                clf.fit(X[train], y[train])

                probas = clf.predict_proba(X[test])
                auc = roc_auc_score(y[test], probas[:, 1])

                logging.info("%s %s AUC: %0.3f" % (learner.value, loop.value, auc))
                aucs.append(auc)

            methods["%s %s" % (learner.value, loop.value)] = np.mean(aucs)

    for loop, aucs in sorted(methods.items(), key=lambda x: x[1]):
        print("%s AUC: %0.4f" % (loop, aucs))

        
if __name__ == "__main__":
    main()

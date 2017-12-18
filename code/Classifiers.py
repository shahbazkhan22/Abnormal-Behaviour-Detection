from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression as lr
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import numpy as np

class Classifiers(object):

    def __init__(self,train_data,train_labels,hyperTune=True):
        self.train_data=train_data
        self.train_labels=train_labels
        self.construct_all_models(hyperTune)

    def construct_all_models(self,hyperTune):
        if hyperTune:
            self.models={'SVM':[SVC(kernel='linear',probability=True),dict(C=np.arange(0.01, 2.01, 0.2))],\
                         'LogisticRegression':[lr(),dict(C=np.arange(0.1,3,0.1))],\
                         'KNN':[KNeighborsClassifier(),dict(n_neighbors=range(1, 100))],}
            for name,candidate_hyperParam in self.models.items():
                self.models[name] = self.train_with_hyperParamTuning(candidate_hyperParam[0],name,candidate_hyperParam[1])
            print ('\nTraining process finished\n')

    def train_with_hyperParamTuning(self,model,name,param_grid):
        grid = GridSearchCV(model, param_grid, cv=10, scoring='accuracy', n_jobs=-1)
        grid.fit(self.train_data, self.train_labels)
        print(
            '\nThe best hyper-parameter for -- {} is {}, the corresponding mean accuracy through 10 Fold test is {} \n'\
            .format(name, grid.best_params_, grid.best_score_))

        model = grid.best_estimator_
        train_pred = model.predict(self.train_data)
        print('{} train accuracy = {}\n'.format(name,(train_pred == self.train_labels).mean()))
        return model

    def prediction_metrics(self,test_data,test_labels,name):
        print('{} test accuracy = {}\n'.format(name,(self.models[name].predict(test_data) == test_labels).mean()))
        prob = self.models[name].predict_proba(test_data)
        print('{} AUC of ROC is {}\n'.format(name,roc_auc_score(test_labels.reshape(-1),prob[:,1])))
        fpr, tpr, thresholds = roc_curve(test_labels.reshape(-1), prob[:,1], pos_label=1)
        plt.figure(figsize=(20,5))
        plt.plot(fpr,tpr)
        plt.ylim([0.0,1.0])
        plt.ylim([0.0, 1.0])
        plt.title('ROC of {}'.format(name))
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.grid(True)
        plt.show()


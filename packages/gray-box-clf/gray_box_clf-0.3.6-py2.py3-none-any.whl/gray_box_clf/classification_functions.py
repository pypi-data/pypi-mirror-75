##
import sklearn.metrics as metrics
import pandas as pd
import pandas as pa
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2, f_classif
import numpy as np
from scipy.signal import savgol_filter as sgf
from matplotlib import pyplot as plt
from sklearn.naive_bayes import GaussianNB
import numpy as np
from sklearn.preprocessing import minmax_scale
import pandas as pd
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, precision_recall_curve, accuracy_score
from sklearn.neural_network import MLPClassifier
from scipy import interp
from sklearn.utils import shuffle
import pandas as pa
import string
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report, accuracy_score, recall_score, precision_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import preprocessing
from xgboost import XGBClassifier
from sklearn.feature_selection import SelectKBest, chi2, f_classif
import numpy as np
from scipy.signal import savgol_filter as sgf
from matplotlib import pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, NuSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly as ply
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.model_selection import cross_validate
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import time
import matplotlib.ticker as mticker
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, f_classif
from scipy.signal import savgol_filter as sgf
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, log_loss, recall_score, roc_auc_score
from sklearn.model_selection import LeaveOneOut
# cllassifiers import
from sklearn.metrics import accuracy_score, log_loss, recall_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
import catboost as cb
from sklearn.ensemble import RandomForestClassifier as RF
from lightgbm import LGBMClassifier
from sklearn.model_selection import GridSearchCV, KFold, LeaveOneOut, train_test_split, LeaveOneGroupOut
from sklearn.datasets import make_classification
# np.random.seed(101)
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from pyod.models.mcd import MCD
from sklearn.utils import shuffle

defualt_classifers = [{"clf": LinearDiscriminantAnalysis(), "name": "LDA"},
                      {"clf": GaussianNB(), "name": "Naiev_Bayes_Gaussian"},
                      {"clf": SVC(gamma=0.01, probability=True, C=1, kernel='linear'), "name": "SVM_linear"}]


def feature_selection_and_derivative(df, labels_columns_name, featur_selection_type=f_classif, selected_features_num='all', derivative=True,
                                     dev_wind=5, dev_smooth=2, dev_level=2, plot=True):
    """
       this function return selected features after derivative using multi_feature selection methods.

       :param df: data fram of the data without labels
       :param labels_columns_name: labels array as pandas series
       :param featur_selection_type: "chi2", "f_classif" or "KL"
       :param selected_features_num: in case using all the features set "all"
       :param derivative: "True" if you want derivative, "False" without derivative (not wrok in "KL")
       :param dev_wind: should be odd number.
       :param dev_smooth: number of smoothing points<dev_wind
       :param dev_level: derivative level(1, 2, 3...)
       :param plot: plot the return data.

       :return:
         (1) X_best: best features as numpy array
         (2) best_features: list of the best features were slected
         (3) best_features_wighet: numpy array of the features wighets
         (4) best_features_wighet_df_sorted: pandas data frame of features wighets sorted
         (5) df_Best_inclod_labels: pandas data frame with the best featuers
       example:
       X_best, best_features, best_features_wighet, best_features_wighet_df_sorted,df_Best_inclod_labels =
       feature_selection_and_derivative(df, labels_columns_name="labels",
        featur_selection_type=f_classif,selected_features_num=3,
         derivative=True, dev_wind=3, dev_smooth=2, dev_level=2, plot=False)
       """

    from sklearn.feature_selection import SelectKBest, chi2, f_classif
    # df = df.sample(frac=1)
    y = df[labels_columns_name]
    X = df.drop(labels_columns_name, axis=1)
    X_df = X.copy()
    Orig_features = list(X.columns.values)  # put the features in list for pandas

    if derivative and featur_selection_type == "KL":
        X = (sgf(X, dev_wind, dev_smooth, deriv=dev_level, mode='nearest'))  # apply derivatve and smoothing
        X = pd.DataFrame(X, columns=Orig_features)
        mean_KL, results, Best_X_df, df_Best_inclod_labels, sorted_results = kl_divergence_means(X, y,
                                                                                                 number_of_features=selected_features_num)
        X_best = Best_X_df.values
        best_features = Best_X_df.columns
        best_features_wighet = results["mean_KL_divregence"].values
        best_features_wighet_df = pd.DataFrame(best_features_wighet, columns=["f_score"])
        best_features_wighet_df["features"] = list(X_df.columns)
        if selected_features_num == "all":
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False)
        else:
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False).head(selected_features_num)

    elif featur_selection_type == "KL":
        mean_KL, results, Best_X_df, df_Best_inclod_labels, sorted_results = kl_divergence_means(X, y,
                                                                                                 number_of_features=selected_features_num)
        X_best = Best_X_df.values
        best_features = Best_X_df.columns
        best_features_wighet = results["mean_KL_divregence"].values
        best_features_wighet_df = pd.DataFrame(best_features_wighet, columns=["f_score"])
        best_features_wighet_df["features"] = list(X_df.columns)
        if selected_features_num == "all":
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False)
        else:
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False).head(selected_features_num)

    if derivative and featur_selection_type == "f_classif":
        X = (sgf(X, dev_wind, dev_smooth, deriv=dev_level, mode='nearest'))  # apply derivatve and smoothing
        selectK = SelectKBest(eval(featur_selection_type), k=selected_features_num)
        selectK.fit(X, y)
        X_best = selectK.transform(X)
        best_features_wighet = selectK.scores_
        best_features_wighet_df = pd.DataFrame(best_features_wighet, columns=["f_score"])
        best_features_wighet_df["features"] = list(df.drop(labels_columns_name, axis=1).columns)
        if selected_features_num == "all":
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False)
            Best_X_df = X_df.loc[:, list(best_features_wighet_df["features"])]
        else:
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False).head(selected_features_num)
            Best_feat = best_features_wighet_df_sorted["features"].iloc[:selected_features_num]
            Best_X_df = X_df.loc[:, list(Best_feat.values)]
        df_Best_inclod_labels = pd.concat([Best_X_df, y], axis=1)
        X = pa.DataFrame(X, columns=Orig_features)  # convert the X inputs into df
        best_features = X.columns[selectK.get_support()]

    elif featur_selection_type == "f_classif":
        selectK = SelectKBest(eval(featur_selection_type), k=selected_features_num)
        selectK.fit(X, y)
        X_best = selectK.transform(X)
        best_features_wighet = selectK.scores_
        best_features_wighet_df = pd.DataFrame(best_features_wighet, columns=["f_score"])
        best_features_wighet_df["features"] = list(df.drop(labels_columns_name, axis=1).columns)
        if selected_features_num == "all":
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False)
            Best_X_df = X_df.loc[:, list(best_features_wighet_df["features"])]
        else:
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False).head(selected_features_num)
            Best_feat = best_features_wighet_df_sorted["features"].iloc[:selected_features_num]
            Best_X_df = X_df.loc[:, list(Best_feat.values)]
        df_Best_inclod_labels = pd.concat([Best_X_df, y], axis=1)
        X = pa.DataFrame(X, columns=Orig_features)  # convert the X inputs into df
        best_features = X.columns[selectK.get_support()]

    if derivative and featur_selection_type == "chi2":
        X = abs(sgf(X, dev_wind, dev_smooth, deriv=dev_level, mode='nearest'))  # apply derivatve and smoothing
        selectK = SelectKBest(eval(featur_selection_type), k=selected_features_num)
        selectK.fit(X, y)
        X_best = selectK.transform(X)
        best_features_wighet = selectK.scores_
        best_features_wighet_df = pd.DataFrame(best_features_wighet, columns=["f_score"])
        best_features_wighet_df["features"] = list(df.drop(labels_columns_name, axis=1).columns)
        if selected_features_num == "all":
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False)
            Best_X_df = X_df.loc[:, list(best_features_wighet_df["features"])]
        else:
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False).head(selected_features_num)
            Best_feat = best_features_wighet_df_sorted["features"].iloc[:selected_features_num]
            Best_X_df = X_df.loc[:, list(Best_feat.values)]
        df_Best_inclod_labels = pd.concat([Best_X_df, y], axis=1)

        X = pa.DataFrame(X, columns=Orig_features)  # convert the X inputs into df
        best_features = X.columns[selectK.get_support()]

    elif featur_selection_type == "chi2":
        selectK = SelectKBest(eval(featur_selection_type), k=selected_features_num)
        selectK.fit(X, y)
        X_best = selectK.transform(X)
        best_features_wighet = selectK.scores_
        best_features_wighet_df = pd.DataFrame(best_features_wighet, columns=["f_score"])
        best_features_wighet_df["features"] = list(df.drop(labels_columns_name, axis=1).columns)
        if selected_features_num == "all":
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False)
            Best_X_df = X_df.loc[:, list(best_features_wighet_df["features"])]
        else:
            best_features_wighet_df_sorted = best_features_wighet_df.sort_values(by="f_score", ascending=False).head(selected_features_num)
            Best_feat = best_features_wighet_df_sorted["features"].iloc[:selected_features_num]
            Best_X_df = X_df.loc[:, list(Best_feat.values)]
        df_Best_inclod_labels = pd.concat([Best_X_df, y], axis=1)

        X = pa.DataFrame(X, columns=Orig_features)  # convert the X inputs into df
        best_features = X.columns[selectK.get_support()]

    if plot:
        plt.plot(X_best.T)
        plt.show()
    return X_best, best_features, best_features_wighet, best_features_wighet_df_sorted, df_Best_inclod_labels


if __name__ == "__main__":
    df = pd.read_csv(
        'C:\\Users\\Adam Hamody Agbaria\\PycharmProjects\\ERandONCO\\DATA\\WBC-LOW_PURE_refrence.csv')  # .iloc[:, 1:].replace([1, 2], [0, 1]) #infectionvs controls
    df = df.loc[df['analysis'] != 'VIR_onc']
    df = df.loc[df['analysis'] != 'BAC_onc']
    df = df.replace([1, 2], [0, 1])
    df = df.drop(columns=['analysis'])
    X_best, best_features, best_features_wighet = feature_selection_and_derivative(df, labels_columns_name='LABEL', featur_selection_type="KL",
                                                                                   selected_features_num=120, derivative=True, dev_wind=13,
                                                                                   dev_smooth=2, dev_level=2)


def creat_data(df, num_obs, class_name, labels_column_name, seed, plot_new_df=True):
    """this function for creat  data based on true one
    input:
        (1) data frame "pandas"
        (2) number of the new observation (mesearments) that you want to creat
        (3) list of class with the name of the ['class1', 'class2...]
        (4) plot the new data if 'true'

    output:
        (1) the new data as pandas df
        (2) covariens
        (3) mean
        """

    np.random.seed(seed)
    df = df.loc[df[labels_column_name] == class_name]
    df = df.drop(columns=[labels_column_name])
    features_names = list(df.columns.values)  # put the features name in list
    covar, mean = df.cov(), df.mean(0)
    x = np.random.multivariate_normal(mean.values, covar.values, num_obs)  # creat the new data based on the observation set
    new_df = pd.DataFrame(abs(x), columns=[features_names])

    if plot_new_df:
        plt.plot(new_df.T.values)
        plt.show()
    return new_df, mean, covar


if __name__ == "__main__":
    import numpy as np
    import pandas as pd

    df = pd.DataFrame()
    df['class_1'] = [_ for _ in range(0, 10)]
    df['class_2'] = [_ for _ in range(100, 110)]
    df['labels'] = np.random.choice(['good', 'bad'], df.shape[0])

    new_df, mean, cov = creat_data(df, num_obs=5, class_name='good', labels_column_name='labels', seed=100, plot_new_df=True)


def convert_to_binary(df, labels_column_name, input_classes, output_classes):
    df = df[labels_column_name].replace([1, 2], [0, 1])
    return df


def classifcation(X, y, leave_one_out=True, split_CV_train=0.8, classifier_name=GaussianNB(), average='macro', labels=[0, 1, 2]):
    """this function for obtain classification report for spesific classifier
        input:
            (1) X: features data as numpy
            (2) y: labels as number form "0" as numpy
            (3) leave_one_out: if true use it false use split_CV_train (train samples rate)
            (4) classifer type
            (5) type of average in order to caluclate the recall and prection average=['binary', 'micro', 'macro','whigted']
            (6) labels order, the first one consedered as "positive"

        output:
            confusion matrix, y_prediction, accuracy, recall, precision
            """
    if leave_one_out:
        from sklearn.model_selection import LeaveOneOut
        loo = LeaveOneOut()
        loo.get_n_splits(X)
        y_hat = []
        for train_index, test_index in loo.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            clf = classifier_name.fit(X_train, y_train)
            y_hat.append(clf.predict(X_test))
            y_test = y
    # elif k_folds:
    #     from sklearn.model_selection import KFold
    #     kf = KFold(n_splits=num_folds_out)
    #     kf.get_n_splits(X)
    #     y_hat = []
    #     for train_index, test_index in kf.split(X):
    #         X_train, X_test = X[train_index], X[test_index]
    #         y_train, y_test = y[train_index], y[test_index]
    #         clf = classifier_name.fit(X_train, y_train)
    #         y_hat.append(clf.predict(X_test))

    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=split_CV_train, test_size=1 - split_CV_train, shuffle=False,
                                                            random_state=2015)
        clf = classifier_name.fit(X_train, y_train)
        y_hat = clf.predict(X_test)

    con_matrix = metrics.confusion_matrix(y_test, y_hat, labels=labels)
    accuracy = metrics.accuracy_score(y_test, y_hat)
    # recall = metrics.recall_score(y, y_hat, labels, average=average)
    # precision = metrics.precision_score(y, y_hat, labels, average=average)
    sen = float(con_matrix[1][1] / (con_matrix[1][1] + con_matrix[1][0]))
    spec = float(con_matrix[0][0] / (con_matrix[0][0] + con_matrix[0][1]))
    ppv = float(con_matrix[1][1] / (con_matrix[1][1] + con_matrix[0][1]))
    npv = float(con_matrix[0][0] / (con_matrix[0][0] + con_matrix[1][0]))
    auc = metrics.roc_auc_score(y_test, y_hat)
    # auc_par = metrics.roc_curve(y, y_hat, pos_label=1)

    report = {'AUC': auc, 'accuracy': accuracy, 'sens': sen, 'spec': spec, 'ppv': ppv, 'npv': npv}
    return report, con_matrix, y_hat


def sen_spe_to_else(sen, spe, postive_label_num, neg_label_num, classifier_name):
    """ this function return accuracy, ppv and npv and confusion matrix when you se the sen(as floaut) and spe(as floaut) and
     number of samples for eaech label"""
    tp, fp = int(sen * postive_label_num), int(postive_label_num - sen * postive_label_num)
    fn, tn = int(neg_label_num - spe * neg_label_num), int(spe * neg_label_num)
    con_mat = np.array([[tp, fp], [fn, tn]])
    acc = (tp + tn) / (tp + fp + fn + tn)
    ppv = tp / (tp + fn)
    npv = tn / (tn + fp)

    dic = {"cls_name": classifier_name, 'acc': round(acc, 2), 'sen': sen, "spe": spe, 'ppv': round(ppv, 2), 'npv': round(npv, 2)}
    return dic, con_mat


if __name__ == '__main__':
    dic, con_mat = sen_spe_to_else(sen=0.8, spe=0.81, postive_label_num=71, neg_label_num=50)


def grid_search_hyperparameters_featureselection(X, y, classifier=xgb.XGBClassifier(), featur_selection_type=f_classif, derivative=True, dev_wind=13,
                                                 dev_smooth=2,
                                                 dev_level=2):
    """this function return table that contain best parameters for each slected feature
    in_put:
     X- data features columns as matrix (float type)
     y- labels (vector of numbers)
     classifier- classifier python link
     derivative- drivative after feature selection!! True or False
     derivateve and smoothing parameters (using Solvsky-Golay)- dev_wind/dev_smooth/dev_level

    out_put:
      repoer table

     """

    num_est = []
    depth_max = []
    score = []
    feature_numbers = []
    kk = [_ for _ in range(1, X.shape[1])]

    for K in kk:
        X_sel = SelectKBest(featur_selection_type, k=K).fit_transform(X, y)
        if derivative:
            X_sel = abs(sgf(X_sel, dev_wind, dev_smooth, deriv=dev_level, mode='nearest'))
        else:
            X_sel = X_sel

        # CLASSIFICATION#

        params = {
            'max_depth': [_ for _ in range(2, 100)],
            'n_estimators': [_ for _ in range(10, 1000)]
        }

        model = GridSearchCV(classifier, params,
                             scoring="roc_auc", cv=5)

        grid_obj = model.fit(X_sel, y)
        feature_numbers.append(K)
        num_est.append(model.best_params_['n_estimators'])
        depth_max.append(model.best_params_['max_depth'])
        score.append(model.best_score_)

    report = pd.DataFrame()
    report['num_features'] = feature_numbers
    report['n_estimators'] = num_est
    report['max_trees_depth'] = depth_max
    report['score_AUC'] = score

    return report


def roc_and__det_curves_for_multi_calssifiers(X, y, clfs=defualt_classifers, name_of_the_labe="Non", feature_selection_type="None",
                                              diff="2nd_derivative", itirations_rate=0.97, plot=True):
    """ return plot of roc curvs for 12 classifiers
    X: data as nump
    y: labels
    """
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'bold',
            'size': 30,
            'fontname': 'Times New Roman'
            }

    X, y = X[y != 2], y[y != 2]
    n_samples, n_features = X.shape

    # Add noisy features
    random_state = np.random.RandomState(0)
    X = np.c_[X, random_state.randn(n_samples, n_features)]

    if plot:
        fig_1, (x1, x2) = plt.subplots(2, figsize=(20, 17))
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)

    MRecall = []
    auc_dict = {}

    for m in clfs:
        random_state = 100
        for j in range(42, random_state):
            X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.70,
                                                                test_size=0.30, shuffle=True,
                                                                random_state=j)
            classifier = m['clf']
            probas_ = classifier.fit(X_train, y_train).predict_proba(X_test)
            fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            y_scores = classifier.predict_proba(X_test)

        if itirations_rate == "all":
            mean_tpr = np.mean(tprs, axis=0)
        else:
            mean_tpr = np.quantile(tprs, itirations_rate, axis=0)
        MRecall.append(mean_tpr)

        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        auc_dict[m['name']] = mean_auc

        if plot:
            x1.plot(mean_fpr, mean_tpr, label='%s(AUC = %0.2f)' % (m['name'], mean_auc), lw=2, alpha=.8)

            x2.plot(mean_fpr, 1 - mean_tpr, label=m['name'], lw=2, alpha=.8)
            x2.set_xscale('log')
            x2.set_yscale('log')

    if plot:
        x1.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Random chance ', alpha=.8)
        x1.set_xlim([-0.05, 1.05])
        x1.set_ylim([-0.05, 1.05])
        x1.set_xlabel('1-Specificity', fontdict=font)
        x1.set_ylabel('Sensitivity', fontdict=font)
        x1.set_title("ROC Curve |" + name_of_the_labe + "| feature_selection= " + feature_selection_type + ", diff= " + diff, fontdict=font)
        x1.legend(loc="lower right", fontsize="large")
        x1.legend(loc="lower right", fontsize=16)
        x1.tick_params(labelsize=12)
        x2.tick_params(labelsize=12)
        x2.plot([0, 1], [0, 1], '--r')

        ticks_to_use = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.6, 1]
        x2.set_xticks(ticks_to_use)
        x2.set_yticks(ticks_to_use)

        x2.xaxis.set_major_formatter(mticker.ScalarFormatter())
        x2.yaxis.set_major_formatter(mticker.ScalarFormatter())
        x2.set_xlabel('False posotive rate (1 - specificity)', fontdict=font)
        x2.set_ylabel('False negative rate (1 - sensitivty)', fontdict=font)
        x2.set_title("DET Curve|" + name_of_the_labe + "| feature_selection= " + feature_selection_type + ", diff= " + diff, fontdict=font)
        x2.legend(loc=3, fontsize="large")
        x2.legend(loc=3, fontsize=16)

        plt.show()
    return auc_dict


##
def classification_competition(X, y, classifiers_list, cv, name_of_the_labe, feature_selection_type="None", diff="2nd_derivative"):
    """ This function return the accuracy score of a seviral classifier and plot a 'horizntal bar' that present.
    inputs:
       1.X: is the data as numpy
       2.y: the labels as pandas series or numpy
       3.classification_list: is list of dicunars wher include the classifirs function and thir names, for example:
         classification_list=[{"clf": SVC(), "nmae": "svm"}, {"clf":XGBoostClassifier(), "name": "XGBoost"}]
       4.cv: for K_fold you can put the number of the folds that you want or using 'LeaveOneOut'
       5.name_of_the_labe: in order to plot a figure with relevant title must write the name og=f the labels as string
       6. scoring: tpe of scoring, defoalt is "accuracy "
    output:
    #polting a hirzontal bar of the accurcy scores for each classifer in the list
    #return a list (pandas series) for the calssifers scores.
    """
    scoring = ['accuracy']
    log_cols = ["Classifier", "macro average Recall", "Log Loss"]
    log = pd.DataFrame(columns=log_cols)
    Acc = []
    clf_name = []
    for clf_list in classifiers_list:
        recall = cross_validate(clf_list["clf"], X, y, scoring=scoring,
                                cv=cv, return_train_score=False)
        name = clf_list["name"]
        Accuracy = np.quantile(recall['test_accuracy'], 0.97, axis=0)

        ll = 1 - Accuracy

        log_entry = pd.DataFrame([[name, Accuracy * 100, ll]], columns=log_cols)
        log = log.append(log_entry)
        Acc.append(Accuracy)
        clf_name.append(name)

    results = pd.DataFrame(Acc, index=[_["name"] for _ in classifiers_list])
    best_clf = results.sort_values(by=0).tail(1)
    sns.set_color_codes("muted")
    sns.barplot(x='macro average Recall', y='Classifier', data=log, color="b")
    plt.xlabel('accuracy %')
    plt.xticks(np.arange(0, 100, step=10))
    plt.title(name_of_the_labe + "| feature_selection= " + feature_selection_type + ", diff= " + diff + "\n" + "best_classifier: " + str(
        best_clf.index.values[0] + ": " + str(np.round(best_clf.values[0][0] * 100)) + "%")
              )
    plt.show()
    return results


def det_Curve(fps, fns):
    """
    Given false positive and false negative rates, produce a DET Curve.
    The false positive rate is assumed to be increasing while the false
    negative rate is assumed to be decreasing.
    """
    axis_min = min(fps[0], fns[-1])
    fig, ax = plt.subplots()
    plt.plot(fps, fns)
    plt.yscale('log')
    plt.xscale('log')
    ticks_to_use = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]
    # ax.get_xaxis().set_major_formatter(plt.ticker.ScalarFormatter())
    # ax.get_yaxis().set_major_formatter(plt.ticker.ScalarFormatter())
    ax.set_xticks(ticks_to_use)
    ax.set_yticks(ticks_to_use)
    plt.axis([0.001, 50, 0.001, 50])


from math import log2


def kl_divergence(X_df, y_df, number_of_features="all"):
    """
    This function select best features using Kullback–Leibler (KL) divergence, where the best feature is the hightes
    KL divergence value.

    :param X_df: data fram of the data without labels
    :param y_df: labels array as pandas series
    :param number_of_features: how much fature you want, default="all"
    :return:
      (1) list of the KL average, where clauclated by, 0.5 * [KL(Q||P)+KL(P||Q)]
      (2) pandas data frame of the KL values per the features names and index
      (3) pandas data frame of the data with the best features (best_X)
      (4) pandas data frame of the data with the best features include the labels (best_df)
      (5) pandas data frame of the KL values per the features names and index sorted by KL values descendly

    example:
    mean_KL, results, Best_X_df, df_Best_inclod_labels, results_sorted = kl_divergence(X, y, number_of_features="all")
    """
    # data preparin
    features = list(X_df.columns.values)

    X = X_df.values
    y = y_df.values
    uniq_lab = np.unique(y)
    ix_lab_1 = np.argwhere(uniq_lab[0] == y)
    ix_lab_2 = np.argwhere(uniq_lab[1] == y)

    X_lab_1 = X[ix_lab_1, :]
    X_lab_2 = X[ix_lab_2, :]
    count = []
    mean_KL = []
    for j in range(0, X.shape[1]):

        p = X_lab_1[:, :, j]
        q = X_lab_2[:, :, j]

        if len(q) < len(p):
            size = len(q)
            ansize = len(q)
        else:
            size = len(p)
            ansize = len(p)

        np.random.seed(100000000)
        equal_len = list((np.random.randint(0, size, ansize)))
        p = p[equal_len]
        sid_p = np.array(list(p * np.log2(abs(p / q))))
        sid_q = np.array(list(q * np.log2(abs(q / p))))

        mean_div = abs(np.sum(0.5 * (sid_p + sid_q)))
        mean_KL.append((mean_div))
        count.append(j)

    results = pd.DataFrame(count, columns=["features_index"])
    results["features"] = features
    results["mean_KL_divregence"] = mean_KL
    results_sorted = results.sort_values(by="mean_KL_divregence", ascending=False)

    if number_of_features == "all":
        Best_X_df = X_df.loc[:, list(results_sorted["features"])]
    else:
        Best_feat = results_sorted["features"].iloc[:number_of_features]
        Best_X_df = X_df.loc[:, list(Best_feat.values)]
    df_Best_inclod_labels = pd.concat([Best_X_df, y_df], axis=1)
    return mean_KL, results, Best_X_df, df_Best_inclod_labels, results_sorted


if __name__ == "__main__":
    df = pd.DataFrame(np.random.randn(300, 10), columns="a b c d e f g h i j".split())
    bac_size = int(df.shape[0] * 0.7)
    vir_size = int(df.shape[0] * 0.3)
    df["labels"] = ["Bac" for _ in range(0, bac_size)] + ["Vir" for _ in range(bac_size, bac_size + vir_size)]
    X = df.select_dtypes(include="float")
    y = df["labels"]

    then = time.time()
    mean_KL, results, Best_X_df, df_Best_inclod_labels, results_sorted = kl_divergence(X, y, number_of_features="all")
    now = time.time()

    print(mean_KL)
    print(results)
    print(Best_X_df)
    print('spent time:' + str(now - then))


def kl_divergence_means(X_df, y_df, number_of_features="all"):
    """
    This function select best features using Kullback–Leibler (KL) divergence, where the best feature is the hightes
    KL divergence value.

    :param X_df: data fram of the data without labels
    :param y_df: labels array as pandas series
    :param number_of_features: how much fature you want, default="all"
    :return:
      (1) list of the KL average, where clauclated by, 0.5 * [KL(Q||P)+KL(P||Q)]
      (2) pandas data frame of the KL values per the features names and index
      (3) pandas data frame of the data with the best features (best_X)
      (4) pandas data frame of the data with the best features include the labels (best_df)
      (5) pandas data frame of the KL values per the features names and index sorted by KL values descendly

    example:
    mean_KL, results, Best_X_df, df_Best_inclod_labels, results_sorted = kl_divergence(X, y, number_of_features="all")
    """
    # data preparin
    features = list(X_df.columns.values)
    X = X_df
    y = y_df
    uniq_lab = np.unique(y.values)
    df = pd.concat([X, y], axis=1)

    X_1 = df[df[df.columns[-1]] == uniq_lab[0]].drop(df.columns[-1], axis=1)
    X_2 = df[df[df.columns[-1]] == uniq_lab[1]].drop(df.columns[-1], axis=1)
    x_lab_1_mean = X_1.mean()
    x_lab_2_mean = X_2.mean()

    p = abs(x_lab_1_mean.values)
    q = abs(x_lab_2_mean.values)
    sid_p = list(p[i] * np.log2(p[i] / q[i]) for i in range(len(p)))
    sid_q = list(q[i] * np.log2(q[i] / p[i]) for i in range(len(p)))

    mean_KL = list(0.5 * (sid_p[_] + sid_q[_]) for _ in range(len(sid_p)))
    results = pd.DataFrame(features, columns=["features"])
    results["mean_KL_divregence"] = mean_KL
    results_sorted = results.sort_values(by="mean_KL_divregence", ascending=False)

    if number_of_features == "all":
        Best_X_df = X_df.loc[:, list(results_sorted["features"])]
    else:
        Best_feat = results_sorted["features"].iloc[:number_of_features]
        Best_X_df = X_df.loc[:, list(Best_feat.values)]
    df_Best_inclod_labels = pd.concat([Best_X_df, y_df], axis=1)
    return mean_KL, results, Best_X_df, df_Best_inclod_labels, results_sorted


def confidenc_rate_df(df, labels_col, positive_label, threshold=0.5, threshold_p=None, threshold_n=None, classifier=SVC(probability=True)):
    y = df[labels_col]
    X = df.drop(labels_col, axis=1)
    samples = X.index.values
    negative_label = y.unique()[y.unique() != positive_label][0]
    dic_str_to_num = {positive_label: 0, negative_label: 1}
    dic_str_to_num = {0: positive_label, 1: negative_label}

    y_num = y.apply(lambda _: dic_str_to_num[_] if _ in dic_str_to_num else _).values
    X = X.values

    y_prob = []
    loo = LeaveOneOut()
    for train_ix, test_ix in loo.split(X):
        X_train, X_test = X[train_ix], X[test_ix]
        y_train, y_test = y_num[train_ix], y_num[test_ix]
        classifier.fit(X_train, y_train)
        y_prob.append(classifier.predict_proba(X_test))

    y_prob = np.array(y_prob)
    y_prob = np.reshape(y_prob, (len(y), 2))
    y_hat = np.where(y_prob[:, 0] >= threshold, 0, 1)
    y_hat_post_ix = np.argwhere(y_hat == 0)
    y_hat_neg_ix = np.argwhere(y_hat == 1)

    if threshold_p:
        y_hat_rej = []
        for _ in y_prob:
            if (y_prob[:, 0] < threshold_p):  # & (y_prob[:, 1] > threshold_n):
                y_hat_rej.append(777)
            elif y_prob[:, 0] > threshold_p:
                y_hat_rej.append(0)

            elif (y_prob[:, 0] < threshold_n):  # & (y_prob[:, 1] > threshold_n):
                y_hat_rej.append(1)
            elif y_prob[:, 0] > threshold_n:
                y_hat_rej.append(777)

    conf_mat = confusion_matrix(y, y_hat)
    accuracy = accuracy_score(y, y_hat)
    sen = conf_mat[0, 0] / (conf_mat[0, 0] + conf_mat[0, 1])
    con_rate_p = (y_prob[:, 0][y_hat_post_ix] - threshold) / (1 - threshold)
    con_rate_n = abs(y_prob[:, 0][y_hat_neg_ix] - threshold) / threshold
    conf_rate = np.zeros(len(y))
    conf_rate[y_hat_post_ix] = con_rate_p
    conf_rate[y_hat_neg_ix] = con_rate_n
    y_hat_str = np.where(y_hat == 0, positive_label, negative_label)
    report = pd.DataFrame(samples, columns=["sample"])
    report["y_actual"] = y
    report["y_prediction"] = y_hat_str
    report["confidence_rate"] = conf_rate
    report["threshold"] = threshold
    report["accracy"] = accuracy
    report["sensitivty"] = sen

    return accuracy, conf_mat, y_prob, sen, con_rate_p, con_rate_n, conf_rate, report


if __name__ == "__main__":
    X, y = make_classification()
    df = pd.DataFrame(X)
    df["label"] = y
    print(X)
    acc, cm, y_prob, sen, con_rate_p, con_rate_n, conf_rate, report = confidenc_rate_df(df, labels_col="label", positive_label=0, threshold=0.5,
                                                                                        threshold_p=None, threshold_n=None,
                                                                                        classifier=SVC(probability=True))
    print(acc, sen)
    print(con_rate_n.shape)
    print(conf_rate)
    # print(y_prob)


def confidenc_rate_np(X, y, positive_label, threshold=0.5, threshold_p=None, threshold_n=None, classifier=SVC(probability=True)):
    np_type = np.array([1, 2])
    df_type = pd.DataFrame()

    if type(y) == type(np_type):
        y = pd.Series(y)

    if type(X) == type(df_type):
        X = X.values

    negative_label = y.unique()[y.unique() != positive_label][0]
    dic_str_to_num = {positive_label: 0, negative_label: 1}
    dic_str_to_num = {0: positive_label, 1: negative_label}

    y_num = y.apply(lambda _: dic_str_to_num[_] if _ in dic_str_to_num else _).values

    y_prob = []
    loo = LeaveOneOut()
    for train_ix, test_ix in loo.split(X):
        X_train, X_test = X[train_ix], X[test_ix]
        y_train, y_test = y_num[train_ix], y_num[test_ix]
        classifier.fit(X_train, y_train)
        y_prob.append(classifier.predict_proba(X_test))

    y_prob = np.array(y_prob)
    y_prob = np.reshape(y_prob, (len(y), 2))
    y_hat = np.where(y_prob[:, 0] >= threshold, 0, 1)
    y_hat_post_ix = np.argwhere(y_hat == 0)
    y_hat_neg_ix = np.argwhere(y_hat == 1)

    if threshold_p:
        y_hat_rej = []
        for _ in y_prob:
            if (y_prob[:, 0] < threshold_p):  # & (y_prob[:, 1] > threshold_n):
                y_hat_rej.append(777)
            elif y_prob[:, 0] > threshold_p:
                y_hat_rej.append(0)

            elif (y_prob[:, 0] < threshold_n):  # & (y_prob[:, 1] > threshold_n):
                y_hat_rej.append(1)
            elif y_prob[:, 0] > threshold_n:
                y_hat_rej.append(777)

    conf_mat = confusion_matrix(y, y_hat)
    accuracy = accuracy_score(y, y_hat)
    sen = conf_mat[0, 0] / (conf_mat[0, 0] + conf_mat[0, 1])
    con_rate_p = (y_prob[:, 0][y_hat_post_ix] - threshold) / (1 - threshold)
    con_rate_n = abs(y_prob[:, 0][y_hat_neg_ix] - threshold) / threshold
    conf_rate = np.zeros(len(y))
    conf_rate[y_hat_post_ix] = (100 * con_rate_p).astype("int32")
    conf_rate[y_hat_neg_ix] = (100 * con_rate_n).astype("int32")
    y_hat_str = np.where(y_hat == 0, positive_label, negative_label)
    report = pd.DataFrame()
    report["y_actual"] = y
    report["y_prediction"] = y_hat_str
    report["probaplity_pos"] = y_prob[:, 0]
    report["confidence_level(%)"] = conf_rate
    report["threshold"] = threshold
    report["accracy"] = accuracy
    report["sensitivty"] = sen

    dic_2 = {0: "S", 1: "R"}
    report["y_actual"] = report["y_actual"].apply(lambda _: dic_2[_] if _ in dic_2 else _)
    report["y_prediction"] = report["y_prediction"].apply(lambda _: dic_2[_] if _ in dic_2 else _)

    return accuracy, conf_mat, y_prob, sen, con_rate_p, con_rate_n, conf_rate, report


if __name__ == "__main__":
    X, y = make_classification()
    df = pd.DataFrame(X)
    df["label"] = y
    print(X)
    acc, cm, y_prob, sen, con_rate_p, con_rate_n, conf_rate, report = confidenc_rate_np(X, y, positive_label=0, threshold=0.5, threshold_p=None,
                                                                                        threshold_n=None, classifier=SVC(probability=True))
    print(acc, sen)
    print(con_rate_n.shape)
    print(conf_rate)
    # print(y_prob)


def mcd_for_one_class(X, y, contm=0.05):
    """

    :param X:
    :param y:
    :param contm:
    :return:

    example:
    X_in, y_in, X_out, y_out, ix_in, ix_out = mcd_for_one_class(X, y, contm=0.05)
    """
    od = MCD(contamination=contm)
    labels = od.fit(X).labels_
    ix_in = np.argwhere(labels == 0)
    ix_out = np.argwhere(labels == 1)

    X_in = X[ix_in]
    X_in = np.reshape(X_in, (X_in.shape[0], X_in.shape[2]))
    X_out = X[ix_out]
    X_out = np.reshape(X_out, (X_out.shape[0], X_out.shape[2]))

    y_in = y[ix_in]
    y_in = np.reshape(y_in, -1)
    y_out = y[ix_out]
    y_out = np.reshape(y_out, -1)
    return X_in, y_in, X_out, y_out, ix_in, ix_out


def convert_X_from_tensor(X):
    """

    :param X:
    :return:
    """
    return np.reshape(X, (X.shape[0], X.shape[2]))


def convert_y_from_matrix(y):
    """

    :param y:
    :return:
    """
    return np.reshape(y, -1)


def outliers_mcd_drop(X, y, classifier=SVC(probability=True), contamination_pos=0.05, contamination_neg=0.05, train_data_drop=False):
    """

    :param X:
    :param y:
    :param contamination:
    :param whole_data_drop:
    :param train_data_drop:
    :return:

    example:
    cls_report, accuracy, auc,accuracy_dev, auc_dev,contamination_total, df_in, df_out = outliers_mcd_drop(X,y,classifier=SVC(probability=True),
     contamination_pos=0.05, contamination_neg=0.05,train_data_drop=False)
    """

    unique_binary = np.unique(y)
    contamination_total = 0.5 * (contamination_pos + contamination_neg)

    if train_data_drop:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=40)

        ix_pos_label_features_train = np.argwhere(y_train == unique_binary[0])
        ix_neg_label_features_train = np.argwhere(y_train == unique_binary[1])

        X_train_pos = convert_X_from_tensor(X_train[ix_pos_label_features_train])
        y_train_pos = convert_y_from_matrix(y_train[ix_pos_label_features_train])

        X_train_neg = convert_X_from_tensor(X_train[ix_neg_label_features_train])
        y_train_neg = convert_y_from_matrix(y_train[ix_neg_label_features_train])

        X_train_pos_in, y_train_pos_in, X_train_pos_out, y_train_pos_out, _, _ = mcd_for_one_class(X_train_pos, y_train_pos, contamination_pos)
        X_train_neg_in, y_train_neg_in, X_train_neg_out, y_train_neg_out, _, _ = mcd_for_one_class(X_train_neg, y_train_neg, contamination_neg)

        X_train_in = np.concatenate((X_train_pos_in, X_train_neg_in))
        y_train_in = np.concatenate((y_train_pos_in, y_train_neg_in))

        X_train_out = np.concatenate((X_train_pos_out, X_train_neg_out))
        y_train_out = np.concatenate((y_train_pos_out, y_train_neg_out))

        # test batch
        model = classifier
        model.fit(X_train_in, y_train_in)
        y_hat = model.predict(X_test)
        cls_report = classification_report(y_test, y_hat)
        accuracy = accuracy_score(y_test, y_hat)
        auc = roc_auc_score(y_test, y_hat)



    else:
        ix_pos_label_features_whole = np.argwhere(y == unique_binary[0])
        ix_neg_label_features_whole = np.argwhere(y == unique_binary[1])

        X_pos = convert_X_from_tensor(X[ix_pos_label_features_whole])
        y_pos = convert_y_from_matrix(y[ix_pos_label_features_whole])

        X_neg = convert_X_from_tensor(X[ix_neg_label_features_whole])
        y_neg = convert_y_from_matrix(y[ix_neg_label_features_whole])

        X_pos_in, y_pos_in, X_pos_out, y_pos_out, _, _ = mcd_for_one_class(X_pos, y_pos, contamination_pos)
        X_neg_in, y_neg_in, X_neg_out, y_neg_out, _, _ = mcd_for_one_class(X_neg, y_neg, contamination_neg)

        # X_pos_out, y_pos_out = mcd_for_one_class(X_pos, y_pos, 1-contamination_pos)
        # X_neg_out, y_neg_out = mcd_for_one_class(X_neg, y_neg, 1-contamination_neg)

        X_in = np.concatenate((X_pos_in, X_neg_in))
        y_in = np.concatenate((y_pos_in, y_neg_in))

        X_out = np.concatenate((X_pos_out, X_neg_out))
        y_out = np.concatenate((y_pos_out, y_neg_out))

        df_in = pd.DataFrame(X_in)
        df_in["labels"] = y_in

        df_out = pd.DataFrame(X_out)
        df_out["labels"] = y_out

        X_train_in, X_test_in, y_train_in, y_test_in = train_test_split(X_in, y_in, test_size=0.33, random_state=40)

        model = classifier
        model.fit(X_train_in, y_train_in)
        y_hat = model.predict(X_test_in)
        cls_report = classification_report(y_test_in, y_hat)
        accuracy = accuracy_score(y_test_in, y_hat)
        auc = roc_auc_score(y_test_in, y_hat)

    # devlop batch
    X_train_dev, X_test_dev, y_train_dev, y_test_dev = train_test_split(X_train_in, y_train_in, test_size=0.33, random_state=40)
    model_dev = classifier
    model_dev.fit(X_train_dev, y_train_dev)
    y_hat_dev = model.predict(X_test_dev)
    accuracy_dev = accuracy_score(y_test_dev, y_hat_dev)
    auc_dev = roc_auc_score(y_test_dev, y_hat_dev)

    return cls_report, accuracy, auc, accuracy_dev, auc_dev, contamination_total, df_in, df_out


if __name__ == "__main__":
    from sklearn.datasets import make_classification
    from pyod.models.mcd import MCD
    import numpy as np

    X, y = make_classification()

    outliers_mcd_drop(X, y, classifier=SVC(probability=True), contamination_pos=0.05, contamination_neg=0.05, train_data_drop=True)


def mixing_restricted_and_goldstandart_data(X_gs, y_gs, X_res, y_res, gs_rate=0.5):
    """
    from 2 data bases (DB) with same features size, one of them is gold-standart (GS) and the second on is restricted (Res).
    Take randomly from the Res DB data and mixed with GS DB and the product should be  with the same GS size.

    :param X_gs: GS featuers (numpy)
    :param y_gs: GS labels (numpy)
    :param X_res: Res DB featuers (numpy)
    :param y_res: Res DB labels (numpy)
    :param gs_rate: the GS DB rate in the last product (defaolt 50%)
    :return:
          X_mix: mixed features (numpy)
          y_mix: mixed labels (numpy)
          df_mix: data frame with mixed features and labels(pandas)

    example:
    X_mix, y_mix, df_mix =  mixing_restricted_and_goldstandart_data(X_gs,y_gs,X_res,y_res,gs_rate=0.5)
    """

    gs_size = len(y_gs)
    gs_random_ix = np.random.randint(0, gs_size, int(gs_rate * gs_size))
    X_gs_product = X_gs[gs_random_ix]
    y_gs_product = y_gs[gs_random_ix]

    res_size = len(y_res)
    res_random_ix = np.random.randint(0, res_size, int((1 - gs_rate) * gs_size))
    X_res_product = X_res[res_random_ix]
    y_res_product = y_res[res_random_ix]

    X_mix = np.concatenate((X_gs_product, X_res_product))
    y_mix = np.concatenate((y_gs_product, y_res_product))
    df_mix = pd.DataFrame(X_mix)
    df_mix["labels"] = y_mix

    return X_mix, y_mix, df_mix


if __name__ == "__main__":
    X, y = make_classification()
    X1, y1 = X[:50], y[:50]
    X2, y2 = X[50:], y[50:]
    X_mix, y_mix, df_mix = mixing_restricted_and_goldstandart_data(X1, y1, X2, y2, gs_rate=0.5)

from sklearn.decomposition.pca import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


def classification_per_pca(X, y, num_pc, classifier=LDA(), plot=False, plot_roc=True):
    accuracy = []
    pc = []
    for num in range(1, num_pc):
        pca = PCA(n_components=num)
        X_pca = pca.fit_transform(X)
        loo = LeaveOneOut()
        y_hat = []
        y_hat_prob = []

        for train_ix, test_ix in loo.split(X_pca):
            X_train, X_test = X_pca[train_ix], X_pca[test_ix]
            y_train, y_test = y[train_ix], y[test_ix]
            classifier.fit(X_train, y_train)
            y_hat.append(classifier.predict(X_test))
            y_hat_prob.append(classifier.predict_proba(X_test))
        accuracy.append(accuracy_score(y, y_hat))
        pc.append(num)

    if plot:
        plt.plot(pc, accuracy)
        plt.show()

    if plot_roc:
        fpr, tpr, thresholds = roc_curve(y, y_hat, pos_label=0)
        plt.plot(tpr, fpr)

    return accuracy


def outliers_for_binary_data(X, y, contamination_label1=0.5, contamination_label2=0):
    """

    :param X: data's features (numpy)
    :param y: datas binary labels (numpy)
    :param contamination_label1: rate of outliers from the first label maximum 0.5
    :param contamination_label2: rate of outliers from the second label maximum 0.5
    :return:

    example:
    X_clear, y_clear, X_contaminated, y_contaminated = outliers_for_binary_data(X,y,contamination_label1=0.5, contamination_label2=0)
    """

    contamination_label1, contamination_label2 = contamination_label1, contamination_label2
    label_1, label_2 = np.unique(y)[0], np.unique(y)[1]

    X_1 = X[np.argwhere(y == label_1)]
    X_1 = np.reshape(X_1, (X_1.shape[0], X_1.shape[2]))

    X_2 = X[np.argwhere(y == label_2)]
    X_2 = np.reshape(X_2, (X_2.shape[0], X_2.shape[2]))

    y_1 = y[np.argwhere(y == label_1)]
    y_1 = np.reshape(y_1, -1)

    y_2 = y[np.argwhere(y == label_2)]
    y_2 = np.reshape(y_2, -1)

    X_in_1, y_in_1, X_out_1, y_out_1, ix_in_1, ix_out_1 = mcd_for_one_class(X_1, y_1, contm=contamination_label1)
    X_in_2, y_in_2, X_out_2, y_out_2, ix_in_2, ix_out_2 = mcd_for_one_class(X_2, y_2, contm=contamination_label2)

    X_clear = np.concatenate((X_in_1, X_in_2))
    y_clear = np.concatenate((y_in_1, y_in_2))

    X_contaminated = np.concatenate((X_out_1, X_out_2))
    y_contaminated = np.concatenate((y_out_1, y_out_2))

    return X_clear, y_clear, X_contaminated, y_contaminated


def roc_and__det_curves_for_multi_calssifiers_with_mcd(X, y, clfs=defualt_classifers, name_of_the_labe="Non", feature_selection_type="None",
                                                       diff="2nd_derivative", itirations_rate=0.97, contam_post=0.05, contam_neg=0.05):
    """ return plot of roc curvs for 12 classifiers
    X: data as nump
    y: labels
    """
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'bold',
            'size': 30,
            'fontname': 'Times New Roman'
            }

    X, y = X[y != 2], y[y != 2]
    n_samples, n_features = X.shape

    # Add noisy features
    random_state = np.random.RandomState(0)
    X = np.c_[X, random_state.randn(n_samples, n_features)]

    params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5]}

    fig_1, (x1, x2) = plt.subplots(2, figsize=(20, 17))
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)

    TPR = []
    FPR = []

    i = 0
    MRecall = []
    auc_dict = {}
    # random_state = 300
    for m in clfs:
        random_state = 100
        for j in range(42, random_state):
            X_tr, X_test, y_tr, y_test = train_test_split(X, y, train_size=0.70,
                                                          test_size=0.30, shuffle=True,
                                                          random_state=j)
            X_train, y_train, _, _ = outliers_for_binary_data(X_tr, y_tr, contamination_label1=contam_post, contamination_label2=contam_neg)
            X_test, y_test, _, _ = outliers_for_binary_data(X_test, y_test, contamination_label1=0.0001, contamination_label2=0.0001)
            classifier = m['clf']
            classifier.fit(X_train, y_train)
            probas_ = classifier.predict_proba(X_test)
            fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            y_scores = classifier.predict_proba(X_test)
            prec, rec, tre = precision_recall_curve(y_test, y_scores[:, 1], )

        if itirations_rate == "all":
            mean_tpr = np.mean(tprs, axis=0)
        else:
            mean_tpr = np.quantile(tprs, itirations_rate, axis=0)
        MRecall.append(mean_tpr)

        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        auc_dict[m['name']] = mean_auc

        macro_recall = 0.5 * (mean_fpr + mean_tpr)
        # MRecall.append(macro_recall)
        std_auc = np.std(aucs)
        # mm = 95

        x1.plot(mean_fpr, mean_tpr, label='%s(AUC = %0.2f)' % (m['name'], mean_auc), lw=2, alpha=.8)

        x2.plot(mean_fpr, 1 - mean_tpr, label=m['name'], lw=2, alpha=.8)
        x2.set_xscale('log')
        x2.set_yscale('log')

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + 0.316 * std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - 0.316 * std_tpr, 0)

    x1.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Random chance ', alpha=.8)
    x1.set_xlim([-0.05, 1.05])
    x1.set_ylim([-0.05, 1.05])
    x1.set_xlabel('1-Specificity', fontdict=font)
    x1.set_ylabel('Sensitivity', fontdict=font)
    x1.set_title("ROC Curve |" + name_of_the_labe + "| feature_selection= " + feature_selection_type + ", diff= " + diff, fontdict=font)
    x1.legend(loc="lower right", fontsize="large")
    x1.legend(loc="lower right", fontsize=16)
    x1.tick_params(labelsize=12)
    x2.tick_params(labelsize=12)
    x2.plot([0, 1], [0, 1], '--r')

    ticks_to_use = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.6, 1]
    x2.set_xticks(ticks_to_use)
    x2.set_yticks(ticks_to_use)

    # x2.xaxis.set_minor_formatter(mticker.ScalarFormatter())
    # x2.yaxis.set_minor_formatter(mticker.ScalarFormatter())
    x2.xaxis.set_major_formatter(mticker.ScalarFormatter())
    x2.yaxis.set_major_formatter(mticker.ScalarFormatter())
    x2.set_xlabel('False posotive rate (1 - specificity)', fontdict=font)
    x2.set_ylabel('False negative rate (1 - sensitivty)', fontdict=font)
    x2.set_title("DET Curve|" + name_of_the_labe + "| feature_selection= " + feature_selection_type + ", diff= " + diff, fontdict=font)
    x2.legend(loc=3, fontsize="large")
    x2.legend(loc=3, fontsize=16)

    plt.show()
    return auc_dict


def praper_multi_target_data(df, targets, x_0='1801.264', x_end='898.703', positive_label="S", xy_return="at_least_one"):
    """

    :param df: data frame with targets
    :param targets: list of the targets
    :param x_0: X feature start from
    :param x_end: X features end in
    :param positive_label: the "sympol" of the positive target
    :param xy_return:  what X and y target you want (defoalt:"at_least_one") you can choose
                       "1/num of targets", "2/num of targets"...
    :param balance_mod: balnced the data by the max/min size
    :return: df_multi_target withe compination columns
             X_
             y
             df_xy
             labels_count
    example:
    df_multi_target, X, y,df_xy,labels_count = praper_multi_target_data(df, targets, x_0='1801.264', x_end='898.703', positive_label="S",
                                                                        xy_return="at_least_one")
    """
    dict = {"I": "R"}
    df = df.applymap(lambda _: dict[_] if _ in dict else _)
    df_clear = df.loc[:, x_0:x_end]
    df_clear[targets] = df[targets]
    df_clear = df_clear.dropna()
    # combine targets
    df_clear["multi_traget"] = df_clear[targets].apply(lambda _: "".join(_), axis=1)
    lis = list(df_clear["multi_traget"])

    num_of_S = []
    for multi_tar_ex in lis:
        num_of_S.append(sum(list(_ in positive_label for _ in multi_tar_ex)))

    df_clear["num_of_S"] = num_of_S
    df_clear["at_least_one"] = df_clear["multi_traget"].apply(lambda _: 0 if positive_label in _ else 1)

    for i in range(len(targets)):
        df_clear[str(i + 1) + "/" + str(len(targets))] = df_clear["num_of_S"].apply(lambda _: 0 if _ == i + 1 else 1)

    df_multi_target = df_clear
    y = df_multi_target[xy_return]
    df_xy = pd.DataFrame(df_multi_target.loc[:, x_0:x_end])
    df_xy["labels"] = y
    labels_count = {"positive_sum_unbalnced": sum(y == 0), "negative_sum_unbalnced": sum(y == 1)}
    X = df_xy.drop("labels", axis=1)

    return df_multi_target, X.values, y.values, df_xy, labels_count


def unbalanced_data_dealing(df, labels_columns="labels", blanced_mod="min", seed=42):
    """

    :param df:
    :param labels_columns:
    :param blanced_mod:
    :param seed:
    :return:
    """
    np.random.seed(seed)

    pos_num = df[df[labels_columns] == 0].shape[0]
    neg_num = df[df[labels_columns] == 1].shape[0]

    pos_df = df[df[labels_columns] == 0]
    neg_df = df[df[labels_columns] == 1]

    if blanced_mod == "min" and pos_num > neg_num:
        pos_df = pos_df.sample(neg_num)
        df_balanced = pd.concat([pos_df, neg_df], axis=0)
    elif blanced_mod == "min" and pos_num < neg_num:
        neg_df = neg_df.sample(pos_num)
        df_balanced = pd.concat([pos_df, neg_df], axis=0)

    if blanced_mod == "max" and pos_num < neg_num:
        pos_df = pos_df.sample(neg_num, replace=True)
        df_balanced = pd.concat([pos_df, neg_df], axis=0)
    elif blanced_mod == "max" and pos_num > neg_num:
        neg_df = neg_df.sample(pos_num, replace=True)
        df_balanced = pd.concat([pos_df, neg_df], axis=0)

    X = df_balanced.drop("labels", axis=1)
    y = df_balanced["labels"]

    return df_balanced, X.values, y.values


def roc_and__det_curves_for_multi_calssifiers_with_feature_sel(X, y, groups_array_forLOGO, CV="split", clfs=defualt_classifers, title="Non",
                                                               plot=True):
    """ return plot of roc curvs for 12 classifiers
    X: data as nump
    y: labels
    """
    df_ = pd.DataFrame(X)
    df_["labels"] = y
    # df_ = df_.sample(frac=1)
    df_ = df_.sample(frac=1, random_state=1989)
    font = {'family': 'serif',
            'color': 'black',
            'weight': 'bold',
            'size': 30,
            'fontname': 'Times New Roman'
            }

    if plot:
        fig_1, (x1, x2) = plt.subplots(2, figsize=(20, 17))
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)

    MRecall = []
    auc_dict = {}

    for m in clfs:
        X_bes, _, _, _, _ = feature_selection_and_derivative(df_,
                                                             labels_columns_name="labels",
                                                             featur_selection_type=m["feature_sle_type"],
                                                             selected_features_num=m["num_of_features"],
                                                             plot=False,
                                                             derivative=m["2nd_diff"])
        if CV == "split":

            X_train, X_test, y_train, y_test = train_test_split(X_bes, y, train_size=0.70,
                                                                test_size=0.30, shuffle=True)

            classifier = m['clf']
            probas_ = classifier.fit(X_train, y_train).predict_proba(X_test)
            mean_fpr, mean_tpr, thresholds = roc_curve(y_test, probas_[:, 1])
            mean_auc = auc(mean_fpr, mean_tpr)
            y_hat_per_class = classifier.fit(X_train, y_train).predict(X_test)

        elif CV == "LOO":
            loo = LeaveOneOut()
            probas_ = np.zeros(len(y))
            y_hat_per_class = []
            for train_ix, test_ix in loo.split(X_bes):
                X_train, X_test, y_train, y_test = X_bes[train_ix], X_bes[test_ix], y[train_ix], y[test_ix]
                classifier = m['clf']
                probas_[test_ix] = (classifier.fit(X_train, y_train).predict_proba(X_test))[:, 1]
                y_hat_per_class = classifier.fit(X_train, y_train).predict(X_test)
            mean_fpr, mean_tpr, thresholds = roc_curve(y, probas_)
            mean_auc = auc(mean_fpr, mean_tpr)

        elif CV == "LOGO":
            logo = LeaveOneGroupOut()
            probas_ = np.zeros(len(y))
            y_test_all = np.zeros(len(y))
            y_hat_per_class = []
            for train_ix, test_ix in logo.split(X_bes, y, groups=groups_array_forLOGO):
                X_train, X_test, y_train, y_test = X_bes[train_ix], X_bes[test_ix], y[train_ix], y[test_ix]
                classifier = m['clf']
                probas_[test_ix] = (classifier.fit(X_train, y_train).predict_proba(X_test))[:, 1]
                y_hat_per_class.append(classifier.fit(X_train, y_train).predict(X_test))
                y_test_all[test_ix] = y_test
            mean_fpr, mean_tpr, thresholds = roc_curve(y_test_all.flatten(), probas_.flatten())
            mean_auc = auc(mean_fpr, mean_tpr)

        if plot:
            x1.plot(mean_fpr, mean_tpr, label='%s(AUC = %0.2f)' % (m['name'], mean_auc), lw=2, alpha=.8)

            x2.plot(mean_fpr, 1 - mean_tpr, label=m['name'], lw=2, alpha=.8)
            x2.set_xscale('log')
            x2.set_yscale('log')

    if plot:
        x1.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Random chance ', alpha=.8)
        x1.set_xlim([-0.05, 1.05])
        x1.set_ylim([-0.05, 1.05])
        x1.set_xlabel('1-Specificity', fontdict=font)
        x1.set_ylabel('Sensitivity', fontdict=font)
        x1.set_title(title, fontdict=font)
        x1.legend(loc="lower right", fontsize="large")
        x1.legend(loc="lower right", fontsize=16)
        x1.tick_params(labelsize=12)
        x2.tick_params(labelsize=12)
        x2.plot([0, 1], [0, 1], '--r')

        ticks_to_use = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.6, 1]
        x2.set_xticks(ticks_to_use)
        x2.set_yticks(ticks_to_use)

        x2.xaxis.set_major_formatter(mticker.ScalarFormatter())
        x2.yaxis.set_major_formatter(mticker.ScalarFormatter())
        x2.set_xlabel('False posotive rate (1 - specificity)', fontdict=font)
        x2.set_ylabel('False negative rate (1 - sensitivty)', fontdict=font)
        x2.set_title(title, fontdict=font)
        x2.legend(loc=3, fontsize="large")
        x2.legend(loc=3, fontsize=16)

        plt.show()
    return auc_dict, mean_tpr, mean_fpr, y_hat_per_class


import itertools
import string


def confegorations_combinations(target_list=["Adam", "Layla", "Reman", "George", "Itsik", "Ravit"], splits=2):
    """
    This function return all the combinations of list on respict to the number of the splits

    input :list of string (or what ever!)[list]
           number of splits[integer]

    output: list with the split combninations
            numer of combinations
   _____________________________________________________________________
    example:
    >>inter, num = confegorations_combinations(target_list=["Adam", "Layla", "Reman", "George", "Itsik", "Ravit"], splits=2)
    >>print (inter)
    >>[['Adam', 'Layla'], ['Adam', 'Reman'], ['Adam', 'George'], ['Adam', 'Itsik'], ['Adam', 'Ravit'], ['Layla', 'Reman'],
      ['Layla', 'George'], ['Layla', 'Itsik'], ['Layla', 'Ravit'], ['Reman', 'George'], ['Reman', 'Itsik'],
      ['Reman', 'Ravit'], ['George', 'Itsik'], ['George', 'Ravit'], ['Itsik', 'Ravit']]

    >>print(num)
    >>15
    ____________________________________________________________________
    note: limited to 52 target_list length
    """

    abc_string = list(string.ascii_lowercase[0:26]) + list(string.ascii_uppercase[0:26])
    index_list = list(np.linspace(0, 2 * 26 - 1, 2 * 26).astype("int"))
    combinations_string = "".join(abc_string[:len(target_list)])
    conf = list(itertools.combinations(combinations_string, splits))  # all the confegrations

    df = pd.DataFrame(conf)
    df = df.replace(abc_string, index_list)
    conf = df.values

    inter = []  # confegrations between splits
    for ii in conf:
        intra = []  # confegrations inside splits
        for _ in range(splits):
            intra += [target_list[int(ii[_])]]
        inter.append(intra)
    num = len(inter)
    return inter, num


##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class SpectraPrapering:

    def __init__(self, X):
        self.X = X

    def spectra_normalization(self, plot=False):
        df = pd.DataFrame(self.X.T)
        df = df.apply(lambda v: v / ((v ** 2).sum()) ** 0.5)
        df = df.apply(lambda v: v / v.max())
        self.X_norm = df.T.values

        if plot:
            fig, (ax1, ax2) = plt.subplots(2)
            ax1.plot(self.X.T)
            ax1.set_title("Original")
            ax2.plot(self.X_norm.T)
            ax2.set_title("Normalized")
            plt.show()
        return self.X_norm


def confedince_threshold_auto(y_test, y_prob, sacrifice_rate=0.15, min_thr=0.001, steps_thr=0.001, max_thr=1.0):
    """

    :param y_test:
    :param y_prob:
    :param sacrifice_rate:
    :param min_thr:
    :param steps_thr:
    :param max_thr:
    :return:

    Example:
     best_accuracy, best_treshold, y_hat_best, samples_sacrifice_rate, y_test_missed_classified_index, y_test_best, y_hat_glob,
      y_test_glob= confedince_threshold_auto(y_test, y_prob, sacrifice_rate=0.15,  min_thr=0.001, steps_thr=0.001, max_thr=1.0)
    """

    if sacrifice_rate == 0:
        sacrifice_rate = 1 * 10 ** -6
    thresholdes = np.arange(min_thr, max_thr, steps_thr)
    std = np.std(y_prob)
    rat = np.arange(0, 0.5, 0.01)
    samples_sacrifice_rate = []

    best_treshold = []
    y_hat_best_ = []
    y_test_missed_classified_index_ = []
    y_test_best_ = []
    y_hat_glob_ = []
    y_test_glob_ = []

    max_acc = []
    y_test_glob = []
    thres = []
    for r in rat:

        def_thresh = r

        acc = []
        threshold = []
        for thr in thresholdes:
            y_hat = np.zeros(len(y_test))
            y_hat[y_prob < thr] = 1
            y_hat[y_prob > thr] = 0

            y_hat[((thr - def_thresh) < y_prob) & (y_prob < (thr + def_thresh))] = 888

            y_test_ = y_test[y_hat != 888]
            y_hat_ = y_hat[y_hat != 888]

            acc.append(accuracy_score(y_test_, y_hat_))
            threshold.append(thr)

        acc = np.array(acc)
        best_accuracy = np.max(acc)
        best_treshold.append(threshold[np.argmax(acc)])

        y_hat_best = np.zeros(len(y_test))
        y_hat_best[y_prob < threshold[np.argmax(acc)]] = 1
        y_hat_best[y_prob > threshold[np.argmax(acc)]] = 0
        y_hat_best[((threshold[np.argmax(acc)] - def_thresh) < y_prob) & (y_prob < (threshold[np.argmax(acc)] + def_thresh))] = 888
        y_hat_glob = y_hat_best
        y_hat_glob_.append(y_hat_glob)

        y_test_missed_classified_index = np.argwhere(y_hat_best == 888)
        y_test_missed_classified_index_.append(y_test_missed_classified_index)

        y_hat_best = y_hat_best[y_hat_best != 888]
        y_hat_best_.append(y_hat_best)

        y_test_glob = y_test
        y_test_glob_.append(y_test_glob)

        y_test_best = y_test[y_hat_glob != 888]
        y_test_best_.append(y_test_best)

        max_acc.append(best_accuracy)
        samples_sacrifice_rate.append((1 - (len(y_hat_best) / (len(y_prob)))))
        thres.append(r)
        if (1 - (len(y_hat_best) / (len(y_prob)))) >= sacrifice_rate:
            break
    arg = np.argwhere(np.array(samples_sacrifice_rate) < sacrifice_rate)
    best_accuracy_ = np.around(np.max((np.array(max_acc))[arg]), 2)
    arg_max = np.argmax((np.array(max_acc))[arg])

    best_rate = np.around(np.array(samples_sacrifice_rate)[arg_max], 5)
    y_hat_best = y_hat_best_[arg_max]
    y_test_missed_classified_index = y_test_missed_classified_index_[arg_max]
    y_test_best = y_test_best_[arg_max]
    y_hat_glob = y_hat_glob_[arg_max]
    y_test_glob = y_test_glob_[arg_max]
    best_treshold = (best_treshold[arg_max],
                     thres[arg_max])
    return best_accuracy_, np.around(best_treshold, 3), y_hat_best, best_rate, y_test_missed_classified_index, y_test_best, y_hat_glob, y_test_glob


def best_result_with_confidence(y_test, y_prob, best_threshold, def_thresh):
    """

    :param y_test:
    :param y_predcit:
    :param y_prob:
    :param best_threshold:
    :param def_thresh:
    :return:y_predcit_, y_test_, samples_sacrifice_rate, missed_classified_index, y_predcit

    Example:
    y_predcit_, y_test_, samples_sacrifice_rate, missed_classified_index, y_predcit = best_result_with_confidence(y_test, y_predcit, y_prob, best_threshold,
                                                                                                       def_thresh)
    """
    y_predcit = np.ones(len(y_test))
    y_predcit[y_prob < best_threshold] = 0
    y_predcit[y_prob > best_threshold] = 1
    y_predcit[((best_threshold - def_thresh) < y_prob) & (y_prob < (best_threshold + def_thresh))] = 888
    missed_classified_index = np.argwhere(y_predcit == 888)

    y_predcit_ = y_predcit[y_predcit != 888]
    y_test_ = y_test[y_predcit != 888]

    samples_sacrifice_rate = 1 - (len(y_test_) / len(y_test))

    return y_predcit_, y_test_, samples_sacrifice_rate, missed_classified_index, y_predcit


def triple_split(X, y, train_size=0.33, random_state=10):
    np.random.seed(random_state)
    df = pd.DataFrame(X)
    df["labels"] = y
    df = df.sample(frac=1)

    df_train = df.sample(frac=train_size)
    y_train = df_train["labels"]
    X_train = df_train.drop("labels", axis=1)

    df = df.drop(index=df_train.index)

    df_valid = df.sample(frac=0.5)
    y_valid = df_valid["labels"]
    X_valid = df_valid.drop("labels", axis=1)

    df_test = df.drop(index=df_valid.index)
    y_test = df_valid["labels"]
    X_test = df_valid.drop("labels", axis=1)

    return X_train, y_train, X_valid, y_valid, X_test, y_test


def optimal_cut_point_on_roc_(tpr, fpr, n_p, n_n, delta_max=0.2, plot_point_on_ROC=False):
    sen = fpr[fpr > 0.55]
    spe = 1 - tpr[fpr > 0.55]

    delt = abs(sen - spe)
    ix_1 = np.argwhere(delt <= delta_max)

    acc = (n_p / (n_p + n_n)) * sen[ix_1] + (n_n / (n_p + n_n)) * spe[ix_1]
    best_point = (1 - spe[np.argmax(acc)], sen[np.argmax(acc)])
    auc = np.around(np.trapz(fpr, tpr), 2)

    recall_1 = sen[np.argmax(acc)]
    recall_2 = spe[np.argmax(acc)]
    precision_1 = (n_p * sen[np.argmax(acc)]) / (n_p * sen[np.argmax(acc)] + n_n * (1 - spe[np.argmax(acc)]))
    precision_2 = (n_n * spe[np.argmax(acc)]) / (n_n * spe[np.argmax(acc)] + n_p * (1 - sen[np.argmax(acc)]))

    report = {"auc": np.around(auc, 2), "acc": np.around(acc.max(), 2), "recall_1": np.around(recall_1, 2),
              "recall_2": np.around(recall_2, 2), "precision_1": np.around(precision_1, 2),
              "precision_2": np.around(precision_2, 2)
              }
    if plot_point_on_ROC:
        plt.plot(tpr, fpr)
        plt.scatter(best_point[0], best_point[1], c="red")
        plt.xlabel("1-specificity")
        plt.ylabel("sensitivity")
    return report


##
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.model_selection import LeaveOneOut, LeaveOneGroupOut, train_test_split
from sklearn.pipeline import Pipeline


class PraperClassified:
    """
    PraperClassified, is class that paraper the data(i.e, derivative, features selection, grid search) and classified.

    Parameters
    ----------
    X : numpy array of shape [n_samples, n_features].

    y : numpy array of shape [n_samples]
        Target values.

    classifier: list where contain tha classifier class, classifier name and the paramters intervals for grid
                search later.

    optimizer: for grid search, what dos your scores based on, deafult "accuracy", "roc_auc" for more you cansee
               in tihs link under scoring title: https://scikit-learn.org/stable/modules/model_evaluation.html





    Examples
    --------

    >>from sklearn.datasets import make_classification
    >>X,y = make_classification(random_state=10)
    >>model = PraperClassified(X,y,classifier=[{'cls': GaussianNB(priors=None, var_smoothing=1e-09), 'name': 'GNB'}, {'parametrs': {'priors': [None], 'var_smoothing': [1e-09]}}],
                        optimizer='roc_auc',)
    >>model.grid_search()
    >>model.best_model_

        Pipeline(memory=None,
             steps=[('feature_selection_method',
                     <__main__.KLDivergence object at 0x0000021E049C1FD0>),
                    ('classifier', GaussianNB(priors=None, var_smoothing=1e-09))],
             verbose=False)

    >>model.train_test_split()
    >>model.accuracy_

        0.8666666666666667

    >>model.auc_

        0.8516746411483254

    >>model.confusion_mat_

        array([[18,  1],
               [ 3,  8]], dtype=int64)

    >> model.show_roc()


    """

    def __init__(self, X, y, classifier=[{"cls": GaussianNB(), "name": "GNB"}, {"parametrs": {"priors": [None], "var_smoothing": [1e-09]}}],
                 optimizer="accuracy"):

        delta = (np.min(X))
        self.X = X + abs(delta * np.ones_like(X))
        self.y = y
        self.classifier = classifier
        self.classifier_name = classifier[0]["name"]
        self.optimizer = optimizer
        self.label_0_sum_ = np.sum(y == 0)
        self.label_1_sum_ = np.sum(y == 1)

    def grid_search(self, cv=5, n_features_list=["all"], feature_selection_tech="all", sacrifice_rate=0, random_state=10, validation_size=0.33):
        self.sacrifice_rate = sacrifice_rate
        pipe = Pipeline([
            # the feature selection stage
            ('feature_selection_method', 'passthrough'),

            # classifier parameters stage
            ('classifier', self.classifier[0]["cls"])
        ])

        chi2_dict = {'feature_selection_method': [SelectKBest(chi2)],
                     'feature_selection_method__k': n_features_list}
        fclass_dict = {'feature_selection_method': [SelectKBest(f_classif)],
                       'feature_selection_method__k': n_features_list}
        kl_dict = {'feature_selection_method': [KLDivergence()],
                   'feature_selection_method__k': n_features_list}

        par_keys = list(self.classifier[1]["parametrs"].keys())
        for _ in par_keys:
            chi2_dict["classifier__" + _] = self.classifier[1]["parametrs"][_]
            fclass_dict["classifier__" + _] = self.classifier[1]["parametrs"][_]
            kl_dict["classifier__" + _] = self.classifier[1]["parametrs"][_]
        if feature_selection_tech == "all":
            param_grid = [chi2_dict, fclass_dict, kl_dict]
        elif feature_selection_tech == "chi2":
            param_grid = [chi2_dict]
        elif feature_selection_tech == "f_classif":
            param_grid = [fclass_dict]
        elif feature_selection_tech == "KL":
            param_grid = [kl_dict]
        elif feature_selection_tech == "KL&chi2":
            param_grid = [kl_dict, chi2_dict]
        elif feature_selection_tech == "KL&f_classif":
            param_grid = [kl_dict, fclass_dict]
        elif feature_selection_tech == "chi2&f_classif":
            param_grid = [chi2_dict, fclass_dict]

        grid_model = GridSearchCV(pipe, param_grid=param_grid, cv=cv, scoring=self.optimizer)
        X_train, X_valid, y_train, y_valid = train_test_split(self.X, self.y, random_state=random_state, test_size=validation_size)
        grid_model.fit(X_train, y_train)

        self.best_model_ = grid_model.best_estimator_
        self.best_score_grid_ = grid_model.best_score_
        self.best_parameters_ = grid_model.best_params_

        report = pd.DataFrame(grid_model.cv_results_)
        report["chi2"] = report["param_feature_selection_method"].apply(lambda _: str(_)[str(_).find("chi2"):(str(_).find("chi2") + 5)])
        report["f_value"] = report["param_feature_selection_method"].apply(lambda _: str(_)[str(_).find("f_classif"):(str(_).find("f_classif") + 7)])
        report["KL"] = report["param_feature_selection_method"].apply(lambda _: str(_)[str(_).find("KLDivergence"):(str(_).find("KLDivergence") + 3)])
        self.grid_search_report_ = report

        # for confidence level
        self.y_predict_prob_grid_ = grid_model.predict_proba(X_valid)
        # best_accuracy_, np.around(best_treshold, 3), y_hat_best, y_test_missed_classified_index, best_rate, y_test_best, y_hat_glob, y_test_glob
        self.best_score_grid_confidence_level_, best_treshold_conf, y_hat_best, self.y_test_missed_classified_index_, self.samples_sacrifice_rate, self.y_test_best_conf_, self.y_hat_glob_, self.y_test_glob_ = confedince_threshold_auto(
            y_valid, self.y_predict_prob_grid_[:, 0], min_thr=0.01, steps_thr=0.001, max_thr=1.0, sacrifice_rate=self.sacrifice_rate)

        self.conf_interval_width = best_treshold_conf[1]
        self.best_treshold_conf_ = best_treshold_conf[0]

    def feature_selection(self, type_tech="chi2", n_features="all"):
        selectK = SelectKBest(eval(type_tech), k=n_features)
        selectK.fit(abs(self.X), self.y)
        self.X_best = selectK.transform(self.X)
        self.best_features_wighet_ = selectK.scores_
        self.X = self.X_best

    def leave_one_out(self, sensitive_label=1, confidence_interval=False):
        loo = LeaveOneOut()
        y_hat_prob = np.zeros(len(self.y))
        y_hat = np.zeros(len(self.y)).astype(type(self.y[0]))

        for ix_train, ix_test in loo.split(self.X):
            X_train, X_test = self.X[ix_train], self.X[ix_test]
            y_train, y_test = self.y[ix_train], self.y[ix_test]
            model = self.best_model_

            model.fit(X_train, y_train)
            y_hat_prob[ix_test] = model.predict_proba(X_test)[:, sensitive_label]
            y_hat[ix_test] = model.predict(X_test)

        self.confusion_mat_ = confusion_matrix(self.y, y_hat)
        self.class_report_ = classification_report(self.y, y_hat)
        self.accuracy_ = accuracy_score(self.y, y_hat)
        self.y_test_ = self.y
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob
        if len(np.unique(self.y)) == 2:
            self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y, y_hat_prob)
            self.auc_ = auc(self.fpt_, self.tpr_)

        if confidence_interval:
            self.y_predict_, self.y_test_, self.samples_sacrifice_rate, self.missed_classified_index, self.y_predcit_whole_ = best_result_with_confidence(
                self.y, y_hat_prob,
                self.best_treshold_conf_,
                self.conf_interval_width)
            y_hat_prob = np.delete(y_hat_prob, self.missed_classified_index, 0)

            self.confusion_mat_ = confusion_matrix(self.y_test_, self.y_predict_)
            self.class_report_ = classification_report(self.y_test_, self.y_predict_)
            self.accuracy_ = accuracy_score(self.y_test_, self.y_predict_)
            self.y_predict_prob_ = y_hat_prob
            if len(np.unique(self.y)) == 2:
                self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y, y_hat_prob)
                self.auc_ = auc(self.fpt_, self.tpr_)

    def leave_group_out(self, groups, sensitive_label=1, confidence_interval=False):
        logo = LeaveOneGroupOut()
        y_hat_prob = np.zeros(len(groups))
        y_hat = np.zeros(len(groups))
        y_hat_per_gr = []
        acc = []
        confmat_per_group = []
        acc_per_group = []
        sen_per_group = []
        spes_per_group = []
        ppv_per_group = []
        Npv_per_group = []
        pos_num = []
        neg_num = []

        for ix_train, ix_test in logo.split(self.X, self.y, groups):
            X_train, X_test = self.X[ix_train], self.X[ix_test]
            y_train, y_test = self.y[ix_train], self.y[ix_test]
            model = self.best_model_

            model.fit(X_train, y_train)
            y_hat_prob[ix_test] = model.predict_proba(X_test)[:, sensitive_label]
            y_hat[ix_test] = model.predict(X_test)
            acc.append(accuracy_score(y_test, model.predict(X_test)))
            y_hat_per_gr.append(model.predict(X_test))
            confmat_per_group.append(confusion_matrix(y_test, model.predict(X_test)))
            acc_per_group.append(accuracy_score(y_test, model.predict(X_test)))
            sen_per_group.append(recall_score(y_test, model.predict(X_test), pos_label=0))
            spes_per_group.append(recall_score(y_test, model.predict(X_test), pos_label=1))
            ppv_per_group.append(precision_score(y_test, model.predict(X_test), pos_label=0))
            Npv_per_group.append(precision_score(y_test, model.predict(X_test), pos_label=1))
            pos_num.append(np.sum(y_test == 0))
            neg_num.append(np.sum(y_test == 1))

        self.confusion_mat_total_ = confusion_matrix(self.y, y_hat)
        self.y_hat_total_ = y_hat
        self.y_vs_yhat_ = abs(self.y - y_hat)
        self.class_report_ = classification_report(self.y, y_hat)
        self.y_hat_per_gr_ = y_hat_per_gr
        self.confusion_mat_per_group_ = confmat_per_group
        self.accuracy_ = acc
        self.accuracy_per_group_ = acc_per_group
        self.sensitivity_per_group = sen_per_group
        self.spes_per_group_ = spes_per_group
        self.ppv_per_group_ = ppv_per_group
        self.ppv_per_group_ = ppv_per_group
        self.Npv_per_group_ = Npv_per_group
        self.y_test_ = self.y
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob
        if len(np.unique(self.y)) == 2:
            self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y, y_hat_prob)
            self.auc_ = auc(self.fpt_, self.tpr_)

        if confidence_interval:
            self.y_predict_, self.y_test_, self.samples_sacrifice_rate, self.missed_classified_index, self.y_predcit_whole_ = best_result_with_confidence(
                self.y, y_hat_prob,
                self.best_treshold_conf_,
                self.conf_interval_width)
            y_hat_prob = np.delete(y_hat_prob, self.missed_classified_index, 0)

            self.confusion_mat_ = confusion_matrix(self.y_test_, self.y_predict_)
            self.class_report_ = classification_report(self.y_test_, self.y_predict_)
            self.accuracy_ = accuracy_score(self.y_test_, self.y_predict_)
            self.y_predict_prob_ = y_hat_prob
            if len(np.unique(self.y)) == 2:
                self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y, y_hat_prob)
                self.auc_ = auc(self.fpt_, self.tpr_)

    def train_test_split(self, test_size=0.3, sensitive_label=1, confidence_interval=False):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=test_size, random_state=10)
        model = self.best_model_

        model.fit(X_train, y_train)
        y_hat_prob = model.predict_proba(X_test)[:, sensitive_label]
        y_hat = model.predict(X_test)
        self.accuracy_ = accuracy_score(y_test, model.predict(X_test))

        self.confusion_mat_ = confusion_matrix(y_test, y_hat)
        self.class_report_ = classification_report(y_test, y_hat)
        self.y_test_ = y_test
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob
        if len(np.unique(self.y)) == 2:
            self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test, y_hat_prob)
            self.auc_ = auc(self.fpt_, self.tpr_)
        if confidence_interval:
            self.y_predict_, self.y_test_, self.samples_sacrifice_rate, self.missed_classified_index, self.y_predcit_whole_ = best_result_with_confidence(
                self.y_test_,
                y_hat_prob,
                self.best_treshold_conf_,
                self.conf_interval_width)
            y_hat_prob = np.delete(y_hat_prob, self.missed_classified_index, 0)

            self.confusion_mat_ = confusion_matrix(self.y_test_, self.y_predict_)
            self.class_report_ = classification_report(self.y_test_, self.y_predict_)
            self.accuracy_ = accuracy_score(self.y_test_, self.y_predict_)
            self.y_predict_prob_ = y_hat_prob

            if len(np.unique(self.y)) == 2:
                self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y_test_, y_hat_prob)
                self.auc_ = auc(self.fpt_, self.tpr_)

    def train_test_custom(self, X_test, y_test, sensitive_label=1, confidence_interval=False):

        X_train, y_train = self.X, self.y

        model = self.best_model_

        model.fit(X_train, y_train)
        y_hat_prob = model.predict_proba(X_test)[:, sensitive_label]
        y_hat = model.predict(X_test)
        self.accuracy_ = accuracy_score(y_test, model.predict(X_test))

        self.confusion_mat_ = confusion_matrix(y_test, y_hat)
        self.class_report_ = classification_report(y_test, y_hat)

        if len(np.unique(self.y)) == 2:
            self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test, y_hat_prob)
            self.auc_ = auc(self.fpt_, self.tpr_)
        self.y_test_ = y_test
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob

        if confidence_interval:
            self.y_predict_, self.y_test_, self.samples_sacrifice_rate, self.missed_classified_index, self.y_predcit_whole_ = best_result_with_confidence(
                self.y_test_,
                y_hat_prob,
                self.best_treshold_conf_,
                self.conf_interval_width)
            y_hat_prob = np.delete(y_hat_prob, self.missed_classified_index, 0)

            self.confusion_mat_ = confusion_matrix(self.y_test_, self.y_predict_)
            self.class_report_ = classification_report(self.y_test_, self.y_predict_)
            self.accuracy_ = accuracy_score(self.y_test_, self.y_predict_)
            self.y_predict_prob_ = y_hat_prob
            if len(np.unique(self.y)) == 2:
                self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test, y_hat_prob)
                self.auc_ = auc(self.fpt_, self.tpr_)

    def train_test_split_mean_median(self, test_size=0.3, itirations_rate="mean", sensitive_label=1):
        """ return plot of roc curvs for 12 classifiers
        X: data as nump
        y: labels (binary:{0,1})
        """

        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)

        accuracy = []
        random_state = 100
        for j in range(42, random_state):
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                                test_size=test_size, shuffle=False,
                                                                random_state=j
                                                                )

            classifier = self.best_model_
            classifier.fit(X_train, y_train)
            probas_ = classifier.predict_proba(X_test)
            y_hat = classifier.predict(X_test)
            fpr, tpr, threshold = roc_curve(y_test, probas_[:, sensitive_label])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            accuracy.append(accuracy_score(y_test, y_hat))
        if itirations_rate == "mean":
            mean_tpr = np.mean(tprs, axis=0)
        else:
            mean_tpr = np.quantile(tprs, itirations_rate, axis=0)

        mean_tpr[-1] = 1.0

        self.auc_ = auc(mean_fpr, mean_tpr)

        if itirations_rate == "mean":
            self.accuracy_ = np.mean(accuracy, axis=0)
        else:
            self.accuracy_ = np.quantile(accuracy, itirations_rate, axis=0)

        ac = (self.label_1_sum_ * (1 - mean_fpr) + self.label_0_sum_ * mean_tpr) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        recal_pos = mean_tpr[index_max][0][0]
        recal_neg = 1 - mean_fpr[index_max][0][0]
        self.confusion_mat_best_on_roc_ = np.array([[int(recal_pos * self.label_0_sum_),
                                                     int(self.label_0_sum_ - int(recal_pos * self.label_0_sum_))],

                                                    [int(self.label_1_sum_ - int(recal_neg * self.label_1_sum_)),
                                                     int(recal_neg * self.label_1_sum_)]])
        self.accuracy_best_on_roc_ = (self.confusion_mat_best_on_roc_[0, 0] + self.confusion_mat_best_on_roc_[1, 1]) / np.sum(
            self.confusion_mat_best_on_roc_)

        self.fpt_ = mean_fpr
        self.tpr_ = mean_tpr
        thresholds = np.linspace(threshold[-1], threshold[0], mean_tpr.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]

    def train_test_split_mean_median_outliers_drop(self, test_size=0.30, itirations_rate="mean", contam_post=0.05, contam_neg=0.05):
        """ return data with droped outliers
        X: data as nump
        y: labels (binary:{0,1})
        """
        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)

        accuracy = []
        random_state = 100
        for j in range(42, random_state):
            X_tr, X_test, y_tr, y_test = train_test_split(self.X, self.y,
                                                          test_size=test_size, shuffle=False,
                                                          random_state=j)
            X_train, y_train, _, _ = outliers_for_binary_data(X_tr, y_tr, contamination_label1=contam_post, contamination_label2=contam_neg)
            X_test, y_test, _, _ = outliers_for_binary_data(X_test, y_test, contamination_label1=0.0001, contamination_label2=0.0001)
            classifier = self.best_model_
            classifier.fit(X_train, y_train)
            probas_ = classifier.predict_proba(X_test)
            y_hat = classifier.predict(X_test)
            fpr, tpr, threshold = roc_curve(y_test, probas_[:, 1])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            accuracy.append(accuracy_score(y_test, y_hat))
        if itirations_rate == "mean":
            mean_tpr = np.mean(tprs, axis=0)

        else:
            mean_tpr = np.quantile(tprs, itirations_rate, axis=0)

        mean_tpr[-1] = 1.0

        self.auc_ = auc(mean_fpr, mean_tpr)

        if itirations_rate == "mean":
            self.accuracy_ = np.mean(accuracy, axis=0)
        else:
            self.accuracy_ = np.quantile(accuracy, itirations_rate, axis=0)

        ac = (self.label_1_sum_ * (1 - mean_fpr) + self.label_0_sum_ * mean_tpr) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        recal_pos = mean_tpr[index_max][0][0]
        recal_neg = 1 - mean_fpr[index_max][0][0]
        self.confusion_mat_best_on_roc_ = np.array([[int(recal_pos * self.label_0_sum_),
                                                     int(self.label_0_sum_ - int(recal_pos * self.label_0_sum_))],

                                                    [int(self.label_1_sum_ - int(recal_neg * self.label_1_sum_)),
                                                     int(recal_neg * self.label_1_sum_)]])
        self.accuracy_best_on_roc_ = (self.confusion_mat_best_on_roc_[0, 0] + self.confusion_mat_best_on_roc_[1, 1]) / np.sum(
            self.confusion_mat_best_on_roc_)

        self.fpt_ = mean_fpr
        self.tpr_ = mean_tpr
        thresholds = np.linspace(threshold[-1], threshold[0], mean_tpr.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]

    def k_folds(self, n_folds=5, shuffle=False, random_state=None, confidence_interval=False, sensitive_label=1):

        kf = KFold(n_splits=n_folds, shuffle=shuffle, random_state=random_state)
        y_hat_prob = np.zeros(len(self.y))
        y_hat = np.zeros(len(self.y)).astype(type(self.y[0]))
        y_test_ = np.zeros(len(self.y)).astype(type(self.y[0]))

        for ix_train, ix_test in kf.split(self.X):
            X_train, X_test = self.X[ix_train], self.X[ix_test]
            y_train, y_test = self.y[ix_train], self.y[ix_test]
            model = self.best_model_

            model.fit(X_train, y_train)
            y_hat_prob[ix_test] = model.predict_proba(X_test)[:, sensitive_label]
            y_hat[ix_test] = model.predict(X_test)
            y_test_[ix_test] = y_test

        self.confusion_mat_ = confusion_matrix(y_test_, y_hat)
        self.class_report_ = classification_report(y_test_, y_hat)
        self.accuracy_ = accuracy_score(y_test_, y_hat)

        self.y_test_ = y_test_
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob
        if len(np.unique(self.y)) == 2:
            self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test_, y_hat_prob)
            self.auc_ = auc(self.fpt_, self.tpr_)

        if confidence_interval:
            self.y_predict_, self.y_test_, self.samples_sacrifice_rate, self.missed_classified_index, self.y_predcit_whole_ = best_result_with_confidence(
                self.y_test_,
                y_hat_prob,
                self.best_treshold_conf_,
                self.conf_interval_width)
            y_hat_prob = np.delete(y_hat_prob, self.missed_classified_index, 0)

            self.confusion_mat_ = confusion_matrix(self.y_test_, self.y_predict_)
            self.class_report_ = classification_report(self.y_test_, self.y_predict_)
            self.accuracy_ = accuracy_score(self.y_test_, self.y_predict_)
            self.y_predict_prob_ = y_hat_prob
            if len(np.unique(self.y)) == 2:
                self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y_test_, y_hat_prob)
                self.auc_ = auc(self.fpt_, self.tpr_)

        return self

    def k_folds_nested(self, n_folds=5, shuffle=False, random_state=None, cv=5, optimzer="accuracy", n_features_list=["all"], sensitive_label=1):
        """
        nested K-foldes
        """

        kf = KFold(n_splits=n_folds, shuffle=shuffle, random_state=random_state)
        y_hat_prob = np.zeros(len(self.y))
        y_hat = np.zeros(len(self.y))
        y_test_ = np.zeros(len(self.y))
        best_parameters_nested_ = []
        for ix_train, ix_test in kf.split(self.X):
            X_train, X_test = self.X[ix_train], self.X[ix_test]
            y_train, y_test = self.y[ix_train], self.y[ix_test]
            pipe = Pipeline([
                # the feature selection stage
                ('feature_selection_method', 'passthrough'),

                # classifier parameters stage
                ('classifier', self.classifier[0]["cls"])
            ])

            chi2_dict = {'feature_selection_method': [SelectKBest(chi2)],
                         'feature_selection_method__k': n_features_list}
            fclass_dict = {'feature_selection_method': [SelectKBest(f_classif)],
                           'feature_selection_method__k': n_features_list}
            kl_dict = {'feature_selection_method': [KLDivergence()],
                       'feature_selection_method__k': n_features_list}

            par_keys = list(self.classifier[1]["parametrs"].keys())
            for _ in par_keys:
                chi2_dict["classifier__" + _] = self.classifier[1]["parametrs"][_]
                fclass_dict["classifier__" + _] = self.classifier[1]["parametrs"][_]
                kl_dict["classifier__" + _] = self.classifier[1]["parametrs"][_]

            param_grid = [chi2_dict, fclass_dict, kl_dict]

            grid_model = GridSearchCV(pipe, param_grid=param_grid, cv=cv, scoring=optimzer)

            grid_model.fit(X_train, y_train)
            self.best_model_nested_ = grid_model.best_estimator_
            best_parameters__ = grid_model.best_params_
            best_parameters_nested_.append(best_parameters__)

            y_hat_prob[ix_test] = grid_model.predict_proba(X_test)[:, sensitive_label]
            y_hat[ix_test] = grid_model.predict(X_test)
            y_test_[ix_test] = y_test

        self.best_parameters_nested_ = best_parameters_nested_
        self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test_, y_hat_prob)
        self.auc_ = auc(self.fpt_, self.tpr_)
        self.confusion_mat_ = confusion_matrix(y_test_, y_hat)
        self.class_report_ = classification_report(y_test_, y_hat)
        self.accuracy_ = accuracy_score(y_test_, y_hat)

        ac = (self.label_1_sum_ * (1 - self.fpt_) + self.label_0_sum_ * self.tpr_) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        thresholds = np.linspace(self.threshold_[-1], self.threshold_[0], self.tpr_.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]
        self.y_test_ = y_test_
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob

        return self

    ### EXTERNAL MODELS
    def leave_one_out_external_model(self, external_model):
        loo = LeaveOneOut()
        y_hat_prob = np.zeros(len(self.y))
        y_hat = np.zeros(len(self.y))

        for ix_train, ix_test in loo.split(self.X):
            X_train, X_test = self.X[ix_train], self.X[ix_test]
            y_train, y_test = self.y[ix_train], self.y[ix_test]
            model = external_model

            model.fit(X_train, y_train)
            y_hat_prob[ix_test] = model.predict_proba(X_test)[:, 1]
            y_hat[ix_test] = model.predict(X_test)

        self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y, y_hat_prob)
        self.auc_ = auc(self.fpt_, self.tpr_)
        self.confusion_mat_ = confusion_matrix(self.y, y_hat)
        self.class_report_ = classification_report(self.y, y_hat)
        self.accuracy_ = accuracy_score(self.y, y_hat)
        self.y_test_ = self.y
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob

    def leave_group_out_external_model(self, external_model, groups):
        logo = LeaveOneGroupOut()
        y_hat_prob = np.zeros(len(groups))
        y_hat = np.zeros(len(groups))
        y_hat_per_gr = []
        acc = []
        confmat_per_group = []
        acc_per_group = []
        sen_per_group = []
        spes_per_group = []
        ppv_per_group = []
        Npv_per_group = []
        pos_num = []
        neg_num = []

        for ix_train, ix_test in logo.split(self.X, self.y, groups):
            X_train, X_test = self.X[ix_train], self.X[ix_test]
            y_train, y_test = self.y[ix_train], self.y[ix_test]
            model = external_model

            model.fit(X_train, y_train)
            y_hat_prob[ix_test] = model.predict_proba(X_test)[:, 1]
            y_hat[ix_test] = model.predict(X_test)
            acc.append(accuracy_score(y_test, model.predict(X_test)))
            y_hat_per_gr.append(model.predict(X_test))
            confmat_per_group.append(confusion_matrix(y_test, model.predict(X_test)))
            acc_per_group.append(accuracy_score(y_test, model.predict(X_test)))
            sen_per_group.append(recall_score(y_test, model.predict(X_test), pos_label=0))
            spes_per_group.append(recall_score(y_test, model.predict(X_test), pos_label=1))
            ppv_per_group.append(precision_score(y_test, model.predict(X_test), pos_label=0))
            Npv_per_group.append(precision_score(y_test, model.predict(X_test), pos_label=1))
            pos_num.append(np.sum(y_test == 0))
            neg_num.append(np.sum(y_test == 1))

        self.fpt_, self.tpr_, self.threshold_ = roc_curve(self.y, y_hat_prob)
        self.auc_ = auc(self.fpt_, self.tpr_)
        self.confusion_mat_total_ = confusion_matrix(self.y, y_hat)
        self.y_hat_total_ = y_hat
        self.y_vs_yhat_ = abs(self.y - y_hat)
        self.class_report_ = classification_report(self.y, y_hat)
        self.y_hat_per_gr_ = y_hat_per_gr
        self.confusion_mat_per_group_ = confmat_per_group
        self.accuracy_ = acc
        self.accuracy_per_group_ = acc_per_group
        self.sensitivity_per_group = sen_per_group
        self.spes_per_group_ = spes_per_group
        self.ppv_per_group_ = ppv_per_group
        self.ppv_per_group_ = ppv_per_group
        self.Npv_per_group_ = Npv_per_group
        self.y_test_ = self.y
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob

    def train_test_split_external_model(self, external_model, test_size=0.3):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=test_size, random_state=10)
        model = external_model

        model.fit(X_train, y_train)
        y_hat_prob = model.predict_proba(X_test)[:, 1]
        y_hat = model.predict(X_test)
        self.accuracy_ = accuracy_score(y_test, model.predict(X_test))
        self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test, y_hat_prob)
        self.auc_ = auc(self.fpt_, self.tpr_)
        self.confusion_mat_ = confusion_matrix(y_test, y_hat)
        self.class_report_ = classification_report(y_test, y_hat)

        ac = (self.label_1_sum_ * (1 - self.fpt_) + self.label_0_sum_ * self.tpr_) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        thresholds = np.linspace(self.threshold_[-1], self.threshold_[0], self.tpr_.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]
        self.y_test_ = y_test
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob

    def train_test_custom_external_model(self, external_model, train_indexs=[1, 2, 3, 4]):

        X_train, y_train = self.X[train_indexs], self.y[train_indexs]
        X_test, y_test = np.delete(self.X, train_indexs, 0), np.delete(self.y, train_indexs, 0)

        model = external_model

        model.fit(X_train, y_train)
        y_hat_prob = model.predict_proba(X_test)[:, 1]
        y_hat = model.predict(X_test)
        self.accuracy_ = accuracy_score(y_test, model.predict(X_test))
        self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test, y_hat_prob)
        self.auc_ = auc(self.fpt_, self.tpr_)
        self.confusion_mat_ = confusion_matrix(y_test, y_hat)
        self.class_report_ = classification_report(y_test, y_hat)

        ac = (self.label_1_sum_ * (1 - self.fpt_) + self.label_0_sum_ * self.tpr_) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        thresholds = np.linspace(self.threshold_[-1], self.threshold_[0], self.tpr_.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]

    def train_test_split_mean_median_external_model(self, external_model, test_size=0.3, itirations_rate="mean"):
        """ return plot of roc curvs for 12 classifiers
        X: data as nump
        y: labels (binary:{0,1})
        """

        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)

        accuracy = []
        random_state = 100
        for j in range(42, random_state):
            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y,
                                                                test_size=test_size, shuffle=False,
                                                                random_state=j)

            classifier = external_model
            classifier.fit(X_train, y_train)
            probas_ = classifier.predict_proba(X_test)
            y_hat = classifier.predict(X_test)
            fpr, tpr, threshold = roc_curve(y_test, probas_[:, 1])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            accuracy.append(accuracy_score(y_test, y_hat))
        if itirations_rate == "mean":
            mean_tpr = np.mean(tprs, axis=0)
        else:
            mean_tpr = np.quantile(tprs, itirations_rate, axis=0)

        mean_tpr[-1] = 1.0

        self.auc_ = auc(mean_fpr, mean_tpr)

        if itirations_rate == "mean":
            self.accuracy_ = np.mean(accuracy, axis=0)
        else:
            self.accuracy_ = np.quantile(accuracy, itirations_rate, axis=0)

        ac = (self.label_1_sum_ * (1 - mean_fpr) + self.label_0_sum_ * mean_tpr) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        recal_pos = mean_tpr[index_max][0][0]
        recal_neg = 1 - mean_fpr[index_max][0][0]
        self.confusion_mat_best_on_roc_ = np.array([[int(recal_pos * self.label_0_sum_),
                                                     int(self.label_0_sum_ - int(recal_pos * self.label_0_sum_))],

                                                    [int(self.label_1_sum_ - int(recal_neg * self.label_1_sum_)),
                                                     int(recal_neg * self.label_1_sum_)]])
        self.accuracy_best_on_roc_ = (self.confusion_mat_best_on_roc_[0, 0] + self.confusion_mat_best_on_roc_[1, 1]) / np.sum(
            self.confusion_mat_best_on_roc_)

        self.fpt_ = mean_fpr
        self.tpr_ = mean_tpr
        thresholds = np.linspace(threshold[-1], threshold[0], mean_tpr.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]

    def train_test_split_mean_median_outliers_drop_external_moddel(self, external_moddel, test_size=0.30, itirations_rate="mean", contam_post=0.05,
                                                                   contam_neg=0.05):
        """ return data with droped outliers
        X: data as nump
        y: labels (binary:{0,1})
        """
        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)

        accuracy = []
        random_state = 100
        for j in range(42, random_state):
            X_tr, X_test, y_tr, y_test = train_test_split(self.X, self.y,
                                                          test_size=test_size, shuffle=False,
                                                          random_state=j)
            X_train, y_train, _, _ = outliers_for_binary_data(X_tr, y_tr, contamination_label1=contam_post, contamination_label2=contam_neg)
            X_test, y_test, _, _ = outliers_for_binary_data(X_test, y_test, contamination_label1=0.0001, contamination_label2=0.0001)
            classifier = external_moddel
            classifier.fit(X_train, y_train)
            probas_ = classifier.predict_proba(X_test)
            y_hat = classifier.predict(X_test)
            fpr, tpr, threshold = roc_curve(y_test, probas_[:, 1])
            tprs.append(interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            accuracy.append(accuracy_score(y_test, y_hat))
        if itirations_rate == "mean":
            mean_tpr = np.mean(tprs, axis=0)

        else:
            mean_tpr = np.quantile(tprs, itirations_rate, axis=0)

        mean_tpr[-1] = 1.0

        self.auc_ = auc(mean_fpr, mean_tpr)

        if itirations_rate == "mean":
            self.accuracy_ = np.mean(accuracy, axis=0)
        else:
            self.accuracy_ = np.quantile(accuracy, itirations_rate, axis=0)

        ac = (self.label_1_sum_ * (1 - mean_fpr) + self.label_0_sum_ * mean_tpr) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        recal_pos = mean_tpr[index_max][0][0]
        recal_neg = 1 - mean_fpr[index_max][0][0]
        self.confusion_mat_best_on_roc_ = np.array([[int(recal_pos * self.label_0_sum_),
                                                     int(self.label_0_sum_ - int(recal_pos * self.label_0_sum_))],

                                                    [int(self.label_1_sum_ - int(recal_neg * self.label_1_sum_)),
                                                     int(recal_neg * self.label_1_sum_)]])
        self.accuracy_best_on_roc_ = (self.confusion_mat_best_on_roc_[0, 0] + self.confusion_mat_best_on_roc_[1, 1]) / np.sum(
            self.confusion_mat_best_on_roc_)

        self.fpt_ = mean_fpr
        self.tpr_ = mean_tpr
        thresholds = np.linspace(threshold[-1], threshold[0], mean_tpr.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]

    def k_folds_external_model(self, extrenal_model, n_folds=5, shuffle=False, random_state=None):

        kf = KFold(n_splits=n_folds, shuffle=shuffle, random_state=random_state)
        y_hat_prob = np.zeros(len(self.y))
        y_hat = np.zeros(len(self.y))
        y_test_ = np.zeros(len(self.y))

        for ix_train, ix_test in kf.split(self.X):
            X_train, X_test = self.X[ix_train], self.X[ix_test]
            y_train, y_test = self.y[ix_train], self.y[ix_test]
            model = extrenal_model

            model.fit(X_train, y_train)
            y_hat_prob[ix_test] = model.predict_proba(X_test)[:, 1]
            y_hat[ix_test] = model.predict(X_test)
            y_test_[ix_test] = y_test

        self.y_test_ = y_test_
        self.y_predict_ = y_hat
        self.y_predict_prob_ = y_hat_prob
        self.fpt_, self.tpr_, self.threshold_ = roc_curve(y_test_, y_hat_prob)
        self.auc_ = auc(self.fpt_, self.tpr_)
        self.confusion_mat_ = confusion_matrix(y_test_, y_hat)
        self.class_report_ = classification_report(y_test_, y_hat)
        self.accuracy_ = accuracy_score(y_test_, y_hat)

        ac = (self.label_1_sum_ * (1 - self.fpt_) + self.label_0_sum_ * self.tpr_) / (self.label_0_sum_ + self.label_1_sum_)
        accuracy_best_on_roc = np.max(ac)
        index_max = np.argwhere(ac == accuracy_best_on_roc)
        thresholds = np.linspace(self.threshold_[-1], self.threshold_[0], self.tpr_.shape[0])
        self.best_threshold_ = thresholds[index_max][0][0]
        return self

    def show_roc(self, legend_location=4, fig_size_x=7, fig_size_y=7):
        fig = plt.figure(figsize=(fig_size_x, fig_size_y))
        plt.rc("font", family="Times New Roman", size=16)
        plt.rc('axes', linewidth=2)
        plt.plot(self.fpt_, self.tpr_, label="%s (AUC = %0.2f)" % (self.classifier_name, self.auc_))
        plt.plot([0, 1], [0, 1], "--r")
        plt.xlabel("1-Specificity", fontdict={"size": 21})
        plt.ylabel("Sensitivity", fontdict={"size": 21})
        plt.legend(loc=legend_location)

    def show_scores_by_featuers(self, legend_location=4, fig_size_x=7, fig_size_y=7, feature_selection_tech="chi2"):
        """

        :param legend_location:
        :param fig_size_x:
        :param fig_size_y:
        :param feature_selection_tech:
        :return:
        """
        fig = plt.figure(figsize=(fig_size_x, fig_size_y))
        plt.rc("font", family="Times New Roman", size=16)
        plt.rc('axes', linewidth=2)

        report = self.grid_search_report_.loc[:, ["param_feature_selection_method__k", "mean_test_score", feature_selection_tech]].dropna()
        report = report[report[feature_selection_tech] != ""]
        n_features = report["param_feature_selection_method__k"].replace("all", self.X.shape[1]).values
        scores = np.around(report["mean_test_score"].values, 2)

        plt.scatter(n_features, scores)
        plt.ylabel("Scores rate", fontdict={"size": 21})
        plt.xlabel("Number of features", fontdict={"size": 21})

    # self.fpt_, self.tpr_, self.label_0_sum_, self.label_1_sum_

    def optimal_cut_point_on_roc(self, delta_max=0.2, plot_point_on_ROC=False):
        """
        This function retrns the optimal cut point on the ROC according to your input
        :param delta_max: maximum difference between recall_1(sensitivity) and recall_2 (specificity) [float number]
        :param plot_point_on_ROC: default "False", in case of "True" the function return ROC curve plot with red point
                                  that indicate the optimal point
        :return: dictionary with classification metrics
        """

        tpr, fpr, n_p, n_n = self.fpt_, self.tpr_, self.label_0_sum_, self.label_1_sum_
        sen = fpr[fpr > 0.55]
        spe = 1 - tpr[fpr > 0.55]

        delt = abs(sen - spe)
        ix_1 = np.argwhere(delt <= delta_max)

        acc = (n_p / (n_p + n_n)) * sen[ix_1] + (n_n / (n_p + n_n)) * spe[ix_1]
        best_point = (1 - spe[np.argmax(acc)], sen[np.argmax(acc)])
        auc = np.around(np.trapz(fpr, tpr), 2)

        recall_1 = sen[np.argmax(acc)]
        recall_2 = spe[np.argmax(acc)]
        precision_1 = (n_p * sen[np.argmax(acc)]) / (n_p * sen[np.argmax(acc)] + n_n * (1 - spe[np.argmax(acc)]))
        precision_2 = (n_n * spe[np.argmax(acc)]) / (n_n * spe[np.argmax(acc)] + n_p * (1 - sen[np.argmax(acc)]))

        report = {"auc": np.around(auc, 2), "acc": np.around(acc.max(), 2), "recall_1": np.around(recall_1, 2),
                  "recall_2": np.around(recall_2, 2), "precision_1": np.around(precision_1, 2),
                  "precision_2": np.around(precision_2, 2)
                  }
        if plot_point_on_ROC:
            plt.plot(tpr, fpr)
            plt.scatter(best_point[0], best_point[1], c="red")
            plt.xlabel("1-specificity")
            plt.ylabel("sensitivity")
        return report


class KLDivergence():
    def __init__(self, k=10):
        self.k = k

    def fit(self, X, y=None):
        """Compute the mean and std to be used for later scaling.
        Parameters
        ----------
        X : {array-like, sparse matrix}, shape [n_samples, n_features]
            The data used to compute the mean and standard deviation
            used for later scaling along the features axis.
        y
            Ignored
        """

        # Reset internal state before fitting

        return self.kl_fit(X, y)

    def kl_fit(self, X, y):

        y_unique = list(np.unique(y))
        features_list = np.linspace(0, X.shape[1] - 1, X.shape[1]).astype("int")
        X_1 = X[y == y_unique[0]]
        X_2 = X[y == y_unique[1]]
        x_1_mean = np.mean(X_1, axis=0)
        x_2_mean = np.mean(X_2, axis=0)

        p = abs(x_1_mean)
        q = abs(x_2_mean)
        sid_p = list(p[i] * np.log2(p[i] / q[i]) for i in range(len(p)))
        sid_q = list(q[i] * np.log2(q[i] / p[i]) for i in range(len(p)))

        mean_KL = list(0.5 * (sid_p[_] + sid_q[_]) for _ in range(len(sid_p)))
        results = pd.DataFrame(features_list, columns=["features_index"])
        results["mean_KL_divregence"] = mean_KL
        self.results_sorted = results.sort_values(by="mean_KL_divregence", ascending=False)

        if self.k == "all":
            self.best_feat = self.results_sorted["features_index"]

        else:
            self.best_feat = self.results_sorted["features_index"].iloc[:self.k]

        return self

    def transform(self, X):
        """Perform standardization by centering and scaling
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data used to scale along the features axis.

        """

        X = X[:, self.best_feat.index]

        return X

    def set_params(self, **params):
        """
        Set the parameters of this estimator.
        The method works on simple estimators as well as on nested objects
        (such as pipelines). The latter have parameters of the form
        ``<component>__<parameter>`` so that it's possible to update each
        component of a nested object.
        Parameters
        ----------
        **params : dict
            Estimator parameters.
        Returns
        -------
        self : object
            Estimator instance.
        """

        return self

    def fit_transform(self, X, y=None, **fit_params):
        """
        Fit to data, then transform it.
        Fits transformer to X and y with optional parameters fit_params
        and returns a transformed version of X.
        Parameters
        ----------
        X : numpy array of shape [n_samples, n_features]
            Training set.
        y : numpy array of shape [n_samples]
            Target values.
        **fit_params : dict
            Additional fit parameters.
        Returns
        -------
        X_new : numpy array of shape [n_samples, n_features_new]
            Transformed array.
        """
        # non-optimized default implementation; override when a better
        # method is possible for a given clustering algorithm
        if y is None:
            # fit method of arity 1 (unsupervised transformation)
            return self.fit(X, **fit_params).transform(X)
        else:
            # fit method of arity 2 (supervised transformation)
            return self.fit(X, y, **fit_params).transform(X)


def blanced_data(X, y, random_state=10):
    """
    This function balances the data (binary) according to the small class
    :param X: numpy array of shape [n_samples, n_features].
    :param y: numpy array of shape [n_samples]
              Target values.
    :return: blanced data (X,y)

    """
    np.random.seed(random_state)
    X_0 = X[y == 0]
    X_1 = X[y == 1]

    y_0 = y[y == 0]
    y_1 = y[y == 1]
    if X_0.shape[0] > X_1.shape[0]:
        np.random.shuffle(X_0)
        X_0 = X_0[:len(X_1)]
        y_0 = y[y == 0][:len(X_1)]
    else:
        np.random.shuffle(X_1)
        X_1 = X_1[:len(X_0)]
        y_1 = y[y == 1][:len(X_0)]

    da_0 = pd.concat([pd.DataFrame(X_0), pd.DataFrame(y_0)], axis=1)
    da_1 = pd.concat([pd.DataFrame(X_1), pd.DataFrame(y_1)], axis=1)

    data = np.concatenate((da_0.values, da_1.values), axis=0)
    np.random.shuffle(data)

    X = data[:, :-1]
    y = data[:, -1]

    return X, y.astype("int")


def mean_stb_data(X, beta=0.5):
    """
    This function calculate the confidence interval
    :param X: data (type: numpy array)
    :param beta: the width of the interval (type: float)
    :return: new data with mean, up_interval and low_interval
    """
    X_mean = X.mean()
    X_std = X.std()
    X_up = X_mean + beta * X_std
    X_low = X_mean - beta * X_std

    df = pd.DataFrame(X_mean, columns=["mean"])
    df["std"] = X_std
    df["X_up"] = X_up
    df["X_low"] = X_low

    return df, X_mean.values, X_up.values, X_low.values


def spectra_plot(df,
                 label,
                 initial_feature="1801.264",
                 final_feature="898.703",
                 out_window_size_tuple_x=(900, 1800),
                 out_window_size_tuple_y=(-0.003, 0.255),
                 inset_axis=True,
                 inset_window_position=[0.02, 0.43, 0.75, 0.54],
                 labels_dict=[{"label": "S", "label_legend": "label_1", "color": "blue"}, {"label": "R", "label_legend": "label_2", "color": "red"}],
                 confidence_iterval_width=0.5,
                 texts_on_graph_dict=[{"which_axis": "ax2", "text_sentence": "ER", "position_x": 1000, "position_y": 0.025}],
                 functional_groups=True,
                 functional_groups_dict=[{"group_name": 'Amid III', "arrow_position": (1241, 0.028), "xytext": (1241, 0.05)},
                                         {"group_name": 'as CH' + r"$_3$", "arrow_position": (1456, 0.018), "xytext": (1456 - 8, 0.045)},
                                         {"group_name": 'Amid II', "arrow_position": (1548, 0.12), "xytext": (1548 - 27, 0.16)},
                                         {"group_name": 'Amid I', "arrow_position": (1659, 0.232), "xytext": (1659 - 25, 0.245)},
                                         {"group_name": "sym CCO" + r"$^-$", "arrow_position": (1400, 0.02), "xytext": (1400, 0.058)}],
                 inset_control_x=(958, 1180),
                 inset_control_y=(0, 0.1),
                 legend_location=2,
                 graph_item="none",
                 save_fig=False,
                 y_title="Absorbance (A.U)",
                 x_title="Wavenumber (cm" + r"$^{-1})$",
                 file_name="spectra"):
    """

    :param df: data frame (type: pandas df)
    :param label: name of column of the labels (type: string)
    :param initial_feature: first column name (type: string)
    :param final_feature: last column name(type: string)
    :param inset_axis: insert inset_axis as small window, True or Falst (type: boolean)
    :param inset_window_position: the limits of the inset window on respect to the major window (type: list of floats)
    :param labels_dict: list of dictionaries include the details about the classes (type: list of dictionaries)
    :param confidence_iterval_width: the width of the confidence interval (type: float)
    :param texts_on_graph_dict: list of dictionaries include the details about texts on the graph (type: list of dictionaries)
    :param functional_groups: insert functional groups as text-arrows, True or Falst (type: boolean)
    :param functional_groups_dict: list of dictionaries include the details about vibration functional groups (type: list of dictionaries)
    :param inset_control_x: tuning the x-axis limtis inside the inset-window (type: tuple)
    :param inset_control_y: tuning the y-axis limtis inside the inset-window (type: tuple)
    :param legend_location: legend location on the window (type: integer)
    :param graph_item: item for the figure, default "none" dont add any thing (type: string)
    :param save_fig: do you want to save the figure?, True or Falst (type: boolean)
    :param y_title: title of the y-axis (type: string)
    :param x_title: title of the x-axis (type: string)
    :param file_name: name of the file in case of saving the figure in file (type: strring)

    :return: show the spectra figure
    """
    wavenumbers = df.loc[:, initial_feature: final_feature].columns.values.astype("float")
    X = df.loc[:, initial_feature: final_feature]
    y = df[label]

    df_sub = pd.concat([X, y], axis=1)
    df_sub = df_sub.dropna()

    plt.rc("font", size=16, family="Times New Roman")
    plt.rc('axes', linewidth=2)
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_axes([0, 0, 1, 1])

    if inset_axis:
        ax2 = fig.add_axes(inset_window_position)
        ax2.set_yticks([])
        for lab_indx in range(len(labels_dict)):
            spectra = df_sub[df_sub[label] == labels_dict[lab_indx]["label"]]
            spectra = pd.DataFrame(spectra.drop(label, axis=1).values.astype("float"))
            _, spec_mean, spec_up, spec_low = mean_stb_data(spectra, beta=confidence_iterval_width)
            ax1.plot(wavenumbers, spec_mean, color=labels_dict[lab_indx]["color"])
            ax1.fill_between(wavenumbers, spec_up, spec_low, color=labels_dict[lab_indx]["color"], alpha=0.1)

            ax2.plot(wavenumbers, spec_mean, color=labels_dict[lab_indx]["color"], label=labels_dict[lab_indx]["label_legend"])
            ax2.fill_between(wavenumbers, spec_up, spec_low, color=labels_dict[lab_indx]["color"], alpha=0.1)

            ax2.set_xlim(inset_control_x)
            ax2.tick_params(axis='x', which='major', labelsize=12)
            ax2.set_ylim(inset_control_y)



    else:
        for lab_indx in range(len(labels_dict)):
            spectra = df_sub[df_sub[label] == labels_dict[lab_indx]["label"]]
            spectra = pd.DataFrame(spectra.drop(label, axis=1).values.astype("float"))
            _, spec_mean, spec_up, spec_low = mean_stb_data(spectra, beta=confidence_iterval_width)
            ax1.plot(wavenumbers, spec_mean, color=labels_dict[lab_indx]["color"], label=labels_dict[lab_indx]["label_legend"])
            ax1.fill_between(wavenumbers, spec_up, spec_low, color=labels_dict[lab_indx]["color"], alpha=0.1)

    if functional_groups:
        for gr in functional_groups_dict:
            ax1.annotate(gr["group_name"], xy=gr["arrow_position"], xytext=gr["xytext"],
                         arrowprops=dict(facecolor='black', shrink=0.05, width=2))

    ax1.set_xlabel(x_title, fontdict=dict(size=23, fontname="Times New Roman", fontweight='bold'))
    ax1.set_ylabel(y_title, fontdict=dict(size=23, fontname="Times New Roman", fontweight='bold'))
    ax1.set_xlim(out_window_size_tuple_x)
    ax1.set_ylim(out_window_size_tuple_y)
    ax1.tick_params(axis='both', which='major', labelsize=16)

    for tex in texts_on_graph_dict:
        if tex["which_axis"] == "ax2":
            ax2.text(tex["position_x"], tex["position_y"], s=tex["text_sentence"], fontdict=dict(size=22, fontname="Times New Roman"))
            ax2.legend(loc=legend_location, ncol=1)
        elif tex["which_axis"] == "ax1":
            ax1.text(tex["position_x"], tex["position_y"], s=tex["text_sentence"], fontdict=dict(size=22, fontname="Times New Roman"))
            ax1.legend(loc=legend_location, ncol=1)

    if graph_item != "none":
        ax1.text(1755, 0.23, s="(" + graph_item + ")", fontdict=dict(size=25, fontname="Times New Roman", fontweight="bold"))

    if save_fig:
        fig.savefig(file_name + texts_on_graph_dict[0]["text_sentence"] + ".tif", dpi=600, bbox_inches='tight',
                    pil_kwargs={"compression": "tiff_lzw"})


def plot_pie_chart(y, classes_present_symbol=["class_A", "class_B"], classes=[0, 1], chatr_title="Pie_Chart", legend_loc=1):
    """

    :param y: labels array (type: numpy array)
    :param classes_present_symbol: list of  labels present names (type: list of strings)
    :param classes: list of the labels symbol as in the array (type: list of integers)
    :param chatr_title: title of the chart (type: string)
    :param legend_loc: legend location (type: integer)
    :return: plot pie-chart
    """
    labels = []
    class_quantity = []
    for c in range(len(classes)):
        class_quantity.append(np.sum(y == classes[c]))
        labels.append(classes_present_symbol[c] + "  %d" % (class_quantity[c]))

    plt.rc("font", size=16, family="Times New Roman")
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    ax1.pie(class_quantity, autopct='%1.0f%%', shadow=True, textprops={"color": "w", "weight": "bold", "size": 21})
    ax1.axis('equal')
    plt.legend(labels, bbox_to_anchor=(0.6, 1.2), loc=legend_loc)
    plt.tight_layout()
    plt.xlabel(chatr_title, fontdict={"size": 24, "weight": "bold"})
    plt.show()


from sklearn.utils import resample


def bootstrap_data(X, y, labels_dict=[{"label": 0, "n_samples": 50}, {"label": 1, "n_samples": 50}], seed=10):
    """
    This function bootstraped the input data
    :param X: data's features values (type: numpy.array)
    :param y: data's labels (type: numpy.array)
    :param labels_dict:  labels details (type: list of dictionary)
    :param seed: random state seeed (type: integer)
    :return: boostraped data with length of n_samples
    """
    np.random.seed(seed)
    df_ = pd.DataFrame(X)
    df_["label"] = y

    boost_data_p = resample(df_[df_["label"] == labels_dict[0]["label"]], n_samples=labels_dict[0]["n_samples"])
    boost_data_n = resample(df_[df_["label"] == labels_dict[1]["label"]], n_samples=labels_dict[1]["n_samples"])

    boost_data = np.concatenate((boost_data_p, boost_data_n), axis=0)
    np.random.shuffle(boost_data)

    y = boost_data[:, -1].astype("int")
    X = boost_data[:, :-1]

    return X, y


def ensemble_targets(actual_targets_list, predicted_targets_list, postive_target):
    """
    This function return classification for ensable targets (at_least_one, ...)
    :param actual_targets_list: list of targets arrays
    :param predicted_targets_list: list of predicted trgets arrays
    :param report: return classification report as pandas Data Frame
    :return: actual, predicted values according to statistical caluclation(pandas data frame)
    """
    actual_ary = actual_targets_list[0]
    predict_ary = predicted_targets_list[0]
    for n_targets in range(1, len(actual_targets_list)):
        actual_ary = np.vstack((actual_ary, actual_targets_list[n_targets]))
        predict_ary = np.vstack((predict_ary, predicted_targets_list[n_targets]))
    sum_act = np.sum(actual_ary, 0)
    sum_pre = np.sum(predict_ary, 0)
    # at_least_one
    y_at_actual = np.zeros(actual_ary[0].shape[0])
    y_at_actual[sum_act != abs(1 - postive_target)] = 1
    y_at_predicted = np.zeros_like(actual_ary[0])
    y_at_predicted[sum_pre != abs(1 - postive_target)] = 1

    df_ = pd.DataFrame()
    df_["at_leas_one_act"] = y_at_actual.astype(int)
    df_["at_leas_one_prd"] = y_at_predicted.astype(int)

    targets_num = len(actual_targets_list)
    indexs_list = []
    for ix in range(targets_num):
        arr_act = np.zeros(actual_ary[0].shape[0])
        arr_prd = np.zeros(actual_ary[0].shape[0])

        arr_act[sum_act == (targets_num - ix)] = 1
        arr_prd[sum_pre == (targets_num - ix)] = 1

        df_[str(ix + 1) + "/" + str(targets_num) + "_act"] = arr_act.astype(int)
        df_[str(ix + 1) + "/" + str(targets_num) + "_prd"] = arr_prd.astype(int)
        indexs_list.append(str(ix + 1) + "/" + str(targets_num))
    df_act = df_.iloc[:, ::2]
    df_prd = df_.iloc[:, 1::2]
    acc = []
    ppv = []
    npv = []
    sen = []
    spe = []
    n_pos = []
    n_neg = []

    for jx in range(targets_num + 1):
        cr = classification_report(df_act.iloc[:, jx], df_prd.iloc[:, jx])
        ppv.append(float(cr[74:78]))
        sen.append(float(cr[84:88]))
        n_pos.append(int(cr[105:108]))
        npv.append(float(cr[128:132]))
        spe.append(float(cr[138:142]))
        n_neg.append(int(cr[159:162]))
        acc.append(float(cr[203:207]))

    df_scores = pd.DataFrame()
    df_scores["n_pos"] = n_pos
    df_scores["n_neg"] = n_neg
    df_scores["acc"] = acc
    df_scores["sen"] = sen
    df_scores["spe"] = spe
    df_scores["ppv"] = ppv
    df_scores["npv"] = npv
    df_scores.index = ["at_leas_one"] + indexs_list

    return df_, df_scores


def split_fitted_unbalnced(X, y, train_size=0.70, random_state=10):
    """

    :param X:
    :param y:
    :param train_size:
    :param random_state:
    :return:
    """
    np.random.seed(random_state)
    np.random.shuffle(X)
    np.random.shuffle(y)
    labels = np.unique(y)
    labels_info = []
    for lab in labels:
        y_ = y[y == lab]
        X_ = X[y == lab]
        dic_ = {}

        dic_["y_train"], dic_["y_test"] = y_[:int(train_size * X_.shape[0])], y_[int(train_size * X_.shape[0]):]
        dic_["X_train"], dic_["X_test"] = X_[:int(train_size * X_.shape[0])], X_[int(train_size * X_.shape[0]):]

        labels_info.append(dic_)
    X_train, X_test = labels_info[0]["X_train"], labels_info[0]["X_test"]
    y_train, y_test = labels_info[0]["y_train"], labels_info[0]["y_test"]

    for _ in range(1, len(labels_info)):
        X_train = np.vstack((X_train, labels_info[_]["X_train"]))
        X_test = np.vstack((X_test, labels_info[_]["X_test"]))
        y_train = np.hstack((y_train, labels_info[_]["y_train"]))
        y_test = np.hstack((y_test, labels_info[_]["y_test"]))

    return X_train, X_test, y_train, y_test


def sampling_unbalanced_data(df, labels_col, sampling_mode="over", new_shape="none", random_state=10):
    """
    This function return sampling data
    :param df: pandas data frame
    :param labels_col:
    :param sampling_mode: "over" for data extenstion and "under" for data reduce
    :param new_shape: new shape, if "none" the shape of the highst class data
    :param random_state:
    :return:resampling data frame
    """
    df = df.dropna()
    labels = df[labels_col].unique()
    df_1 = df[df[labels_col] == labels[0]]
    df_2 = df[df[labels_col] == labels[1]]

    if (df_1.shape[0] > df_2.shape[0]) & (sampling_mode == "over") & (new_shape == "none"):
        df_2_new = pd.concat([df_2.sample(df_1.shape[0] - df_2.shape[0], replace=True, random_state=random_state), df_2])
        df_1_new = df_1

    elif (df_2.shape[0] > df_1.shape[0]) & (sampling_mode == "over") & (new_shape == "none"):
        df_1_new = pd.concat([df_1.sample(df_2.shape[0] - df_1.shape[0], replace=True, random_state=random_state), df_1])
        df_2_new = df_2

    elif (df_1.shape[0] > df_2.shape[0]) & (sampling_mode == "under") & (new_shape == "none"):
        df_1_new = df_1.sample(df_2.shape[0], replace=True, random_state=random_state)
        df_2_new = df_2

    elif (df_2.shape[0] > df_1.shape[0]) & (sampling_mode == "under") & (new_shape == "none"):
        df_2_new = df_2.sample(df_1.shape[0], replace=True, random_state=random_state)
        df_1_new = df_1






    elif (df_1.shape[0] > df_2.shape[0]) & (sampling_mode == "over") & (new_shape != "none"):
        df_2_new = pd.concat([df_2.sample(new_shape - df_2.shape[0], replace=True, random_state=random_state), df_2])
        df_1_new = df_1

    elif (df_2.shape[0] > df_1.shape[0]) & (sampling_mode == "over") & (new_shape != "none"):
        df_1_new = pd.concat([df_1.sample(new_shape - df_1.shape[0], replace=True, random_state=random_state), df_1])
        df_2_new = df_2

    elif (df_1.shape[0] > df_2.shape[0]) & (sampling_mode == "under") & (new_shape != "none"):
        df_1_new = df_1.sample(new_shape, replace=True, random_state=random_state)
        df_2_new = df_2

    elif (df_2.shape[0] > df_1.shape[0]) & (sampling_mode == "under") & (new_shape != "none"):
        df_2_new = df_2.sample(new_shape, replace=True, random_state=random_state)
        df_1_new = df_1

    return pd.concat([df_1_new, df_2_new], axis=0).sample(frac=1)
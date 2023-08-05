#!/usr/bin/env python
# coding: utf-8

# @Author: dehong
# @Date: 2020-06-09
# @Time: 18:24
# @Name: model_tools

from sklearn import ensemble, gaussian_process, linear_model, naive_bayes, neighbors, svm, tree, discriminant_analysis
from sklearn import model_selection, feature_selection
from xgboost import XGBClassifier
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .view_tools import correlation_heatmap

model = [
    # 集成方法
    ensemble.AdaBoostClassifier(),
    ensemble.BaggingClassifier(),
    ensemble.GradientBoostingClassifier(),
    ensemble.RandomForestClassifier(),
    ensemble.ExtraTreesClassifier(),

    # 高斯过程
    gaussian_process.GaussianProcessClassifier(),

    # 线性模型
    linear_model.LogisticRegressionCV(),
    linear_model.LogisticRegression(),
    linear_model.PassiveAggressiveClassifier(),
    linear_model.RidgeClassifierCV(),
    linear_model.SGDClassifier(),
    linear_model.Perceptron(),

    # 贝叶斯
    naive_bayes.GaussianNB(),
    naive_bayes.BernoulliNB(),

    # 近邻算法
    neighbors.KNeighborsClassifier(),

    # SVM
    svm.SVC(probability=True),
    svm.LinearSVC(),
    svm.NuSVC(),

    # Trees
    tree.DecisionTreeClassifier(),
    tree.ExtraTreeClassifier(),

    # 判别分析
    discriminant_analysis.LinearDiscriminantAnalysis(),
    discriminant_analysis.QuadraticDiscriminantAnalysis(),

    # XGBoost
    XGBClassifier()
]

cv_split = model_selection.ShuffleSplit(n_splits=10, test_size=0.2, train_size=0.7, random_state=0)
model_columns = ['MLA_Name', 'MLA_Parameters', 'MLA Train Accuracy Mean', 'MLA Test Accuracy Mean',
                 'MLA Test Accuracy 3*STD', 'MLA Time']
model_compare = pd.DataFrame(columns=model_columns)


def predict(data, features, target):
    print('------预选模型')
    """
    模型粗选，展示各个模型的效果
    :param data: 测试数据集
    :param features: 特征字段 array
    :param target: 目标字段 array
    :return:
    """
    model_predict = pd.DataFrame()
    model_predict['label'] = data[target]
    row_index = 0
    for alg in model:
        # 设置名字和参数
        model_name = alg.__class__.__name__
        print(model_name)
        model_compare.loc[row_index, 'MLA_Name'] = model_name
        model_compare.loc[row_index, 'MLA_Parameters'] = str(alg.get_params())

        # 交叉验证得分模型
        cv_results = model_selection.cross_validate(alg, data[features], data[target], cv=cv_split,
                                                    return_train_score=True)
        model_compare.loc[row_index, 'MLA Train Accuracy Mean'] = cv_results['train_score'].mean()
        model_compare.loc[row_index, 'MLA Test Accuracy Mean'] = cv_results['test_score'].mean()
        model_compare.loc[row_index, 'MLA Test Accuracy 3*STD'] = cv_results['test_score'].std() * 3
        model_compare.loc[row_index, 'MLA Time'] = cv_results['fit_time'].mean()

        # 保存预测值
        alg.fit(data[features], data[target])
        model_predict[model_name] = alg.predict(data[features])
        row_index += 1

    model_compare.sort_values(by=['MLA Test Accuracy Mean'], ascending=False, inplace=True)
    # 通过图表展示效果
    sns.barplot(x='MLA Test Accuracy Mean', y='MLA_Name', data=model_compare, color='m')
    plt.xlabel('Accuracy Score(%)')
    plt.ylabel('Algorithm')
    plt.title('Machine Learning Algorithm Accuracy Score \n')
    plt.show()
    return model_predict


def thermogram_model(model_predict):
    print('------热力图，观察不同模型之间的相关性')
    correlation_heatmap(model_predict)


def tune_feature(data, features, target, model):
    print('------自动选择特征')
    alg_rfe = feature_selection.RFECV(model, step=1, scoring='accuracy', cv=cv_split)
    alg_rfe.fit(data[features], data[target])

    x_rfe = data[features].columns[alg_rfe.get_support()]
    rfe_results = model_selection.cross_validate(alg_rfe, data[x_rfe], data[target], cv=cv_split,
                                                 return_train_score=True)
    print('------最好的特征以及该特征下模型效果')
    print('AFTER DT RFE Training Shape New: ', data[x_rfe].shape)
    print('AFTER DT RFE Training Columns New: ', x_rfe)
    print("AFTER DT RFE Training w/bin score mean: {:.2f}".format(rfe_results['train_score'].mean() * 100))
    print("AFTER DT RFE Test w/bin score mean: {:.2f}".format(rfe_results['test_score'].mean() * 100))
    print("AFTER DT RFE Test w/bin score 3*std: +/- {:.2f}".format(rfe_results['test_score'].std() * 100 * 3))


def tune_model(data, features, target, model, param_dict):
    print('------自动调节参数')
    best_model = model_selection.GridSearchCV(model, param_grid=param_dict, scoring='roc_auc', cv=cv_split)
    best_model.fit(data[features], data[target])

    print('------最好的模型参数以及该参数下模型效果')
    best_results = model_selection.cross_validate(best_model, data[features], data[target], cv=cv_split,
                                                  return_train_score=True)
    print('AFTER DT Parameters: ', best_model.best_params_)
    print("AFTER DT Training w/bin set score mean: {:.2f}".format(best_results['train_score'].mean() * 100))
    print("AFTER DT Test w/bin set score mean: {:.2f}".format(best_results['test_score'].mean() * 100))
    print("AFTER DT Test w/bin set score min: {:.2f}".format(best_results['test_score'].min() * 100))

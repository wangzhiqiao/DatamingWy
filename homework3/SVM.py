import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.mixture import GMM
import csv
import matplotlib.pyplot as plt


train_data = []
test_data = []
train_label = []


database_train = './train.csv'
database_test = './test.csv'
attr = [2, 4, 5, 6, 7, 9, 11]
bin_num = [3, 2, 20, 4, 4, 20, 3]
attr_name = []


NA = ['NA', 'None', '', 'NONE', 'none', 'Na']

sex = {'male': 0, 'female': 1}
embarked = {'C': 0, 'Q': 1, 'S': 2, '': 3}


def data_preprocess():
    global train_data, test_data, train_label, attr_name
    with open(database_train, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        events = []
        for i, row in enumerate(reader):
            event = []
            for j in attr:
                if i != 0:
                    if j == 4:
                        row[j] = sex[row[j]]
                    elif j == 11:
                        row[j] = embarked[row[j]]
                    else:
                        if row[j] in NA:
                            row[j] = -1
                        else:
                            row[j] = float(row[j])
                # print(row[j])
                event.append(row[j])

            if i == 0:
                attr_name = event
            else:
                train_label.append(int(row[1]))
                events.append(event)

        train_data = np.array(events)

    with open(database_test, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        events = []
        for i, row in enumerate(reader):
            event = []
            if i != 0:
                for j in attr:
                    j = j - 1

                    if j == 3:
                        row[j] = sex[row[j]]
                    elif j == 10:
                        row[j] = embarked[row[j]]
                    else:
                        if row[j] in NA:
                            row[j] = 0
                        else:
                            row[j] = float(row[j])

                    event.append(row[j])

                events.append(event)

        test_data = np.array(events)


def classification_svm():
    clf = svm.SVC(C=0.8)
    clf.fit(train_data, train_label)

    return clf.predict(test_data)


def plot_classificaton_result(test_label, classifier=''):
    pred = []
    labelled = []
    pred.append([])
    pred.append([])
    labelled.append([])
    labelled.append([])

    for i, l in enumerate(test_label):
        pred[l].append(test_data[i])

    for i, l in enumerate(train_label):
        labelled[l].append(train_data[i])

    for i in range(2):
        pred[i] = np.array(pred[i]).transpose()

    for i in range(2):
        labelled[i] = np.array(labelled[i]).transpose()

    for i in range(7):

        fig, axes = plt.subplots(ncols=2)
        fig.set_size_inches(8, 5)
        ax0, ax1 = axes.flatten()
        ax0.hist([pred[0][i], pred[1][i]], bins=bin_num[i],
                 label=['Death', 'Survival'])
        ax0.set_title('Predicted Survival over %s' % attr_name[i])

        ax1.hist([labelled[0][i], labelled[1][i]],
                 bins=bin_num[i], label=['Death', 'Survival'])
        ax1.set_title('Labelled Survival over %s' % attr_name[i])

        plt.legend()

        plt.savefig('./figures/%s.png' % (attr_name[i]))
        plt.close()


def main():
    data_preprocess()
    label_svm = classification_svm()
    plot_classificaton_result(label_svm, 'svm')


if __name__ == '__main__':
    main()

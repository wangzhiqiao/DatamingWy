import pandas
import numpy
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.externals.six import StringIO
from matplotlib.colors import ListedColormap
import pydotplus
data_train = pandas.read_csv('./train.csv')


def dataPreprocess(data_train):
    age_df = data_train[['Age', 'Fare', 'Parch', 'SibSp', 'Pclass']]

# 乘客分成已知年龄和未知年龄两部分
    known_age = age_df[age_df.Age.notnull()].as_matrix()
    unknown_age = age_df[age_df.Age.isnull()].as_matrix()

# y即目标年龄
    y = known_age[:, 0]

# X即特征属性值
    X = known_age[:, 1:]

# fit到RandomForestRegressor之中
    rfr = RandomForestRegressor(random_state=0, n_estimators=2000, n_jobs=-1)
    rfr.fit(X, y)

    # 用得到的模型进行未知年龄结果预测
    predictedAges = rfr.predict(unknown_age[:, 1::])

    # 用得到的预测结果填补原缺失数据
    data_train.loc[(data_train.Age.isnull()), 'Age'] = predictedAges
    data_train.loc[(data_train.Cabin.notnull()), 'Cabin'] = "Yes"
    data_train.loc[(data_train.Cabin.isnull()), 'Cabin'] = "No"
    return data_train, rfr


data_train, rfr = dataPreprocess(data_train)
# 特征因子化
dummies_Cabin = pandas.get_dummies(data_train['Cabin'], prefix='Cabin')

dummies_Embarked = pandas.get_dummies(
    data_train['Embarked'], prefix='Embarked')

dummies_Sex = pandas.get_dummies(data_train['Sex'], prefix='Sex')

dummies_Pclass = pandas.get_dummies(data_train['Pclass'], prefix='Pclass')

data_train = pandas.concat([data_train, dummies_Cabin,
                            dummies_Embarked, dummies_Sex, dummies_Pclass], axis=1)

# 数值数据归一化处理
import sklearn.preprocessing as preprocessing
scaler = preprocessing.StandardScaler()
age_scale_param = scaler.fit(data_train['Age'].values.reshape(-1, 1))
data_train['Age_scaled'] = scaler.fit_transform(
    data_train['Age'].values.reshape(-1, 1), age_scale_param)
fare_scale_param = scaler.fit(data_train['Fare'].values.reshape(-1, 1))
data_train['Fare_scaled'] = scaler.fit_transform(
    data_train['Fare'].values.reshape(-1, 1), fare_scale_param)

# 将标称型数据转化为数值型数据
data_train.loc[data_train['Sex'] == 'male', 'Sex'] = 1
data_train.loc[data_train['Sex'] == 'female', 'Sex'] = 0

X = data_train[["Age", "SibSp", "Parch", "Fare", "Pclass", "Sex"]]
y = data_train['Survived']
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=33)

# decision tree
dt = tree.DecisionTreeClassifier()
dt = dt.fit(X_train, y_train)


from sklearn.metrics import classification_report

print(dt.score(X_test, y_test))

y_predict = dt.predict(X_test)
print(classification_report(y_predict, y_test,
                            target_names=['遇难者', '生还者']))

feature_name = ["Age", "SibSp", "Parch", "Fare", "Pclass", "Sex"]
target_name = ["Survived", "Died"]
dot_data = StringIO()
tree.export_graphviz(dt, out_file=dot_data, feature_names=feature_name,
                     class_names=target_name, filled=True, rounded=True,
                     special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png("Decision_Tree_graph.png")

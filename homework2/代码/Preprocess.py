import csv
import pickle
database = './dataset/Building_Permits.csv'
NA = ['NA', 'None', '', 'NONE', 'none', 'Na']


def preprocess():
    dt = []

    with open('./dataset/item', 'r') as fp:
        attr = [int(i) - 1 for i in fp.read().split(' ')]

    with open(database, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        for _, row in enumerate(reader):
            item = []
            if _ == 0:
                name = row
            for i in attr:
                at = row[i]
                if at in NA:
                    at = '(%s) NA' % (name[i])
                else:
                    at = '(%s) %s' % (name[i], row[i])

                item.append(at)

            dt.append(item)
            # print(item)

    with open('./dataset/preprocessed.pkl', 'wb') as fp:
        pickle.dump(dt, fp)


if __name__ == '__main__':
    preprocess()

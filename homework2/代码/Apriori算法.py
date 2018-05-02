import numpy as np
import pickle
import apyori
from apyori import apriori


def check_set(set_):
    cnt = 0
    for item in set_:
        if item[-2:] != 'NA':
            cnt += 1
    return cnt


def main():
    with open('./dataset/preprocessed.pkl', 'rb') as fp:
        transactions = pickle.load(fp, encoding='iso-8859-1')
    results = list(apriori(transactions, min_support=0.01, max_length=1000))
    # print(len(results))

    items_by_k = []
    relations_by_k = []

    for i in range(9):
        items_by_k.append([])
        relations_by_k.append([])

    for event in results:
        items = event.items
        n = len(items)
        # print(n)
        support = event.support
        ordered_statistics = event.ordered_statistics
        items_by_k[n - 1].append((support, items))
        relations_by_k[n - 1].append((support, ordered_statistics))

    with open('frequent_items.txt', 'w') as fp:
        for _, items in enumerate(items_by_k):
            items = sorted(items, reverse=True)
            fp.write(
                '\n%d-Itemset\n' % (_ + 1))
            for item in items:
                set_ = item[1]
                support_ = item[0]
                for i, ele in enumerate(set_):
                    if i != 0:
                        fp.write(', ')
                    fp.write('"Itemset: %s"' % ele)

                fp.write(' Support: %f\n' % support_)

    with open('relation_rules.txt', 'w') as fp:
        for _, relations in enumerate(relations_by_k):
            relations = sorted(relations, reverse=True)
            fp.write(
                '\n%d-Itemset Relation Rules\n' % (_))
            for relation in relations:
                set_list = relation[1]
                support = relation[0]
                for set_ in set_list:
                    lhs = set_.items_base
                    rhs = set_.items_add

                    confidence = set_.confidence
                    lift = set_.lift

                    if check_set(lhs) == 0 or check_set(rhs) == 0:
                        continue
                    if confidence < 0.6 or lift < 3:
                        continue
                    for i, ele in enumerate(lhs):
                        if i != 0:
                            fp.write(', ')
                        fp.write('"LHS: %s"' % ele)

                    for i, ele in enumerate(rhs):
                        if i != 0:
                            fp.write(', ')
                        fp.write(' "RHS: %s"' % ele)
                    fp.write(' support: %f confidence: %f lift: %f \n' %
                             (support, confidence, lift))


if __name__ == '__main__':
    main()

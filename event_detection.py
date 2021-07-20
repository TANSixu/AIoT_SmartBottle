from sklearn import svm

clf = svm.SVC()

def svm_train(X):
    # only be used for x_data3.npy
    y = [0] * 53
    y[6] = 1
    y[12] = 1
    y[28] = 1
    y[33] = 1
    y[39] = 1
    y[50] = 1

    clf.fit(X, y)
    # print(X[6])
    # print(X[12])
    # print(X[28])
    # print(X[33])
    # print(X[39])
    # print(X[50])
    # print(X[51])
    # print(X[52])
    # print(clf.support_)
    # print(clf.support_vectors_)
    # print(clf.n_support_)


def svm_test(test):
    print(clf.predict(test))

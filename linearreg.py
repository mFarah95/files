import pandas as pd
import numpy as np
from  matplotlib import pyplot 


train_data = pd.read_csv('dataset/regression/train_1d_reg_data.csv',sep=',', header=None)
test_data = pd.read_csv('dataset/regression/test_1d_reg_data.csv', sep=',',header=None)

Xtest = test_data.iloc[:,:-1].values[1:].astype(np.float)


def linear_regression(train_data, weights=None):

    y = train_data.iloc[:,-1].values[1:].astype(np.float)
    X = train_data.iloc[:,:-1].values[1:].astype(np.float)

    # merge an extra dimension to the input vector
    ones = np.ones(len(X))
    X = np.column_stack((ones,X))

    if weights is None:
        weights = np.dot(np.linalg.pinv(np.dot(X.T,X)), np.dot(X.T,y))
    
    # calculate h(x)
    pred = []
    for i in X[:,1:]:
        pred.append(sum(weights[1:] * i) + weights[0])


    # Mean square error
    mse = (np.square(pred - y )).mean()
    print ("mse:", mse)

    # visualize results

    hyperplane = weights[1] * X[:,1:] + weights[0]

    pyplot.plot(X[:,1:],y,'o',X[:,1:],hyperplane)
    pyplot.title('Plot of OLS')

    pyplot.show()




    return weights

if __name__ == "__main__":

    train_w = linear_regression(train_data)
    
    print ("weights:",train_w)

    test_w = linear_regression(test_data,train_w)

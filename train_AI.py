# Import libraries
import pandas as pd
import pickle
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer


def main():
    # Import data
    dataset = pd.read_csv('data.csv')
    X = dataset.iloc[:, 0:4]
    y = dataset.iloc[:, 5]

    # Preprocess data
    preprocess = make_column_transformer(
        (StandardScaler(), ['Hour', 'Minute', 'Day', 'Temperature']))
    X = preprocess.fit_transform(X)

    y = y.values
    X_train = X
    y_train = y

    # Initialising the ANN
    classifier = Sequential()
    classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu', input_dim = 4))
    classifier.add(Dense(units = 6, kernel_initializer = 'uniform', activation = 'relu'))
    classifier.add(Dense(units = 1, kernel_initializer = 'uniform', activation = 'sigmoid'))
    classifier.compile(optimizer = 'Adadelta', loss = 'binary_crossentropy', metrics = ['accuracy'])
    # Fitting the ANN to the Training set
    classifier.fit(X_train, y_train, batch_size = 100, epochs = 300)

    # Save the model to disk
    filename_fit = 'trained_model.sav'
    pickle.dump(classifier, open(filename_fit, 'wb'))
    filename_preprocess = 'preprocess_model.sav'
    pickle.dump(preprocess, open(filename_preprocess, 'wb'))


if __name__ == '__main__':
    main()
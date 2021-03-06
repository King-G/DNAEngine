import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

class DNA_ANN():
    def __init__(self, feed, output, optimizer):
        self.feed = feed
        self.output = output
        self.optimizer = optimizer
    
    def GenerateBestParameterSet(self, X,Y, parameters, njobs):  
        
        #Splitting the dataset into Training set and test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.5, random_state = 0)
                
        #Genereate multiple ann and find the best one 
        from keras.wrappers.scikit_learn import KerasClassifier
        from sklearn.model_selection import GridSearchCV
        classifier = KerasClassifier(build_fn = self.BuildBestStandardClassifier)
        
        grid_search = GridSearchCV(estimator = classifier,
                                   param_grid = parameters,
                                   scoring = 'accuracy',
                                   cv = 10, n_jobs=njobs)
        grid_search = grid_search.fit(X_train, Y_train)
        
        bestparameters = []
        best_parameters = grid_search.best_params_
        best_accuracy = grid_search.best_score_
        
        bestparameters.append("Best Parameters: {0}".format(best_parameters))
        bestparameters.append("Best Accuracy: {0}".format(best_accuracy))
        
        return bestparameters
    
    def CreateANN(self, X, Y, batchsize, epochs):
        #Splitting the dataset into Training set and test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.5, random_state = 0)
         
        #Initialize ANN
        classifier = self.BuildStandardClassifier()  
        #Fitting the ANN to the training set
        classifier.fit(X_train, Y_train, batch_size = batchsize, epochs = epochs)
        
        #Predicting the Test set results
        y_pred = classifier.predict(X_test)
        y_pred = (y_pred > 0.5)
        
        print(y_pred)
        
        from sklearn.metrics import confusion_matrix
        con = confusion_matrix(Y_test, y_pred)
        print("Con: {0}".format(con))
        
        return classifier
    
    def EvaluateANN(self, X, Y, batchsize, epochs):
        #Splitting the dataset into Training set and test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.5, random_state = 0)
        
        #Evaluating the ANN
        from keras.wrappers.scikit_learn import KerasClassifier
        from sklearn.model_selection import cross_val_score
        
        classifier = KerasClassifier(build_fn = self.BuildStandardClassifier, batch_size = batchsize, epochs = epochs)
        accuracies = cross_val_score(estimator = classifier, X = X_train, y = Y_train, cv = 10)
        
        mean = accuracies.mean()
        variance = accuracies.std()
        
        evaluation = []
        evaluation.append("Mean Accuracy: {0}".format(mean))
        evaluation.append("Variance: {0}".format(variance))
        
        return evaluation
    
    def BuildClassifier(self, feed, output, optimizer):
        #Initialize ANN   
        classifier = Sequential() 
    
        #When using real data
        #hiddenlayersize = feed * 0.000001
        hiddenlayersize = feed
        if(hiddenlayersize < 1):
            hiddenlayersize = 1
        #Adding the input layer and first hidden layer   
        classifier.add(Dense(units = hiddenlayersize, kernel_initializer = 'uniform', activation = 'relu', input_dim = feed))  
        classifier.add(Dropout(rate = 0.25)) #Disable % of nodes
        
        #Adding the output layer
        classifier.add(Dense(units = output, kernel_initializer = 'uniform', activation = 'sigmoid'))
        #Compile ANN
        classifier.compile(optimizer = optimizer, loss = 'binary_crossentropy', metrics = ['accuracy']) 
        return classifier
      
    def BuildStandardClassifier(self):
        return self.BuildClassifier(self.feed, 
                               self.output, 
                               self.optimizer)
    
    def BuildBestStandardClassifier(self, optimizer):
        return self.BuildClassifier(self.feed, 
                               self.output, 
                               optimizer)
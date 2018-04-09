import keras
from keras.models import Sequential
from keras.layers import Dense

def dash():
    dash = []
    dash.append("[")
    for i in range(0, 20):
        dash.append("=")
    dash.append("]")
    return str(dash)
def main():
    
    displayresult = []
    displayresult.append(dash())
    
    filepath = "./DNAs"  
    import DNA_Reader as dna_reader
    
    #Read DNA Folder
    dna_reader.ReadAllInFolder(filepath)
    
    # X (DNA)
    X = dna_reader.Stream.X
    # Y (results)
    Y = dna_reader.Stream.Y
    
    #Transform to numpy array
    import numpy as np
    X = np.array(X)
    Y = np.array(Y)
    
    #Feed(input): number of bits (bytes*8)
    feed = dna_reader.GetFeed()
    #Output: Either Black(0) or White(1), 1 output
    output = dna_reader.GetOutputNodes()
    
    displayresult.append("DNA READER")
    displayresult.append("X (DNA) Shape: {}".format(X.shape))
    displayresult.append("Y (Result) Shape: {}".format(X.shape))
    displayresult.append("Feed: {}".format(feed))
    displayresult.append("Output: {}".format(output))
    displayresult.append(dash())
    
    displayresult.append(dash())
    displayresult.append("BEST PARAMETER GENERATION")
    #njobs (processes) set to 1 if on windows (slower), set to n=number of processes on linux
    njobs = -1 #if linux ex. 4 (4 processes))
      
    #Set parameters to test on....
    parameters = {'batch_size': [10, 20],
                  'epochs': [10, 50, 100],
                  'optimizer': ['adam', 'rmsprop'],}
    displayresult.append("Parameters to test: {}".format(parameters))
    #Generate best parameters (WARNING: takes a while...)
    bestparameters = GenerateBestParameterSet(X, Y, feed, output, parameters, njobs)
    displayresult.append("Parameters Result: {}".format(bestparameters))
    displayresult.append(dash())
    
    displayresult.append(dash())
    displayresult.append("GENERATE ANN USING BEST PARAMETERS")
    
    #Use best ANN
    #Set optimizer to rmsprop
    optimizer = 'adam'
    #Set batchsize
    batchsize = 10
    #Set epochs
    epochs = 100
    
    classifier = CreateANN(X,Y,feed, output, optimizer, batchsize, epochs) 
    displayresult.append("Classifier: {}".format(classifier.get_config()))
    
    evaluation = EvaluateANN(X, Y, feed, output, optimizer, batchsize, epochs)
    displayresult.append("Evaluation: {}".format(evaluation))
    displayresult.append(dash())
    
    displayresult.append(dash())
    displayresult.append("PREDICTING ONE SPECIMEN")
    #count = 0
    #for layer in classifier.layers: 
        #print (layer.get_weights())
        #count +=1
    #print ("Weights: {}".format(count))
    
    #Read one specimen and test if is white or black
    filepath = "./DNAs/Mouse10"  
    dna_reader.ReadOneSpecimen(filepath)
    # X (chromosomes)
    X = dna_reader.Stream.X
    # Y (results)
    Y = dna_reader.Stream.Y
    
    #Transform to numpy array
    import numpy as np
    X = np.array(X)
    Y = np.array(Y)
    
    displayresult.append("ONE SPECIMEN")
    displayresult.append("Filepath : {}".format(filepath))
    displayresult.append("X (DNA) Shape: {}".format(X.shape))
    displayresult.append("Y (Result) Shape: {}".format(X.shape))
    displayresult.append("Feed: {}".format(feed))
    displayresult.append("Output: {}".format(output))
    
    new_prediction = classifier.predict(X)
    outcome = (new_prediction > 0.5)
    if(outcome):
        displayresult.append("Mouse prediction is White ({})".format(new_prediction))
    else:
        displayresult.append("Mouse prediction is Black ({})".format(new_prediction))
    
    displayresult.append(dash())
    print(np.array(displayresult))

    

def GenerateBestParameterSet(X, Y, feed, output, parameters, njobs):
    import DNA_ANN as dna_ann  
    #Set Standard Parameters
    dna_ann.SetANNParameters(feed, output ,None)
    #Generate best ANN using the parameters
    return dna_ann.GenerateBestParameterSet(X,Y, parameters, njobs)

def CreateANN(X, Y, feed, output, optimizer, batchsize, epochs):  
    import DNA_ANN as dna_ann  
    dna_ann.SetANNParameters(feed, output, optimizer)
    return dna_ann.CreateANN(X, Y, batchsize, epochs)

def EvaluateANN(X,Y,feed, output, optimizer, batchsize, epochs):
    import DNA_ANN as dna_ann
    dna_ann.SetANNParameters(feed, output, optimizer)
    return dna_ann.EvaluateANN(X, Y, batchsize, epochs) 
    
if __name__ == "__main__":
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    main()       
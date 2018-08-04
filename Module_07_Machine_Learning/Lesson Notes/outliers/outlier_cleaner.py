#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []
   
    ### your code goes here
    for i, value in enumerate(net_worths):
        # Calculates Error         
        error = value - predictions[i] 
        # Creates Tuple 
        row = (int(ages[i]), float(net_worths[i]), abs(float(error)))
        # print row
        cleaned_data.append(row) 

    # Sorts & keeps best 90% of set
    cleaned_data = sorted(cleaned_data, key=lambda x: x[2])
    cleaned_data = cleaned_data[:int(round(len(cleaned_data)*.9))] 
 

    return cleaned_data


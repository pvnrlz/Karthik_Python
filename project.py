import pandas as pd
import json
import sys

pathToPositions = input("Please enter a path to positions file")
pathToTransactions = input("Please enter a path to transactions file")
pathToOutput = input("Please give path for output file")

try:
    positions = pd.read_csv(pathToPositions)
except Exception as ex:
    print("Error in reading the positions file")
    print(ex)
    sys.exit(1)

try:
    f = open(pathToTransactions, encoding = 'utf8')
    data = json.loads(f.read())
    transactions = pd.DataFrame(data)
    f.close()
except Exception as ex:
    print("Error in reading the transactions file")
    print(ex)
    sys.exit(1)
 
positions['OriginalQuantity'] = positions['Quantity']
    
def calculateQuantity(quantity, transactionQuantity, accountType, transactionType):
    if transactionType == 'B' and accountType == 'E':
        return quantity + transactionQuantity
    
    elif transactionType == 'B' and accountType == 'I':
        return quantity - transactionQuantity
    
    elif transactionType == 'S' and accountType == 'E':
        return quantity - transactionQuantity
    
    elif transactionType == 'S' and accountType == 'I':
        return quantity + transactionQuantity
    
    else:
        return quantity

for i, row in transactions.iterrows():
    for j, positionRow in positions[positions.Instrument == row.Instrument].iterrows():
        positions.at[j, 'Quantity'] = calculateQuantity(positionRow['Quantity'], row['TransactionQuantity'],positionRow['AccountType'],row['TransactionType'])


positions['Delta'] = positions['Quantity'] - positions['OriginalQuantity']        
positions[['Delta','Quantity']] = positions[['Delta','Quantity']].astype(int)

positions.drop('OriginalQuantity', inplace = True, axis = 1)

try:
    positions.to_csv(pathToOutput, index = False)
except Exception as ex:
    print("Error in saving the output")
    print(ex)
    sys.exit(1)



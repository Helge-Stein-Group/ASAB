import pandas as pd
import os 
cwd = os.getcwd()
print(cwd)
import pickle
import sys
sys.path.append(r"../tests")
sys.path.append(r"../experiment")
from helpers import SaveToFile, LoadFile

class chemical:
    ''' This class defines chemicals in a way to determine the required volume in order to achieve a certain mixing ratio and to evaluate their compatibility with the ASAB setup. '''

    def __init__(self, nameShort, nameLong, density, molarMass):
        # Initialize a class object with the specified properties
        self.nameShort = nameShort
        self.nameLong = nameLong
        self.density = density
        self.molarMass = molarMass

        ''' RELEVANT FOR FUTURE DEVELOPMENT '''
        # self.chemFormula = smiles
        # self.flashPoint = flashPoint
        # self.decompTemp = decompositionTemp
        # self.decompProd = decompositionProd
        # self.dangerousPartners = dangerousReactionPartners
        # self.categories = categories
        # self.stabilityWater = stabilityWater
        # self.stabilityAir = stabilityAir
        # self.safety = safety
        # self.ghs = ghs
        
        # standard values for the extended version:
        # name = "empty"
        # smiles = None
        # density = None
        # decompositionTemp = None
        # decompositionProd = []
        # dangerousReactionPartners = []
        # stabilityWater = "No"
        # stabilityAir = "No"
        # tox = []
        # safety = []
        # ghs = []

    # def addInfo(self, info, x):
    #     ''' Add an item to a property. Works for decomposition products, dangerous reaction partners, categories, toxicity, safety, ghs. '''
    #     getattr(self, info).append(x)

    # def removeInfo(self, info, x):
    #     getattr(self, info, x).remove(x)
 
def getChemicalsList(dataFile):         #input: .csv-file, output: dict
    ''' This function loads the .csv database including the information regarding the chemicals and generates objects of the chemicals class. A dictionary containing all the chemicals listed in the database is returned using the NameShort in the database as keys. '''
    chemInfo = pd.read_csv(dataFile, sep=";")       
    chemList = {}
    for i in chemInfo.index:        #write each chemical as object into the dict
        chem = chemical(chemInfo.loc[i, "NameShort"], chemInfo.loc[i, "NameLong"], chemInfo.loc[i, "Density at 20 degreeC / g/cm3"], chemInfo.loc[i, "Molar mass / g/mol"])
        chemList[chemInfo.loc[i, "NameShort"]] = chem
    # save the chemList dictionary in order to be able to load once it is generated. It does not need to be newly generated, if no changes in the database occured.
    SaveToFile("chemList.pck", chemList)
    
    return chemList

def loadChemicalsList(file_chemList):   #input: path to pickle file
    ''' This function loads a saved chemList object. '''
    out = LoadFile(file_chemList)
    return out
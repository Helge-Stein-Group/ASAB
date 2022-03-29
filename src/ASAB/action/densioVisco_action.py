## Get the configuration
try:
    # if there is a main file, get conf from there
    from __main__ import conf   # https://stackoverflow.com/questions/6011371/python-how-can-i-use-variable-from-main-file-in-module
except ImportError:
    # if the import was not successful, go to default config
    from ASAB.configuration import default_config
    conf = default_config.config

## Imports from ASAB
from ASAB.driver import densioVisco_driver

def measure(sampleName:str, method:str="Density"):
    ''' This function calls the driver function "measure" to perform a measurement. '''
    densioVisco_driver.measure(sampleName=sampleName, method=method)

def check(sampleName:str, checktype:str, method:str="Density"):
    ''' This function calls the driver function "check" for automatically running checks. '''
    densioVisco_driver.check(sampleName=sampleName, checktype=checktype, method=method)

def retrieveData(sampleName:str, method:str, methodtype:str, savePath:str):
    ''' This funciton calls the driver function "retrieveData" to retrieve data from density and viscosity measurements and save them in a dict data format to a .json file in the specified folder (savePath). '''
    densioVisco_driver.retrieveData(sampleName=sampleName, method=method, methodtype=methodtype, savePath=savePath)
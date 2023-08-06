import os, glob
import pandas as pd
import h5py
import numpy as np
from configparser import ConfigParser
from datetime import datetime



def create_plotly_container(configini, probabilityTables, timebinTables, sklearnTables, severityTables):
    config = ConfigParser()
    configFile = str(configini)
    config.read(configFile)
    projectPath = config.get('General settings', 'project_path')
    machine_results_dir = os.path.join(projectPath, 'csv', 'machine_results')
    logsFolder = os.path.join(projectPath, 'csv', 'logs')


    wfileType = config.get('General settings', 'workflow_file_type')
    dateTime = datetime.now().strftime('%Y%m%d%H%M%S')
    storageFile = pd.HDFStore('SimBA_dash_file_' + str(dateTime) + '.h5', table=True, complib='blosc:zlib', complevel=9)
    vidInfoFilePath = os.path.join(projectPath, 'logs', 'video_info.csv')
    vidInfoDf = pd.read_csv(vidInfoFilePath, index_col=0)
    storageFile['Video_info'] = vidInfoDf
    model_nos = config.getint('SML settings', 'No_targets')
    target_names, probabilityColNames = [], []
    for i in range(model_nos):
        currentModelName = 'target_name_' + str(i)
        currentModelName = config.get('SML settings', currentModelName)
        currProbColName = 'Probability_' + currentModelName
        target_names.append(currentModelName)
        probabilityColNames.append(currProbColName)
    cols2Keep = target_names + probabilityColNames

    if probabilityTables == 1:
        probabilityFiles = glob.glob(machine_results_dir + '/*.' + wfileType)
        for file in probabilityFiles:
            currDf = pd.read_csv(file, index_col=0)
            currDf = currDf[cols2Keep]
            vidName = os.path.basename(file).replace('.' + wfileType, '')
            identifier = 'VideoData/' + vidName
            storageFile[identifier] = currDf
    if timebinTables == 1:
        timeBinsFiles = glob.glob(logsFolder + '/*' + 'Time_bins_ML_results')
        for file in timeBinsFiles:


























timeBinsFile = r"Z:\Classifiers\Attack\project_folder\logs\Time_bins_ML_results_20200615145809.csv"
timeBinsDf = pd.read_csv(timeBinsFile, index_col=0)
sklearnFile = r"Z:\Classifiers\Attack\project_folder\logs\sklearn_20200615100537.csv"
sklearnDf = pd.read_csv(sklearnFile, index_col=0)
severityFile = r"Z:\Classifiers\Attack\project_folder\logs\severity_20200615145538.csv"
severityDf = pd.read_csv(severityFile, index_col=0)


ExampleStorage['sklearn_results'] = sklearnDf
ExampleStorage['time_bins_results'] = timeBinsDf

infoDf = pd.DataFrame(columns = ['Classifier_names', "Used_threshold", "fps", "Classifier_link"])
infoDf.loc[len(infoDf)] = ['Attack', '0.5', "30", 'https://osf.io/stvhr/' ]
infoDf.loc[len(infoDf)] = ['Sniffing', '0.5', "30", 'https://osf.io/sn72j/']

ExampleStorage['Dataset_info'] = infoDf

for csvfile in filesFound:
    currDf = pd.read_csv(csvfile, index_col=0)
    currDf = currDf[['Attack', 'Probability_Attack']]
    currDf['Sniffing'] = np.random.randint(0, 1, currDf.shape[0])
    currDf['Probability_Sniffing'] = np.random.uniform(low=0.00, high=1.00, size=(currDf.shape[0],))
    vidName = os.path.basename(csvfile).replace('.csv', '')
    identifier = 'VideoData/' + vidName
    ExampleStorage[identifier] = currDf
    print(ExampleStorage[identifier])
ExampleStorage.close()

import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=DeprecationWarning)
import pickle
from configparser import ConfigParser
import os
import pandas as pd
import cv2
from scipy import ndimage
import warnings
import random
from simba.drop_bp_cords import drop_bp_cords
import matplotlib.pyplot as plt
import numpy as np
import io
import PIL
from simba.rw_dfs import *

plt.interactive(True)
plt.ioff()
warnings.simplefilter(action='ignore', category=FutureWarning)

def validate_model_one_vid(inifile,classifier_path,savfile,dt,sb,generategantt):
    configFile = str(inifile)
    config = ConfigParser()
    config.read(configFile)
    sample_feature_file = str(csvfile)
    sample_feature_file_Name = os.path.basename(sample_feature_file)
    sample_feature_file_Name = sample_feature_file_Name.split('.', 1)[0]
    discrimination_threshold = float(dt)
    classifier_name = os.path.basename(classifier_path).replace('.sav','')
    wfileType = config.get('General settings', 'workflow_file_type')
    inputFile = read_df(sample_feature_file, wfileType)
    inputFile = inputFile.loc[:, ~inputFile.columns.str.contains('^Unnamed')]
    inputFile = inputFile.drop(['scorer'], axis=1, errors='ignore')
    outputDf = inputFile.copy()
    inputFileOrganised = drop_bp_cords(inputFile, inifile)
    if (classifier_name == 'attack_prediction') or (classifier_name == 'anogenital_prediction') or (classifier_name == 'pursuit_prediction'):
        try:
            inputFileOrganised = inputFileOrganised.drop(
                ['Mouse_1_Nose_to_lateral_left', 'Mouse_2_Nose_to_lateral_left', 'Mouse_1_Nose_to_lateral_right',
                 'Mouse_2_Nose_to_lateral_right', 'Mouse_1_Centroid_to_lateral_left',
                 'Mouse_2_Centroid_to_lateral_left', 'Mouse_1_Centroid_to_lateral_right',
                 'Mouse_2_Centroid_to_lateral_right'], axis=1)
        except KeyError:
            pass
    print('Running model...')
    clf = pickle.load(open(classifier_path, 'rb'))
    ProbabilityColName = 'Probability_' + classifier_name
    predictions = clf.predict_proba(inputFileOrganised)
    outputDf[ProbabilityColName] = predictions[:, 1]
    outputDf[classifier_name] = np.where(outputDf[ProbabilityColName] > discrimination_threshold, 1, 0)

    # CREATE LIST OF GAPS BASED ON SHORTEST BOUT
    shortest_bout = int(sb)
    vidInfPath = config.get('General settings', 'project_path')
    videoInputFolder = os.path.join(vidInfPath, 'videos')
    outputPath = os.path.join(vidInfPath, 'frames', 'output', 'validation')
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    outputFileName = os.path.join(outputPath, os.path.basename(sample_feature_file.replace('.' +wfileType, '_' + classifier_name + '.avi')))
    vidInfPath = os.path.join(vidInfPath, 'logs', 'video_info.csv')
    vidinfDf = pd.read_csv(vidInfPath)
    fps = vidinfDf.loc[vidinfDf['Video'] == str(sample_feature_file_Name.replace('.' + wfileType, ''))]
    try:
        fps = int(fps['fps'])
    except TypeError:
        print('Error: make sure all the videos that are going to be analyzed are represented in the project_folder/logs/video_info.csv file')
    framesToPlug = int(fps * (shortest_bout / 1000))
    framesToPlugList = list(range(1, framesToPlug + 1))
    framesToPlugList.reverse()
    patternListofLists = []
    for k in framesToPlugList:
        zerosInList = [0] * k
        currList = [1]
        currList.extend(zerosInList)
        currList.extend([1])
        patternListofLists.append(currList)
    patternListofLists.append([0, 1, 1, 0])
    patternListofLists.append([0, 1, 0])
    patterns = np.asarray(patternListofLists)
    for l in patterns:
        currPattern = l
        n_obs = len(currPattern)
        outputDf['rolling_match'] = (outputDf[classifier_name].rolling(window=n_obs, min_periods=n_obs)
                                     .apply(lambda x: (x == currPattern).all())
                                     .mask(lambda x: x == 0)
                                     .bfill(limit=n_obs - 1)
                                     .fillna(0)
                                     .astype(bool)
                                     )
        if (currPattern == patterns[-2]) or (currPattern == patterns[-1]):
            outputDf.loc[outputDf['rolling_match'] == True, classifier_name] = 0
        else:
            outputDf.loc[outputDf['rolling_match'] == True, classifier_name] = 1
        outputDf = outputDf.drop(['rolling_match'], axis=1)
    outFname = sample_feature_file_Name + '.' + wfileType
    csv_dir_out_validation = config.get('General settings', 'csv_path')
    csv_dir_out_validation = os.path.join(csv_dir_out_validation,'validation')
    if not os.path.exists(csv_dir_out_validation):
        os.makedirs(csv_dir_out_validation)
    outFname = os.path.join(csv_dir_out_validation, outFname)
    save_df(outputDf, wfileType, outFname)
    print('Predictions generated...')

    #generate the video based on the just generated classification
    target_counter = 0
    if wfileType == 'csv':
        currentDf = pd.read_csv(outFname)
    if wfileType == 'parquet':
        currentDf = pd.read_parquet(outFname)
    currentDf = currentDf.fillna(0)
    currentDf = currentDf.astype(int)
    Xlocs, Ylocs = (currentDf.filter(like='_x', axis=1), currentDf.filter(like='_y', axis=1))
    Xlocs = Xlocs.rename(columns=lambda x: x.strip('_x'))
    Ylocs = Ylocs.rename(columns=lambda x: x.strip('_y'))
    bodypartColNames = list(Xlocs.columns)
    targetColumn = classifier_name
    if os.path.exists(os.path.join(videoInputFolder, os.path.basename(outFname.replace('.' + wfileType, '.mp4')))):
        currVideoFile = os.path.join(videoInputFolder, os.path.basename(outFname.replace('.' + wfileType, '.mp4')))
    if os.path.exists(os.path.join(videoInputFolder, os.path.basename(outFname.replace('.' +wfileType, '.avi')))):
        currVideoFile = os.path.join(videoInputFolder, os.path.basename(outFname.replace('.' + wfileType, '.avi')))
    cap = cv2.VideoCapture(currVideoFile)

    ## find vid size and fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    if height < width:
        videoHeight, videoWidth = width, height
    if height >= width:
        videoHeight, videoWidth = height, width
    writer = cv2.VideoWriter(outputFileName, fourcc, fps, (videoWidth, videoHeight))
    mySpaceScale, myRadius, myResolution, myFontScale = 60, 20, 1500, 1.5
    maxResDimension = max(width, height)
    circleScale = int(myRadius / (myResolution / maxResDimension))
    fontScale = float(myFontScale / (myResolution / maxResDimension))
    spacingScale = int(mySpaceScale / (myResolution / maxResDimension))
    currRow = 0
    colorList = []
    for color in range(len(bodypartColNames)):
        r, g, b = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        colorTuple = (r, g, b)
        colorList.append(colorTuple)

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            loop = 0
            for bodyParts in bodypartColNames:
                currXval = Xlocs.loc[Xlocs.index[currRow], bodyParts]
                currYval = Ylocs.loc[Ylocs.index[currRow], bodyParts]
                cv2.circle(frame, (int(currXval), int(currYval)), circleScale, colorList[loop], -1, lineType=cv2.LINE_AA)
                loop+=1
            target_timer = (1/fps) * target_counter
            target_timer = round(target_timer, 2)
            if height < width:
                frame = ndimage.rotate(frame, 90)
            cv2.putText(frame, str('Timer'), (10, ((height-height)+spacingScale)), cv2.FONT_HERSHEY_COMPLEX, fontScale, (0, 255, 0), 2)
            addSpacer = 2
            cv2.putText(frame, (str(classifier_name) + ' ' + str(target_timer) + str('s')), (10, (height-height)+spacingScale*addSpacer), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 0, 255), 2)
            addSpacer+=1
            cv2.putText(frame, str('ensemble prediction'), (10, (height-height)+spacingScale*addSpacer), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), 2)
            addSpacer += 2
            if currentDf.loc[currentDf.index[currRow], targetColumn] == 1:
                cv2.putText(frame, str(classifier_name), (10, (height - height) + spacingScale * addSpacer), cv2.FONT_HERSHEY_TRIPLEX, fontScale, (2, 166, 249), 2)
                target_counter += 1
                addSpacer += 1
            writer.write(frame)
            currRow += 1
            print('Frame: ' + str(currRow) + '/' + str(frames) + '.')
        if frame is None:
            print('Video ' + str(currVideoFile) + ' saved.')
            cap.release()
            writer.release()
            break

    if int(generategantt) == 1:
        outputFileNameGantt = os.path.join(outputPath, os.path.basename(sample_feature_file.replace('.' +wfileType, '_' + classifier_name + '_gantt.avi')))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer2 = cv2.VideoWriter(outputFileNameGantt, fourcc, int(fps), (640, 480))
        boutsList, nameList, startTimeList, endTimeList, endFrameList = [], [], [], [], []
        groupDf = pd.DataFrame()
        v = (currentDf[classifier_name] != currentDf[classifier_name].shift()).cumsum()
        u = currentDf.groupby(v)[classifier_name].agg(['all', 'count'])
        m = u['all'] & u['count'].ge(1)
        groupDf['groups'] = currentDf.groupby(v).apply(lambda x: (x.index[0], x.index[-1]))[m]
        for indexes, rows in groupDf.iterrows():
            currBout = list(rows['groups'])
            boutTime = ((currBout[-1] - currBout[0]) + 1) / fps
            startTime = (currBout[0] + 1) / fps
            endTime = (currBout[1]) / fps
            endFrame = (currBout[1])
            endTimeList.append(endTime)
            startTimeList.append(startTime)
            boutsList.append(boutTime)
            nameList.append(classifier_name)
            endFrameList.append(endFrame)
        boutsDf = pd.DataFrame(list(zip(nameList, startTimeList, endTimeList, endFrameList, boutsList)), columns=['Event', 'Start_time', 'End Time', 'End_frame', 'Bout_time'])



        for k in range(len(inputFile)):
            fig, ax = plt.subplots()
            currentDf = currentDf.iloc[:k]
            relRows = boutsDf.loc[boutsDf['End_frame'] <= k]
            for i, event in enumerate(relRows.groupby("Event")):
                data_event = event[1][["Start_time", "Bout_time"]]
                ax.broken_barh(data_event.values, (4, 4), facecolors='red')
                loop+=1
            xLength = (round(k / fps)) + 1
            if xLength < 10:
                xLength = 10
            loop=0
            ax.set_xlim(0, xLength)
            ax.set_ylim([0, 12])
            plt.ylabel(classifier_name, fontsize=12)
            plt.yticks([])
            plt.xlabel('time(s)', fontsize=12)
            ax.yaxis.set_ticklabels([])
            ax.grid(True)
            buffer_ = io.BytesIO()
            plt.savefig(buffer_, format="png")
            buffer_.seek(0)
            image = PIL.Image.open(buffer_)
            ar = np.asarray(image)
            open_cv_image = ar[:, :, ::-1]
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
            open_cv_image = cv2.resize(open_cv_image, (640, 480))
            open_cv_image = np.uint8(open_cv_image)
            buffer_.close()
            writer2.write(open_cv_image)
            plt.close('all')
            print('Gantt: ' + str(k) + '/' + str(len(inputFile)) + '.')
        cv2.destroyAllWindows()
        writer2.release()
        print('Gantt ' + str(os.path.basename(outputFileNameGantt)) + ' saved.')
    else:
        pass
    print('Validation videos saved @' + 'project_folder/frames/output/validation')

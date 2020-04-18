import numpy as np

import matplotlib.pyplot as plt
import math
import os
import json

def calculateDistance(p1,p2):
     dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)
     return dist

def calculateAngle(v1,v2):
    dotProduct = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
    magnitudeProduct = math.sqrt((v1[0]**2 + v1[1]**2 + v1[2]**2) * (v2[0]**2 + v2[1]**2 + v2[2]**2))

    angle = math.acos(dotProduct/magnitudeProduct)
    return angle

def getVector(p1,p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    z = p1[2] - p2[2]

    vec = [x, y, z]
    return vec


if __name__ == '__main__':
    mode = int(input("Enter 1 to Train or 2 to Test: "))

    if mode == 1:
        outFile = open('rad_d1', 'a')
    elif mode == 2:
        outFile = open('rad_d1.t', 'a')
    else:
        print("Mode Error")
        exit()

    algo = int(input("Enter 1 to use RAD or 2 to use HJPD"))

    filepath = input("Enter filepath of the dataset to be used: ")

    numJoints = 20

    # Open each file in dataset
    for file in os.listdir(filepath):
        with open(os.path.join(filepath, file), 'r') as f:

            eof = False
            distances = []
            angles = []
            frame = 1
            badFrames = 0

            if algo == 1:
                while not eof:

                    # print("Frame: " + str(frame))

                    #Process each frame
                    hip, head, lHand, rHand, lFoot, rFoot = ([] for i in range(6))
                    joint = 0

                    while joint != numJoints:
                        line = f.readline()

                        if not line:
                            eof = True
                            break

                        # print(line.strip())
                        currLine = [float(x) for x in line.split()]

                        if currLine[0] != frame:
                            print("Frame Error: " + str(currLine[0] + " " + str(frame)))
                        else:
                            joint = currLine[1]
                            if joint == 1:
                                hip = currLine[2:]
                            elif joint == 4:
                                head = currLine[2:]
                            elif joint == 8:
                                lHand = currLine[2:]
                            elif joint == 12:
                                rHand = currLine[2:]
                            elif joint == 16:
                                lFoot = currLine[2:]
                            elif joint == 20:
                                rFoot = currLine[2:]
                            else:
                                pass


                    # Compute the Distances and Angles for the Star Representation
                    # Make Sure the Frame data is not Empty or NaN
                    if (not hip or not head or not lHand or not rHand or not lFoot or not rFoot) and not eof:
                        print("One of the Joints is Empty: " + str(frame))
                    elif np.isnan(hip).any() or np.isnan(head).any() or np.isnan(rHand).any() or np.isnan(rFoot).any() or np.isnan(lFoot).any() or np.isnan(lHand).any():
                        print("Error with Frame Data")
                        badFrames += 1
                    elif not eof:
                        d1 = calculateDistance(hip,head)
                        d2 = calculateDistance(hip,rHand)
                        d3 = calculateDistance(hip,rFoot)
                        d4 = calculateDistance(hip,lFoot)
                        d5 = calculateDistance(hip,lHand)

                        vhead = getVector(hip, head)
                        vrHand = getVector(hip, rHand)
                        vrFoot = getVector(hip, rFoot)
                        vlFoot = getVector(hip, lFoot)
                        vlHand = getVector(hip, lHand)

                        a1 = calculateAngle(vhead,vrHand)
                        a2 = calculateAngle(vrHand,vrFoot)
                        a3 = calculateAngle(vrFoot,vlFoot)
                        a4 = calculateAngle(vlFoot,vlHand)
                        a5 = calculateAngle(vlHand,vhead)

                        distances.append([d1,d2,d3,d4,d5])
                        angles.append([a1,a2,a3,a4,a5])

                    frame += 1

                try:
                    # Create Histograms
                    dHead, drHand, drFoot, dlFoot, dlHand = ([] for i in range(5))
                    for elem in distances:
                        dHead.append(elem[0])
                        drHand.append(elem[1])
                        drFoot.append(elem[2])
                        dlFoot.append(elem[3])
                        dlHand.append(elem[4])

                    aHead, arHand, arFoot, alFoot, alHand = ([] for i in range(5))
                    for elem in angles:
                        aHead.append(elem[0])
                        arHand.append(elem[1])
                        arFoot.append(elem[2])
                        alFoot.append(elem[3])
                        alHand.append(elem[4])

                    histdHead, dhead_bins = np.histogram(dHead, bins=10)
                    histdrHand, drHand_bins = np.histogram(drHand, bins=10)
                    histdrFoot, drFoot_bins = np.histogram(drFoot, bins=10)
                    histdlFoot, dlFoot_bins = np.histogram(dlFoot, bins=10)
                    histdlHand, dlHand_bins = np.histogram(dlHand, bins=10)

                    histaHead, ahead_bins = np.histogram(aHead, bins=10)
                    histarHand, arHand_bins = np.histogram(arHand, bins=10)
                    histarFoot, arFoot_bins = np.histogram(arFoot, bins=10)
                    histalFoot, alFoot_bins = np.histogram(alFoot, bins=10)
                    histalHand, alHand_bins = np.histogram(alHand, bins=10)

                    ## Plot the Histograms
                    # plt.subplot(2,5,1)
                    # plt.hist(dHead)
                    # plt.ylabel('Count')
                    # plt.xlabel('Distance Head')
                    #
                    # plt.subplot(2,5,2)
                    # plt.hist(drHand)
                    # plt.ylabel('Count')
                    # plt.xlabel('Distance Right Hand')
                    #
                    # plt.subplot(2,5,3)
                    # plt.hist(drFoot)
                    # plt.ylabel('Count')
                    # plt.xlabel('Distance Right Foot')
                    #
                    # plt.subplot(2,5,4)
                    # plt.hist(dlFoot)
                    # plt.ylabel('Count')
                    # plt.xlabel('Distance Left Foot')
                    #
                    # plt.subplot(2,5,5)
                    # plt.hist(dlHand)
                    # plt.ylabel('Count')
                    # plt.xlabel('Distance Left Hand')
                    #
                    # plt.subplot(2,5,6)
                    # plt.hist(aHead)
                    # plt.ylabel('Count')
                    # plt.xlabel('Angle Head')
                    #
                    # plt.subplot(2,5,7)
                    # plt.hist(arHand)
                    # plt.ylabel('Count')
                    # plt.xlabel('Angle Right Hand')
                    #
                    # plt.subplot(2,5,8)
                    # plt.hist(arFoot)
                    # plt.ylabel('Count')
                    # plt.xlabel('Angle Right Foot')
                    #
                    # plt.subplot(2,5,9)
                    # plt.hist(alFoot)
                    # plt.ylabel('Count')
                    # plt.xlabel('Angle Left Foot')
                    #
                    # plt.subplot(2,5,10)
                    # plt.hist(alHand)
                    # plt.ylabel('Count')
                    # plt.xlabel('Angle Left Hand')
                    #
                    #
                    # plt.show()

                    # Normalize Histograms
                    totalFrames = frame - badFrames - 1

                    normhistdHead = [x / totalFrames for x in histdHead]
                    normhistdrHand = [x / totalFrames for x in histdrHand]
                    normhistdrFoot = [x / totalFrames for x in histdrFoot]
                    normhistdlFoot = [x / totalFrames for x in histdlFoot]
                    normhistdlHand = [x / totalFrames for x in histdlHand]

                    normhistaHead = [x / totalFrames for x in histaHead]
                    normhistarHand = [x / totalFrames for x in histarHand]
                    normhistarFoot = [x / totalFrames for x in histarFoot]
                    normhistalFoot = [x / totalFrames for x in histalFoot]
                    normhistalHand = [x / totalFrames for x in histalHand]


                    # print(histdHead)
                    # print(normhistdHead)


                    # Concatenate Histograms
                    outputVector = []

                    outputVector.extend(normhistdHead)
                    outputVector.extend(normhistaHead)

                    outputVector.extend(normhistdrHand)
                    outputVector.extend(normhistarHand)

                    outputVector.extend(normhistdrFoot)
                    outputVector.extend(normhistarFoot)

                    outputVector.extend(normhistdlFoot)
                    outputVector.extend(normhistalFoot)

                    outputVector.extend(normhistdlHand)
                    outputVector.extend(normhistalHand)

                    totalLength = 5*(10 + 10)
                    if len(outputVector) != totalLength:
                        print("Error with Concatenation")
                        exit()
                    else:
                        json.dump(outputVector, outFile)
                        outFile.write("\n")
                except:
                    print("Error with File: " + file)

            elif algo == 2:

                while not eof:
                    #Process each frame
                    # hip, spine, shoulderCenter, head, lHand,lWrist, lElbow, lShoulder, rHand, rWrist, rElbow, rShoulder, lFoot, lAnkle, lKnee, lHip, rFoot, rAnkle, rKnee, rHip = ([] for i in range(20))
                    joint = 0
                    jointDict = dict()

                    while joint != numJoints:
                        line = f.readline()

                        if not line:
                            eof = True
                            break

                        # print(line.strip())
                        currLine = [float(x) for x in line.split()]

                        if currLine[0] != frame:
                            print("Frame Error: " + str(currLine[0] + " " + str(frame)))
                        else:
                            jointDict[currLine[1]] = currLine[2:]

                    # Compute the Distances and Angles for the Star Representation
                    # Make Sure the Frame data is not Empty or NaN
                    if len(jointDict) != numJoints and not eof:
                        print("One of the Joints is Empty: " + str(frame))
                    elif np.isnan(jointDict.keys()).any():
                        print("Error with Frame Data")
                        badFrames += 1
                    elif not eof:
                        ####TODO Calculate the displacements of each joint to the hip and then create histogram etc.
                        pass

            else:
                print("An Error Occured")

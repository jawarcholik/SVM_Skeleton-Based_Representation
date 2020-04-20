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

def getDisplacement(p1,p2):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    dz = abs(p1[2] - p2[2])

    vec = [dx, dy, dz]
    return vec


if __name__ == '__main__':
    mode = int(input("Enter 1 to Train or 2 to Test: "))

    algo = int(input("Enter 1 to use RAD or 2 to use HJPD: "))

    if mode == 1:
        if algo == 1:
            outFile = open('rad_d1', 'w')
        elif algo == 2:
            outFile = open('custom_d1', 'w')
        else:
            print("Invalid Algorithm Entry")
            exit()
    elif mode == 2:
        if algo == 1:
            outFile = open('rad_d1.t', 'w')
        elif algo == 2:
            outFile = open('custom_d1.t', 'w')
        else:
            print("Invalid Algorithm Entry")
            exit()
    else:
        print("Invalid Mode Entry")
        exit()

    filepath = input("Enter filepath of the dataset to be used: ")

    numBins = int(input("Enter the Number of Bins to be Used: "))

    numJoints = 20

    # Open each file in dataset
    for file in os.listdir(filepath):
        with open(os.path.join(filepath, file), 'r') as f:

            eof = False
            frame = 1
            badFrames = 0

            if algo == 1:
                distances = []
                angles = []

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
                            print("Frame Error: " + str(currLine[0]) + " " + str(frame))
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

                    histdHead, dhead_bins = np.histogram(dHead, bins=numBins)
                    histdrHand, drHand_bins = np.histogram(drHand, bins=numBins)
                    histdrFoot, drFoot_bins = np.histogram(drFoot, bins=numBins)
                    histdlFoot, dlFoot_bins = np.histogram(dlFoot, bins=numBins)
                    histdlHand, dlHand_bins = np.histogram(dlHand, bins=numBins)

                    histaHead, ahead_bins = np.histogram(aHead, bins=numBins)
                    histarHand, arHand_bins = np.histogram(arHand, bins=numBins)
                    histarFoot, arFoot_bins = np.histogram(arFoot, bins=numBins)
                    histalFoot, alFoot_bins = np.histogram(alFoot, bins=numBins)
                    histalHand, alHand_bins = np.histogram(alHand, bins=numBins)

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

                centroidJointID = 1
                hip, spine, shoulderCenter, head, lHand,lWrist, lElbow, lShoulder, rHand, rWrist, rElbow, rShoulder, lFoot, lAnkle, lKnee, lHip, rFoot, rAnkle, rKnee, rHip = ([] for i in range(20))

                while not eof:
                    #Process each frame
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
                            print("Frame Error: " + str(currLine[0]) + " " + str(frame))
                        else:
                            joint = currLine[1]
                            jointDict[joint] = currLine[2:]


                    # Make Sure the Frame data is not Empty or NaN
                    jointValues = jointDict.values()
                    badValues = False

                    for val in jointValues:
                        if np.isnan(val).any():
                            badValues = True


                    # Compute the Distances and Angles for the Star Representation
                    # Make Sure the Frame data is not Empty or NaN
                    if len(jointDict) != numJoints and not eof:
                        print("One of the Joints is Empty: " + str(frame))
                    elif badValues:
                        print("Error with Frame Data")
                        badFrames += 1
                    elif not eof:
                        #Calculate the displacements of each joint to the hip
                        comparator = jointDict[centroidJointID]

                        for j in jointDict.keys():
                            if j == centroidJointID:
                                pass
                            else:
                                delta = getDisplacement(jointDict[j], comparator)

                                if j == 1:
                                    print("This should not happen")
                                elif j == 2:
                                    spine.append(delta)
                                elif j == 3:
                                    shoulderCenter.append(delta)
                                elif j == 4:
                                    head.append(delta)
                                elif j == 5:
                                    lShoulder.append(delta)
                                elif j == 6:
                                    lElbow.append(delta)
                                elif j == 7:
                                    lWrist.append(delta)
                                elif j == 8:
                                    lHand.append(delta)
                                elif j == 9:
                                    rShoulder.append(delta)
                                elif j == 10:
                                    rElbow.append(delta)
                                elif j == 11:
                                    rWrist.append(delta)
                                elif j == 12:
                                    rHand.append(delta)
                                elif j == 13:
                                    lHip.append(delta)
                                elif j == 14:
                                    lKnee.append(delta)
                                elif j == 15:
                                    lAnkle.append(delta)
                                elif j == 16:
                                    lFoot.append(delta)
                                elif j == 17:
                                    rHip.append(delta)
                                elif j == 18:
                                    rKnee.append(delta)
                                elif j == 19:
                                    rAnkle.append(delta)
                                elif j == 20:
                                    rFoot.append(delta)
                                else:
                                    print("Key ID Error Doesn't Correspond to a Joint")

                    frame += 1

                #Create Histogram
                try:
                    histSpine, spine_bins = np.histogram(spine, bins=numBins)
                    histShoulderCenter, shoulderCenter_bins = np.histogram(shoulderCenter, bins=numBins)
                    histHead, head_bins = np.histogram(head, bins=numBins)
                    histrShoulder, rShoulder_bins = np.histogram(rShoulder, bins=numBins)
                    histrElbow, rElbow_bins = np.histogram(rElbow, bins=numBins)
                    histrWrist, rWrist_bins = np.histogram(rWrist, bins=numBins)
                    histrHand, rHand_bins = np.histogram(rHand, bins=numBins)
                    histrHip, rHip_bins = np.histogram(rHip, bins=numBins)
                    histrKnee, rKnee_bins = np.histogram(rKnee, bins=numBins)
                    histrAnkle, rAnkle_bins = np.histogram(rAnkle, bins=numBins)
                    histrFoot, rFoot_bins = np.histogram(rFoot, bins=numBins)
                    histlHip, lHip_bins = np.histogram(lHip, bins=numBins)
                    histlKnee, lKnee_bins = np.histogram(lKnee, bins=numBins)
                    histlAnkle, lAnkle_bins = np.histogram(lAnkle, bins=numBins)
                    histlFoot, lFoot_bins = np.histogram(lFoot, bins=numBins)
                    histlShoulder, lShoulder_bins = np.histogram(lShoulder, bins=numBins)
                    histlElbow, lElbow_bins = np.histogram(lElbow, bins=numBins)
                    histlWrist, lWrist_bins = np.histogram(lWrist, bins=numBins)
                    histlHand, lHand_bins = np.histogram(lHand, bins=numBins)



                    # Normalize Histograms
                    totalFrames = frame - badFrames - 1

                    normhistHead = [x / totalFrames for x in histHead]
                    normhistShoulderCenter = [x / totalFrames for x in histShoulderCenter]
                    normhistSpine = [x / totalFrames for x in histSpine]
                    normhistrShoulder = [x / totalFrames for x in histrShoulder]
                    normhistrElbow = [x / totalFrames for x in histrElbow]
                    normhistrWrist = [x / totalFrames for x in histrWrist]
                    normhistrHand = [x / totalFrames for x in histrHand]
                    normhistrHip = [x / totalFrames for x in histrHip]
                    normhistrKnee = [x / totalFrames for x in histrKnee]
                    normhistrAnkle = [x / totalFrames for x in histrAnkle]
                    normhistrFoot = [x / totalFrames for x in histrFoot]
                    normhistlHip = [x / totalFrames for x in histlHip]
                    normhistlKnee = [x / totalFrames for x in histlKnee]
                    normhistlAnkle = [x / totalFrames for x in histlAnkle]
                    normhistlFoot = [x / totalFrames for x in histlFoot]
                    normhistlShoulder = [x / totalFrames for x in histlShoulder]
                    normhistlElbow = [x / totalFrames for x in histlElbow]
                    normhistlWrist = [x / totalFrames for x in histlWrist]
                    normhistlHand = [x / totalFrames for x in histlHand]

                    # Concatenate Histograms
                    outputVector = []

                    outputVector.extend(normhistSpine)
                    outputVector.extend(normhistShoulderCenter)
                    outputVector.extend(normhistHead)
                    outputVector.extend(normhistlShoulder)
                    outputVector.extend(normhistlElbow)
                    outputVector.extend(normhistlWrist)
                    outputVector.extend(normhistlHand)
                    outputVector.extend(normhistrShoulder)
                    outputVector.extend(normhistrElbow)
                    outputVector.extend(normhistrWrist)
                    outputVector.extend(normhistrHand)
                    outputVector.extend(normhistlHip)
                    outputVector.extend(normhistlKnee)
                    outputVector.extend(normhistlAnkle)
                    outputVector.extend(normhistlFoot)
                    outputVector.extend(normhistrHip)
                    outputVector.extend(normhistrKnee)
                    outputVector.extend(normhistrAnkle)
                    outputVector.extend(normhistrFoot)


                    totalLength = (numJoints-1)*(10)
                    if len(outputVector) != totalLength:
                        print("Error with Concatenation")
                        exit()
                    else:
                        json.dump(outputVector, outFile)
                        outFile.write("\n")
                except:
                    print("Error with File: " + file)




            else:
                print("An Error Occured")

import numpy as np

#testing of dictionary {string : list}
vertDict = {"a":[5,6,7]}
vertDict["z"] = [5,6,7]
vertDict["c"] = [5,6,7]
vertDict["p"] = [5,6,7]
#print (vertDict)
#if  "x" in vertDict :
	#print ("vertDict true")
#else :
	#print ("vertDict false")

#testing of dictionary {tuple : list}
nodeDict = {("a","N"):[5,6,7]}
nodeDict[("f","Z")] = [5,6,7]
#print (nodeDict)
#if  ("a","M") in nodeDict :
	#print ("node true")
#else :
	#print ("node false")

#testing list of lists [string, string, list]
vertList = [["carrier", "NK", [0,1,2,3]]]
vertList.append(["carrier", "MX", [4,5,6]])
vertList.append(["dep_apt", "HKG", [7,8,9,10]])
vertList.append(["arr_apt", "PRG", [11,12]])
#print (vertList)
search = "PRG"
result = -1
for sublist in vertList :
    if sublist[1] == search :
        result = (vertList.index(sublist))
#print (result)
#if result >= 0 :
	#print (vertList[result])

#testing sets	
setA = {1,2,3,4}
setB = {4,3,2,1}
#if setA == setB :
	#print ("setAB true")
#else :
	#print ("setAB false")

#testing nodeList [set, list]
nodeList = [[{"PRG", "615"}, [1,2,3]]]
nodeList.append([{"LAX", "CX"}, [4,5,6]])
nodeList.append([{"PRG", "LAX"}, [1,2,3]])
nodeList.append([{"615", "CX"}, [1,2,3]])
nodeList.append([{"HKG", "YVR"}, [1,2,3]])
#print (nodeList)
#arr and dep is not recognized
search = {"PRG", "LAX"}
result = -1
for sublist in nodeList :
    if sublist[0] == search :
        result = (nodeList.index(sublist))
        #print (sublist)
        break
#print (result)
#if result >= 0 :
	#print (nodeList[result])

#sublist test
i = 0	
while i < len(vertList) :
	#print (str(vertList[i][0]) + "," + str(vertList[i][1]) + ",", end="")
	n = 0
	sublist = vertList[i][2]
	while n < len(sublist) :
		#print (str(sublist[n]) + ",", end="")
		n += 1
	#print("")
	i += 1

#tripple array
nodeList = [[], [], []]
nodeList[0] = ["carrier","carrier","dep_apt","arr_apt"]
nodeList[1] = ["NK","MX","HKG","PRG"]
nodeList[2] = [[0,1,2,3], [4,5,6], [7,8,9,10], [11,12]]

search = "HKG"
n = nodeList[1].index(search)

i = 0
while i < 3:
	print(str(nodeList[i][n]), end="")
	if i < 2:
		print(", ", end="")
	i += 1
print ("\n")


#vertDict = {"a":[5,6,7]}
#vertDict["z"] = [5,6,7]
#vertDict["c"] = [5,6,7]
#vertDict["p"] = [5,6,7]
#print (vertDict)

#if  "x" in vertDict :
	#print ("vert true")
#else :
	#print ("vert false")

#nodeDict = {("a","N"):[5,6,7]}
#nodeDict[("f","Z")] = [5,6,7]
#print (nodeDict)

#if  ("a","M") in nodeDict :
	#print ("node true")
#else :
	#print ("node false")
	
vertList = [["carrier", "NK", [1,2,3]]]
vertList.append(["carrier", "MX", [1,2,3]])
vertList.append(["dep_apt", "HKG", [1,2,3]])
vertList.append(["arr_apt", "PRG", [1,2,3]])
print (vertList)
search = "PRG"
result = -1
for sublist in vertList :
    if sublist[1] == search :
        result = (vertList.index(sublist))
print (result)
if result >= 0 :
	print (vertList[result])

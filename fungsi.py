import math


def Ecl_dist(v,w):
	result=0
	for i in range (2048):
		result = result+((v[i]-w[i])*(v[i]-w[i]))
	return math.sqrt(result)


def Cos_simil(v,w):
	resultv=0
	resultw=0
	dotvw=0
	for i in range (2048):
		resultv+=float(v[i])**2
		resultw+=float(w[i])**2
		dotvw+=float(v[i])*float(w[i])
	normv=math.sqrt(resultv)
	normw=math.sqrt(resultw)

	return dotvw/(normv*normw)







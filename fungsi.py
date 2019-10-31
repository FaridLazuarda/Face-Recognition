import math


def Ecl_dist(v,w):
	result=0
	for i in range (2048):
		result+=(v[i]-w[i])**2
	return math.sqrt(result)


def Cos_simil(v,w):
	resultv=0
	resultw=0
	dotvw=0
	for i in range (2048):
		resultv+=v[i]**2
		resultw+=w[i]**2
		dotvw+=v[i]*w[i]
	normv=math.sqrt(resultv)
	normw=math.sqrt(resultw)

	return dotvw/(normv*normw)







import numpy as np
import matplotlib.pyplot as plt
import csv


def fit_quadratic_RANSAC(x,y,num_iterations=50, threshold=0.1):
	best_score=0
	best_coefficients=None
	
	for i in range(num_iterations):
		sample_indices=np.random.choice(len(x), size=3, replace=False)
		sample_x=x[sample_indices]
		sample_y=y[sample_indices]
	
		X=np.column_stack([sample_x**2, sample_x, np.ones(3)])
		coefficients=np.linalg.lstsq(X,sample_y, rcond=None)[0]
		
		distances=np.abs(y-np.polyval(coefficients,x))
		inliers=distances<threshold
		num_inliers=np.count_nonzero(inliers)
		
		if num_inliers>best_score:
			best_score=num_inliers
			best_coefficients=coefficients
			
	return tuple(best_coefficients)
	

f=open('RANSAC_data2.csv','r')
rdr=csv.reader(f)
_mydata=[]
for line in rdr:
	_mydata.append([float(line[0]),float(line[1])])
f.close()
data=np.array(_mydata)
x=data[:,0]
y=data[:,1]

a,b,c=fit_quadratic_RANSAC(x,y)
fig, ax=plt.subplots()
ax.scatter(x,y,color='blue')
ax.plot(x,a*x**2+b*x+c, color='red')
plt.show()


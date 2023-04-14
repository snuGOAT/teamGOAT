import numpy as np
import matplotlib.pyplot as plt
import csv

f=open('RANSAC_data.csv','r')
rdr=csv.reader(f)
_mydata=[]
for line in rdr:
	x_data=float(line[0])
	y_data=float(line[1])
	_mydata.append([x_data,y_data])
f.close()
data=np.array(_mydata)

def ransac_line_fitting(data, n_iterations=100, threshold=1, min_inliers=10):
	best_fit=None
	best_error=np.inf
	best_inliers=None
	
	for i in range(n_iterations):
		#Randomly select 2 points from the data
		sample=data[np.random.choice(data.shape[0], 2, replace=False), :]
		#Fit a line to the selected points
		x1, y1=sample[0]
		x2, y2=sample[1]
		a=(y2-y1)/(x2-x1)
		b=y1-a*x1
		
		distances=np.abs(a*data[:,0]-data[:,1]+b)/np.sqrt(a**2+1)
		inliers=data[distances<threshold]
		
		if len(inliers)>=min_inliers:
			error=np.sum(distances**2)
			if error<best_error:
				best_fit=(a,b)
				best_error=error
				best_inliers=inliers
	return best_fit, best_inliers

model, inliers=ransac_line_fitting(data,n_iterations=100, threshold=1, min_inliers=10)
plt.scatter(data[:,0],data[:,1],label="Data")
plt.scatter(inliers[:,0],inliers[:,1],label="inliers")
x_range=np.linspace(0,10,100)
plt.plot(x_range,model[0]*x_range+model[1],'r',label="RANSAC Line")
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

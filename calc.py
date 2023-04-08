def add(a,b):
	return a+b
def mul(a,b):
	return a*b
def sub(a,b):
	return a-b
def div(a,b):
	if(b==0):
		print('Error')
		quit()
	else:
		return a/b
	
if __name__=='__main__':
	x=int(input('x>'))
	y=int(input('y>'))
	print('%d + %d = %d'%(x,y, add(x,y)))
	print('%d - %d = %d'%(x,y, sub(x,y)))
	print('%d * %d = %d'%(x,y, mul(x,y)))
	print('%d / %d = %d'%(x,y, div(x,y)))

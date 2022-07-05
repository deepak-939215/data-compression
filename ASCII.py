def assignedCode(file,file1):

	res = ''
	for line in file.readlines():
		for char in line:
			res += (format(ord(char),'08b'))
	file1.write(res)
	print(len(res))

if __name__=='__main__':

	file = open('MnM.txt', 'r')
	file1 = open('ASCII.txt','w')
	assignedCode(file,file1)
	file.close()
	file1.close()
#LZ-78 Encoding Algorithm proposed by Ziv and Lempel

import operator

#Function to calculate number of 1 bits in a binary number
def countbits(a):

	count = 0
	while(a):
		if a&1:
			count += 1
		a = a>>1
	return count

#Function to create dictionary for input bit stream
def assignedCode(file):

	assign_dict = dict()

	for line in file.readlines():
		for char in line:
			if char in assign_dict:
				assign_dict[char] += 1
			else:
				assign_dict[char] = 1

	
	#Gives total number of characters present in the input text file
	total = sum(assign_dict.values(), 0.0)
	#To calculate probability of occurence for each character and storing them in an array
	assign_dict = {k: v / total for k, v in assign_dict.items()}
	#Storing characters in the dictionary in the decreasing order of their probabilities
	sorted_d = dict(sorted(assign_dict.items(), key=operator.itemgetter(-1), reverse=True))

	assign = dict()

	n  = len(assign_dict)
	onebits = dict()

	#Fixed length Encoding of characters to generate input file dictionary
	for i in range(n+1):
		onebits[i] = countbits(i)

	sorted_o = dict(sorted(onebits.items(), key=operator.itemgetter(-1)))

	for d,o in zip(sorted_d.keys(),reversed(sorted_o.keys())):
		assign[d] = "{0:06b}".format(o)

	return assign

#Printing input bit stream to new text file
def inputBitStream(file, file2, assign):

	IBS = ''

	for line in file.readlines():
		for char in line:
			IBS += assign[char]
			file2.write(assign[char])

	return IBS

#Application of LZ-78 algorithm on the generated input bit stream
def encodedBitStream(IBS, file3):

	encode = dict()

	encode['0'] = [1,'',1]
	encode['1'] = [2,'',2]
	word = ''
	j = 3
	for char in IBS:
		word += char
		if word not in encode.keys():
			encode[word] = [encode[word[:-1]][2], char, j]
			j += 1
			word = ''
	
	encodeBits = ''
	
	#Printing binary encoded block bit stream to text file which is our actual encoding
	for item in encode:
		if encode[item][2] == 2 or encode[item][2] == 1:
			continue
		
		encodeBits += "{0:014b}".format(encode[item][0])+encode[item][1]
		file3.write("{0:014b}".format(encode[item][0]))
		file3.write(encode[item][1])
	
	encodeBits += "{0:014b}".format(encode[word][0])
	file3.write("{0:014b}".format(encode[word][0]))

	return encode, encodeBits

#Steps for decoding
#Storing all the key and value pairs in new lists as reverse mapping to encoding
def outputBitStream(encode, encodeBits, file4):

	encode3 = dict()

	for i in encode:
		encode3[i] = encode[i][2]

	keys = list(encode.keys())
	values = list(encode3.values())
	decode = ''

	for i in range(0,len(encodeBits), 15):
		if (i == len(encodeBits)-14):
			decode += keys[values.index(int(encodeBits[i:i+14],2))]+encodeBits[i+12]
			continue

		decode += keys[values.index(int(encodeBits[i:i+14],2))]+encodeBits[i+14]
	file4.write(decode)

	return decode

def outputFile(decode, assign, file5):
	
	keys = list(assign.keys())
	values = list(assign.values())

	for i in range(0, len(decode), 6):

		file5.write(keys[values.index(decode[i:i+6])])


if __name__=='__main__':

	#Reading input file
	file = open('MnM.txt', 'r')
	assign_dict = assignedCode(file)
	file.close()

	#Printing input bit stream to new text file
	file1 = open('MnM.txt', 'r')
	file2 = open('inputBitStream.txt', 'w')	
	IBS = inputBitStream(file1, file2, assign_dict)
	file2.close()
	file1.close()

	#Printing encoded input bit stream to new text file
	file3 = open('encodedBitStream.txt','w')
	encode, encodeBits = encodedBitStream(IBS, file3)
	file3.close()

	#Printing decoded value in a new file
	file4 = open('outputBitStream.txt', 'w')	
	decode = outputBitStream(encode, encodeBits, file4)
	file4.close()

	#Printing the completely decoded file
	file5 = open('outputFile.txt', 'w')
	outputFile(decode, assign_dict, file5)
	file5.close()

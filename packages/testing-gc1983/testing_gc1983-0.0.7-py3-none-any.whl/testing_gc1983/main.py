import os

def hello():
	print("Hello world.")
	
def jupyter():
	file = open("gothere.txt", "w") 
	file.write("Got here") 
	file.close() 
	os.system('jupyter lab test1.ipynb')
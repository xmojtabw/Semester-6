import hashlib 

def hash_string(string): # Generate a hash for a string
    return hashlib.md5(string.encode()).hexdigest()

file_path_prefix  = './Q1/file'
file_count = 5000
files = {}

for i in range(1,file_count+1):
    file_path = file_path_prefix + str(i) 
    with open(file_path, 'r') as file:
        hash = hash_string(file.read()) # Generate hash for the file content
        if hash in files :  # If the hash already exists, append the file path to the list
            files[hash].append(file_path) 
        else :
            files[hash] = [file_path] # If the hash does not exist, create a new list with the file path

for key in files: # Iterate through the dictionary
    if len(files[key]) == 1: # If the list has only one file, it is unique
        different_file = files[key][0]
        print(f'The different file is {different_file}')
        with open (different_file, 'r') as file:
            print(file.read())
import os

# current working directory
# print(os.getcwd())

# to change current directory
# os.chdir('/home/sooraj/Desktop/hw/workout')

# to list  directory
# print(os.listdir())

# make directory
# os.mkdir('asdd')
# os.makedirs('asdd/efdf/sffdes')

# remove
# os.rmdir('asdd')
# os.removeddirs('asdd/efdf/sffdes')

# rename
# os.reame('current file name','new name')

# print(os.stat('urllib pkg.py'))

# for dirpath,dirname,filenames in os.walk('/home/sooraj/Desktop/'):
#     print('current path:',dirpath)
#     print('directories:',dirname)
#     print('files:',filenames)
#     print()



# file_path=os.path.join(os.environ.get('HOME'),'test.txt')
# print(file_path)


print(os.path.basename('/tmp/test.txt'))

print(os.path.dirname('/tmp/test.txt'))

print(os.path.split('/tmp/test.txt'))

print(os.path.splitext('/tmp/test.txt'))

print(os.path.exists('/tmp/test.txt'))


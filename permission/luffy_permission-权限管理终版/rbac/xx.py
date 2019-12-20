import sys

a = 10
def xx():
    print('xxoo')

f = sys.modules['__main__']
print(f)

f.xx()
print(f.a)


# 변수
name =  '민님'
age = 22
print (name, age)

# 함수
def say_hello():
    print("Hello from FastAPI!")

say_hello()

# 매개변수 있는 함수
def add(a, b):
    return a + b

result = add(1, 2)
print(result)

# 딕셔너리 (JS의 객체)
user = {'name': '민', 'age': 22}
print(user['name'])

# 리스트 (배열)
fruits = [ 'apple', 'banana', 'cherry' ]
print(fruits[0])

# 제어문
# if
x = 10
if x > 5:
    print('크다')
elif x == 5:
    print('같다')
else:
    print('작다')

# for
for fruit in fruits:
    print(fruit)

# while
count = 0
while count < 3:
    print(count)
    count += 1


import time

curr=time.time()
last=curr
#print(curr)

while True:
    if abs(curr-last)>=20:
        print("time now",curr)
        last=curr
    curr=time.time()
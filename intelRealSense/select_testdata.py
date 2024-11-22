import random
degree=['+45deg','+30deg','+15deg','0deg','-15deg','-30deg','-45deg']
distance=['10cm','15cm','20cm','25cm','30cm']

pop_count=4
for i in range(10):
    print("number: ", i)
    popped=[]
    for j in range(pop_count):
        random_degree = 0
        random_distance = 0
        while True:
            random_degree = random.randint(0, len(degree)-1)
            random_distance = random.randint(0, len(distance)-1)
            if (random_degree, random_distance) not in popped:
                popped.append((random_degree, random_distance))
                break
        print("degree: ", degree[random_degree], "distance: ", distance[random_distance])


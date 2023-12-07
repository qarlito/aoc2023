import math

def get_winning_number_range(T, D):
    discr = T*T - 4*D
    if discr <= 0:
        return 0
    left = math.floor((T - math.sqrt(discr))/2)
    right = math.ceil((T + math.sqrt(discr))/2)
    return (right - left - 1)


# Part 1 demo
s = '''Time:      7  15   30
Distance:  9  40  200'''

# Part 1 production
s = '''Time:        60     80     86     76
Distance:   601   1163   1559   1300'''

# Part 2 demo
s = '''Time:      71530
Distance:  940200'''

# Part 2 production
s = '''Time: 60808676
Distance: 601116315591300'''

total_times_line, distance_line = s.splitlines()
total_times = list(map(int, total_times_line.split(':')[1].strip().split()))
distances = list(map(int, distance_line.split(':')[1].strip().split()))

print(total_times, distances)

prod = 1
for race in range(len(total_times)):
    wins = get_winning_number_range(total_times[race], distances[race])
    print(wins)
    prod = prod * wins

print("PROD", prod)

def parse(line):
    maxima = dict()
    game, content = line.split(':')
    gamenum = int(game.split(' ')[1])
    shows = content.split(';')
    for show in shows:
        entries = show.split(',')
        for entry in entries:
            e1, e2 = entry.strip().split(' ')
            count = int(e1)
            value = e2.strip()
            maxima[value] = max(maxima.get(value, 0), count)
    return gamenum, maxima

s = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''


from advent_input_02 import s

result = 0
for line in s.strip().splitlines():
    game_num, game_maxima = parse(line)
    product = 1
    for maximum in game_maxima.values():
        product *= maximum
    result += product

print(result)

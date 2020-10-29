import random

player_details = {}


def input_validation(input_val, sentence):
    while not str(input_val).isnumeric():
        input_val = input(sentence)
    return input_val


def get_players_count():
    players = input('Please enter the number of players count : ')
    players = input_validation(players, 'Please enter the number of players count : ')
    accumulate = input('Please enter the accumulate count : ')
    accumulate = input_validation(accumulate, 'Please enter the accumulate count : ')
    return {'players_count': players, 'accumulate_val': accumulate}


def generate_name_for_player(count):
    players_name = {'Player-{num}'.format(num=num): {'score': 0, 'rank': 0, 'penalty': False, 'dice_values': []} for num
                    in
                    range(1, count + 1)}
    random_names = list(players_name.items())
    random.shuffle(random_names)
    return dict(random_names)


def print_score():
    print('{:<20} {:<20} {:<20}'.format('PLAYERS NAME', 'PLAYERS SCORE', 'PLAYER RANK'))
    for name, val in player_details.items():
        print('{:<20} {:<20} {:<20}'.format(name, val['score'], val['rank']))


def get_player_rank(player_name):
    return player_details[player_name]['rank']


def set_player_rank(player_name):
    player_details[player_name]['rank'] = max(
        list(map(lambda key: player_details[key]['rank'], player_details.keys()))) + 1


def check_player_score(player_name, max_score):
    if player_details[player_name]['score'] >= max_score:
        set_player_rank(player_name)
        print('{player_name} won the game with the rank of {player_rank}... 👏✌️'.format(player_name=player_name,
                                                                                         player_rank=get_player_rank(
                                                                                             player_name)))
        return get_player_rank(player_name)
    return 0


def pre_roll_dice_msg(player_name):
    player_input = input('{player_name} its your turn (press ‘r’ to roll the dice): '.format(player_name=player_name))
    if player_input.lower() == 'r':
        return
    else:
        pre_roll_dice_msg(player_name)


def dice_value(player_name):
    val = random.randint(1, 6)
    print('{name} has scored {val} in this turn...'.format(name=player_name, val=val))
    return val


def update_player_score(player_name, player_value, player_dice_val, player_rank, max_score):
    player_details[player_name]['dice_values'].append(player_dice_val)
    player_value += player_dice_val
    player_details[player_name]['score'] = player_value
    player_details[player_name]['rank'] = check_player_score(player_name, max_score)
    return player_details[player_name]['rank']


def roll_dice_again(player_name, old_value):
    player_input = input(
        f'{player_name} its your turn again due to the value of {old_value} (press ‘r’ to roll the dice): ')
    if player_input.lower() == 'r':
        return dice_value(player_name)
    else:
        roll_dice_again(player_name, old_value)


def penalty_msg(player_name):
    print(f'{player_name} is penalised due to rolled "1" twice consecutively.. 😞')


def roll_dice(player_name, player_value, max_score):
    pre_roll_dice_msg(player_name)
    player_dice_value = dice_value(player_name)
    check_penalty(player_name, player_dice_value)
    update_player_score(player_name, player_value['score'], player_dice_value, get_player_rank(player_name), max_score)
    loop_next_try = True if player_dice_value == 6 else False
    second_dice_value = player_dice_value
    while loop_next_try:
        check_current_player_score = 0
        if second_dice_value == 6:
            second_dice_value = roll_dice_again(player_name, second_dice_value)
            player_dice_value += second_dice_value
            check_current_player_score = update_player_score(player_name, player_value['score'], second_dice_value,
                                                             get_player_rank(player_name), max_score)
        loop_next_try = True if second_dice_value == 6 and check_current_player_score == 0 else False

    return True


def check_game_over():
    return min(list(map(lambda key: player_details[key]['rank'], player_details.keys())))


def check_penalty(player_name, new_dice_value):
    temp_list = player_details[player_name]['dice_values']
    if player_details[player_name]['penalty']:
        player_details[player_name]['penalty'] = False
        return True
    if len(temp_list) >= 2 and temp_list[-1] == 1 and temp_list[-1] == new_dice_value:
        player_details[player_name]['dice_values'].append(0)
        player_details[player_name]['penalty'] = True
        penalty_msg(player_name)
    return False


def main_function():
    player_count = get_players_count()
    global player_details
    player_details = generate_name_for_player(int(player_count.get('players_count')))
    game_over = True
    while game_over:
        for (name, val) in player_details.items():
            if check_game_over() > 0:
                game_over = False
                break
            if player_details[name]['rank'] > 0:
                continue
            if player_details[name]['penalty']:
                player_details[name]['penalty'] = False
                continue
            game_over = roll_dice(name, val, int(player_count.get('accumulate_val')))
            print_score()
            if not game_over:
                break


if __name__ == '__main__':
    main_function()

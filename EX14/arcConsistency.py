
def arc_consistency(xx, yy):
    type_x, num_x, words_x = xx
    type_1, num_1, words_1 = yy

    new_words_x = words_x[:]

    for word_x in words_x:
        is_found_consistent_value_1 = False
        for word_1 in words_1:
            ch_x = word_x[num_1 - 1:num_1]
            ch_1 = word_1[num_x - 1:num_x]

            if ch_x == ch_1:
                is_found_consistent_value_1 = True
                break
        if not is_found_consistent_value_1:
            new_words_x.remove(word_x)
            continue

    return type_x, num_x, new_words_x


if __name__ == "__main__":

    words_list = ["add", "ado", "age", "ago", "aid", "ail", "aim", "air", "and", "any", "ape", "apt", "arc", "are",
                  "ark", "arm", "art", "ash", "ask", "auk", "awe", "awl", "aye", "bad", "bag", "ban", "bat", "bee",
                  "boa", "ear", "eel", "eft", "far", "fat", "fit", "lee", "oaf", "rat", "tar", "tie"]

    dict_variables = {'a1': ('a', 1, words_list[:]), 'a2': ('a', 2, words_list[:]), 'a3': ('a', 3, words_list[:]),
                      'd1': ('d', 1, words_list[:]), 'd2': ('d', 2, words_list[:]), 'd3': ('d', 3, words_list[:])}

    list_constrains = [('a1', 'd1'), ('d1', 'a1'), ('a1', 'd2'), ('d2', 'a1'), ('a1', 'd3'), ('d3', 'a1'),
                       ('a2', 'd1'), ('d1', 'a2'), ('a2', 'd2'), ('d2', 'a2'), ('a2', 'd3'), ('d3', 'a2'),
                       ('a3', 'd1'), ('d1', 'a3'), ('a3', 'd2'), ('d2', 'a3'), ('a3', 'd3'), ('d3', 'a3')]

    is_first = True
    is_changed = False
    while is_changed or is_first:
        is_first = False
        is_changed = False
        for constrain in list_constrains:
            x, y = constrain
            new_x = arc_consistency(dict_variables.get(x), dict_variables.get(y))
            if len(new_x[2]) != len(dict_variables.get(x)[2]):
                is_changed = True
                dict_variables[x] = new_x

    for key in dict_variables.keys():
        print key + ": " + str(dict_variables.get(key)[2])

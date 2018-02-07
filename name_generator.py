import pandas
import numpy as np


def main():
    print('start')

    # the names to use as an input
    source_names_path = './names/100_boys_names_uk.csv'
    source_names = pandas.read_csv(source_names_path)

    source_names = source_names['Names'].values

    filtered_source_names = []
    for source_name in source_names:
        filtered_source_name = source_name.lower()
        filtered_source_name = list(filtered_source_name)
        filtered_source_name[0] = filtered_source_name[0].upper()
        filtered_source_name = ''.join(filtered_source_name)
        filtered_source_names.append(filtered_source_name)

    print(filtered_source_names)

    fragments = fragment_builder(filtered_source_names, frag_size=2)

    print(fragments)

    words_to_generate = 20
    while words_to_generate > 0:
        new_word = build_word(fragments, min_length=5, max_length=7)

        new_word = list(new_word)
        new_word[0] = new_word[0].upper()
        new_word = ''.join(new_word)

        if new_word not in filtered_source_names:
            print(new_word)
            words_to_generate -= 1

def build_word(fragments, min_length, max_length):
    """Generates a word from the fragments provided that is of a random length between min_length and max_length."""

    target_length = np.random.randint(min_length, max_length + 1)

    word_building_attempts = 0
    max_attempts = 100
    while word_building_attempts < max_attempts:
        random_index = np.random.randint(0, len(fragments))

        # starting generated word with a random fragment
        word = fragments.keys()[random_index]
        frag_size = len(word)

        while len(word) < target_length:
            end_fragment = word[-frag_size:len(word)]

            try:
                word += fragments[end_fragment][np.random.randint(0, len(fragments[end_fragment]))]
            except KeyError:
                    word_building_attempts += 1
                    break
        if len(word) == target_length:
            return word

    raise ValueError('could not construct any words of the required length after %i attempts' % max_attempts)


def fragment_builder(words, frag_size):
    fragments = {}

    for word in words:
        if len(word) > frag_size:
            word_position = 0
            while len(word) - (word_position + frag_size) > 0:
                fragment = word[word_position:word_position + frag_size].lower()
                next_character = word[word_position + frag_size]

                try:
                    if next_character not in fragments[fragment]:
                        fragments[fragment].append(next_character)
                except KeyError:
                    fragments[fragment] = [next_character]

                word_position += 1

    return fragments

if __name__ == '__main__':
    main()
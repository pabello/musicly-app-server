#!/usr/bin/python3

from typing import OrderedDict


file_names = ['artists.md', 'ppl_artists.md']
artists = {}
banned_artists = {}

for path in file_names:
    with open(path, 'r') as file:
        for line in file:
            line_artists = line.strip().rstrip('.').replace(', ', ';').replace('; ', ';').replace(',', ';').lower().strip(';').split(';')
            for artist in line_artists:
                if artist != '':
                    if "'" not in artist:
                        if artist in artists.keys():
                            artists[artist] += 1
                        else:
                            artists[artist] = 1
                    else:
                        if artist in banned_artists.keys():
                            banned_artists[artist] += 1
                        else:
                            banned_artists[artist] = 1

# artists = {' '.join([word.capitalize() for word in key.split()]): artists[key] for key in artists.keys()}

# sorted_artists = {artist: artists[artist] for artist in sorted(artists, key=lambda artist: artists[artist], reverse=True)}

# for artist in sorted_artists:
#     print(f'{artist} -> {artists[artist]}')

for artist in banned_artists:
    print(artist)
print(len(artists) + len(banned_artists))

artists_dump = '\', \''.join(artists)
with open('artist_list.txt', 'w') as file:
    file.write(f'\'{artists_dump}\'')
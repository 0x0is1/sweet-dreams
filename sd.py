from sdlib import sdlib

def main():
    categories = sdlib.get_categories()
    for i, j in enumerate(categories): print(f"{i+1}. {j[1]}")
    category = categories[int(input("Select category: "))-1]
    category_types = ['movies', 'series']
    for i, j in enumerate(category_types): print(f"{i+1}. {j.capitalize()}")
    cidx = int(input("Select category type: "))-1
    category_type = category_types[cidx]
    contents = sdlib.get_contents(category[0], category_type)
    for i,j in enumerate(contents):
        print(f"{i+1}. {j[1]}")
    content = contents[int(input("Select content: "))-1]
    if cidx!=0:
        seasons = sdlib.get_seasons(content[0])
        for _, i, j in seasons: print(f"{i}. {j}")
        season = seasons[int(input("Select season: "))-1]
        episodes = sdlib.get_episodes(season[1], season[0])
        for i, j in enumerate(episodes): print(f"{i+1}. {j[1]}")        
        episode = episodes[int(input("Select episode: "))-1]
        eid = sdlib.get_eid(episode[0], None)
    else:
        eid = sdlib.get_eid(None, content[0])
        
    file_url, title= sdlib.fetch_data(sdlib.generate_url(eid))
    sdlib.play(file_url, title)

if __name__ == '__main__':
    main()

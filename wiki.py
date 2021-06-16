import wikipedia as wk
import networkx as nx
from operator import itemgetter


def generate_wiki_graph():
    SEED = "Graph theory".title()

    STOPS = ("International Standard Serial Number",
            "International Standard Book Number",
            "National Diet Library",
            "International Standard Name Identifier",
            "International Standard Book Number (Identifier)",
            "Pubmed Identifier", "Pubmed Central",
            "Digital Object Identifier", "Arxiv",
            "Proc Natl Acad Sci Usa", "Bibcode",
            "Library Of Congress Control Number", "Jstor")

    todo_list = [(0, SEED)]
    todo_set = set(SEED)
    done_set = set()

    W = nx.DiGraph()
    layer, page = todo_list[0]

    while layer < 2:
        del todo_list[0]
        done_set.add(page)
        print(layer, page)

        try:
            wiki = wk.page(page)
        except:
            layer, page = todo_list[0]
            print(f'Couldn\'t load {page}')
            continue

        for link in wiki.links:
            link = link.title()

            if link not in STOPS and not link.startswith('List of'):
                if link not in todo_set and link not in done_set:
                    todo_list.append((layer+1, link))
                    todo_set.add(link)
                W.add_edge(page,link)
        layer, page = todo_list[0]
    print(f'{len(W)} nodes, {nx.number_of_edges(W)} edges')

    nx.write_graphml(W, 'wiki.graphml')


import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages = len(corpus)
    dict_pages = dict.fromkeys(corpus, None)
    total_links = len(corpus[page])

    if total_links == 0:
        for i in dict_pages:
            dict_pages.update({i: 1/total_pages})
        return dict_pages

    #definindo o valor base para os links da pagina
    for i in corpus:
        dict_pages.update({i: (1-damping_factor)/total_pages})

    #defindo o valor extra somando ao valor base
    for j in corpus[page]:
        dict_pages.update({j: dict_pages[j] + (damping_factor/total_links)})

    return dict_pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_sample = n
    dict_count = dict.fromkeys(corpus, 0)
    first_sample = random.choice(list(dict_count))
    dict_count[first_sample] += 1
    currency_page = first_sample

    for _ in range(n-1):
        dict_pages = transition_model(corpus, currency_page, damping_factor)
        pages = list(dict_pages.keys())
        probability = list(dict_pages.values())

        next_page = random.choices(pages, weights=probability, k=1)[0]
        dict_count[next_page] += 1
        currency_page = next_page

    for i in dict_count:
        dict_count[i] = dict_count[i] / total_sample

    return dict_count


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    new_corpus = {}
    pagerank = dict.fromkeys(corpus)

    for i in corpus:
        if len(corpus[i]) == 0:
            new_corpus[i] = set(corpus.keys())
        else:
            new_corpus[i] = corpus[i]

    for j in  pagerank:
        pagerank[j] = 1/n

    while True:
        pagerank_antigo = pagerank.copy()
        pagerank_novo = {}
        convergiu = True

        for page in corpus:
            base = (1 - damping_factor) / n
            somatorio = 0
            for i in new_corpus:
                if page in new_corpus[i]:
                    somatorio += pagerank_antigo[i] / len(new_corpus[i])
            pagerank_novo[page] = base + (damping_factor * somatorio)

        for pagina in new_corpus:
            diferenca = abs(pagerank_novo[pagina] - pagerank_antigo[pagina])
            if diferenca > 0.001:
                convergiu = False
        if convergiu:
            break
        pagerank = pagerank_novo

    return pagerank_novo

if __name__ == "__main__":
    main()

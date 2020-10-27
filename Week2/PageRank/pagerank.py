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

    if len(corpus[page]) == 0:
        answer_dict = {key: 1 / len(corpus) for key in corpus}
    else:
        answer_dict = {key: ((1 - damping_factor) / len(corpus)) for key in corpus}

        linked_prob = damping_factor / len(corpus[page])

        for key in answer_dict:
            if key in corpus[page]:
                answer_dict[key] += linked_prob

    return answer_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_pages = {key: 0 for key in corpus}

    pages = list(corpus.keys())

    current_page = pages[random.randint(0, len(pages) - 1)]

    sample_pages[current_page] += 1

    for _ in range(n - 1):
        pages = transition_model(corpus, current_page, damping_factor)
        
        page_names = []
        page_probabilities = []

        for key, value in pages.items():
            page_names.append(key)
            page_probabilities.append(value)

        current_page = random.choices(page_names, weights=page_probabilities, k=1)[0]

        sample_pages[current_page] += 1


    for key in sample_pages:
        sample_pages[key] /= n

    return sample_pages


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_ranks = {key: (1 / len(corpus)) for key in corpus}

    for key, value in corpus.items():
        if (len(value)) == 0:
            for key2 in corpus:
                corpus[key].add(key2)

    not_converged = True

    while not_converged:
        page_ranks_new = {}

        for key, value in corpus.items():
            probab = (1 - damping_factor) / len(corpus)

            sum_of_probs = 0
            for key2, value2 in corpus.items():
                if key in value2:
                    sum_of_probs += (page_ranks[key2] / len(value2))

            page_ranks_new[key] = probab + (damping_factor * sum_of_probs)

        not_converged = False

        for key in page_ranks:
            if abs(page_ranks[key] - page_ranks_new[key]) > 0.001:
                not_converged = True
                break

        page_ranks = page_ranks_new

    return page_ranks



if __name__ == "__main__":
    main()

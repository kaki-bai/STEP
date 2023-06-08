import sys
import collections
# import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# pages_path = os.path.join(current_dir, './wikipedia_dataset/pages_small.txt')
# links_path = os.path.join(current_dir, './wikipedia_dataset/links_small.txt')

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        queue = collections.deque() # the pages that are waiting to be visited
        visited_index = {}          # the index of visited pages
        prev = {}                   # one previous page's index
        answer_index = []           # the index of pages in the shortest path
        answer_title = []           # the title of pages in the shortest path

        # find start index and goal index
        start_index = None
        goal_index = None
        for id in self.titles.keys():
            if self.titles[id] == start:
                start_index = id
            elif self.titles[id] == goal:
                goal_index = id
            if start_index and goal_index:
                break
        if not start_index or not goal_index:
            print("No start or final page found")
            exit(1)
        
        queue.append(start_index)
        visited_index[start_index] = True
        prev[start_index] = None

        while queue:
            visiting_index = queue.popleft()
            # if the goal gets visited
            if self.titles[visiting_index] == goal:
                back_index = visiting_index
                # go back to present the shortest path
                while back_index:
                    answer_index.append(back_index)
                    back_index = prev[back_index]
                for id in answer_index[::-1]:
                    answer_title.append(self.titles[id])
                print(answer_title)
                return answer_title
            else:
                for id in self.links[visiting_index]:
                    if id not in visited_index:
                        queue.append(id)
                        visited_index[id] = True
                        prev[id] = visiting_index
        print("No path found")
        return False


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        page_num = len(self.titles)
        old_page_rank = {}
        new_page_rank = {}
        zero_page_rank = {}
        no_to_link_index = []
        # initialize the page ranks
        for id in self.titles.keys():
            old_page_rank[id] = 1.0
            new_page_rank[id] = 0.0
            zero_page_rank[id] = 0.0

        for id, link_array in self.links.items():
            if len(link_array) == 0:
                no_to_link_index.append(id)
        
        circulation_count = 0
        while circulation_count < 100:
            page_rank_sum_fifteen = 0
            page_rank_sum_hundred = 0
            # page_rank_sum = sum(old_page_rank.values())
            for from_index, link_array in self.links.items():
                for to_index in link_array:
                    new_page_rank[to_index] += 0.85 * old_page_rank[from_index] / len(link_array)
            for id in self.titles.keys():
                if id not in no_to_link_index:
                    page_rank_sum_fifteen += old_page_rank[id]
                else:
                    page_rank_sum_hundred += old_page_rank[id]
            for id in self.titles.keys():
                new_page_rank[id] += (0.15*page_rank_sum_fifteen + page_rank_sum_hundred) / page_num
                

            if circulation_count > 80:
                difference = sum(abs(new_page_rank[id] - old_page_rank[id]) for id in old_page_rank.keys())
                if difference < 0.01:
                    break

            old_page_rank = new_page_rank.copy()
            new_page_rank = zero_page_rank.copy()

            circulation_count += 1

        max_page_rank = max(old_page_rank.values())
        for key, value in old_page_rank.items():
            if value == max_page_rank:
                max_page_index = key
                break
        print(circulation_count)
        print(self.titles[max_page_index])
        # print(old_page_rank)
        return self.titles[max_page_index]

    
    def find_most_no_titles(self):
        count_no = {}
        for value in self.titles.values():
            count = value.count('の')
            if count not in count_no:
                count_no[count] = []
            count_no[count].append(value)
        titles = sorted(count_no.keys(), reverse=True)
        print("The titles with most 'の' are:")
        print(f'{count_no[titles[0]]} with {titles[0]} "の"')
        print()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    # wikipedia.find_shortest_path("A", "F")
    # wikipedia.find_most_popular_pages()
    # wikipedia.find_most_no_titles()
    wikipedia.find_most_popular_pages()
    
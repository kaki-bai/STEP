import sys
import ex1

# Implement a data structure that stores the most recently accessed N pages.
# See the below test cases to see how it should work.
#
# Note: Please do not use a library like collections.OrderedDict). The goal is
#       to implement the data structure yourself!


# A page that contains the URL and contents
class Page:
    # Initialize the page
    # |prev|: the page accessed after it
    # |next|: the page accessed before it
    def __init__(self, url, contents):
        self.url = url
        self.contents = contents
        self.prev = None
        self.next = None

# A data structure that stores the most recently accessed N pages.
class Cache:
    # Initialize the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        self.cache_table = ex1.HashTable()
        self.size = n
        self.head = None
        self.tail = None

    # Access a page and update the cache so that it stores the most recently
    # accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    def access_page(self, url, contents):
        # if the page has been in the cache
        if self.cache_table.get(url)[1]:
            page = self.head
            while page:
                if page.url == url and page.contents == contents:
                    self.move_to_top(page)
                    return True
                page = page.next

        # if the page has not been in the cache
        new_page = Page(url, contents)
        self.cache_table.put(url, contents)
        self.add_to_top(new_page)
        # if the cache is empty
        if not self.tail:
            self.tail = new_page
        # if there are more than n(self.size) pages in the cache
        if self.cache_table.item_count > self.size:
            self.tail = self.tail.prev
            self.tail.next = None

    # Return the URLs stored in the cache. The URLs are ordered in the order
    # in which the URLs are mostly recently accessed.
    def get_pages(self):
        pages = []
        page = self.head
        while page:
            pages.append(page.url)
            page = page.next
        return pages

    # add the page to the top
    def add_to_top(self, page):
        page.next = self.head
        page.prev = None
        if self.head:
            self.head.prev = page
        self.head = page

    # remove the page from ordered list
    def delete_page(self, page):
        if page == self.head:
            self.head = page.next
            if self.head:
                self.head.prev = None
        if page == self.tail:
            self.tail = page.prev
            if self.tail:
                self.tail.next = None
        if page.next:
            page.next.prev = page.prev
        if page.prev:
            page.prev.next = page.next
    
    # move the page to the top
    def move_to_top(self, page):
        if page == self.head:
            return
        self.delete_page(page)
        self.add_to_top(page)

def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)

    # Initially, no page is cached.
    assert cache.get_pages() == []

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    assert cache.get_pages() == ["a.com"]

    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["b.com", "a.com"]

    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["c.com", "b.com", "a.com"]

    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    assert cache.get_pages() == ["d.com", "c.com", "b.com", "a.com"]

    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "d.com", "c.com", "b.com"]

    cache.access_page("c.com", "CCC")
    assert cache.get_pages() == ["c.com", "a.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]
    cache.access_page("a.com", "AAA")
    assert cache.get_pages() == ["a.com", "c.com", "d.com", "b.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "a.com", "c.com", "d.com"]

    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["f.com", "e.com", "a.com", "c.com"]

    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "f.com", "a.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["e.com", "f.com", "a.com", "c.com"]

    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "e.com", "f.com", "c.com" -->(least recently accessed)
    assert cache.get_pages() == ["a.com", "e.com", "f.com", "c.com"]

    print("Tests passed!")


if __name__ == "__main__":
    cache_test()
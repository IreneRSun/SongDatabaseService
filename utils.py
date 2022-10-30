import os

def display_line():
    """
    print a line of dashes
    :return: N/A
    """
    print("-" * 80)


def check_blank(inp):
    """
    checks whether the user entered a blank line
    :return: whether the user entered a blank line (bool)
    """
    return inp == "" or inp.isspace()

def get_keywords():
    """
    get keywords to search for from user
    :return: a blank line if the user enters a blank line (str), otherwise returns keywords to search for (list of str)
    """
    # get keywords from user
    keywords = input("Enter keywords seperated by whitespace: ")
    # check if user inputted a blank line
    if check_blank(keywords):
        return keywords
    # otherwise return the list of keywords
    keywords = keywords.split()
    return keywords

def get_num_pages(results):
    """
    get number of pages that can be displayed
    :param results: list used to determine how many pages there
    should be
    :return: number of pages that can be displayed (int)
    """
    num_pages = len(results) // 5
    if (len(results) / 5) > num_pages:
        num_pages += 1
    return num_pages

def display_page(results, page_num):
    """
    display a page of the results
    :param results: ordered list of results to display
    :param page_num: the page to display (int)
    :return: N/A
    """
    print(f"Keyword Matching Results Page {page_num}")
    # get rows for current page
    start = 5 * (page_num - 1)
    if (start + 4) > (len(results) - 1):
        end = len(results)
    else:
        end = start + 5
    curr = results[start:end]

    # display rows of current page
    curr = enumerate(curr, start + 1)
    for num, row in curr:
        print(num, "\t", row)

def handle_next(curr_page, results):
    """
    displays the next page of results
    :param curr_page: the current page (int)
    :param results: the ordered list of results to display
    :return: the current page number (int)
    """
    os.system('cls')
    
    # change page to the next page if possible
    if curr_page < get_num_pages(results):
        curr_page += 1
        display_page(results, curr_page)
    # if there is no next page
    else:
        print("This is the last page")
    return curr_page


def handle_prev(curr_page, results):
    """
    displays the previous page of results
    :param curr_page: the current page (int)
    :param matches: the ordered list of results to display
    :return: the current page number (int)
    """
    os.system('cls')

    # change page to previous page if possible
    if curr_page > 1:
        curr_page -= 1
        display_page(results, curr_page)
    # if there is no previous page
    else:
        print("This is the first page")
    return curr_page

def handle_page_logic(results, cursor, on_select):
  """
    Utility function to handle multi-page logic
    :param results: the ordered list of results to display
    :param cursor: database cursor
    :param on_select: function to call when an option is selected

    Adapted from isun's original code
  """
  # display instructions for selecting an option
  os.system('cls')
  print("To select the match number n, type: select n")
  print("To see the next page of matches, type: next")
  print("To see the previous page of matches, type: prev")
  print("To quit the program, type: quit")

  # display first page
  curr_page = 1
  display_page(results, 1)

  # handle user input
  while True:
    # get user input
    action = input("Enter input: ")

    # if user entered a blank line
    if check_blank(action):
        return
    
    if action == "quit":
        quit()

    # else parse input
    action = action.lower()
    action = action.split()
    action_type = action[0]

    # handle the select option
    if action_type == "select" and len(action) > 1 and action[1].isdigit():
        choice = int(action[1])

        # Make sure choice is within bounds        
        if choice > len(results) or choice < 1:
            print("Invalid input")
        else:
            # retrieve choice selected and pass on
            data = results[choice - 1]
            on_select(data, cursor)

    # handle the next option
    elif action_type == "next":
        curr_page = handle_next(curr_page, results)

    # handle the prev option
    elif action_type == "prev":
        curr_page = handle_prev(curr_page, results)
        
    # handle invalid input
    else:
        print("Invalid input")

# Third-party
import requests
import bs4

# Python
import random
import tabulate


# Take information from site about countries
r: requests.Response = requests.get('https://geography-a.ru/evraziya/strany-evrazii.html')

# Use bs4 to get useful information for our application
data: bs4.BeautifulSoup   = bs4.BeautifulSoup(r.text, 'lxml')
data: bs4.NavigableString = data.find('tbody')
data: bs4.NavigableString = data.find_all('tr')

# Define variables
COUNTRIES: list = [] # ALL COUNTRIES
CAPITALS : list = [] # ALL CAPITALS
PAIRS    : dict = {} # PAIRS OF COUNTRY: CAPITAL

# Take information from a parsed site and
# add data to the necessary variables
line: bs4.element.Tag
for line in data:

    info = line.text.split('\n')
    a = info[1]
    b = info[2]
    COUNTRIES.append(a)
    CAPITALS.append(b)
    PAIRS[a] = b

# Define difficulty (amount of possible capitals to one country)
while True:

    difficulty: str = input('выберите солжность (2-10 | max): ')
    if difficulty == 'max':
        break
    if not difficulty.isdigit():
        continue
    difficulty: int = int(difficulty)
    if difficulty < 2 or difficulty > 10:
        continue
    print('')
    break

# Define count of all questions to give the result
# of the number of correct answers and detailed information
# about all answers at the end of the test
while True:

    quiz_length: str = input('выберите длину теста (1-100 | inf) : ')
    if quiz_length == 'inf':
        break
    if not quiz_length.isdigit():
        continue
    quiz_length: int = int(quiz_length)
    if quiz_length < 1 or quiz_length > 100:
        continue
    print('')
    break

# Define variables
all_answers_list: list = [] # List to save all user's answers

correct_answers_counter: int = 0 # Counter of correct user's answers
all_answers_counter    : int = 0 # Counter of all users's answers

if quiz_length == 'ing':
    all_answers_counter = - float('infinity')

# Test process
while True:

    country: str = random.choice(COUNTRIES) # Choose one random country
    # Remove country from list of all countries to except repetition
    if quiz_length != 'inf':
        COUNTRIES.remove(country)

    print('Столица страны %s : ' % country) # Print it to the user

    # Define capital of this country and add it to the list
    correct_answer: str  = PAIRS.get(country)
    all_answers   : list = [correct_answer]

    # Fills the list of all possible answers
    if difficulty != 'max':
        while len(all_answers) != difficulty:
            capital: str = random.choice(CAPITALS)
            if capital == correct_answer or capital in all_answers:
                continue
            all_answers.append(capital)

        random.shuffle(all_answers) # shuffles all the answers

        # Take all possible answers and print it to the user
        i     : int
        answer: str
        for i, answer in enumerate(all_answers):
            print('%d) %s' % (i+1, answer))

    # Define variable to check if the answer is correct
    is_correct: bool = None

    # Take answer of the user
    while (answer := input()) not in all_answers:
        if difficulty == 'max':
            break
        pass

    # Define if the answer was correct
    if answer.lower() != correct_answer.lower():
        print('  [x] НЕПРАВИЛЬНО')
        print('  [i] Верным ответом было : %s\n' % correct_answer)
        is_correct = False
    else:
        print('  [V] ПРАВИЛЬНО\n')
        correct_answers_counter = correct_answers_counter + 1
        is_correct = True

    # Increase counter by one
    all_answers_counter = all_answers_counter + 1
    # Add user's answer to list of all it's answers
    all_answers_list.append([
        ['НЕПРАВИЛЬНО', 'ПРАВИЛЬНО'][is_correct],
        country, answer, correct_answer
    ])

    # Check if the test is completed
    if all_answers_counter == quiz_length:
        break

# Create a beautiful table of all user's answers
# for display using the tabulate library
result = tabulate.tabulate(
    headers=('ПРАВИЛЬНО ЛИ', 'СТРАНА', 'ВАШ ОТВЕТ', 'ПРАВИЛЬНЫЙ ОТВЕТ'),
    tabular_data=all_answers_list, tablefmt='rounded_grid'
)
# Print the result
print(result)
# Print a report on the count of correct answers
print('\n%d / %d правильных ответов' %
      (correct_answers_counter, quiz_length))

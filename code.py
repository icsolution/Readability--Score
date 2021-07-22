import re
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument('--infile')
parser.add_argument('--words')
args = parser.parse_args()


class ReadabilityScore:

    def __init__(self, text, words):
        self.text = open('in.txt', 'r').read().lower()
        self.difficult_words = open('words.txt', 'r').read().split()
        self.word = re.sub(r'[^a-z0-9 ]', '', self.text).replace('\n', '').split()
        self.words = len(self.word)
        self.sentences = len([i for i in self.text if i in '.!?'])
        if self.text[-1] not in '.!?':
            self.sentences += 1
        self.characters = len(re.findall(r"\S", self.text))
        self.syllables = self.calculate_syllables()
        self.difficult_list = len([word for word in self.word if word not in self.difficult_words])
        self.age = [0, 0]
        self.display()

    def display(self):
        print(f'The text is:\n{self.text}')
        print()
        print(f'Words: {len(self.text.split())}')
        print(f'Difficult words: {self.difficult_list}')
        print(f'Sentences: {self.sentences}')
        print(f'Characters: {self.characters}')
        print(f'Syllables: {self.syllables["syllables"]}')
        print(f'Polysyllables: {self.syllables["polysyllables"]}')
        choice = input('Enter the score you want to calculate (ARI, FK, SMOG, CL, PB, all): ')
        print()
        exec(f'self.calculate_{choice.lower()}()')
        print()
        print(f'This text should be understood in average by {self.age[0] / self.age[1]:.2f}-year-olds.')

    def calculate_syllables(self):
        syllables = polysyllables = 0
        for word in self.word:
            word = re.sub(r'[aeiouy][aeiouy]', 'a', word)  # omit double vowels
            word = re.sub(r'e$', '', word)  # remove silent vowel
            vowel_count = len(re.findall(r'[aeiouy]', word))
            if vowel_count == 0:
                vowel_count += 1
            if 'ed' in word[-2:]:
                vowel_count -= 1
            syllables += vowel_count
            if vowel_count > 2:
                polysyllables += 1
        return {'syllables': syllables, 'polysyllables': polysyllables}

    def calculate_ari(self):
        score = 4.71 * (self.characters / self.words) + 0.5 * (self.words / self.sentences) - 21.43
        age = self.match_ari_table(score)
        self.age[0] += age
        self.age[1] += 1
        print(f'Automated Readability Index: {score:.2f} (about {age}-year-olds).')

    def calculate_fk(self):
        score = 0.39 * (self.words / self.sentences) + 11.8 * (self.syllables["syllables"] / self.words) - 15.59
        age = self.match_ari_table(score)
        self.age[0] += age
        self.age[1] += 1
        print(f'Flesch–Kincaid readability tests: {score:.2f} (about {age}-year-olds).')

    def calculate_smog(self):
        score = 1.042 * math.sqrt((self.syllables["polysyllables"] * 30) / self.sentences) + 3.1291
        age = self.match_ari_table(score)
        self.age[0] += age
        self.age[1] += 1
        print(f'Simple Measure of Gobbledygook: {score:.2f} (about {age}-year-olds).')

    def calculate_cl(self):
        score = (5.89 * (self.characters / self.words)) - (30 *(self.sentences / self.words)) - 15.8
        age = self.match_ari_table(score)
        self.age[0] += age
        self.age[1] += 1
        print(f'Coleman–Liau index: {score:.2f} (about {age}-year-olds).')

    def calculate_pb(self):
        score = 0.1579 * (self.difficult_list / self.words) * 100 + 0.0496 * (self.words / self.sentences)
        if math.ceil(score) >= 4:
            score += 3.6365
        age = self.match_difficult_table(score)
        self.age[0] += age
        self.age[1] += 1
        print(f'Probability-based score: {score:.2f} (about {age}-year-olds).')

    def calculate_all(self):
        self.calculate_ari()
        self.calculate_fk()
        self.calculate_smog()
        self.calculate_cl()
        self.calculate_pb()

    @staticmethod
    def match_ari_table(score):
        score = round(score)
        table = {1: 6, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 13,
                 8: 14, 9: 15, 10: 16, 11: 17, 12: 18, 13: 24, 14: 25}
        return table[score] if score in table else 25

    @staticmethod
    def match_difficult_table(score):
        score = math.floor(score)
        table = {4: 10, 5: 12, 6: 14, 7: 16, 8: 18, 9: 24}
        return table[score] if score in table else 25


if __name__ == '__main__':
    ReadabilityScore(args.infile, args.words)


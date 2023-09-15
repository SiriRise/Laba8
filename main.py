#Составьте все различные лексемы, переставляя буквы в слове «институт»
#ограничение - гласные не могут стоять рядом
#целевая функция - лексемы с наибольшим числом согласных на нечетных местах

#Требуется для своего варианта второй части л.р. №6 (усложненной программы) или ее объектно-ориентированной реализации (л.р. №7)
#разработать реализацию с использованием графического интерфейса. Допускается использовать любую графическую библиотеку питона.
#Рекомендуется использовать внутреннюю библиотеку питона  tkinter.

#В программе должны быть реализованы минимум одно окно ввода, одно окно вывода,
#текстовое поле, кнопка.



import tkinter as tk
from tkinter import ttk


class LexemeFinder:
    def __init__(self, s):
        self.s = s
        self.vowels = set('аеёиоуыэюяАЕЁИОУЫЭЮЯ aeiouAEIOU')
        self.max_consonants = -1
        self.max_lexemes = []

    def is_vowel(self, c):
        return c in self.vowels

    def has_consecutive_vowels(self, seq):
        for i in range(len(seq) - 1):
            if self.is_vowel(seq[i]) and self.is_vowel(seq[i + 1]):
                return True
        return False

    def count_odd_positioned_consonants(self, seq):
        count = 0
        for i in range(0, len(seq), 2):
            if not self.is_vowel(seq[i]):
                count += 1
        return count

    def lexico_permute_string(self):
        a = sorted(self.s)
        n = len(a) - 1

        while True:
            if not self.has_consecutive_vowels(a):
                lexeme = ''.join(a)
                odd_positioned_consonants = self.count_odd_positioned_consonants(lexeme)
                if odd_positioned_consonants > self.max_consonants:
                    self.max_consonants = odd_positioned_consonants
                    self.max_lexemes = [lexeme]
                elif odd_positioned_consonants == self.max_consonants:
                    self.max_lexemes.append(lexeme)

            for j in range(n - 1, -1, -1):
                if a[j] < a[j + 1]:
                    break
            else:
                break

            v = a[j]
            for k in range(n, j, -1):
                if v < a[k]:
                    break

            a[j], a[k] = a[k], a[j]
            a[j + 1:] = a[j + 1:][::-1]

        return self.max_lexemes


class LexemeFinderApp(tk.Tk):
    def __init__(self):
        super().__init__()


        self.title("Lexeme Finder")
        self.geometry("400x500")


        self.input_label = ttk.Label(self, text="Введите слово (по умолчанию 'институт')")
        self.input_label.pack(anchor="n", pady= 8)

        self.default_text = tk.StringVar(value="институт")

        self.input_text = ttk.Entry(self, textvariable=self.default_text)
        self.input_text.pack(anchor="n", padx=8,)

        self.submit_button = ttk.Button(self, text="Найти лексемы", command=self.submit)
        self.submit_button.pack(anchor='n', padx=8, pady= 8)

        self.output_label = ttk.Label(self, text="Результат:")
        self.output_label.pack(anchor='n', padx=8,)

        self.text_frame = tk.Frame(self)
        self.text_frame.pack(anchor='n', padx=8, pady=8)

        self.scrollbar = ttk.Scrollbar(self.text_frame)
        self.output_text = tk.Text(self.text_frame, wrap=tk.WORD, width=40, height=40,yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.output_text.yview)

        self.output_text.pack(side=tk.LEFT, padx=0, pady=0)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)


    def submit(self):
        s = self.input_text.get()
        finder = LexemeFinder(s)
        lexemes = finder.lexico_permute_string()

        self.output_text.delete(1.0, tk.END)

        if finder.max_consonants == 0:
            self.output_text.insert(tk.END, "Лексем с согласными на нечетных местах не существует")
        else:
            self.output_text.insert(tk.END, "Лексемы с наибольшим числом согласных на нечетных местах:")
            for i, lexeme in enumerate(lexemes, start=1):
                self.output_text.insert(tk.END, f"\n{i}. {lexeme}")


if __name__ == "__main__":
    app = LexemeFinderApp()
    app.mainloop()
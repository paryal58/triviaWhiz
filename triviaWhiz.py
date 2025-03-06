import tkinter as tk
import random

"""
    Question Class
    Responsible to handle questions, the options and the correct answer
"""
class Question:
    def __init__(self, question, options, correct_answer):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer 

    def display(self):
        return self.question, self.options

    def is_correct(self, answer):
        return self.correct_answer == answer

"""
    Game Class
    Responsible to handle game logic, timer and tkinter window
"""
class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Trivia Whiz")
        self.root.geometry("500x550")
        self.questions = []
        self.score = 0
        self.current_question_index = 0
        self.lifelines = {"50:50": True,}
        self.lives = 3
        self.load_questions()
        self.create_widgets()  
        self.timer_started = False
        self.time_left = 30  

    def load_questions(self):
        try:
            with open("questions.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip() 
                    if line.startswith("#") or not line:
                        continue  
                    parts = line.split('|')
                    if len(parts) == 6:
                        question = parts[0]
                        options = parts[1:5]
                        correct_answer = int(parts[5]) 
                        self.questions.append(Question(question, options, correct_answer))
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.root.quit()  

    def create_widgets(self):
        self.question_label = tk.Label(self.root, text="", font=("Trebuchet", 18))
        self.question_label.pack(pady=20)
        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", width=30, height=2, fg="blue", command=lambda i=i: self.check_answer(i))
            button.pack(pady=5)
            self.option_buttons.append(button)

        self.score_label = tk.Label(self.root, text="Score: $0", font=("Trebuchet", 16))
        self.score_label.place(x=100, y= 300)

        self.lifeline_button = tk.Button(self.root, text="Use 50:50", width=10, height=2, command=self.use_lifeline)
        self.lifeline_button.place(x=100, y=400)

        self.timer_label = tk.Label(self.root, text="Time left: 30", font=("Helvetica", 16))
        self.timer_label.place(x=215, y= 300)

        self.lives_label = tk.Label(self.root, text="Lives: 3", font=("Helvetica", 16))
        self.lives_label.place(x=330, y= 300)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.result_label.place(x=110, y=350)

        self.next_button = tk.Button(self.root, text="Next Question", width=14, height=2, state=tk.DISABLED, command=self.next_question)
        self.next_button.place(x=240, y=400)

    def start(self):
        self.show_question()

    def show_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            question_text, options = question.display()
            self.question_label.config(text=question_text)
            for i, option in enumerate(options):
                self.option_buttons[i].config(text=option, state=tk.NORMAL)  
            self.result_label.config(text="")
            self.next_button.config(state=tk.DISABLED)
            if not self.timer_started:
                self.start_timer()
        else:
            self.end_game()

    def start_timer(self):
        self.timer_started = True
        self.time_left = 30 
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)  
        else:
            self.check_answer(None)  
            self.lives -= 1
            self.check_lives()

    def check_answer(self, selected_option):
        if selected_option is None:  
            selected_option = -1  
            self.lives -= 1
            self.lives_label.config(text=f"Lives: {self.lives}")
            self.check_lives()

        for button in self.option_buttons:
            button.config(state=tk.DISABLED)

        current_question = self.questions[self.current_question_index]
        if current_question.is_correct(selected_option + 1):  
            self.score += 1000  
            self.result_label.config(text=f"Well done! The answer {current_question.options[current_question.correct_answer - 1]} is correct", fg="green")
            self.time_left = 30 
        else:
            self.result_label.config(text=f"Incorrect! The correct answer was {current_question.options[current_question.correct_answer - 1]}", fg="red")
            self.lives -= 1
            self.lives_label.config(text=f"Lives: {self.lives}")
            self.check_lives()
        
        self.score_label.config(text=f"Score: ${self.score}")
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.show_question() 
        else:
            self.end_game()  

    def use_lifeline(self):
        if self.lifelines["50:50"]:
            print("Using 50:50 Lifeline...")
            current_question = self.questions[self.current_question_index]
            correct_answer_index = current_question.correct_answer - 1
            incorrect_answers = [i for i in range(4) if i != correct_answer_index]
            removed_answers = random.sample(incorrect_answers, 2)

            for i in range(4):
                if i not in removed_answers:
                    self.option_buttons[i].config(state=tk.NORMAL)
                else:
                    self.option_buttons[i].config(state=tk.DISABLED)

            self.lifelines["50:50"] = False
        else:
            self.result_label.config(text="You have already used your 50:50 lifeline.", fg="red")
    
    def check_lives(self):
        if self.lives <= 0:
            self.end_game()

    def end_game(self):
        self.result_label.config(text=f"Game Over! Final Score: ${self.score}", fg="blue")

        for button in self.option_buttons:
            button.config(state=tk.DISABLED)  

        self.next_button.config(state=tk.DISABLED) 
        self.root.after(1500, self.force_close)
        
    def force_close(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    game.start()  
    root.mainloop()

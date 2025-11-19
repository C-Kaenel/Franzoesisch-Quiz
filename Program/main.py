import os
from yaspin import yaspin
from cryptography.fernet import Fernet
import inquirer

# Quiz erstellen
def quizmaker():
    # Quiz Abfrage fertig
    global question_maker_file
    name = input("Bitte Namen des Quizes eingeben: ")
    quizcreate = "Nein"
    create = "nein"
    question_maker_file = []
    question_maker_string = ""

    while create == "nein":
        # Erste Quizfrage
        question_right = "Nein"
        while question_right == "Nein":
            question = input("Bitte die erste Quizfrage eingeben: ")
            answer_count = 1
            answers = ["", "", "", "", "", ""]
            right_answers = ["0", "0", "0", "0", "0", "0"]
            everything_right_answer = f"{question}\n"
            i = 0
            while answer_count <= 6:
                if i == 0:
                    answer = input(f"Bitte die {answer_count}. Antwortmöglichkeit eingeben (leer zum Beenden): ")
                    if answer == "":
                        i = 1
                    else:
                        answers[answer_count - 1] = answer
                        right = inquirer.list_input("Ist diese Antwort richtig?", choices=['Ja', 'Nein'])
                        if right == "Ja":
                            right_answers[answer_count - 1] = 1
                            everything_right_answer += f"Antwortmöglichkeit|{answer} Richtig|Ja\n"
                        else:
                            right_answers[answer_count - 1] = 0
                            everything_right_answer += f"Antwortmöglichkeit|{answer} Richtig|Nein\n"
                else:
                    answers[answer_count - 1] = ""
                answer_count += 1

            question_right = inquirer.list_input(f"{everything_right_answer}\nIst dies korrekt?", choices=["Ja", "Nein"])
            # bestätigte erste Frage in die Sammlung übernehmen
            for a, r in zip(answers, right_answers):
                if a:
                    question_maker_file.append((question, a, r))
            question_maker_string += f"{everything_right_answer}\n"

        # weitere Quizfragen
        while quizcreate == "Nein":
            question_right = "Nein"
            while question_right == "Nein":
                question = input("Bitte die nächste Quizfrage eingeben: ")
                answer_count = 1
                answers = ["", "", "", "", "", ""]
                right_answers = ["0", "0", "0", "0", "0", "0"]
                everything_right_answer = f"{question}\n"
                i = 0
                while answer_count <= 6:
                    if i == 0:
                        answer = input(f"Bitte die {answer_count}. Antwortmöglichkeit eingeben (leer zum Beenden): ")
                        if answer == "":
                            i = 1
                        else:
                            answers[answer_count - 1] = answer
                            right = inquirer.list_input("Ist diese Antwort richtig?", choices=['Ja', 'Nein'])
                            if right == "Ja":
                                right_answers[answer_count - 1] = 1
                                everything_right_answer += f"Antwortmöglichkeit|{answer} Richtig|Ja\n"
                            else:
                                right_answers[answer_count - 1] = 0
                                everything_right_answer += f"Antwortmöglichkeit|{answer} Richtig|Nein\n"
                    else:
                        answers[answer_count - 1] = ""
                    answer_count += 1

                question_right = inquirer.list_input(f"{everything_right_answer}\nIst dies korrekt?", choices=["Ja", "Nein"])
                for a, r in zip(answers, right_answers):
                    if a:
                        question_maker_file.append((question, a, r))
                question_maker_string += f"{everything_right_answer}\n"

            quizcreate = inquirer.list_input("Sind alle Quizfragen eingegeben?", choices=["Ja", "Nein"])

        create = inquirer.list_input(f"{question_maker_string}\nAlles richtig?", choices=["Ja", "Nein"])

    # Nur speichern, wenn bestätigt
    if create == "Ja":
        # Ordner erstellen
        folder_path = os.path.join(os.path.dirname(__file__), "output", name)
        os.makedirs(folder_path, exist_ok=True)

        # Schlüssel erzeugen und speichern
        key_path = os.path.join(folder_path, "key.key")
        key_maker = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key_maker)
        fer_maker = Fernet(key_maker)

        # Datei schreiben (verschlüsselt)
        path = os.path.join(folder_path, "quiz.txt")
        with open(path, "w", encoding="utf-8") as g:
            for question, answer, right_answer in question_maker_file:
                g.write(
                    fer_maker.encrypt(question.encode()).decode() + "|" +
                    fer_maker.encrypt(answer.encode()).decode() + "|" +
                    fer_maker.encrypt(str(right_answer).encode()).decode() + "\n"
                )

        print(f"\n Quiz '{name}' wurde erfolgreich erstellt!")
        print(f" Dateien gespeichert unter: {folder_path}\n")
    else:
        print("\n Erstellung abgebrochen. Es wurden keine Dateien gespeichert.\n")


def quizsolver():
    print(" Quiz lösen kommt bald...")


while True:
    MainMenu = inquirer.list_input(
        "Willkommen beim Quizer\nBitte Funktion Auswählen",
        choices=['Quiz Erstellen', 'Quiz Ausfüllen', 'Beenden']
    )
    if MainMenu == 'Quiz Erstellen':
        quizmaker()
    elif MainMenu == "Quiz Ausfüllen":
        quizsolver()
    else:
        break
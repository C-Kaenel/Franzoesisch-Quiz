import os
from fileinput import filename
import random
from yaspin import yaspin
from cryptography.fernet import Fernet
import inquirer
from fpdf import FPDF


# Quiz erstellen
def quizmaker():
    global question_maker_file
    print("\n=== Quiz-Erstellung ===")
    name = input("Bitte geben Sie den Namen des Quiz ein: ").strip()
    quizcreate = "NOK"
    create = "NOK"
    question_maker_file = []
    question_maker_string = ""

    while create == "NOK":
        # Erste Quizfrage
        question_right = "NOK"
        while question_right == "NOK":
            print("\n--- Erste Frage ---")
            question = input("Bitte geben Sie die erste Quizfrage ein: ").strip()
            answers = []
            everything_right_answer = f"{question}\n"

            # Antworten einsammeln (max. 6)
            answer_count = 1
            while answer_count <= 6:
                answer = input(f"Bitte geben Sie die {answer_count}. Antwortmöglichkeit ein (leer = keine weiteren Antworten): ").strip()
                if answer == "":
                    break
                answers.append(answer)
                answer_count += 1

            if not answers:
                print("Es muss mindestens eine Antwortmöglichkeit erfasst werden.")
                continue

            # Antworten mit Buchstaben anzeigen
            print("\nAntwortmöglichkeiten:")
            for idx, a in enumerate(answers):
                print(f"{chr(65 + idx)}: {a}")

            # Richtige Antworten per Buchstaben
            print("\nGeben Sie die Buchstaben der richtigen Antworten ein (z. B. AC).")
            print("Falls keine Antwort richtig ist, drücken Sie einfach Enter.")
            korrekt_input = input("Richtige Antworten: ").upper().replace(" ", "")

            right_answers = []
            for idx, a in enumerate(answers):
                letter = chr(65 + idx)
                if letter in korrekt_input:
                    right_answers.append(1)
                    everything_right_answer += f"Antwortmöglichkeit|{a} Richtig|Ja\n"
                else:
                    right_answers.append(0)
                    everything_right_answer += f"Antwortmöglichkeit|{a} Richtig|Nein\n"

            # Zusammenfassung bestätigen mit OK/NOK
            question_right = inquirer.list_input(
                f"\nZusammenfassung der erfassten Frage:\n\n{everything_right_answer}\nSind Frage und Antworten korrekt?",
                choices=["OK", "NOK"]
            )

            if question_right == "OK":
                # bestätigte Frage in die Sammlung übernehmen
                for a, r in zip(answers, right_answers):
                    if a:
                        question_maker_file.append((question, a, r))
                question_maker_string += f"{everything_right_answer}\n"

        # weitere Quizfragen
        while quizcreate == "NOK":
            question_right = "NOK"
            while question_right == "NOK":
                print("\n--- Weitere Frage ---")
                question = input("Bitte geben Sie die nächste Quizfrage ein: ").strip()
                answers = []
                everything_right_answer = f"{question}\n"

                answer_count = 1
                while answer_count <= 6:
                    answer = input(f"Bitte geben Sie die {answer_count}. Antwortmöglichkeit ein (leer = keine weiteren Antworten): ").strip()
                    if answer == "":
                        break
                    answers.append(answer)
                    answer_count += 1

                if not answers:
                    print("Es muss mindestens eine Antwortmöglichkeit erfasst werden.")
                    continue

                print("\nAntwortmöglichkeiten:")
                for idx, a in enumerate(answers):
                    print(f"{chr(65 + idx)}: {a}")

                print("\nGeben Sie die Buchstaben der richtigen Antworten ein (z. B. AC).")
                print("Falls keine Antwort richtig ist, drücken Sie einfach Enter.")
                korrekt_input = input("Richtige Antworten: ").upper().replace(" ", "")

                right_answers = []
                for idx, a in enumerate(answers):
                    letter = chr(65 + idx)
                    if letter in korrekt_input:
                        right_answers.append(1)
                        everything_right_answer += f"Antwortmöglichkeit|{a} Richtig|Ja\n"
                    else:
                        right_answers.append(0)
                        everything_right_answer += f"Antwortmöglichkeit|{a} Richtig|Nein\n"

                question_right = inquirer.list_input(
                    f"\nZusammenfassung der erfassten Frage:\n\n{everything_right_answer}\nSind Frage und Antworten korrekt?",
                    choices=["OK", "NOK"]
                )

                if question_right == "OK":
                    for a, r in zip(answers, right_answers):
                        if a:
                            question_maker_file.append((question, a, r))
                    question_maker_string += f"{everything_right_answer}\n"

            quizcreate = inquirer.list_input(
                "Sind alle Fragen für dieses Quiz erfasst?",
                choices=["OK", "NOK"]
            )

        create = inquirer.list_input(
            f"\nGesamte Quiz-Zusammenfassung:\n\n{question_maker_string}\nMöchten Sie dieses Quiz so speichern?",
            choices=["OK", "NOK"]
        )

    # Nur speichern, wenn bestätigt
    if create == "OK":
        print("\nSpeichere Quizdaten...")
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

        print(f"\nDas Quiz '{name}' wurde erfolgreich erstellt.")
        print(f"Die Dateien wurden im Ordner gespeichert: {folder_path}\n")
    else:
        print("\nDie Erstellung des Quiz wurde abgebrochen. Es wurden keine Dateien gespeichert.\n")


def quizsolver():
    print("\n=== Quiz ausfüllen ===")
    nameNutzer = input("Bitte geben Sie Ihren Namen ein: ").strip()

    base_dir = os.path.dirname(__file__)
    output_dir = os.path.join(base_dir, "output")

    # Prüfen, ob überhaupt Quizzes existieren
    if not os.path.isdir(output_dir):
        print("Es wurden noch keine Quiz erstellt.")
        return

    quizzes = [d for d in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, d))]
    if not quizzes:
        print("Es wurden noch keine Quiz erstellt.")
        return

    quiz = inquirer.list_input(
        "Bitte wählen Sie ein Quiz aus:",
        choices=quizzes
    )

    print(f"\nLade das Quiz '{quiz}'...")

    folder_path = os.path.join(output_dir, quiz)
    key_path = os.path.join(folder_path, "key.key")
    quiz_path = os.path.join(folder_path, "quiz.txt")

    # Schlüssel laden
    with open(key_path, "rb") as kf:
        key = kf.read()
    fernet = Fernet(key)

    # verschlüsselte Fragen laden
    with open(quiz_path, "r", encoding="utf-8") as file:
        questions = file.readlines()

    random.shuffle(questions)

    # Fragen strukturieren: frage -> liste von (antwort, ist_richtig)
    quiz_data = {}

    for each_question in questions:
        each_question = each_question.strip()
        if not each_question:
            continue

        enc_q, enc_a, enc_r = each_question.split("|")

        frage = fernet.decrypt(enc_q.encode()).decode()
        antwort = fernet.decrypt(enc_a.encode()).decode()
        richtig_flag = fernet.decrypt(enc_r.encode()).decode()  # "0" oder "1"
        ist_richtig = (richtig_flag == "1")

        quiz_data.setdefault(frage, []).append((antwort, ist_richtig))

    # Quiz durchführen – mit Mehrfachauswahl und 0-Punkte-Regel
    score = 0
    total = 0
    user_results = []

    print("\nDie Fragen werden nun gestellt. Sie können bei jeder Frage eine oder mehrere Antworten auswählen.")

    for frage, antworten in quiz_data.items():
        print("\nFrage:")
        print(frage)
        random.shuffle(antworten)

        # Antworten anzeigen
        for idx, (antwort, _) in enumerate(antworten, start=1):
            print(f"{idx}. {antwort}")

        # Mehrfachauswahl einlesen
        while True:
            auswahl = input("Bitte geben Sie die Nummer(n) Ihrer Antwort(en) ein (z. B. 1,3): ").replace(" ", "")
            if auswahl == "":
                print("Bitte geben Sie mindestens eine Antwortnummer ein.")
                continue

            try:
                ausgewaehlt = [int(x) for x in auswahl.split(",")]
                if all(1 <= x <= len(antworten) for x in ausgewaehlt):
                    break
            except ValueError:
                pass

            print("Ungültige Eingabe. Beispiel für eine gültige Eingabe: 1,2")

        total += 1

        # richtige Antworten ermitteln (Index 1-basiert)
        richtige = [i + 1 for i, (_, r) in enumerate(antworten) if r]

        # Punktelogik:
        # 1 Punkt nur, wenn die Menge der gewählten Antworten genau der Menge der richtigen entspricht
        if set(ausgewaehlt) == set(richtige):
            punkt = 1
            print("Ihre Antwort ist richtig.")
        else:
            punkt = 0
            print("Ihre Antwort ist falsch.")

        score += punkt

        # Text der Antworten heraussuchen
        gewaehlte_antworten = [antworten[i - 1][0] for i in ausgewaehlt]
        richtige_antworten = [antworten[i - 1][0] for i in richtige]

        user_results.append({
            "frage": frage,
            "gewaehlt": gewaehlte_antworten,
            "ist_richtig": punkt == 1,
            "richtige_antworten": richtige_antworten
        })

    if total == 0:
        print("Dieses Quiz enthält keine Fragen.")
        return

    prozent = score / total * 100

    # Offizielle Schweizer Note (linear 1–6)
    offizielle_note = round(1 + 5 * (score / total), 1)

    # Pädagogische 50%-Grenznote
    if prozent >= 50:
        paed_note = 4.0 + (prozent - 50) * 0.04
    else:
        paed_note = 4.0 - (50 - prozent) * 0.06
    paed_note = round(paed_note, 1)

    print(f"\n{nameNutzer}, Sie haben {score} von {total} Fragen richtig beantwortet.")
    print(f"Prozentuale Punktzahl: {prozent:.1f} %")
    print(f"Offizielle Note: {offizielle_note}")
    print(f"Pädagogische Note (50%-Regel): {paed_note}")

    # Nur PDF-Report erzeugen
    print("\nErstelle PDF-Ergebnisbericht...")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Quiz-Ergebnis", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Name: {nameNutzer}", ln=True)
    pdf.cell(0, 8, f"Quiz: {quiz}", ln=True)
    pdf.cell(0, 8, f"Punktzahl: {score} / {total}", ln=True)
    pdf.cell(0, 8, f"Prozentuale Punktzahl: {prozent:.1f} %", ln=True)
    pdf.cell(0, 8, f"Offizielle Note: {offizielle_note}", ln=True)
    pdf.cell(0, 8, f"Pädagogische Note (50%-Regel): {paed_note}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Details zu den Fragen:", ln=True)

    pdf.set_font("Arial", "", 11)

    # verfügbare Seitenbreite berechnen
    page_width = pdf.w - 2 * pdf.l_margin

    for res in user_results:
        pdf.ln(2)
        pdf.set_x(pdf.l_margin)

        pdf.multi_cell(page_width, 6, f"Frage: {res['frage']}")
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(page_width, 6, "Ihre Antwort(en): " + ", ".join(res["gewaehlt"]))
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(page_width, 6, "Richtige Antwort(en): " + ", ".join(res['richtige_antworten']))
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(page_width, 6, "Ergebnis: " + ("Richtig" if res["ist_richtig"] else "Falsch"))

    report_path = os.path.join(folder_path, f"{nameNutzer}_{quiz}_Report.pdf")
    pdf.output(report_path)

    print("\nDer PDF-Ergebnisbericht wurde erfolgreich erstellt.")
    print(f"Datei gespeichert unter: {report_path}")


while True:
    MainMenu = inquirer.list_input(
        "\nWillkommen beim Quiz-Programm\nBitte wählen Sie eine Funktion:",
        choices=['Quiz erstellen', 'Quiz ausfüllen', 'Beenden']
    )
    if MainMenu == 'Quiz erstellen':
        quizmaker()
    elif MainMenu == "Quiz ausfüllen":
        quizsolver()
    else:
        print("\nProgramm wird beendet. Auf Wiedersehen.")
        break

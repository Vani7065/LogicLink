import spacy
from sympy import symbols
from sympy.logic.boolalg import Or, And, Not, Implies, Equivalent
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Load spaCy model for NLP
nlp = spacy.load('en_core_web_sm')

# Function to detect logical structure from a sentence
def detect_logic(sentence):
    lower_sentence = sentence.lower()
    print(f"Debug: Analyzing sentence: {lower_sentence}")  # Debug print

    # Improved logic detection
    if "if and only if" in lower_sentence:
        return "Biconditional"
    elif "if" in lower_sentence and "then" in lower_sentence:
        return "Conditional"
    elif "and" in lower_sentence:
        return "Conjunction"
    elif "or" in lower_sentence:
        return "Disjunction"
    elif "not" in lower_sentence:
        return "Negation"
    elif "neither" in lower_sentence and "nor" in lower_sentence:
        return "Neither/Nor"
    elif "is" in lower_sentence or "are" in lower_sentence:
        return "Assertion"
    else:
        return "Unknown"

# Function to convert sentence into a logic expression
def convert_to_logic(sentence):
    logic_type = detect_logic(sentence)
    symbols_dict = {}
    var_counter = 1
    
    # Extracting variables from the sentence
    doc = nlp(sentence)
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN", "ADJ"]:  # Including adjectives for more flexibility
            symbols_dict[f'Var{var_counter}'] = symbols(token.text)
            var_counter += 1

    # Logic conversion based on detected type
    if logic_type == "Conditional" and len(symbols_dict) >= 2:
        return Implies(symbols_dict['Var1'], symbols_dict['Var2']), f"Detected: Conditional Logic (Var1 → Var2)", f"If {symbols_dict['Var1']}, then {symbols_dict['Var2']}."
    elif logic_type == "Conjunction":
        return And(*symbols_dict.values()), f"Detected: Conjunction (Var1 ∧ Var2 ∧ ...)", " ∧ ".join(symbols_dict.keys())
    elif logic_type == "Disjunction":
        return Or(*symbols_dict.values()), f"Detected: Disjunction (Var1 ∨ Var2 ∨ ...)", " ∨ ".join(symbols_dict.keys())
    elif logic_type == "Negation" and 'Var1' in symbols_dict:
        return Not(symbols_dict['Var1']), f"Detected: Negation (¬{symbols_dict['Var1']})", f"Not {symbols_dict['Var1']}."
    elif logic_type == "Biconditional" and len(symbols_dict) >= 2:
        return Equivalent(symbols_dict['Var1'], symbols_dict['Var2']), f"Detected: Biconditional Logic (Var1 ↔ Var2)", f"{symbols_dict['Var1']} if and only if {symbols_dict['Var2']}."
    elif logic_type == "Neither/Nor":
        return Not(Or(*symbols_dict.values())), f"Detected: Neither/Nor (¬(Var1 ∨ Var2))", "Neither " + " nor ".join(symbols_dict.keys()) + "."
    elif logic_type == "Assertion" and len(symbols_dict) >= 2:
        return Equivalent(symbols_dict['Var1'], symbols_dict['Var2']), f"Detected: Assertion (Var1 = Var2)", f"{symbols_dict['Var1']} is {symbols_dict['Var2']}."
    else:
        return None, "Logic type could not be detected or insufficient variables.", ""

# Function to handle the logic conversion when the button is pressed
def process_sentence():
    sentence = input_entry.get()
    if not sentence:
        messagebox.showwarning("Input Error", "Please enter a sentence!")
        return

    logic_expr, message, converted_sentence = convert_to_logic(sentence)
    logic_type_label.config(text=message)

    if logic_expr:
        converted_label.config(text=f"Converted to: {logic_expr}")
        converted_sentence_label.config(text=f"Converted sentence: {converted_sentence}")
    else:
        converted_label.config(text="")
        converted_sentence_label.config(text="")

# Function to clear the input and outputs
def clear_input():
    input_entry.delete(0, tk.END)
    logic_type_label.config(text="")
    converted_label.config(text="")
    converted_sentence_label.config(text="")

# Setting up the GUI using Tkinter
root = tk.Tk()
root.title("AI Logic Converter")
root.geometry("600x500")

# Set the background image
try:
    background_img = Image.open(r"C:\Users\Vani krishna\OneDrive\Desktop\AI PROJECT\background.jpg")  # Update this path if needed
    background_img = background_img.resize((600, 500), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(background_img)

    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Error loading background image: {e}")  # Debugging image loading

# Fonts and Colors
header_font = ("Helvetica", 16, "bold")
subheader_font = ("Helvetica", 12, "italic")
button_font = ("Helvetica", 10, "bold")
bg_color = "#F0F4FF"  # Light Blue
btn_color = "#3D85C6"  # Dark Blue
text_color = "#333333"  # Dark Gray

# Input section
input_label = tk.Label(root, text="Enter a sentence:", font=header_font, bg=bg_color, fg=text_color)
input_label.pack(pady=20)

input_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
input_entry.pack(pady=10)

# Button to process the sentence with a modern look
process_button = tk.Button(root, text="Convert", font=button_font, bg=btn_color, fg="white", command=process_sentence)
process_button.pack(pady=10)

# Label to display the detected logic type
logic_type_label = tk.Label(root, text="", font=header_font, bg=bg_color, fg=text_color)
logic_type_label.pack(pady=10)

# Label to display the converted logical expression
converted_label = tk.Label(root, text="", font=subheader_font, bg=bg_color, fg=text_color)
converted_label.pack(pady=10)

# Label to display the converted sentence
converted_sentence_label = tk.Label(root, text="", font=subheader_font, bg=bg_color, fg=text_color)
converted_sentence_label.pack(pady=10)

# Button to clear the input
clear_button = tk.Button(root, text="Clear", font=button_font, bg=btn_color, fg="white", command=clear_input)
clear_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

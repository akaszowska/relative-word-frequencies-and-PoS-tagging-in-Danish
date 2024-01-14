# ### 

# The following code creates an annotation GUI. 

# Purpose:
#     Annotating individual words in text with part of speech.
    
# Functionality:
#     The GUI displays default text to be annotated. The user can use < > arrows to move between words to annotate.
#     Word currently annotated will be highlighted and showed as a header above list box.
#     List box will contain all possible options for part of speech, per reference corpus. 
#     Comment box allows user to type relevant comments.
#     Press "Add to Output" button to add highlighted option (from listbox) and content of comment to output file.
#     Press "Save file" to save output file. 
#     GUI requires annotation of every single word, even if only one option is listed in corpus.
    
#     Please note that:
#         In order to add highlighted choice and/or comments to output file, you MUST press "Add to Output"
#         If you annotate the same word twice, BOTH versions will be added to output file. New annotation of already annotated word does not override previous annotation.
#         If you do not highlight a choice (or there is no choice) and press "Add to Output", the output file will contain an empty line. 
        
# Input files:
#     text_file: original text  in .txt format without headers
#     identified_file: {file_name}_identifiedWords_{version}.txt 
#         identified file contains words cross-referenced with a relevant corpus of relative frequencies
#         generated using analyze_text_FLEXIKON.py or analyze_text_NLP.py    
    
# Output files:
#     output_file: {file_name}_{version}_output.csv
#         output file with a list of all identified words, annotated for part of speech, with relative frequencies
#     summary_file: {file_name}_{version}_pos_annotation_summary.txt
#         summary file with annotation details
    
# @AUTHOR: Aleksandra Kaszowska
# 02/10/2023

# ###


# %%% set up file names and version here

text_file = 'SAMPLE_TEXT.txt'
version = 'FLEXIKON' # 'NLP' or 'FLEXIKON' depending on previous step

# %%%

file_name = text_file[:-4]
identified_file = f'{file_name}_identifiedWords_{version}.txt'
output_file = f'{file_name}_{version}_output.csv'
summary_file = f'{file_name}_{version}_pos_annotation_summary.txt'

import tkinter as tk
from tkinter import messagebox
import csv
import string
from datetime import datetime

# Read the text file
with open(text_file, "r", encoding='utf-8') as f:
    content = f.read().strip()
wordList = content.split()
words = []

for word in wordList:
    for punctuation in string.punctuation:
        word = word.replace(punctuation,'')
    words.append(word.lower())
    
words2 = [(word, idx) for idx, word in enumerate(content.split())]

# Read the identified words file
word_data = {}
with open(identified_file, "r", encoding='utf-8') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        word = row[1]
        if word not in word_data:
            word_data[word] = []
        word_data[word].append(row)

selected_rows = []
current_index = 0

def display_matches():
    word = words[current_index]
    listbox.delete(0, tk.END)
    for row in word_data.get(word, []):
        listbox.insert(tk.END, ', '.join(row))
    highlight_word()
                
def highlight_word():
    word, idx = words2[current_index]
    text_label.tag_remove("highlight", "1.0", tk.END)
    start_pos = sum(len(w) + 1 for w, _ in words2[:idx])
    start_index = "1.0 + {}c".format(start_pos)
    end_index = "1.0 + {}c".format(start_pos + len(word))
    text_label.tag_add("highlight", start_index, end_index)        

def add_comment():
    comment = comment_text.get("1.0", tk.END).strip()  # Extract comment from Text widget
    selected_row = None

    if listbox.curselection():
        selected_row = listbox.get(listbox.curselection()[0])
    
    if selected_row:
        row_data = []
        row_data.append(current_index+1)
        for item in selected_row.split(', '):
            row_data.append(item)
        row_data.append(comment)
        selected_rows.append(row_data)
    elif comment:
        selected_rows.append([(current_index+1),"", words2[current_index][0], "", "", comment])
    move_word(1)
    
    comment_text.delete("1.0", tk.END)  # Clear the Text widget

def move_word(direction):
    global current_index
    current_index += direction
    if current_index < 0:
        current_index = 0
    elif current_index >= len(words):
        current_index = len(words) - 1

    word_label.config(text=words[current_index])
    display_matches()

def save_to_file():
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        for row in selected_rows:
            writer.writerow(row)
    messagebox.showinfo("Success", f"Saved file as {file_name}_{version}_output.csv")
    
root = tk.Tk()

text_label = tk.Text(root, wrap=tk.WORD, height=15, bg="light gray", fg="black")
text_label.insert(tk.END, content)
text_label.config(state=tk.DISABLED, font=("Arial", 12))
text_label.pack(pady=10)
text_label.tag_configure("highlight", background="yellow")

word_label = tk.Label(root, text=wordList[current_index], font=("Arial", 12, "bold"))
word_label.pack(pady=10)

left_button = tk.Button(root, text="<", command=lambda: move_word(-1))
left_button.pack(side=tk.LEFT, padx=20)

right_button = tk.Button(root, text=">", command=lambda: move_word(1))
right_button.pack(side=tk.RIGHT, padx=20)

listbox = tk.Listbox(root, width=50, height=10)
listbox.pack(pady=10)

# Entry for user to type in comments
comment_label = tk.Label(root, text="Your comment:", font=("Arial", 10))
comment_label.pack(pady=5)
comment_text = tk.Text(root, wrap=tk.WORD, height=3, width=50)
comment_text.config(takefocus=0)  # Ensure the Text widget doesn't trap focus
comment_text.pack(pady=5)

comment_button = tk.Button(root, text="Add to Output", command=add_comment)
comment_button.pack(pady=10)

save_button = tk.Button(root, text="Save File", command=save_to_file)
save_button.pack(pady=10)

# Hotkey bindings
root.bind('<Left>', lambda e: move_word(-1))
root.bind('<Right>', lambda e: move_word(1))
root.bind('<Return>', lambda e: add_comment())
root.bind('<Control-s>', lambda e: save_to_file())
root.bind('2', lambda e: comment_text.focus_set())
root.bind('1', lambda e: listbox.focus_set())

display_matches()

root.mainloop()

# generate summary file
with open(summary_file, 'w') as file:
    file.write(f'original text analyzed: {text_file}\n')
    file.write(f'output file: {file_name}_{version}_output.csv\n')
        
    now = datetime.now()
    format_date = now.strftime("%A, %B %d, %Y - %H:%M:%S")
        
    file.write(f'annotation conducted on: {format_date}\n') 
    file.write('the following annotation was completed manually on all words in the source text.')

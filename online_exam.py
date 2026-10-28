import tkinter as tk
from tkinter import messagebox
import time

# ============================================================
# ONLINE EXAM MODULE - DSA EDITION
# Built with Python + Tkinter. No database or extra packages.
# Demo admin login: admin / admin123
# ============================================================

APP_BG = "#0B1220"
PANEL = "#131F33"
PANEL_2 = "#1A2942"
ACCENT = "#22D3C5"
ACCENT_DARK = "#0F766E"
WHITE = "#F8FAFC"
MUTED = "#A7B4C8"
GREEN = "#34D399"
RED = "#FB7185"
YELLOW = "#FBBF24"

QUESTIONS = [
    {
        "question": "Which data structure follows the LIFO principle?",
        "options": ["Queue", "Stack", "Linked List", "Graph"],
        "answer": 1,
        "explanation": "A stack follows Last In, First Out (LIFO). The most recently added item is removed first."
    },
    {
        "question": "Which data structure follows the FIFO principle?",
        "options": ["Stack", "Tree", "Queue", "Heap"],
        "answer": 2,
        "explanation": "A queue follows First In, First Out (FIFO). The earliest inserted item is removed first."
    },
    {
        "question": "What is the time complexity of binary search on a sorted array?",
        "options": ["O(n)", "O(log n)", "O(n²)", "O(1) always"],
        "answer": 1,
        "explanation": "Binary search halves the remaining search space each step, so its time complexity is O(log n)."
    },
    {
        "question": "Which data structure is commonly used for function-call management?",
        "options": ["Stack", "Queue", "Graph", "Hash table"],
        "answer": 0,
        "explanation": "Function calls and their local contexts are managed using a call stack."
    },
    {
        "question": "In a singly linked list, each node normally stores data and what else?",
        "options": ["Two parent nodes", "A pointer to the next node", "A sorted array", "A hash value only"],
        "answer": 1,
        "explanation": "A singly linked-list node stores its data and a reference/pointer to the next node."
    },
    {
        "question": "Which traversal of a Binary Search Tree visits keys in sorted order?",
        "options": ["Preorder", "Postorder", "Inorder", "Level order"],
        "answer": 2,
        "explanation": "Inorder traversal visits left subtree, node, then right subtree; in a BST this produces sorted keys."
    },
    {
        "question": "Which data structure is most suitable for a priority queue?",
        "options": ["Heap", "Stack only", "Singly linked list only", "Circular array only"],
        "answer": 0,
        "explanation": "A heap supports efficient access to the highest- or lowest-priority item."
    },
    {
        "question": "What is the average-case lookup time of a well-designed hash table?",
        "options": ["O(n²)", "O(log n)", "O(1)", "O(n log n)"],
        "answer": 2,
        "explanation": "A well-designed hash table provides average-case lookup close to O(1), though worst-case lookup can be O(n)."
    },
    {
        "question": "Which algorithmic technique explores a graph level by level?",
        "options": ["Depth-First Search (DFS)", "Breadth-First Search (BFS)", "Binary search", "Selection sort"],
        "answer": 1,
        "explanation": "BFS explores all nearby vertices level by level and commonly uses a queue."
    },
    {
        "question": "What is the worst-case time complexity of Bubble Sort?",
        "options": ["O(log n)", "O(n)", "O(n log n)", "O(n²)"],
        "answer": 3,
        "explanation": "Bubble Sort can compare adjacent elements across repeated passes, giving O(n²) worst-case time."
    },
]


class OnlineExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ExamNova | Online Exam Module")
        self.root.geometry("1080x720")
        self.root.minsize(900, 620)
        self.root.configure(bg=APP_BG)
        self.root.option_add("*Font", ("Segoe UI", 10))

        self.student_name = ""
        self.reg_no = ""
        self.answers = {}
        self.current_question = 0
        self.seconds_left = 15 * 60
        self.timer_job = None
        self.results = []
        self.exam_active = False

        self.show_home()

    def clear(self):
        if self.timer_job:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, bg=ACCENT, fg=APP_BG, width=None):
        return tk.Button(
            parent, text=text, command=command, bg=bg, fg=fg,
            activebackground=ACCENT_DARK, activeforeground=WHITE,
            relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI Semibold", 10), padx=18, pady=12,
            width=width
        )

    def label(self, parent, text, size=11, color=WHITE, bold=False, **kwargs):
        return tk.Label(
            parent, text=text, bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color, font=("Segoe UI", size, "bold" if bold else "normal"),
            **kwargs
        )

    def top_bar(self, subtitle="YOUR SMART ASSESSMENT SPACE"):
        bar = tk.Frame(self.root, bg=APP_BG)
        bar.pack(fill="x", padx=34, pady=(22, 10))
        logo = tk.Frame(bar, bg=ACCENT, width=44, height=44)
        logo.pack(side="left")
        logo.pack_propagate(False)
        tk.Label(logo, text="EN", bg=ACCENT, fg=APP_BG,
                 font=("Segoe UI Black", 15)).pack(expand=True)
        titlebox = tk.Frame(bar, bg=APP_BG)
        titlebox.pack(side="left", padx=12)
        self.label(titlebox, "EXAMNOVA", 16, WHITE, True).pack(anchor="w")
        self.label(titlebox, subtitle, 8, MUTED, True).pack(anchor="w")
        self.label(bar, "●  SYSTEM READY", 9, GREEN, True).pack(side="right", pady=10)

    def show_home(self):
        self.clear()
        self.top_bar()
        body = tk.Frame(self.root, bg=APP_BG)
        body.pack(fill="both", expand=True, padx=34, pady=18)

        hero = tk.Frame(body, bg=PANEL, padx=34, pady=30)
        hero.pack(fill="x")
        self.label(hero, "DSA KNOWLEDGE CHALLENGE", 10, ACCENT, True).pack(anchor="w")
        self.label(hero, "Think fast. Solve smart.", 30, WHITE, True).pack(anchor="w", pady=(9, 4))
        self.label(hero, "Test your Data Structures & Algorithms skills with 10 carefully selected MCQs.",
                   12, MUTED).pack(anchor="w")
        stats = tk.Frame(hero, bg=PANEL)
        stats.pack(anchor="w", pady=(22, 0))
        for number, caption in [("10", "QUESTIONS"), ("15 MIN", "TIME LIMIT"), ("100", "TOTAL POINTS")]:
            tile = tk.Frame(stats, bg=PANEL_2, padx=18, pady=12)
            tile.pack(side="left", padx=(0, 10))
            self.label(tile, number, 16, ACCENT, True, bg=PANEL_2).pack(anchor="w")
            self.label(tile, caption, 8, MUTED, True, bg=PANEL_2).pack(anchor="w")

        cards = tk.Frame(body, bg=APP_BG)
        cards.pack(fill="both", expand=True, pady=18)
        student = tk.Frame(cards, bg=PANEL, padx=24, pady=24)
        student.pack(side="left", fill="both", expand=True, padx=(0, 9))
        admin = tk.Frame(cards, bg=PANEL, padx=24, pady=24)
        admin.pack(side="left", fill="both", expand=True, padx=(9, 0))

        self.label(student, "01  /  STUDENT PORTAL", 9, ACCENT, True).pack(anchor="w")
        self.label(student, "Ready for the challenge?", 18, WHITE, True).pack(anchor="w", pady=(12, 6))
        self.label(student, "Enter your details, answer the questions, and review the correct answers after submission.",
                   10, MUTED, wraplength=390, justify="left").pack(anchor="w", pady=(0, 20))
        self.make_button(student, "Start Examination  →", self.show_student_login).pack(anchor="w")

        self.label(admin, "02  /  ADMIN CONSOLE", 9, YELLOW, True).pack(anchor="w")
        self.label(admin, "Track performance", 18, WHITE, True).pack(anchor="w", pady=(12, 6))
        self.label(admin, "View exam attempts and scores recorded during this application session.",
                   10, MUTED, wraplength=390, justify="left").pack(anchor="w", pady=(0, 20))
        self.make_button(admin, "Administrator Login  →", self.show_admin_login,
                         bg=YELLOW, fg=APP_BG).pack(anchor="w")

        self.label(body, "BUILT FOR LEARNING  •  DSA BASICS  •  INSTANT ANSWER REVIEW",
                   8, MUTED, True).pack(anchor="center", pady=(2, 0))

    def show_student_login(self):
        self.clear()
        self.top_bar("STUDENT ACCESS")
        outer = tk.Frame(self.root, bg=APP_BG)
        outer.pack(expand=True)
        card = tk.Frame(outer, bg=PANEL, padx=42, pady=34)
        card.pack()
        self.label(card, "WELCOME, LEARNER", 9, ACCENT, True).pack(anchor="w")
        self.label(card, "Let's get you started.", 24, WHITE, True).pack(anchor="w", pady=(8, 4))
        self.label(card, "Fill in your details to begin the DSA exam.", 10, MUTED).pack(anchor="w", pady=(0, 22))

        self.label(card, "FULL NAME", 9, MUTED, True).pack(anchor="w", pady=(0, 6))
        self.name_entry = tk.Entry(card, font=("Segoe UI", 12), bg=PANEL_2, fg=WHITE,
                                   insertbackground=WHITE, relief="flat", width=36)
        self.name_entry.pack(ipady=10, pady=(0, 16))
        self.label(card, "REGISTRATION NUMBER", 9, MUTED, True).pack(anchor="w", pady=(0, 6))
        self.reg_entry = tk.Entry(card, font=("Segoe UI", 12), bg=PANEL_2, fg=WHITE,
                                  insertbackground=WHITE, relief="flat", width=36)
        self.reg_entry.pack(ipady=10, pady=(0, 22))
        row = tk.Frame(card, bg=PANEL)
        row.pack(fill="x")
        self.make_button(row, "← Home", self.show_home, bg=PANEL_2, fg=WHITE).pack(side="left")
        self.make_button(row, "Begin Exam  →", self.begin_exam).pack(side="right")
        self.name_entry.focus_set()

    def begin_exam(self):
        name = self.name_entry.get().strip()
        reg = self.reg_entry.get().strip()
        if not name or not reg:
            messagebox.showwarning("Missing details", "Please enter both your name and registration number.")
            return
        self.student_name, self.reg_no = name, reg
        self.answers = {}
        self.current_question = 0
        self.seconds_left = 15 * 60
        self.exam_active = True
        self.show_exam()

    def show_exam(self):
        self.clear()
        self.exam_active = True
        self.top_bar("DSA EXAMINATION  /  10 QUESTIONS")
        header = tk.Frame(self.root, bg=APP_BG)
        header.pack(fill="x", padx=34, pady=(8, 14))
        self.label(header, f"Candidate: {self.student_name}  •  ID: {self.reg_no}", 10, MUTED).pack(side="left")
        self.timer_label = self.label(header, "15:00", 13, YELLOW, True)
        self.timer_label.pack(side="right")
        self.progress_label = self.label(header, "QUESTION 1 OF 10", 9, ACCENT, True)
        self.progress_label.pack(side="right", padx=20)

        self.progress_canvas = tk.Canvas(self.root, height=5, bg=PANEL_2, highlightthickness=0)
        self.progress_canvas.pack(fill="x", padx=34)
        self.progress_bar = self.progress_canvas.create_rectangle(0, 0, 0, 5, fill=ACCENT, width=0)

        self.exam_area = tk.Frame(self.root, bg=APP_BG)
        self.exam_area.pack(fill="both", expand=True, padx=34, pady=18)
        self.render_question()
        self.update_timer()

    def render_question(self):
        for widget in self.exam_area.winfo_children():
            widget.destroy()
        q = QUESTIONS[self.current_question]
        self.progress_label.config(text=f"QUESTION {self.current_question + 1:02d} OF {len(QUESTIONS)}")
        self.progress_canvas.update_idletasks()
        width = max(self.progress_canvas.winfo_width(), 100)
        amount = width * (self.current_question + 1) / len(QUESTIONS)
        self.progress_canvas.coords(self.progress_bar, 0, 0, amount, 5)

        card = tk.Frame(self.exam_area, bg=PANEL, padx=28, pady=25)
        card.pack(fill="both", expand=True)
        self.label(card, f"QUESTION {self.current_question + 1:02d}", 9, ACCENT, True).pack(anchor="w")
        self.label(card, q["question"], 19, WHITE, True, wraplength=850,
                   justify="left").pack(anchor="w", pady=(12, 22))

        self.choice_var = tk.IntVar(value=self.answers.get(self.current_question, -1))
        self.option_buttons = []
        for i, option in enumerate(q["options"]):
            selected = self.choice_var.get() == i
            opt = tk.Radiobutton(
                card, text=f"  {chr(65+i)}.   {option}", variable=self.choice_var, value=i,
                command=lambda idx=i: self.save_answer(idx),
                indicatoron=0, anchor="w", padx=15, pady=13,
                bg=ACCENT_DARK if selected else PANEL_2, fg=WHITE,
                selectcolor=ACCENT_DARK, activebackground=ACCENT_DARK,
                activeforeground=WHITE, relief="flat", bd=0,
                font=("Segoe UI", 11), cursor="hand2"
            )
            opt.pack(fill="x", pady=5)
            self.option_buttons.append(opt)

        nav = tk.Frame(self.exam_area, bg=APP_BG)
        nav.pack(fill="x", pady=(14, 0))
        self.make_button(nav, "← Previous", self.previous_question,
                         bg=PANEL_2, fg=WHITE).pack(side="left")
        answered = len(self.answers)
        self.label(nav, f"{answered} / {len(QUESTIONS)} answered", 10, MUTED).pack(side="left", padx=18, pady=12)
        if self.current_question == len(QUESTIONS) - 1:
            self.make_button(nav, "Submit Exam  ✓", self.confirm_submit,
                             bg=GREEN, fg=APP_BG).pack(side="right")
        else:
            self.make_button(nav, "Next Question  →", self.next_question).pack(side="right")

    def save_answer(self, idx):
        self.answers[self.current_question] = idx
        for i, button in enumerate(self.option_buttons):
            button.config(bg=ACCENT_DARK if i == idx else PANEL_2)
        # Refresh answer count without rebuilding the question.
        for widget in self.exam_area.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label) and "answered" in str(child.cget("text")):
                        child.config(text=f"{len(self.answers)} / {len(QUESTIONS)} answered")

    def previous_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.render_question()

    def next_question(self):
        if self.current_question < len(QUESTIONS) - 1:
            self.current_question += 1
            self.render_question()

    def update_timer(self):
        if not self.exam_active:
            return
        mins, secs = divmod(self.seconds_left, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        if self.seconds_left <= 60:
            self.timer_label.config(fg=RED)
        if self.seconds_left <= 0:
            self.exam_active = False
            messagebox.showinfo("Time is up", "The exam time has ended. Your answers will be submitted now.")
            self.finish_exam()
            return
        self.seconds_left -= 1
        self.timer_job = self.root.after(1000, self.update_timer)

    def confirm_submit(self):
        unanswered = len(QUESTIONS) - len(self.answers)
        prompt = "Submit your exam now?"
        if unanswered:
            prompt += f"\n\nYou have {unanswered} unanswered question(s)."
        if messagebox.askyesno("Confirm submission", prompt):
            self.exam_active = False
            self.finish_exam()

    def finish_exam(self):
        self.exam_active = False
        if self.timer_job:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None
        score = sum(1 for i, q in enumerate(QUESTIONS) if self.answers.get(i) == q["answer"])
        total = len(QUESTIONS)
        result = {
            "name": self.student_name,
            "reg": self.reg_no,
            "score": score,
            "total": total,
            "percentage": score / total * 100,
            "time": time.strftime("%d %b %Y, %I:%M %p")
        }
        self.results.append(result)
        self.show_result(result)

    def show_result(self, result):
        self.clear()
        self.top_bar("EXAM COMPLETED  /  PERFORMANCE REPORT")
        outer = tk.Frame(self.root, bg=APP_BG)
        outer.pack(fill="both", expand=True, padx=34, pady=10)

        summary = tk.Frame(outer, bg=PANEL, padx=24, pady=18)
        summary.pack(fill="x")
        status = "EXCELLENT WORK!" if result["percentage"] >= 80 else (
            "GOOD EFFORT!" if result["percentage"] >= 50 else "KEEP PRACTISING!")
        self.label(summary, status, 10, ACCENT, True).pack(anchor="w")
        self.label(summary, f"{result['score']} / {result['total']} correct", 25, WHITE, True).pack(anchor="w", pady=(4, 0))
        self.label(summary, f"Score: {result['percentage']:.0f}%   •   Candidate: {result['name']}   •   ID: {result['reg']}",
                   10, MUTED).pack(anchor="w", pady=(5, 0))
        self.label(summary, "ANSWER REVIEW", 10, YELLOW, True).pack(anchor="w", pady=(16, 0))

        # Scrollable review list
        review_wrap = tk.Frame(outer, bg=APP_BG)
        review_wrap.pack(fill="both", expand=True, pady=(12, 10))
        canvas = tk.Canvas(review_wrap, bg=APP_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(review_wrap, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=APP_BG)
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(canvas_window, width=e.width))

        for i, q in enumerate(QUESTIONS):
            chosen = self.answers.get(i)
            correct = q["answer"]
            is_correct = chosen == correct
            card = tk.Frame(content, bg=PANEL, padx=16, pady=13)
            card.pack(fill="x", pady=5)
            self.label(card, f"Q{i+1:02d}  •  {'CORRECT' if is_correct else 'INCORRECT'}",
                       9, GREEN if is_correct else RED, True).pack(anchor="w")
            self.label(card, q["question"], 11, WHITE, True, wraplength=900,
                       justify="left").pack(anchor="w", pady=(5, 6))
            your_text = "Not answered" if chosen is None else f"{chr(65+chosen)}. {q['options'][chosen]}"
            correct_text = f"{chr(65+correct)}. {q['options'][correct]}"
            self.label(card, f"Your answer: {your_text}", 10,
                       GREEN if is_correct else MUTED, False, wraplength=900,
                       justify="left").pack(anchor="w")
            self.label(card, f"Correct answer: {correct_text}", 10, GREEN, True,
                       wraplength=900, justify="left").pack(anchor="w", pady=(2, 0))
            self.label(card, f"Why: {q['explanation']}", 9, MUTED, False,
                       wraplength=900, justify="left").pack(anchor="w", pady=(5, 0))

        bottom = tk.Frame(outer, bg=APP_BG)
        bottom.pack(fill="x")
        self.make_button(bottom, "← Home", self.show_home, bg=PANEL_2, fg=WHITE).pack(side="left")
        self.make_button(bottom, "Take Another Exam  ↻", self.show_student_login).pack(side="right")

    def show_admin_login(self):
        self.clear()
        self.top_bar("ADMINISTRATOR ACCESS")
        outer = tk.Frame(self.root, bg=APP_BG)
        outer.pack(expand=True)
        card = tk.Frame(outer, bg=PANEL, padx=42, pady=34)
        card.pack()
        self.label(card, "SECURE AREA", 9, YELLOW, True).pack(anchor="w")
        self.label(card, "Administrator login", 23, WHITE, True).pack(anchor="w", pady=(8, 20))
        self.label(card, "USERNAME", 9, MUTED, True).pack(anchor="w", pady=(0, 6))
        self.admin_user = tk.Entry(card, font=("Segoe UI", 12), bg=PANEL_2, fg=WHITE,
                                   insertbackground=WHITE, relief="flat", width=34)
        self.admin_user.pack(ipady=9, pady=(0, 14))
        self.label(card, "PASSWORD", 9, MUTED, True).pack(anchor="w", pady=(0, 6))
        self.admin_pass = tk.Entry(card, show="•", font=("Segoe UI", 12), bg=PANEL_2, fg=WHITE,
                                   insertbackground=WHITE, relief="flat", width=34)
        self.admin_pass.pack(ipady=9, pady=(0, 20))
        row = tk.Frame(card, bg=PANEL)
        row.pack(fill="x")
        self.make_button(row, "← Home", self.show_home, bg=PANEL_2, fg=WHITE).pack(side="left")
        self.make_button(row, "Login  →", self.check_admin).pack(side="right")
        self.admin_user.focus_set()

    def check_admin(self):
        if self.admin_user.get().strip() == "admin" and self.admin_pass.get() == "admin123":
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Login failed", "Incorrect username or password.")

    def show_admin_dashboard(self):
        self.clear()
        self.top_bar("ADMIN CONSOLE  /  RESULTS")
        outer = tk.Frame(self.root, bg=APP_BG, padx=34, pady=18)
        outer.pack(fill="both", expand=True)
        self.label(outer, "Exam attempts", 24, WHITE, True).pack(anchor="w")
        self.label(outer, "Results are kept in memory while this application remains open.", 10, MUTED).pack(anchor="w", pady=(4, 15))
        table = tk.Frame(outer, bg=PANEL, padx=12, pady=12)
        table.pack(fill="both", expand=True)
        headings = ["Student", "Registration No.", "Score", "Percentage", "Submitted"]
        for col, heading in enumerate(headings):
            self.label(table, heading, 9, ACCENT, True, bg=PANEL).grid(row=0, column=col, sticky="w", padx=8, pady=8)
        if not self.results:
            self.label(table, "No exam attempts have been recorded yet.", 11, MUTED, bg=PANEL).grid(
                row=1, column=0, columnspan=5, sticky="w", padx=8, pady=18)
        else:
            for row_idx, result in enumerate(self.results, start=1):
                values = [result["name"], result["reg"], f'{result["score"]}/{result["total"]}',
                          f'{result["percentage"]:.0f}%', result["time"]]
                for col, value in enumerate(values):
                    self.label(table, value, 9, WHITE if row_idx % 2 else MUTED,
                               bg=PANEL).grid(row=row_idx, column=col, sticky="w", padx=8, pady=8)
        self.make_button(outer, "← Back to Home", self.show_home, bg=PANEL_2, fg=WHITE).pack(anchor="w", pady=(16, 0))


if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineExamApp(root)
    root.mainloop()

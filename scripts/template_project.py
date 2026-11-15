"""
Starter template: copy this file, replace the screens and run
    OUT=./MyProject_Wireframes_v1 python3 template_project.py

Fictional example: "Book an appointment", two proposals with 3 screens each.
Each function receives s (Screen) and draws from top to bottom.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lowfi_kit import render_project

NAV = [("home", "Home"), ("search", "Explore"), ("list", "Bookings"), ("user", "Profile")]

# ---------------- Proposal 1 · Guided (linear steps) ----------------
def g1_home(s):
    s.header("My bookings", chip="0")
    s.text("You have no bookings yet", 10, bold=True)
    s.steps(["Service", "Date", "Confirm"])
    s.button("+ New booking", "pri", h=56)
    s.label("Upcoming (0)"); s.begin_box(kind="dashed"); s.hint("Nothing yet"); s.end_box()
    s.list_item("History", "Past bookings")
    s.nav(NAV, 2)

def g2_service(s):
    s.header("New booking", left="x", right="1/3")
    s.progress(1, 3, "Service")
    s.title("Which service do you need?")
    s.radios(["*Haircut", "Beard trim", "Haircut + beard", "Other"])
    s.label("Professional"); s.chips(["*Anyone", "Ana", "Luis"])
    s.footer([("Next: date →", "pri")])

def g3_confirm(s):
    s.header("Confirm", left="back", right="3/3")
    s.progress(3, 3, "Confirm")
    s.begin_box("Summary", "strong")
    s.kv([("Service", "Haircut"), ("Date", "Sat 10 am"), ("Price", "$20")])
    s.end_box()
    s.row_edit("Service"); s.row_edit("Date and time")
    s.check_line("Ready to book")
    s.note(["On confirm: message 'Booking created'", "+ button See my bookings"])
    s.footer([("Back", "sec"), ("Confirm booking", "pri")])

# ---------------- Proposal 2 · Modular (free-order sections) ----------------
def m1_home(s):
    s.header("My bookings", chip="0")
    s.tabs(["Upcoming", "History"], 0)
    s.text("Quick booking", 9.5, bold=True); s.hint("The service is preselected")
    s.card_grid(["Haircut", "Beard", "Cut + beard", "Other"])
    s.info("How do cancellations work?")
    s.fab("+ New booking", "no service yet", hint="Or start from scratch:")
    s.nav(NAV, 2)

def m2_editor(s):
    s.header("Draft", left="x", link="Preview")
    s.hint("Autosaved · 1 of 2 complete")
    s.accordion("Service: haircut", "done", "Change")
    s.begin_box("Date and time", "accordion", "open")
    s.chips(["Today", "*Sat 13", "Sun 14", "Other..."])
    s.label("Time"); s.chips(["9 am", "*10 am", "11 am", "4 pm"])
    s.toggle("Reminder 1 h before", True)
    s.end_box()
    s.accordion("Notes for the professional", "closed")
    s.footer([("Review (1 missing)", "sec")])

def m3_review(s):
    s.header("Review", left="Editor")
    s.alert("Missing: professional", "Pick one here:", ["*Anyone", "Ana", "Luis"])
    s.begin_box("Preview · tap to edit")
    s.list_item("Haircut", "Sat 13 · 10 am", avatar="AN", right="Edit", chevron=False)
    s.lines(2)
    s.end_box()
    s.note(["Once complete, Confirm becomes active", "After confirming: toast with Undo"])
    s.footer([("Confirm (1 missing)", "off")])

if __name__ == "__main__":
    render_project({
        "Proposal_1_Guided":  [("01_Home", g1_home), ("02_Service", g2_service), ("03_Confirm", g3_confirm)],
        "Proposal_2_Modular": [("01_Home", m1_home), ("02_Editor", m2_editor), ("03_Review", m3_review)],
    }, os.environ.get("OUT", "./Wireframes_out"), "Bookings · low-fi sketches")

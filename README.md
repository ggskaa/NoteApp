# Notes App (PyQt6 + SQLAlchemy)

A simple note-taking desktop app built with **PyQt6** and **SQLite** via **SQLAlchemy**.  
Educational / hobby project.

---

## Features
- Create, view, edit and delete notes  
- Notes stored in local SQLite database  
- Minimal custom UI with PyQt6  

---

## Requirements
Install inside a **virtual environment** (recommended, since PyQt6 only installs cleanly that way):

```bash
python -m venv venv
source venv/bin/activate   # Linux & macOS
venv\Scripts\activate  

pip install -r requirements.txt
 
 
greenlet==3.2.4
PyQt6==6.9.1
PyQt6-Qt6==6.9.1
PyQt6_sip==13.10.2
SQLAlchemy==2.0.43
typing_extensions==4.14.1 


python app.py  # Windows
```



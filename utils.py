from database.base import session, Notes_model

def create_note(title, content):
    new_note = Notes_model(title=title, content=content)
    session.add(new_note)
    session.commit()
    return new_note

def all_notes():
    return session.query(Notes_model).all()

def change_note_content(id, content):
    note = session.query(Notes_model).filter(Notes_model.id == id).first()
    if note:
        note.content = content
        session.commit()
    return note

def delete_note(id):
    note = session.query(Notes_model).filter(Notes_model.id == id).first()
    if note:
        session.delete(note)
        session.commit()
    return note

def get_note(id):
    return session.query(Notes_model).filter(Notes_model.id == id).first()

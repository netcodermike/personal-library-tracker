"""Local SQLite book catalog, reading tracker, and lending register."""
import csv,datetime,sqlite3
from pathlib import Path

class Library:
    def __init__(self,path='library.sqlite3'):
        self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
        version=self.db.execute('PRAGMA user_version').fetchone()[0]
        if version not in (0,1):raise ValueError('Unsupported library schema')
        self.db.execute("""CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,title TEXT NOT NULL,author TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'unread',borrower TEXT NOT NULL DEFAULT '',due TEXT NOT NULL DEFAULT '')""")
        self.db.execute('PRAGMA user_version=1');self.db.commit()
    def close(self):self.db.close()
    def add(self,title,author):
        if not title.strip():raise ValueError('A title is required')
        with self.db:return self.db.execute('INSERT INTO books(title,author) VALUES(?,?)',(title.strip(),author.strip())).lastrowid
    def books(self,query=''):
        # LIKE metacharacters are escaped so searches remain literal substrings.
        q='%'+query.replace('!','!!').replace('%','!%').replace('_','!_')+'%'
        return self.db.execute("SELECT * FROM books WHERE title LIKE ? ESCAPE '!' OR author LIKE ? ESCAPE '!' ORDER BY title COLLATE NOCASE,id",(q,q)).fetchall()
    def get(self,book):
        row=self.db.execute('SELECT * FROM books WHERE id=?',(book,)).fetchone()
        if row is None:raise ValueError('Book not found')
        return row
    def status(self,book,status):
        self.get(book)
        if status not in ('unread','reading','finished'):raise ValueError('Unknown reading status')
        with self.db:self.db.execute('UPDATE books SET status=? WHERE id=?',(status,book))
    def lend(self,book,borrower,due):
        row=self.get(book)
        if row['borrower']:raise ValueError('This book is already checked out')
        if not borrower.strip():raise ValueError('Borrower is required')
        due=datetime.date.fromisoformat(due).isoformat()
        with self.db:self.db.execute('UPDATE books SET borrower=?,due=? WHERE id=?',(borrower.strip(),due,book))
    def returned(self,book):
        self.get(book)
        with self.db:self.db.execute("UPDATE books SET borrower='',due='' WHERE id=?",(book,))
    def export(self,path):
        def safe(value):
            value=str(value)
            return "'"+value if value.lstrip().startswith(('=','+','-','@')) else value
        with open(path,'w',newline='',encoding='utf-8')as f:
            writer=csv.writer(f);writer.writerow(['id','title','author','status','borrower','due'])
            for row in self.books():writer.writerow([safe(v)for v in row])

def launch(path):
    import tkinter as tk
    from tkinter import ttk,simpledialog,messagebox,filedialog
    library=Library(path);root=tk.Tk();root.title('Personal Library');root.geometry('1000x610')
    panel=ttk.Frame(root,padding=20);panel.pack(fill='both',expand=True)
    ttk.Label(panel,text='Your shelves, in order.',font=('Segoe UI',24)).pack(anchor='w')
    search=tk.StringVar();ttk.Entry(panel,textvariable=search).pack(fill='x',pady=12)
    tree=ttk.Treeview(panel,columns=('title','author','status','borrower','due'),show='headings')
    for col in tree['columns']:tree.heading(col,text=col.title());tree.column(col,width=155)
    tree.tag_configure('overdue',foreground='#b91c1c');tree.pack(fill='both',expand=True)
    def refresh(*args):
        tree.delete(*tree.get_children());today=datetime.date.today().isoformat()
        for b in library.books(search.get()):tree.insert('', 'end',iid=str(b['id']),values=tuple(b[k]for k in tree['columns']),tags=('overdue',)if b['borrower'] and b['due']<today else())
    def selected():
        if not tree.selection():raise ValueError('Select a book first')
        return int(tree.selection()[0])
    def action(fn):
        try:fn();refresh()
        except (ValueError,sqlite3.Error,OSError)as e:messagebox.showerror('Library',str(e))
    def add():
        title=simpledialog.askstring('Add book','Title:',parent=root)
        if title is None:return
        author=simpledialog.askstring('Add book','Author:',parent=root)
        if author is not None:library.add(title,author)
    def lend():
        book=selected();borrower=simpledialog.askstring('Check out','Borrower:',parent=root)
        if borrower is None:return
        due=simpledialog.askstring('Due date','YYYY-MM-DD:',initialvalue=(datetime.date.today()+datetime.timedelta(days=14)).isoformat(),parent=root)
        if due is not None:library.lend(book,borrower,due)
    def export():
        path=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])
        if path:library.export(path)
    buttons=ttk.Frame(panel);buttons.pack(fill='x',pady=12)
    for label,fn in [('Add book',add),('Check out',lend),('Return',lambda:library.returned(selected())),('Export CSV',export)]:ttk.Button(buttons,text=label,command=lambda f=fn:action(f)).pack(side='left',padx=4)
    status=ttk.Combobox(buttons,values=['unread','reading','finished'],state='readonly',width=10);status.set('reading');status.pack(side='left',padx=8)
    ttk.Button(buttons,text='Set status',command=lambda:action(lambda:library.status(selected(),status.get()))).pack(side='left')
    search.trace_add('write',refresh);root.protocol('WM_DELETE_WINDOW',lambda:(library.close(),root.destroy()));refresh();root.mainloop()

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--store',default='library.sqlite3');a=p.parse_args()
    try:launch(a.store)
    except (sqlite3.Error,ValueError,OSError)as e:p.exit(1,str(e)+'\n')


# -*- coding: utf-8 -*-
"""
gui_v12.py — YellowFresh 亮黄绿调现代风 GUI
运行：python gui_v12.py
"""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from db import ReviveDB

DB_PATH = Path('revive.db')

# 主题配色（Yellow Fresh）
COLORS = {
    "bg": "#FFFBEA",
    "card": "#FFFFFF",
    "primary": "#FFE600",
    "primary_hover": "#FDD835",
    "accent": "#32C671",
    "title": "#1A1A1A",
    "text": "#222222",
    "muted": "#777777",
    "border": "#EDE7D9",
    "strip1": "#FFFFFF",
    "strip2": "#FCF6D6",
    "danger": "#FF5252",
    "orange": "#FF7B00",
}

class ReviveGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('🍋 物品复活 Revive ')
        self.geometry('980x640')
        self.configure(bg=COLORS["bg"])
        self.resizable(True, True)
        self.db = ReviveDB(DB_PATH)
        self._init_style()
        self._build_header()
        self._build_form()
        self._build_toolbar()
        self._build_table()
        self.refresh()

    def _init_style(self):
        s = ttk.Style(self)
        s.theme_use('default')
        s.configure(".", background=COLORS["bg"], foreground=COLORS["text"], padding=4, font=("Misans", 10))
        s.configure("Title.TLabel", background=COLORS["bg"], foreground=COLORS["title"], font=("Misans", 18, "bold"))
        s.configure("Sub.TLabel", background=COLORS["bg"], foreground=COLORS["muted"], font=("Misans", 10))
        s.configure("Card.TFrame", background=COLORS["card"], relief="flat", borderwidth=1)
        s.configure("Accent.TButton", background=COLORS["primary"], foreground="#000000", padding=(14,8), font=("Misans", 10, "bold"))
        s.map("Accent.TButton", background=[("active", COLORS["primary_hover"])], relief=[("pressed","sunken"), ("!pressed","flat")])
        s.configure("TEntry", fieldbackground="#FFFFFF", bordercolor=COLORS["border"], padding=6)
        s.configure("Toolbar.TFrame", background=COLORS["bg"])
        s.configure("Treeview", background="#FFFFFF", fieldbackground="#FFFFFF", bordercolor=COLORS["border"], rowheight=28)
        s.configure("Treeview.Heading", background=COLORS["primary"], foreground="#000000", font=("Misans", 10, "bold"))
        s.map("Treeview.Heading", background=[("active", COLORS["primary_hover"])])

    def _build_header(self):
        canvas = tk.Canvas(self, height=88, highlightthickness=0, bd=0)
        canvas.pack(fill="x", padx=0, pady=(0,8))
        self._draw_gradient(canvas, COLORS["primary"], COLORS["bg"])
        canvas.create_text(24, 26, anchor="nw", text="物品复活 Revive", font=("Misans", 22, "bold"))
        canvas.create_text(24, 56, anchor="nw", text="轻松发布闲置 · 让好物重新流动", font=("Misans", 11))

    def _draw_gradient(self, canvas, c1, c2):
        width = canvas.winfo_reqwidth() or 980
        steps = 120
        r1,g1,b1 = self.winfo_rgb(c1)
        r2,g2,b2 = self.winfo_rgb(c2)
        r_ratio = (r2 - r1) / steps
        g_ratio = (g2 - g1) / steps
        b_ratio = (b2 - b1) / steps
        for i in range(steps):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
            canvas.create_rectangle(i*(width/steps), 0, (i+1)*(width/steps), 88, outline="", fill=color)

    def _panel(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame")
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(fill="x", padx=12, pady=12)
        return card, inner

    def _build_form(self):
        card, inner = self._panel(self)
        card.pack(fill="x", padx=16, pady=(0,8))

        tk.Label(inner, text="名称*", bg=COLORS["card"]).grid(row=0, column=0, sticky="e", padx=(0,6), pady=4)
        self.ent_name = ttk.Entry(inner, width=28)
        self.ent_name.grid(row=0, column=1, sticky="w", pady=4)

        tk.Label(inner, text="价格(0=赠送)", bg=COLORS["card"]).grid(row=0, column=2, sticky="e", padx=(18,6), pady=4)
        self.ent_price = ttk.Entry(inner, width=10)
        self.ent_price.insert(0, "0")
        self.ent_price.grid(row=0, column=3, sticky="w", pady=4)

        tk.Label(inner, text="联系方式*", bg=COLORS["card"]).grid(row=1, column=0, sticky="e", padx=(0,6), pady=4)
        self.ent_contact = ttk.Entry(inner, width=28)
        self.ent_contact.grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(inner, text="描述", bg=COLORS["card"]).grid(row=1, column=2, sticky="e", padx=(18,6), pady=4)
        self.ent_desc = ttk.Entry(inner, width=38)
        self.ent_desc.grid(row=1, column=3, sticky="w", pady=4)

        ttk.Button(inner, text="添加", style="Accent.TButton", command=self.on_add).grid(row=0, column=4, rowspan=2, padx=(18,0), ipadx=6, ipady=2)

    def _build_toolbar(self):
        bar = ttk.Frame(self, style="Toolbar.TFrame")
        bar.pack(fill="x", padx=16, pady=(0,8))
        tk.Label(bar, text="搜索关键词", bg=COLORS["bg"]).pack(side="left")
        self.ent_q = ttk.Entry(bar, width=36)
        self.ent_q.pack(side="left", padx=6)
        ttk.Button(bar, text="搜索", style="Accent.TButton", command=self.on_search).pack(side="left")
        ttk.Button(bar, text="刷新", style="Accent.TButton", command=self.refresh).pack(side="left", padx=(8,0))
        ttk.Button(bar, text="删除选中", style="Accent.TButton", command=self.on_delete_selected).pack(side="left", padx=(8,0))

    def _build_table(self):
        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="both", expand=True, padx=16, pady=(0,16))
        inner = tk.Frame(card, bg=COLORS["card"])
        inner.pack(fill="both", expand=True, padx=12, pady=12)

        columns = ("id","name","price","contact","description","created_at")
        self.tree = ttk.Treeview(inner, columns=columns, show="headings", height=14)
        headers = ['ID','名称','价格','联系方式','描述','创建时间']
        for c,t in zip(columns, headers):
            self.tree.heading(c, text=t)
            self.tree.column(c, anchor="w", width=120 if c!="description" else 320)
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure('odd', background=COLORS["strip2"])
        self.tree.tag_configure('even', background=COLORS["strip1"])

    def on_add(self):
        name = self.ent_name.get().strip()
        contact = self.ent_contact.get().strip()
        desc = self.ent_desc.get().strip()
        price_raw = self.ent_price.get().strip() or '0'
        try:
            price = float(price_raw)
        except ValueError:
            messagebox.showerror('错误', '价格必须是数字')
            return
        if not name or not contact:
            messagebox.showerror('错误', '名称与联系方式为必填项')
            return
        self.db.add_item(name, desc, contact, price)
        for e in (self.ent_name, self.ent_desc):
            e.delete(0, tk.END)
        self.ent_price.delete(0, tk.END); self.ent_price.insert(0,'0')
        self.refresh()
        messagebox.showinfo('成功', '已添加')

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = self.db.list_items(limit=500)
        for idx, r in enumerate(rows):
            price_str = '赠送' if float(r['price']) == 0 else f"¥{r['price']:.2f}"
            tag = 'odd' if idx % 2 else 'even'
            self.tree.insert('', tk.END, values=(r['id'], r['name'], price_str, r['contact'], r['description'] or '', r['created_at']), tags=(tag,))

    def on_search(self):
        q = self.ent_q.get().strip()
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = self.db.search_items(q, limit=500) if q else self.db.list_items(limit=500)
        for idx, r in enumerate(rows):
            price_str = '赠送' if float(r['price']) == 0 else f"¥{r['price']:.2f}"
            tag = 'odd' if idx % 2 else 'even'
            self.tree.insert('', tk.END, values=(r['id'], r['name'], price_str, r['contact'], r['description'] or '', r['created_at']), tags=(tag,))

    def on_delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning('提示', '请先选中一行再删除')
            return
        item = self.tree.item(sel[0])
        item_id = int(item['values'][0])
        if messagebox.askyesno('确认', f'确认删除 ID={item_id} 吗？'):
            self.db.delete_item(item_id)
            self.refresh()

    def on_close(self):
        self.db.close()
        self.destroy()

if __name__ == "__main__":
    app = ReviveGUI()
    app.protocol('WM_DELETE_WINDOW', app.on_close)
    app.mainloop()

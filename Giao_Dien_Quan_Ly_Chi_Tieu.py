import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import json

class GiaoDienChiTieu:
    def __init__(self, root, ten_dang_nhap, quyen, api):
        self.root = root
        self.ten_dang_nhap = ten_dang_nhap
        self.quyen = quyen
        self.api = api
        self.du_lieu = []

        self.root.title("Quản lý chi tiêu")
        self.root.geometry("700x500")

        self.khung = tk.Frame(self.root)
        self.khung.pack(padx=10, pady=10, fill="both", expand=True)

        self.tao_giao_dien_nhap_lieu()
        self.tao_giao_dien_bang()
        self.tao_giao_dien_tim_kiem()
        self.load_du_lieu()

    def tao_giao_dien_nhap_lieu(self):
        f = tk.Frame(self.khung)
        f.pack(fill="x")

        tk.Label(f, text="Nội dung").grid(row=0, column=0)
        self.entry_noi_dung = tk.Entry(f)
        self.entry_noi_dung.grid(row=0, column=1)

        tk.Label(f, text="Số tiền").grid(row=0, column=2)
        self.entry_so_tien = tk.Entry(f)
        self.entry_so_tien.grid(row=0, column=3)

        tk.Label(f, text="Ngày (YYYY-MM-DD)").grid(row=0, column=4)
        self.entry_ngay = tk.Entry(f)
        self.entry_ngay.grid(row=0, column=5)

        tk.Button(f, text="Thêm", command=self.them).grid(row=0, column=6, padx=5)
        tk.Button(f, text="Cập nhật", command=self.cap_nhat).grid(row=0, column=7, padx=5)
        tk.Button(f, text="Xóa", command=self.xoa).grid(row=0, column=8, padx=5)

    def tao_giao_dien_bang(self):
        self.tree = ttk.Treeview(self.khung, columns=("id", "noi_dung", "so_tien", "ngay"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("noi_dung", text="Nội dung")
        self.tree.heading("so_tien", text="Số tiền")
        self.tree.heading("ngay", text="Ngày")
        self.tree.pack(fill="both", expand=True, pady=10)

        self.tree.bind("<ButtonRelease-1>", self.chon_dong)

    def tao_giao_dien_tim_kiem(self):
        f = tk.Frame(self.khung)
        f.pack(fill="x")

        tk.Label(f, text="Tìm nội dung").pack(side="left")
        self.entry_tim_noi_dung = tk.Entry(f)
        self.entry_tim_noi_dung.pack(side="left", padx=5)

        tk.Label(f, text="Tìm ngày (YYYY-MM-DD)").pack(side="left")
        self.entry_tim_ngay = tk.Entry(f)
        self.entry_tim_ngay.pack(side="left", padx=5)

        tk.Button(f, text="Tìm kiếm", command=self.tim_kiem).pack(side="left", padx=5)
        tk.Button(f, text="Làm mới", command=self.load_du_lieu).pack(side="left", padx=5)

    def load_du_lieu(self):
        self.du_lieu = self.api.lay_danh_sach(self.ten_dang_nhap)
        self.hien_thi_du_lieu(self.du_lieu)

    def hien_thi_du_lieu(self, ds):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for d in ds:
            self.tree.insert("", "end", values=(d["id"], d["noi_dung"], d["so_tien"], d.get("ngay", "")))

    def chon_dong(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.entry_noi_dung.delete(0, tk.END)
            self.entry_noi_dung.insert(0, values[1])
            self.entry_so_tien.delete(0, tk.END)
            self.entry_so_tien.insert(0, values[2])
            self.entry_ngay.delete(0, tk.END)
            self.entry_ngay.insert(0, values[3])

    def them(self):
        noi_dung = self.entry_noi_dung.get()
        so_tien = self.entry_so_tien.get()
        ngay = self.entry_ngay.get() or datetime.today().strftime("%Y-%m-%d")

        if not noi_dung or not so_tien:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin")
            return

        id_moi = max([d["id"] for d in self.du_lieu], default=0) + 1
        data = {
            "id": id_moi,
            "nguoi_dung": self.ten_dang_nhap,
            "noi_dung": noi_dung,
            "so_tien": so_tien,
            "ngay": ngay
        }
        self.api.them_chi_tieu(data)
        self.load_du_lieu()

    def cap_nhat(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn dòng", "Vui lòng chọn dòng để cập nhật")
            return

        values = self.tree.item(selected[0], "values")
        id = int(values[0])
        new_data = {
            "noi_dung": self.entry_noi_dung.get(),
            "so_tien": self.entry_so_tien.get(),
            "ngay": self.entry_ngay.get() or datetime.today().strftime("%Y-%m-%d")
        }
        self.api.cap_nhat_chi_tieu(id, new_data)
        self.load_du_lieu()

    def xoa(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn dòng", "Vui lòng chọn dòng để xóa")
            return

        values = self.tree.item(selected[0], "values")
        id = int(values[0])
        self.api.xoa_chi_tieu(id)
        self.load_du_lieu()

    def tim_kiem(self):
        noi_dung = self.entry_tim_noi_dung.get().lower()
        ngay = self.entry_tim_ngay.get().strip()

        ket_qua = [d for d in self.du_lieu if
                   (noi_dung in d["noi_dung"].lower() if noi_dung else True) and
                   (ngay == d.get("ngay", "") if ngay else True)]
        self.hien_thi_du_lieu(ket_qua)


class ChiTieuAPI:
    def __init__(self):
        self.file = "du_lieu_chi_tieu.json"
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = []

    def _save_data(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def lay_danh_sach(self, ten_dang_nhap):
        return [d for d in self.data if d["nguoi_dung"] == ten_dang_nhap]

    def them_chi_tieu(self, data):
        self.data.append(data)
        self._save_data()

    def xoa_chi_tieu(self, id):
        self.data = [d for d in self.data if d["id"] != id]
        self._save_data()

    def cap_nhat_chi_tieu(self, id, new_data):
        for d in self.data:
            if d["id"] == id:
                d.update(new_data)
                break
        self._save_data()

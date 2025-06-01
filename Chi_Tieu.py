import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NGUOI_DUNG = "nguoi_dung.json"

def doc_nguoi_dung():
    if os.path.exists(FILE_NGUOI_DUNG):
        with open(FILE_NGUOI_DUNG, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def ghi_nguoi_dung(ds):
    with open(FILE_NGUOI_DUNG, "w", encoding="utf-8") as f:
        json.dump(ds, f, indent=4, ensure_ascii=False)

def mo_giao_dien_chi_tieu(ten, quyen):
    from Giao_Dien_Quan_Ly_Chi_Tieu import GiaoDienChiTieu, ChiTieuAPI

    new_root = tk.Tk()
    api = ChiTieuAPI()
    app = GiaoDienChiTieu(new_root, ten, quyen, api)
    new_root.mainloop()



def dang_ky():
    def thuc_hien_dang_ky():
        ten = entry_ten.get().strip()
        mk = entry_mk.get().strip()
        quyen = var_quyen.get()

        if not ten or not mk:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ.")
            return

        ds = doc_nguoi_dung()
        if any(u["ten"] == ten for u in ds):
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
            return

        ds.append({"ten": ten, "mat_khau": mk, "quyen": quyen})
        ghi_nguoi_dung(ds)
        messagebox.showinfo("Thành công", "Đăng ký thành công!")
        win.destroy()

    win = tk.Toplevel()
    win.title("Đăng ký")
    win.geometry("200x300")
    win.configure(bg="#f7f7f7")

    frame = tk.Frame(win, bg="white", padx=20, pady=20, relief="groove", bd=2)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="📝 Đăng ký", font=("Arial", 16, "bold"), bg="white").pack(pady=(0, 10))

    tk.Label(frame, text="👤 Username", bg="white", anchor="w").pack(fill="x")
    entry_ten = tk.Entry(frame, bd=1, relief="solid")
    entry_ten.pack(fill="x", pady=(0, 10))

    tk.Label(frame, text="🔒 Password", bg="white", anchor="w").pack(fill="x")
    entry_mk = tk.Entry(frame, show="*", bd=1, relief="solid")
    entry_mk.pack(fill="x", pady=(0, 10))   

    tk.Label(frame, text="🛡️ Quyền", bg="white", anchor="w").pack(fill="x")
    var_quyen = tk.StringVar(value="user")
    drop = tk.OptionMenu(frame, var_quyen, "admin", "user")
    drop.config(width=15)
    drop.pack(pady=(0, 10))

    tk.Button(frame, text="Đăng ký", bg="#34A853", fg="white", command=thuc_hien_dang_ky).pack()

def quen_mat_khau():
    messagebox.showinfo("Quên mật khẩu", "Liên hệ admin để đặt lại mật khẩu.")

def dang_nhap():
    ten = entry_user.get().strip()
    mk = entry_pass.get().strip()

    ds = doc_nguoi_dung()
    for u in ds:
        if u["ten"] == ten and u["mat_khau"] == mk:
            messagebox.showinfo("Đăng nhập", f"Xin chào {ten} ({u['quyen']})")
            root.destroy()
            mo_giao_dien_chi_tieu(ten, u["quyen"])
            return
    messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu.")

# Giao diện chính
root = tk.Tk()
root.title("Đăng Nhập")
root.geometry("250x320")
root.configure(bg="#f7f7f7")

frame = tk.Frame(root, bg="white", padx=20, pady=20, relief="groove", bd=2)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="👤", font=("Arial", 32), bg="white").pack()
tk.Label(frame, text="Login", font=("Arial", 16, "bold"), bg="white").pack(pady=(0, 10))

tk.Label(frame, text="🧑 Username", anchor="w", bg="white").pack(fill="x")
entry_user = tk.Entry(frame, bd=1, relief="solid")
entry_user.pack(fill="x", pady=(0, 10))

tk.Label(frame, text="🔒 Password", anchor="w", bg="white").pack(fill="x")
entry_pass = tk.Entry(frame, show="*", bd=1, relief="solid")
entry_pass.pack(fill="x", pady=(0, 10))

frame_bottom = tk.Frame(frame, bg="white")
frame_bottom.pack(fill="x", pady=(5, 5))

var_remember = tk.BooleanVar()
tk.Checkbutton(frame_bottom, text="Remember me", variable=var_remember, bg="white").pack(side="left")

tk.Button(frame_bottom, text="Forgot password?", fg="blue", bg="white", relief="flat", bd=0,
          font=("Arial", 9, "underline"), command=quen_mat_khau).pack(side="right")

tk.Button(frame, text="LOGIN", width=20, bg="#4285F4", fg="white", command=dang_nhap).pack(pady=(10, 5))
tk.Button(frame, text="ĐĂNG KÝ", width=20, bg="#F4B400", fg="white", command=dang_ky).pack()


root.mainloop()

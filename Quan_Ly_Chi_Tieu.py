import sys
import json
from datetime import datetime


class GiaoDich:
    def __init__(self, danh_muc="", so_tien=0.0, ngay=datetime.now().strftime("%Y-%m-%d"), mo_ta=""):
        self.danh_muc = danh_muc
        self.so_tien = so_tien
        self.ngay = ngay
        self.mo_ta = mo_ta

    def nhap(self):
        self.danh_muc = input("Nhập danh mục chi tiêu: ")

        while True:
            try:
                self.so_tien = float(input("Nhập số tiền: "))
                break
            except ValueError:
                print("Số tiền phải là số, vui lòng nhập lại.")

        self.ngay = input("Nhập ngày (yyyy-mm-dd, để trống lấy ngày hôm nay): ")
        if not self.ngay:
            self.ngay = datetime.now().strftime("%Y-%m-%d")

        self.mo_ta = input("Nhập mô tả: ")

    def xuat(self):
        print("{:<20} {:<15} {:<15} {:<40}".format(self.danh_muc, self.so_tien, self.ngay, self.mo_ta))


class DanhSachGiaoDich:
    def __init__(self, danh_sach=[]):
        self.danh_sach = danh_sach

    def doc_file_json(self, ten_file):
        try:
            with open(ten_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.danh_sach = []
                for gd in data:
                    gd_moi = GiaoDich(
                        gd['danh_muc'],
                        gd['so_tien'],
                        gd['ngay'],
                        gd['mo_ta']
                    )
                    self.danh_sach.append(gd_moi)
                print(f"Đã đọc dữ liệu từ file {ten_file} thành công.")
        except FileNotFoundError:
            print(f"File {ten_file} không tồn tại.")
        except json.JSONDecodeError:
            print(f"File {ten_file} không hợp lệ.")
        except Exception as e:
            print(f"Có lỗi xảy ra: {e}")

    def ghi_file_json(self, ten_file):
        try:
            with open(ten_file, 'w', encoding='utf-8') as file:
                data = []
                for gd in self.danh_sach:
                    data.append({
                        'danh_muc': gd.danh_muc,
                        'so_tien': gd.so_tien,
                        'ngay': gd.ngay,
                        'mo_ta': gd.mo_ta
                    })
                json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"Đã ghi dữ liệu vào file {ten_file} thành công.")
        except Exception as e:
            print(f"Có lỗi xảy ra khi ghi file: {e}")

    def xuat_danh_sach(self):
        if not self.danh_sach:
            print("Danh sách giao dịch trống.")
            return
        print("{:<20} {:<15} {:<15} {:<40}".format("Danh Mục", "Số Tiền", "Ngày", "Mô Tả"))
        print("-" * 90)
        for gd in self.danh_sach:
            gd.xuat()

    def them_giao_dich(self, ten_file):
        gd = GiaoDich()
        gd.nhap()
        self.danh_sach.append(gd)
        self.ghi_file_json(ten_file)
        print("Đã thêm giao dịch.")

    def cap_nhat_giao_dich(self, ten_file):
        if not self.danh_sach:
            print("Danh sách giao dịch trống.")
            return
        tim = input("Nhập ngày giao dịch cần cập nhật (yyyy-mm-dd): ")
        found = False
        for gd in self.danh_sach:
            if gd.ngay == tim:
                found = True
                while True:
                    print("Thông tin hiện tại:")
                    gd.xuat()
                    print("Chọn thông tin cần cập nhật:")
                    print("1. Danh mục")
                    print("2. Số tiền")
                    print("3. Ngày")
                    print("4. Mô tả")
                    print("0. Thoát")
                    chon = input("Lựa chọn: ")
                    if chon == '0':
                        break
                    elif chon == '1':
                        gd.danh_muc = input("Nhập danh mục mới: ")
                    elif chon == '2':
                        while True:
                            try:
                                gd.so_tien = float(input("Nhập số tiền mới: "))
                                break
                            except ValueError:
                                print("Số tiền phải là số.")
                    elif chon == '3':
                        gd.ngay = input("Nhập ngày mới (yyyy-mm-dd): ")
                    elif chon == '4':
                        gd.mo_ta = input("Nhập mô tả mới: ")
                    else:
                        print("Lựa chọn không hợp lệ.")
                    self.ghi_file_json(ten_file)
                print("Đã cập nhật giao dịch.")
                break
        if not found:
            print("Không tìm thấy giao dịch theo ngày:", tim)

    def xoa_giao_dich(self, ten_file):
        if not self.danh_sach:
            print("Danh sách giao dịch trống.")
            return
        tim = input("Nhập ngày giao dịch cần xoá (yyyy-mm-dd): ")
        for gd in self.danh_sach:
            if gd.ngay == tim:
                self.danh_sach.remove(gd)
                self.ghi_file_json(ten_file)
                print("Đã xoá giao dịch.")
                return
        print("Không tìm thấy giao dịch.")


def menu():
    print("\n\tMenu Quản Lý Chi Tiêu")
    print("1. Đọc danh sách giao dịch từ file JSON")
    print("2. Ghi danh sách giao dịch vào file JSON")
    print("3. Xuất danh sách giao dịch")
    print("4. Thêm giao dịch")
    print("5. Cập nhật giao dịch")
    print("6. Xoá giao dịch")
    print("0. Thoát")


def thuc_thi():
    ds_giao_dich = DanhSachGiaoDich()
    ten_file = "File\\danh_sach_chi_tieu.json"
    while True:
        menu()
        try:
            chon = int(input("Nhập lựa chọn: "))
        except ValueError:
            print("Lựa chọn phải là số.")
            continue

        if chon == 0:
            break
        elif chon == 1:
            ds_giao_dich.doc_file_json(ten_file)
        elif chon == 2:
            ds_giao_dich.ghi_file_json(ten_file)
        elif chon == 3:
            ds_giao_dich.xuat_danh_sach()
        elif chon == 4:
            ds_giao_dich.them_giao_dich(ten_file)
        elif chon == 5:
            ds_giao_dich.cap_nhat_giao_dich(ten_file)
        elif chon == 6:
            ds_giao_dich.xoa_giao_dich(ten_file)
        else:
            print("Lựa chọn không hợp lệ.")


def main():
    thuc_thi()


if __name__ == "__main__":
    main()
    sys.exit(0)

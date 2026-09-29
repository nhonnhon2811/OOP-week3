# ********************************
# Mã sinh viên: 202419001
# Họ tên: Đặng Nhật Trọng
# ********************************

class Employee:
    # Sử dụng tham số mặc định để mô phỏng 3 constructor
    def __init__(self, emp_id="UNKNOWN", full_name="Unnamed employee", base_salary=0.0):
        if not emp_id or not full_name:
            raise ValueError("Mã và họ tên không được rỗng.") 
        if base_salary < 0:
            raise ValueError("Lương cơ bản không âm.") 
            
        self._id = emp_id
        self._full_name = full_name
        self._base_salary = float(base_salary)

    # Mô phỏng nạp chồng increaseSalary bằng tham số mặc định
    def increase_salary(self, value, by_percentage=False):
        if value <= 0:
            return
        if by_percentage:
            self._base_salary += self._base_salary * (value / 100.0)
        else:
            self._base_salary += value

    @property
    def id(self):
        return self._id

    @property
    def full_name(self):
        return self._full_name

    def calculate_monthly_cost(self):
        return self._base_salary

    def display_info(self):
        print(f"[Employee] ID: {self._id} | Name: {self._full_name} | Salary: ${self._base_salary:.2f}")

    def __del__(self):
        # Phương thức hủy (Destructor)
        print(f"=> [Hủy Employee] Vòng đời của nhân sự {self._id} đã kết thúc.")


class SoftwareEngineer(Employee):
    # Kế thừa từ Employee
    def __init__(self, emp_id, full_name, base_salary=0.0, primary_language=None, technical_allowance=0.0):
        super().__init__(emp_id, full_name, base_salary)
        
        if not primary_language:
            raise ValueError("Ngôn ngữ chính không được rỗng.") # Ràng buộc
        if technical_allowance < 0:
            raise ValueError("Phụ cấp không âm.") # Ràng buộc
            
        self._primary_language = primary_language
        self._technical_allowance = float(technical_allowance)

    # Ghi đè phương thức (Override)
    def calculate_monthly_cost(self):
        return self._base_salary + self._technical_allowance

    def display_info(self):
        print(f"[SoftEng]  ID: {self._id} | Name: {self._full_name} | Base: ${self._base_salary:.2f} "
              f"| Lang: {self._primary_language} | Allow: ${self._technical_allowance:.2f} "
              f"| Total: ${self.calculate_monthly_cost():.2f}")

    def __del__(self):
        print(f"=> [Hủy SoftEng] Vòng đời của kỹ sư {self._id} đã kết thúc.")


class ProjectTeam:
    # Constructor nạp chồng bằng tham số leader mặc định
    def __init__(self, project_code, project_name, leader=None):
        self._project_code = project_code
        self._project_name = project_name
        self._leader = None
        self._members = [] # Danh sách liên kết không sở hữu
        
        if leader:
            self.add_member(leader, make_leader=True)

    def contains(self, employee_id):
        return any(member.id == employee_id for member in self._members)

    # Mô phỏng nạp chồng addMember
    def add_member(self, employee, make_leader=False):
        added = False
        if not self.contains(employee.id):
            self._members.append(employee)
            added = True
            
        if make_leader:
            self._leader = employee # Trưởng nhóm phải thuộc danh sách
            
        return added or make_leader

    def remove_member(self, employee_id):
        if self._leader and self._leader.id == employee_id:
            print(f"Lỗi: Không được xóa trưởng nhóm hiện tại ({employee_id}) khi chưa chọn thay thế!") # Ràng buộc
            return False
            
        for i, member in enumerate(self._members):
            if member.id == employee_id:
                del self._members[i]
                return True
        return False

    def change_leader(self, new_leader):
        self.add_member(new_leader) # Thêm vào nhóm nếu chưa có
        self._leader = new_leader

    def calculate_total_monthly_cost(self):
        return sum(member.calculate_monthly_cost() for member in self._members)

    def display_team(self):
        print(f"\n--- TEAM: {self._project_name} ({self._project_code}) ---")
        print(f"Leader: {self._leader.full_name if self._leader else '[Chưa có]'}")
        print("Danh sách thành viên:")
        for member in self._members:
            member.display_info() # Lời gọi đa hình
        print("-" * 35)

    def __del__(self):
        print(f"=> [Hủy Team] Nhóm {self._project_code} bị hủy (không hủy đối tượng nhân sự).")
        self._members.clear() # Chỉ hủy danh sách


# ==========================================
# C. KIỂM THỬ
# ==========================================
def main():
    print("--- KHỞI TẠO DỮ LIỆU ---")
    # 1. Tạo 2 Employee 
    emp1 = Employee("E01", "Nguyen Van A")
    emp2 = Employee("E02", "Tran Thi B", 1000.0)

    # 2. Tạo 2 Software Engineer
    se1 = SoftwareEngineer("SE01", "Le Van C", primary_language="C++")
    se2 = SoftwareEngineer("SE02", "Hoang Thi D", 1500.0, "Python", 300.0)

    # 3 & 4. Tăng lương 
    emp1.increase_salary(500.0)
    emp2.increase_salary(10.0, by_percentage=True)

    # 5. Tạo nhóm không trưởng nhóm
    team1 = ProjectTeam("PRJ01", "Hệ thống Điểm Danh")

    # 6. Thêm nhân sự 
    team1.add_member(emp1)

    # 7. Thêm kỹ sư làm trưởng nhóm
    team1.add_member(se1, make_leader=True)

    # 8. Thử thêm lại thành viên
    check_add = team1.add_member(emp1)
    print(f"Thử thêm lại E01: {'Thành công' if check_add else 'Từ chối'}")

    # 9. Hiển thị danh sách 
    team1.add_member(emp2)
    team1.display_team()

    # 10. Tính tổng chi phí
    print(f"Tổng chi phí nhân sự: ${team1.calculate_total_monthly_cost():.2f}")

    # 11. Xóa trưởng nhóm hiện tại (Bị từ chối)
    team1.remove_member("SE01")

    # 12. Đổi trưởng nhóm và xóa 
    team1.change_leader(emp2)
    team1.remove_member("SE01")
    print("\nSau khi đổi trưởng nhóm sang E02 và xóa SE01:")
    team1.display_team()

    # 13, 14, 15. Kiểm tra quan hệ kết tập và vòng đời
    print("\n--- TEST QUAN HỆ KẾT TẬP ---")
    def test_scope():
        team2 = ProjectTeam("PRJ02", "Dự án AI", leader=se2)
        team2.add_member(emp2)
        team2.display_team()
        # Khi hàm kết thúc, team2 sẽ bị hủy do ra khỏi scope (14)

    test_scope() 

    # 15. Chứng minh nhân sự vẫn tồn tại
    print("\nSau khi team2 bị hủy, nhân sự emp2 và se2 vẫn tồn tại độc lập:")
    emp2.display_info()
    se2.display_info()
    
    print("\n--- KẾT THÚC ---")

if __name__ == "__main__":
    main()
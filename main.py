# NIM: STI202500002
# NAMA: Sabrina Azzahra
# UTS PBO
import json
from abc import ABC, abstractmethod

# 1. STACK (Struktur Data LIFO)
class MyStack:
    def __init__(self):
        self._data = []
    def push(self, item):
        self._data.append(item)
    def pop(self):
        return self._data.pop() if self._data else None
    def is_empty(self):
        return len(self._data) == 0

# 2. BONUS - INHERITANCE & OVERRIDE
class Bonus(ABC):
    @abstractmethod
    def calc(self, base): pass

class NoBonus(Bonus):
    def calc(self, base): return 0 # Override

class Perf2026Bonus(Bonus):
    def calc(self, base): return base * 0.20 # Override 20%

class Senior10Bonus(Bonus):
    def calc(self, base): return base * 0.10 # Override 10%

class Lead2026Bonus(Bonus):
    def calc(self, base): return base * 0.30 # Override 30%

def get_bonus_obj(code):
    if code == "PERF2026": return Perf2026Bonus()
    if code == "SENIOR10": return Senior10Bonus()
    if code == "LEAD2026": return Lead2026Bonus()
    return NoBonus()

# 3. EMPLOYEE - INHERITANCE, POLYMORPHISM, OVERRIDE
class Employee(ABC):
    def __init__(self, emp_id, name, base_salary, bonus_code):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary
        self.bonus_code = bonus_code
        self.bonus_obj = get_bonus_obj(bonus_code)

    @abstractmethod
    def calculate_total_salary(self): pass # Akan di-Override

    def display(self):
        return f"{self.emp_id} | {self.name}"

class PermanentEmployee(Employee): # Inheritance
    def calculate_total_salary(self): # Override + Polymorphism
        return self.base_salary + self.bonus_obj.calc(self.base_salary) + 1000000

class ContractEmployee(Employee): # Inheritance
    def calculate_total_salary(self): # Override + Polymorphism
        return self.base_salary + self.bonus_obj.calc(self.base_salary)

# 4. SENSOR - INHERITANCE, POLYMORPHISM, OVERRIDE
class Sensor(ABC):
    def __init__(self, sid, loc, temp, op):
        self.sid = sid; self.loc = loc; self.temp = temp; self.op = op
    @abstractmethod
    def process(self): pass

class DangerSensor(Sensor):
    def process(self): return f"DANGER - {self.sid} {self.loc} {self.temp}C Operator:{self.op} -> SHUTDOWN!"

class WarningSensor(Sensor):
    def process(self): return f"WARNING - {self.sid} {self.loc} {self.temp}C -> CHECK"

class NormalSensor(Sensor):
    def process(self): return f"NORMAL - {self.sid} {self.loc} {self.temp}C -> OK"

# MAIN PROGRAM
if __name__ == "__main__":
    print("=== UTS PBO - STI202500002 Sabrina Azzahra ===\n")

    # --- Employee dengan Stack ---
    with open("employee.json") as f:
        emps = json.load(f)["employees"]

    stack_emp = MyStack()
    for e in emps:
        obj = PermanentEmployee(e["emp_id"], e["name"], e["base_salary"], e["bonus_code"]) if e["is_permanent"] else ContractEmployee(e["emp_id"], e["name"], e["base_salary"], e["bonus_code"])
        stack_emp.push(obj)

    print("--- DATA GAJI (Stack LIFO - keluar terakhir dulu) ---")
    while not stack_emp.is_empty():
        emp = stack_emp.pop()
        # Polymorphism: method sama, hasil beda tergantung Permanent/Contract
        print(f"{emp.display()} | Bonus:{emp.bonus_code} | Total Gaji: Rp {emp.calculate_total_salary():,.0f}")

    # --- Sensor dengan Stack ---
    with open("sensor_logs.json") as f:
        sens = json.load(f)["readings"]

    stack_sens = MyStack()
    for s in sens:
        if s["status"] == "DANGER": obj = DangerSensor(s["sensor_id"], s["location"], s["temperature"], s["operator_id"])
        elif s["status"] == "WARNING": obj = WarningSensor(s["sensor_id"], s["location"], s["temperature"], s["operator_id"])
        else: obj = NormalSensor(s["sensor_id"], s["location"], s["temperature"], s["operator_id"])
        stack_sens.push(obj)

    print("\n--- DATA SENSOR (Stack LIFO + Override) ---")
    while not stack_sens.is_empty():
        print(stack_sens.pop().process())
import tkinter as tk
from tkinter import ttk, messagebox
import os

def initialize_files():
    if not os.path.exists("lounge.txt"):
        with open("lounge.txt", "w", encoding="utf-8") as f:
            # New York (JFK): 35/75 → 46.7% → Stable (Green)
            f.write("JFK,John F. Kennedy International Airport,New York Lounge,75,40\n")
            # London (LHR): 76/80 → 95% → Critical (Red)
            f.write("LHR,London Heathrow Airport,London Lounge,80,4\n")
            # Dubai (DXB): 55/100 → 55% → Moderate (Yellow)
            f.write("DXB,Dubai International Airport,Dubai Lounge,100,45\n")
            # Sydney (SYD): 12/80 → 15% → Stable (Green)
            f.write("SYD,Sydney Airport,Sydney Lounge,80,68\n")
            # Singapore (SIN): 22/90 → 24.4% → Stable (Green)
            f.write("SIN,Singapore Changi Airport,Singapore Lounge,90,68\n")

    if not os.path.exists("order.txt"):
        with open("order.txt", "w", encoding="utf-8") as f:
            f.write("")

class FlyDreamAirGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FlyDreamAir Lounge System")
        self.root.geometry("700x800")
        self.root.resizable(False,False)
        self.current_user = ""
        self.selected_lounge = None
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        tk.Label(self.root, text="Welcome", font=("Arial",22,"bold")).pack(pady=20)
        tk.Label(self.root, text="Name", font=("Arial",14)).pack()
        self.e_name = ttk.Entry(self.root, width=40)
        self.e_name.pack(pady=5)
        tk.Label(self.root, text="City", font=("Arial",14)).pack()
        self.e_city = ttk.Entry(self.root, width=40)
        self.e_city.pack(pady=5)
        ttk.Button(self.root, text="Continue", command=self.login_go).pack(pady=30)

    def login_go(self):
        self.current_user = self.e_name.get().strip()
        if not self.current_user:
            messagebox.showwarning("Warning","Please enter your name")
            return
        self.show_home()

    def show_home(self):
        self.clear()
        tk.Label(self.root, text="FlyDreamAir", font=("Arial",24,"bold")).pack(pady=30)
        ttk.Button(self.root, text="Find a Lounge", width=30, command=self.show_search).pack(pady=10)
        ttk.Button(self.root, text="Check Global Occupancy", width=30, command=self.show_global_status).pack(pady=10)
        ttk.Button(self.root, text="My Bookings", width=30, command=self.show_bookings).pack(pady=10)
        ttk.Button(self.root, text="Exit", width=30, command=self.root.quit).pack(pady=10)

    def show_global_status(self):
        self.clear()
        tk.Label(self.root, text="Global Occupancy Monitor", font=("Arial",22,"bold")).pack(pady=20)
        ttk.Button(self.root, text="Check the Global Occupancy", command=self.load_global_status).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.show_home).pack(pady=5)

    def load_global_status(self):
        for w in self.root.winfo_children():
            if isinstance(w, ttk.Button) and (w["text"] == "Check the Global Occupancy" or w["text"] == "Back"):
                continue
            if isinstance(w, tk.Label) and w["text"] == "Global Occupancy Monitor":
                continue
            w.destroy()

        columns = ("location", "current", "max", "status")
        tree = ttk.Treeview(self.root, columns=columns, show="headings", height=8)
        tree.heading("location", text="Lounge Location")
        tree.heading("current", text="Current Guests")
        tree.heading("max", text="Max Capacity")
        tree.heading("status", text="Status")

        tree.column("location", width=180)
        tree.column("current", width=120, anchor="center")
        tree.column("max", width=120, anchor="center")
        tree.column("status", width=180, anchor="center")

        with open("lounge.txt","r",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                code, airport, name, total, avail = parts[0], parts[1], parts[2], int(parts[3]), int(parts[4])
                current = total - avail
                ratio = current / total

                if ratio >= 0.9:
                    status = "Critical (Red)"
                elif ratio >= 0.5:
                    status = "Moderate (Yellow)"
                else:
                    status = "Stable (Green)"

                tree.insert("", tk.END, values=(f"{name} ({code})", current, total, status))

        tree.pack(pady=10)

    def show_search(self):
        self.clear()
        tk.Label(self.root, text="Lounge Search", font=("Arial",22,"bold")).pack(pady=20)
        tk.Label(self.root, text="Airport / Code").pack()
        self.e_search = ttk.Entry(self.root, width=40)
        self.e_search.pack(pady=5)
        ttk.Button(self.root, text="Search", command=self.do_search).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.show_home).pack()

    def do_search(self):
        key = self.e_search.get().lower().strip()
        res = []
        with open("lounge.txt","r",encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                p = line.split(",")
                code, airport, name, total, avail = p[0], p[1], p[2], int(p[3]), int(p[4])
                if key in code.lower() or key in airport.lower():
                    occ = total - avail
                    rate = f"{occ/total*100:.1f}%"
                    res.append((code, airport, name, total, avail, occ, rate))
        self.show_result(res)

    def show_result(self, lst):
        self.clear()
        tk.Label(self.root, text="Results & Occupancy", font=("Arial",22,"bold")).pack(pady=20)
        if not lst:
            tk.Label(self.root,text="No lounge found").pack()
        for item in lst:
            code, airport, name, total, avail, occ, rate = item
            frm = ttk.LabelFrame(self.root, text=name)
            frm.pack(pady=10, padx=30, fill="x")
            tk.Label(frm, text=f"Airport: {airport} ({code})").pack(anchor="w")
            tk.Label(frm, text=f"Capacity: {total} | Available: {avail}").pack(anchor="w")
            tk.Label(frm, text=f"Occupancy Rate: {rate}").pack(anchor="w")
            ttk.Button(frm, text="Book Now", command=lambda x=item: self.book(x)).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.show_search).pack(pady=10)

    def book(self, lounge):
        self.selected_lounge = lounge
        self.clear()
        tk.Label(self.root, text="Booking", font=("Arial",22,"bold")).pack(pady=30)
        tk.Label(self.root, text=f"Lounge: {lounge[2]}").pack()
        tk.Label(self.root, text=f"Airport: {lounge[1]}").pack()
        tk.Label(self.root, text="Time (YYYY-MM-DD HH:MM)").pack(pady=10)
        self.e_time = ttk.Entry(self.root, width=40)
        self.e_time.pack(pady=5)
        ttk.Button(self.root, text="Confirm Booking", command=self.confirm).pack(pady=20)
        ttk.Button(self.root, text="Back", command=self.show_search).pack()

    def confirm(self):
        t = self.e_time.get().strip()
        if not t:
            messagebox.showwarning("Warning","Please enter booking time")
            return
        code, airport, name, total, avail, occ, rate = self.selected_lounge
        with open("lounge.txt","r",encoding="utf-8") as f:
            lines = f.readlines()
        new_lines = []
        ok = False
        for line in lines:
            p = line.strip().split(",")
            if len(p)>=5 and p[1] == airport and int(p[4])>0:
                p[4] = str(int(p[4])-1)
                new_lines.append(",".join(p)+"\n")
                ok = True
            else:
                new_lines.append(line)
        if ok:
            with open("lounge.txt","w",encoding="utf-8") as f:
                f.writelines(new_lines)
            with open("order.txt","a",encoding="utf-8") as f:
                f.write(f"{self.current_user},{airport},{t}\n")
            messagebox.showinfo("Success","Booking Confirmed")
            self.show_done()
        else:
            messagebox.showerror("Failed","No available seats")

    def show_done(self):
        self.clear()
        tk.Label(self.root, text="You're all set!!", font=("Arial",24,"bold")).pack(pady=50)
        tk.Label(self.root, text="Booking Successful", font=("Arial",16)).pack()
        ttk.Button(self.root, text="Home", command=self.show_home).pack(pady=30)

    def show_bookings(self):
        self.clear()
        tk.Label(self.root, text="My Bookings", font=("Arial",22,"bold")).pack(pady=30)
        with open("order.txt","r",encoding="utf-8") as f:
            lines = f.readlines()
        user_bookings = [line.strip() for line in lines if line.startswith(self.current_user+",")]
        if not user_bookings:
            tk.Label(self.root, text="No bookings yet").pack(pady=10)
        else:
            for line in user_bookings:
                parts = line.split(",")
                if len(parts)!=3:
                    continue
                user, airport, time = parts
                frm = ttk.Frame(self.root)
                frm.pack(pady=4)
                tk.Label(frm, text=f"{airport} | {time}", font=("Arial",13)).pack(side="left", padx=5)
                ttk.Button(frm, text="Cancel", command=lambda line=line: self.cancel_booking(line)).pack(side="left")
        ttk.Button(self.root, text="Back", command=self.show_home).pack(pady=20)

    def cancel_booking(self, booking_line):
        user, airport, time = booking_line.split(",")
        if not messagebox.askyesno("Confirm","Are you sure to cancel this booking?"):
            return
        with open("order.txt","r",encoding="utf-8") as f:
            lines = f.readlines()
        new_order_lines = [l for l in lines if l.strip() != booking_line.strip()]
        with open("order.txt","w",encoding="utf-8") as f:
            f.writelines(new_order_lines)
        with open("lounge.txt","r",encoding="utf-8") as f:
            lounge_lines = f.readlines()
        new_lounge_lines = []
        for l in lounge_lines:
            p = l.strip().split(",")
            if len(p)>=5 and p[1] == airport:
                p[4] = str(int(p[4])+1)
                new_lounge_lines.append(",".join(p)+"\n")
            else:
                new_lounge_lines.append(l)
        with open("lounge.txt","w",encoding="utf-8") as f:
            f.writelines(new_lounge_lines)
        messagebox.showinfo("Success","Booking cancelled successfully")
        self.show_bookings()

if __name__ == "__main__":
    initialize_files()
    root = tk.Tk()
    FlyDreamAirGUI(root)
    root.mainloop()

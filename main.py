Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
# -----------------------------------------------------------------------------
# PURPOSE: Initialize data files if they do not exist
# -----------------------------------------------------------------------------
import os

def initialize_files():
    if not os.path.exists("lounge.txt"):
        with open("lounge.txt", "w") as f:
            f.write("John F. Kennedy International Airport,JFK Lounge,50,42\n")
            f.write("Los Angeles International Airport,LAX Lounge,40,33\n")
            f.write("London Heathrow Airport,LHR Lounge,60,51\n")
            f.write("Dubai International Airport,DXB Lounge,70,60\n")
            f.write("Singapore Changi Airport,SIN Lounge,45,38\n")

    if not os.path.exists("order.txt"):
        with open("order.txt", "w") as f:
            f.write("")

# -----------------------------------------------------------------------------
# PURPOSE: Search lounges by airport name
# -----------------------------------------------------------------------------
def search_lounge():
    print("\n----- Lounge Search -----")
    airport = input("Enter airport name: ")
    found = False

    with open("lounge.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split(",")
        if airport.lower() in parts[0].lower():
            print("Airport:         " + parts[0])
            print("Lounge Name:     " + parts[1])
            print("Total Capacity:  " + parts[2])
            print("Available:       " + parts[3])
            found = True

    if not found:
        print("No matching lounge found.")

# -----------------------------------------------------------------------------
# PURPOSE: Book a lounge and reduce available capacity
# -----------------------------------------------------------------------------
def book_lounge():
    print("\n----- Lounge Booking -----")
    airport = input("Enter airport name: ")
    username = input("Enter your username: ")
    booking_time = input("Enter booking time (YYYY-MM-DD HH:MM): ")

    with open("lounge.txt", "r") as f:
        lines = f.readlines()

    new_lines = []
    success = False

    for line in lines:
        parts = line.strip().split(",")
        if airport.lower() in parts[0].lower() and int(parts[3]) > 0:
            new_available = int(parts[3]) - 1
            new_line = parts[0] + "," + parts[1] + "," + parts[2] + "," + str(new_available) + "\n"
            new_lines.append(new_line)
            success = True

            with open("order.txt", "a") as f:
                f.write(username + "," + parts[0] + "," + booking_time + "\n")
            print("Booking successful!")
        else:
            new_lines.append(line)

    if success:
        with open("lounge.txt", "w") as f:
            f.writelines(new_lines)
    else:
        print("Booking failed: No availability or invalid airport.")

# -----------------------------------------------------------------------------
# PURPOSE: Cancel booking and restore available capacity
# -----------------------------------------------------------------------------
def cancel_booking():
    print("\n----- Cancel Booking -----")
    username = input("Enter username: ")
    airport = input("Enter airport to cancel: ")

    with open("order.txt", "r") as f:
        orders = f.readlines()

    new_orders = []
    found = False

    for order in orders:
        parts = order.strip().split(",")
        if parts[0] == username and parts[1].lower() == airport.lower():
            found = True
            with open("lounge.txt", "r") as f:
                lounges = f.readlines()

            new_lounges = []
            for lounge in lounges:
                l_parts = lounge.strip().split(",")
                if l_parts[0].lower() == airport.lower():
                    updated_avail = int(l_parts[3]) + 1
                    new_lounges.append(l_parts[0] + "," + l_parts[1] + "," + l_parts[2] + "," + str(updated_avail) + "\n")
                else:
                    new_lounges.append(lounge)

            with open("lounge.txt", "w") as f:
                f.writelines(new_lounges)
        else:
            new_orders.append(order)

    if found:
        with open("order.txt", "w") as f:
            f.writelines(new_orders)
        print("Booking cancelled successfully.")
    else:
        print("No matching booking found.")

# -----------------------------------------------------------------------------
# PURPOSE: View all bookings for a user
# -----------------------------------------------------------------------------
def view_bookings():
    print("\n----- My Bookings -----")
    username = input("Enter username: ")
    found = False

    with open("order.txt", "r") as f:
        orders = f.readlines()

    for order in orders:
...         parts = order.strip().split(",")
...         if parts[0] == username:
...             print("User: " + parts[0] + " | Airport: " + parts[1] + " | Time: " + parts[2])
...             found = True
... 
...     if not found:
...         print("No bookings found.")
... 
... # -----------------------------------------------------------------------------
... # PURPOSE: Main menu system
... # -----------------------------------------------------------------------------
... def main():
...     initialize_files()
...     while True:
...         print("\n===== FlyDreamAir Lounge Management System =====")
...         print("1. Search Lounge")
...         print("2. Book Lounge")
...         print("3. Cancel Booking")
...         print("4. View My Bookings")
...         print("0. Exit System")
... 
...         choice = input("Enter your choice: ")
... 
...         if choice == "1":
...             search_lounge()
...         elif choice == "2":
...             book_lounge()
...         elif choice == "3":
...             cancel_booking()
...         elif choice == "4":
...             view_bookings()
...         elif choice == "0":
...             print("System exited.")
...             break
...         else:
...             print("Invalid input. Please try again.")
... 
... if __name__ == "__main__":

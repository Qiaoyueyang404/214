import os

def initialize_files():
    if not os.path.exists("lounge.txt"):
        with open("lounge.txt", "w") as f:
            f.write("JFK,John F. Kennedy International Airport,JFK Lounge,220,186\n")
            f.write("LAX,Los Angeles International Airport,LAX Lounge,180,142\n")
            f.write("LHR,London Heathrow Airport,LHR Lounge,230,179\n")
            f.write("DXB,Dubai International Airport,DXB Lounge,210,165\n")
            f.write("SIN,Singapore Changi Airport,SIN Lounge,160,121\n")

    if not os.path.exists("order.txt"):
        with open("order.txt", "w") as f:
            f.write("")

def search_lounge():
    print("\n----- Lounge Search -----")
    airport = input("Enter airport name or code: ")
    found = False

    with open("lounge.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split(",")
        code = parts[0]
        airport_name = parts[1]
        lounge_name = parts[2]
        total = int(parts[3])
        available = int(parts[4])
        occupied = total - available
        occupancy_rate = (occupied / total) * 100

        if airport.lower() in code.lower() or airport.lower() in airport_name.lower():
            print(f"Airport Code:    {code}")
            print(f"Airport:         {airport_name}")
            print(f"Lounge Name:     {lounge_name}")
            print(f"Total Capacity:  {total}")
            print(f"Available:       {available}")
            print(f"Occupied:        {occupied}")
            print(f"Occupancy Rate:  {occupancy_rate:.1f}%")
            found = True

    if not found:
        print("No matching lounge found.")

def book_lounge():
    print("\n----- Lounge Booking -----")
    airport = input("Enter airport code or name: ")
    username = input("Enter your username: ")
    booking_time = input("Enter booking time (YYYY-MM-DD HH:MM): ")

    with open("lounge.txt", "r") as f:
        lines = f.readlines()

    new_lines = []
    success = False

    for line in lines:
        parts = line.strip().split(",")
        code = parts[0]
        name = parts[1]
        if (airport.lower() in code.lower() or airport.lower() in name.lower()) and int(parts[4]) > 0:
            new_available = int(parts[4]) - 1
            new_line = parts[0] + "," + parts[1] + "," + parts[2] + "," + parts[3] + "," + str(new_available) + "\n"
            new_lines.append(new_line)
            success = True

            with open("order.txt", "a") as f:
                f.write(username + "," + parts[1] + "," + booking_time + "\n")
            print("Booking successful!")
        else:
            new_lines.append(line)

    if success:
        with open("lounge.txt", "w") as f:
            f.writelines(new_lines)
    else:
        print("Booking failed: No availability or invalid airport.")

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
        if parts[0] == username and airport.lower() in parts[1].lower():
            found = True
            with open("lounge.txt", "r") as f:
                lounges = f.readlines()

            new_lounges = []
            for lounge in lounges:
                l_parts = lounge.strip().split(",")
                if airport.lower() in l_parts[1].lower() or airport.lower() in l_parts[0].lower():
                    updated_avail = int(l_parts[4]) + 1
                    new_lounges.append(l_parts[0] + "," + l_parts[1] + "," + l_parts[2] + "," + l_parts[3] + "," + str(updated_avail) + "\n")
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

def view_bookings():
    print("\n----- My Bookings -----")
    username = input("Enter username: ")
    found = False

    with open("order.txt", "r") as f:
        orders = f.readlines()

    for order in orders:
        parts = order.strip().split(",")
        if parts[0] == username:
            print("User: " + parts[0] + " | Airport: " + parts[1] + " | Time: " + parts[2])
            found = True

    if not found:
        print("No bookings found.")

def main():
    initialize_files()
    while True:
        print("\n===== FlyDreamAir Lounge Management System =====")
        print("1. Search Lounge")
        print("2. Book Lounge")
        print("3. Cancel Booking")
        print("4. View My Bookings")
        print("0. Exit System")

        choice = input("Enter your choice: ")

        if choice == "1":
            search_lounge()
        elif choice == "2":
            book_lounge()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            view_bookings()
        elif choice == "0":
            print("System exited.")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()

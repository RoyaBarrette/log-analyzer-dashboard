import sqlite3

# Connect to the database file (it is created if it doesn't exist)
connection = sqlite3.connect("logs.db")
cursor = connection.cursor()

# Make the table
cursor.execute("CREATE TABLE IF NOT EXISTS error_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, log_date TEXT, log_time TEXT, error_message TEXT)")

# Empty the table so we never get duplicates
cursor.execute("DELETE FROM error_logs")

# Open the log file and read all the lines
file = open("server_logs.txt", "r")
lines = file.readlines()
file.close()

# Go through each line
for line in lines:
    if "ERROR" in line:
        # Cut the line into 4 pieces at the spaces
        parts = line.split(" ", 3)

        log_date = parts[0]
        log_time = parts[1]
        error_message = parts[3].strip()

        # Show the error on the screen
        print(log_date, log_time, error_message)

        # Save the error in the database
        cursor.execute("INSERT INTO error_logs (log_date, log_time, error_message) VALUES (?, ?, ?)", (log_date, log_time, error_message))

# Save and close
connection.commit()
connection.close()

print("Done! Errors saved to logs.db")
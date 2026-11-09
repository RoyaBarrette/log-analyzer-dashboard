import sqlite3

# Connect to the database file (it is created if it doesn't exist)
connection = sqlite3.connect("errors.db")
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


# Read the errors back from the database
cursor.execute("SELECT log_date, log_time, error_message FROM error_logs")
rows = cursor.fetchall()

# Build the web page text
html = "<h1>Server Errors</h1>"
html = html + "<table border='1'>"
html = html + "<tr><th>Date</th><th>Time</th><th>Message</th></tr>"

for row in rows:
    html = html + "<tr><td>" + row[0] + "</td><td>" + row[1] + "</td><td>" + row[2] + "</td></tr>"

html = html + "</table>"

# Write the page to a file
page = open("errors.html", "w")
page.write(html)
page.close()


connection.close()

print("Done! Errors saved to errors.db")

#comment
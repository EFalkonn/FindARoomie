from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Find My Roomie</title>
            <style>
                /* CSS styles can go here */
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    margin: 0;
                    padding: 20px;
                }
                h1, h2 {
                    color: #333;
                    text-align: center;
                }
                form {
                    background-color: #fff;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input[type="text"], input[type="submit"] {
                    padding: 10px;
                    margin: 5px 0;
                    width: 100%;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Find My Roomie</h1>
                <form id="addRoomieForm" action="/add_roomie" method="post">
                    <h2>Add Roomie</h2>
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required><br>
                    <label for="reg_no">Registration Number:</label>
                    <input type="text" id="reg_no" name="reg_no" required><br>
                    <label for="phone_number">Phone Number:</label>
                    <input type="text" id="phone_number" name="phone_number" required><br>
                    <label for="hostel_block">Hostel Block:</label>
                    <input type="text" id="hostel_block" name="hostel_block" required><br>
                    <label for="room_no">Room Number:</label>
                    <input type="text" id="room_no" name="room_no" required><br>
                    <input type="submit" value="Add Roomie">
                </form>
                <form id="findRoomieForm" action="/find_roomie" method="post">
                    <h2>Find Roomie</h2>
                    <label for="find_hostel_block">Hostel Block:</label>
                    <input type="text" id="find_hostel_block" name="hostel_block" required><br>
                    <label for="find_room_no">Room Number:</label>
                    <input type="text" id="find_room_no" name="room_no" required><br>
                    <input type="submit" value="Find Roomie">
                </form>
                <div id="roomieResult"></div>
            </div>
            <script>
                // JavaScript code can go here
                document.getElementById('addRoomieForm').addEventListener('submit', async function(event) {
                    event.preventDefault();
                    let formData = new FormData(this);
                    let response = await fetch('/add_roomie', {
                        method: 'POST',
                        body: formData
                    });
                    let result = await response.text();
                    document.getElementById('roomieResult').innerHTML = result;
                    this.reset();
                });

                document.getElementById('findRoomieForm').addEventListener('submit', async function(event) {
                    event.preventDefault();
                    let formData = new FormData(this);
                    let response = await fetch('/find_roomie', {
                        method: 'POST',
                        body: formData
                    });
                    let result = await response.text();
                    document.getElementById('roomieResult').innerHTML = result;
                    this.reset();
                });
            </script>
        </body>
        </html>
    '''

@app.route('/add_roomie', methods=['POST'])
def add_roomie():
    name = request.form['name']
    reg_no = request.form['reg_no']
    phone_number = request.form['phone_number']
    hostel_block = request.form['hostel_block']
    room_no = request.form['room_no']

    # Connect to the database
    conn = sqlite3.connect('roomie.db')
    c = conn.cursor()
    c.execute("INSERT INTO roomies VALUES (?, ?, ?, ?, ?)",
              (name, reg_no, phone_number, hostel_block, room_no))
    conn.commit()
    conn.close()
    return 'Roomie added!'

@app.route('/find_roomie', methods=['POST'])
def find_roomie():
    hostel_block = request.form['hostel_block']
    room_no = request.form['room_no']

    # Connect to the database
    conn = sqlite3.connect('roomie.db')
    c = conn.cursor()
    c.execute("SELECT * FROM roomies WHERE hostel_block=? AND room_no=?",
              (hostel_block, room_no))
    roomies = c.fetchall()
    conn.close()

    if roomies:
        result = 'Roomies found:<br>'
        for roomie in roomies:
            result += f"Name: {roomie[0]}, Reg No: {roomie[1]}, Phone Number: {roomie[2]}<br>"
        return result
    else:
        return 'No roomies found.'

if __name__ == '__main__':
    app.run()

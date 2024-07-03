from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h1>Find My Roomie</h1>
        <form action="/add_roomie" method="post">
            <h2>Add Roomie</h2>
            Name: <input type="text" name="name"><br>
            Registration Number: <input type="text" name="reg_no"><br>
            Phone Number: <input type="text" name="phone_number"><br>
            Hostel Block: <input type="text" name="hostel_block"><br>
            Room Number: <input type="text" name="room_no"><br>
            <input type="submit" value="Add Roomie">
        </form>
        <form action="/find_roomie" method="post">
            <h2>Find Roomie</h2>
            Hostel Block: <input type="text" name="hostel_block"><br>
            Room Number: <input type="text" name="room_no"><br>
            <input type="submit" value="Find Roomie">
        </form>
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

from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector
import datetime

app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost", user="root", passwd="AbCd@123", database="railway_system")
mycursor = mydb.cursor()

current_user = 0;

def date_timesetup(given):
    return given.strftime("%m/%d/%Y, %H:%M:%S")

def redirect_url(default='index.html'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

@app.route('/')
def hello_world():  # put application's code here
    global current_user;
    current_user = 0;
    return render_template("index.html");


@app.route('/admin_login')
def admin_log():
    return render_template("admin_log.html");


@app.route('/user_login')
def user_log():
    global current_user;
    current_user = 0;
    return render_template("user_login.html");


@app.route('/Registration_screen')
def user_register():
    return render_template("Registration_screen.html");

@app.route('/admin_station')
def admin_station():
    return render_template("admin_station.html");

@app.route('/admin_seats')
def admin_seats():
    return render_template("admin_seats.html");

@app.route('/admin_afterlogin', methods = ["POST", "GET"])
def admin_afterlogin():
    if (request.method == "GET"):
        return render_template("admin_log.html");
    else:
        admin_user = str(request.form["username"])
        u_password = str(request.form["password"])
        if (admin_user=="__octopus__" and u_password=="monkey_man"):
            return render_template("admin_afterlogin.html")
        return render_template("admin_log.html");

@app.route('/About_us')
def aboutuspage():
    return render_template("about_us.html");


@app.route('/Contact_us')
def contact_us():
    return render_template("contact_us.html");


@app.route('/Browse_trains')
def browse_train():
    return render_template("browse_trains.html");


@app.route('/user_info', methods= ["POST", "GET"])
def user_info():
    global current_user;
    if (request.method == "GET"):
        return render_template("user_login.html");

    else:
        # print(request.form)
        u_adhaar = request.form["adhaar"]
        u_password = request.form["password"]

        chk_adh_str = f"SELECT * FROM users WHERE Adhaar_no='{u_adhaar}';"
        mycursor.execute(chk_adh_str);
        now_user_data_all = mycursor.fetchall();
        if (len(now_user_data_all)==0):
            return render_template("user_login.html");

        now_user_data = now_user_data_all[0];

        if now_user_data[7]!=u_password:
            return render_template("user_login.html");

        current_user = u_adhaar;

        return render_template("user_info.html", user_data = now_user_data);

@app.route('/registered', methods= ["POST", "GET"])
def regis_ok():
    if (request.method=="GET"):
        return render_template("Registration_screen.html");
    else:
        r_adhaar = request.form["adhaar"]
        r_password = request.form["password"]
        r_firstname = request.form["first_name"]
        r_lastname = request.form["last_name"]
        r_dob = request.form["DOB"]
        r_phone = request.form["phone_no"]
        r_username = request.form["username"]
        r_email = request.form["email"]
        # exc_str = f"INSERT INTO users(Adhaar_no,Username,e_mail,Mobile,DOB,First_name,Last_name,password) VALUES ({r_adhaar},'{r_username}','{r_email}',{r_phone},'{r_dob}','{r_firstname}','{r_lastname}','{r_password}');"
        # if len(r_phone)==0: render_template("Registration_screen.html");
        # if r_dob is None: render_template("Registration_screen.html");
        chk_adh_str = f"SELECT * FROM users WHERE Adhaar_no='{r_adhaar}';"
        if len(chk_adh_str)>0:
            return render_template("user_login.html");
        exc_str = f"INSERT INTO users(Adhaar_no,Username,e_mail,Mobile,DOB,First_name,Last_name,passwords) VALUES({str(r_adhaar)}, '{r_username}', '{r_email}', {str(r_phone)}, '{r_dob}', '{r_firstname}', '{r_lastname}', '{r_password}');"
        print(exc_str);
        mycursor.execute(exc_str);
        # useless = mycursor.fetchall();
        mydb.commit();

        # print("INSERT INTO users(Adhaar_no,Username,e_mail,Mobile,DOB,First_name,Last_name,password) VALUES({}, '{}', '{}', {}, '{}', '{}', '{}', '{}');".format(r_adhaar,r_username,r_email,r_phone,r_dob,r_firstname,r_lastname,r_password))

        return render_template("registered.html");

@app.route('/station_added', methods=["POST", "GET"])
def congo_station():
    if (request.method == "GET"):
        return render_template("admin_station.html");
    else:
        station_name = request.form["station_name"]
        terminal_count = int(request.form["terminal_count"])
        if (terminal_count<1): return render_template("admin_station.html");

        cnt_allsttn = f"SELECT MAX(Station_id) FROM station;"
        mycursor.execute(cnt_allsttn)
        new_station_id = int((mycursor.fetchall())[0][0]) + 1;

        adding_new_station = f"INSERT INTO station(Station_id, Station_name, No_of_terminals) VALUES({str(new_station_id)}, '{station_name}', {str(terminal_count)});"
        mycursor.execute(adding_new_station)
        mydb.commit();

        for ti in range(1, terminal_count+1):
            adding_new_terminal = f"INSERT INTO terminal(Terminal_id, Station_id) VALUES ({str((new_station_id)*10 + ti)}, {str(new_station_id)});"
            mycursor.execute(adding_new_terminal)
            mydb.commit();


        return render_template("station_added.html");


@app.route('/available_trains', methods = ["POST", "GET"])
def available_trains():
    if (request.method == "GET"):
        return render_template("index.html");
    else:
        # print(request.form)
        from_station = request.form["from_station"]
        from_station = from_station.title()
        from_station = from_station.replace(" ", "_")
        to_station = request.form["to_station"]
        to_station = to_station.title()
        to_station = to_station.replace(" ", "_")
        print(from_station, to_station)
        chk_start = f"SELECT * FROM station WHERE Station_name='{from_station}';"
        mycursor.execute(chk_start);
        start_station_list = mycursor.fetchall();
        if len(start_station_list)<1:
            return render_template("index.html")
        chk_end = f"SELECT * FROM station WHERE Station_name='{to_station}';"
        mycursor.execute(chk_end);
        end_station_list = mycursor.fetchall();
        if len(end_station_list)<1:
            return render_template("index.html")

        start_station = start_station_list[0]
        end_station = end_station_list[0]
        # cheking printing; and its working
        # print(start_station)
        # print(end_station)
        start_station_id = start_station[0]
        end_station_id = end_station[0]
        get_all_route = f"SELECT * FROM route WHERE (Start_station_id='{start_station_id}' OR Start_station_id='{end_station_id}');"
        mycursor.execute(get_all_route)
        all_route_list = mycursor.fetchall();
        # checkpoint 2 success
        # print(all_route_list);
        # print(len(all_route_list))
        all_route_list.sort(key=lambda x:x[0])
        final_route_list = []
        ir = 0
        lnr = len(all_route_list)
        while(ir<lnr-1):
            if (all_route_list[ir][5]!=start_station_id):
                ir+=1
                continue
            if (all_route_list[ir+1][5]==start_station_id):
                ir+=1
                continue
            if (all_route_list[ir][7]!=all_route_list[ir+1][7]):
                ir+=1
                continue
            final_route_list.append(all_route_list[ir])
            final_route_list.append(all_route_list[ir+1])
            ir+=2
        # print(final_route_list)
        train_name_dict = {}
        for i in final_route_list:
            # print(i[7])
            trnfind = f"SELECT Train_name FROM train WHERE Train_id={i[7]};"
            mycursor.execute(trnfind)
            train_ka_naam = (mycursor.fetchall())[0][0]
            train_name_dict[i[7]] = train_ka_naam

        # Another checkpoint working fine
        # for i in final_route_list:
        #     print(i[7])
        #     print(train_name_dict[i[7]])

        # if len(final_route_list)<1:
        #     return render_template()
        final_render_list = []
        for i in range(0, len(final_route_list)-1, 2):
            xrender = [(i//2)+1, final_route_list[i][7], train_name_dict[final_route_list[i][7]], from_station, date_timesetup(final_route_list[i][4]), to_station, date_timesetup(final_route_list[i+1][3])]
            final_render_list.append(xrender)

        print(final_render_list)
        return render_template("available_trains.html", final_render_list=final_render_list)

    # return render_template("available_trains.html")

@app.route('/All_ticket_list', methods = ["GET", "POST"])
def all_ticket_list():
    global current_user;
    if (request.method == "GET"):
        return render_template("index.html");
    else:
        # if (current_user==0):
        #     return render_template("index.html")
        get_tcks_list = f"SELECT * FROM passenger WHERE Adhaar_no={current_user};"
        mycursor.execute(get_tcks_list);
        all_tckt = mycursor.fetchall();
        final_render_list = []
        for i in range(len(all_tckt)):
            xrender = [i+1, all_tckt[i][0], date_timesetup(all_tckt[i][2])]
            frm_st = f"SELECT Station_name FROM station WHERE Station_id={all_tckt[i][5]};"
            mycursor.execute(frm_st)
            xrender.append(mycursor.fetchall()[0][0])
            to_st = f"SELECT Station_name FROM station WHERE Station_id={all_tckt[i][6]};"
            mycursor.execute(to_st)
            xrender.append(mycursor.fetchall()[0][0])
            trn_nme = f"SELECT Train_name FROM train WHERE Train_id={all_tckt[i][9]};"
            mycursor.execute(trn_nme)
            xrender.append(mycursor.fetchall()[0][0])
            print(xrender)
            final_render_list.append(xrender)

        print(final_render_list)
        return render_template("All_ticket_list.html", final_render_list=final_render_list);




@app.route('/Booking_details', methods = ["GET", "POST"])
def booking_details():
    global current_user
    if (request.method == "GET"):
        return render_template("index.html");
    else:
        ticket_id = request.form["ticket_id_show"]
        # print(ticket_id)
        get_tck = f"SELECT * FROM passenger WHERE Ticket_id = {ticket_id};"
        mycursor.execute(get_tck)
        all_tck = mycursor.fetchall()
        if len(all_tck)==0:
            return redirect_url()
        this_tck = all_tck[0]
        if this_tck[1]!=current_user:
            return redirect_url()



        return render_template("booking_details.html")


if __name__ == '__main__':
    app.run()

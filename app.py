from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector
import datetime

app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost", user="root", passwd="AbCd@123", database="railway_system")
mycursor = mydb.cursor()

current_user = 0;
station_booking=[]  # only 2 arguments from_station_id to_station_id

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
    # global current_user
    if (request.method == "GET"):
        return render_template("index.html");
    else:
        global current_user
        ticket_id = request.form["ticket_id_show"]
        # ticket_id = (request.args.get("ticket_id_show"))
        print(ticket_id)
        get_tck = f"SELECT * FROM passenger WHERE Ticket_id = {ticket_id};"
        mycursor.execute(get_tck)
        all_tck = mycursor.fetchall()
        print(all_tck)
        print(current_user)
        if len(all_tck)==0:
            return render_template("index.html")
        this_tck = all_tck[0]
        # if this_tck[1]!=current_user:
        #     return redirect_url("index.html")

        final_render_list = []
        frm_st = f"SELECT Station_name FROM station WHERE Station_id={this_tck[5]};"
        mycursor.execute(frm_st)
        final_render_list.append(mycursor.fetchall()[0][0])
        to_st = f"SELECT Station_name FROM station WHERE Station_id={this_tck[6]};"
        mycursor.execute(to_st)
        final_render_list.append(mycursor.fetchall()[0][0])
        ch_name = f"SELECT Coach_name FROM coach WHERE Coach_id={this_tck[3]};"
        mycursor.execute(ch_name)
        final_render_list.append(mycursor.fetchall()[0][0])
        final_render_list.append(this_tck[7])
        final_render_list.append(this_tck[8])
        arrvt = f"SELECT Arrival_time FROM route WHERE Train_id={this_tck[9]} AND Start_station_id={this_tck[6]};"
        mycursor.execute(arrvt);
        final_render_list.append(date_timesetup((mycursor.fetchall())[0][0]))
        # print(mycursor.fetchall())
        depvt = f"SELECT Departure_time FROM route WHERE Train_id={this_tck[9]} AND Start_station_id={this_tck[5]};"
        mycursor.execute(depvt);
        final_render_list.append((date_timesetup((mycursor.fetchall())[0][0])))
        # print(mycursor.fetchall())

        print(final_render_list)

        return render_template("booking_details.html", final_render_list=final_render_list);


@app.route("/available_trains_userin", methods = ["GET", "POST"])
def available_trains_userin():
    if (request.method == "GET"):
        return render_template("index.html");
    else:
        global current_user
        global station_booking
        from_station = request.form["from_station"]
        from_station = from_station.title()
        from_station = from_station.replace(" ", "_")
        to_station = request.form["to_station"]
        to_station = to_station.title()
        to_station = to_station.replace(" ", "_")

        # coach_req = request.form["coach_req"]
        # date_want = request.form["date_want"]

        chk_start = f"SELECT * FROM station WHERE Station_name='{from_station}';"
        mycursor.execute(chk_start);
        start_station_list = mycursor.fetchall();
        if len(start_station_list) < 1:
            return render_template("index.html")
        chk_end = f"SELECT * FROM station WHERE Station_name='{to_station}';"
        mycursor.execute(chk_end);
        end_station_list = mycursor.fetchall();
        if len(end_station_list) < 1:
            return render_template("index.html")

        start_station = start_station_list[0]
        end_station = end_station_list[0]


        start_station_id = start_station[0]
        end_station_id = end_station[0]
        get_all_route = f"SELECT * FROM route WHERE (Start_station_id='{start_station_id}' OR Start_station_id='{end_station_id}');"
        mycursor.execute(get_all_route)
        all_route_list = mycursor.fetchall();
        # checkpoint 2 success
        # print(all_route_list);
        # print(len(all_route_list))
        all_route_list.sort(key=lambda x: x[0])
        final_route_list = []
        ir = 0
        lnr = len(all_route_list)
        while (ir < lnr - 1):
            if (all_route_list[ir][5] != start_station_id):
                ir += 1
                continue
            if (all_route_list[ir + 1][5] == start_station_id):
                ir += 1
                continue
            if (all_route_list[ir][7] != all_route_list[ir + 1][7]):
                ir += 1
                continue
            final_route_list.append(all_route_list[ir])
            final_route_list.append(all_route_list[ir + 1])
            ir += 2
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
        for i in range(0, len(final_route_list) - 1, 2):
            xrender = [(i // 2) + 1, final_route_list[i][7], train_name_dict[final_route_list[i][7]], from_station,
                       date_timesetup(final_route_list[i][4]), to_station,
                       date_timesetup(final_route_list[i + 1][3])]
            coaches_data = f"SELECT Coach_name FROM coach WHERE Train_id={final_route_list[i][7]};"
            mycursor.execute(coaches_data);
            coaches_naam = mycursor.fetchall();
            print(coaches_naam)
            final_coaches_naam = []
            for j in coaches_naam:
                final_coaches_naam.append(j[0])
            xrender.append(final_coaches_naam)
            final_render_list.append(xrender)
            # global ssi
            # ssi = start_station_id
            # global esi
            # esi = end_station_id
            station_booking = [];
            station_booking.append(start_station_id)
            station_booking.append(end_station_id)
        return render_template("available_trains_userin.html", final_render_list = final_render_list);


@app.route("/ticket_booked", methods=["POST", "GET"])
def ticket_booked():
    if (request.method == "GET"):
        return render_template("index.html");
    else:
        global current_user;
        global station_booking;
        train_id = request.form["train_id"]
        coach_name = request.form["coach_name"]
        # av_seats = f"UPDATE train SET Available_seats=Available_seats-1 WHERE Train_id = '{train_id}' ';"
        all_route_lst = f"SELECT * FROM route WHERE Train_id={train_id};"
        mycursor.execute(all_route_lst);
        route_list_now = mycursor.fetchall();
        if len(route_list_now)<2:
            return render_template("index.html");

        first_route_id = 0
        last_route_id = 0

        for i in route_list_now:
            if i[5]==station_booking[0]:
                first_route_id = i[0]
                break

        for i in route_list_now:
            if i[5]==station_booking[1]:
                last_route_id = i[0]
                break



        start_term_id, end_term_id = 0, 0;

        for i in route_list_now:
            if i[5]==station_booking[0]:
                start_term_id = i[1]
                break

        for i in route_list_now:
            if i[5]==station_booking[1]:
                end_term_id = i[1]
                break

        for i in route_list_now:
            if (i[0]<last_route_id) and (i[0]>=first_route_id):
                if coach_name=="Genral":
                    chstr = f"UPDATE route SET Seats_General = Seats_General - 1 WHERE Route_id={i[0]};"
                    mycursor.execute(chstr);
                    mydb.commit()
                elif coach_name=="AC_1":
                    chstr = f"UPDATE route SET Seats_AC1 = Seats_AC1 - 1 WHERE Route_id={i[0]};"
                    mycursor.execute(chstr);
                    mydb.commit()
                else:
                    chstr = f"UPDATE route SET Seats_AC2 = Seats_AC2 - 1 WHERE Route_id={i[0]};"
                    mycursor.execute(chstr);
                    mydb.commit()




        coach_id_str = f"SELECT Coach_id FROM coach WHERE (Train_id={train_id} AND Coach_name ='{coach_name}');"
        mycursor.execute(coach_id_str);
        coach_id = mycursor.fetchall()[0][0]
        ticket_id_str = f"SELECT max(Ticket_id) FROM passenger;"
        mycursor.execute(ticket_id_str)
        ticket_id = mycursor.fetchall()[0][0]
        ticket_id+=5
        now = datetime.datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S") #"2022-09-06 20:50:32"
        # route_id = 0

        # adding_ticket = f"INSERT INTO passenger(Ticket_id,Adhaar_no,Date_of_Booking,Coach_id,Route_id,Start_station_id,End_station_id,Start_terminal_id,End_terminal_id,Train_id) " \
        #                 f"VALUES({ticket_id}, {current_user}, {dt},{coach_id},{Route_id},{station_booking[-2]},{station_booking[-1]},{},{},{train_id});"
        add_tck_str = f"INSERT INTO passenger(Ticket_id, Adhaar_no, Date_of_Booking, Coach_id, Route_id, Start_station_id, End_Station_id, Start_terminal_id, End_terminal_id, Train_id) VALUES ({str(ticket_id)},{str(current_user)},'{dt}', {str(coach_id)}, {str(first_route_id)}, {str(station_booking[0])}, {str(station_booking[1])}, {str(start_term_id)}, {str(end_term_id)}, {str(train_id)});"
        print(add_tck_str)
        mycursor.execute(add_tck_str);
        mydb.commit()
        pass_str = f"SELECT passwords FROM users WHERE Adhaar_no={current_user};"
        mycursor.execute(pass_str);
        pasw = (mycursor.fetchall())[0][0]
        return render_template("ticket_booked.html", thisuser = current_user, thispasswd = pasw);


@app.route('/ticket_cancelled', methods=["GET", "POST"])
def ticket_cancelled():
    if (request.method == "GET"):
        return render_template("index.html");
    else:
        global current_user;
        ticket_id = request.form["ticket_id_show"]
        gettckstr = f"SELECT * FROM passenger WHERE Ticket_id={ticket_id};"
        mycursor.execute(gettckstr);
        req_tck = mycursor.fetchall()

        pass_str = f"SELECT passwords FROM users WHERE Adhaar_no={current_user};"
        mycursor.execute(pass_str);
        pasw = (mycursor.fetchall())[0][0]
        if len(req_tck)<1:
            return render_template("ticket_cancelled.html", thisuser=current_user, thispasswd=pasw)

        this_tck = req_tck[0]
        coach_id = this_tck[3]
        train_id = this_tck[9]
        first_route_id = this_tck[4]
        last_route_id = 0
        get_coach_str = f"SELECT Coach_name FROM coach WHERE Coach_id={coach_id}"
        mycursor.execute(get_coach_str)
        coach_name = (mycursor.fetchall())[0][0]

        get_all_rts = f"SELECT * FROM route WHERE Train_id={train_id};"
        mycursor.execute(get_all_rts)
        all_routes = mycursor.fetchall();
        start_station_id = this_tck[5];
        end_station_id = this_tck[6];

        for i in all_routes:
            if i[5]==end_station_id:
                last_route_id = i[0]

        # for i in all_routes:
        #     if (i[0]<last_route_id) and (i[0]>=first_route_id):
        #         if coach_name=="Genral":
        #             chstr = f"UPDATE route SET Seats_General = Seats_General + 1 WHERE Route_id={i[0]};"
        #             mycursor.execute(chstr);
        #             mydb.commit()
        #         elif coach_name=="AC_1":
        #             chstr = f"UPDATE route SET Seats_AC1 = Seats_AC1 + 1 WHERE Route_id={i[0]};"
        #             mycursor.execute(chstr);
        #             mydb.commit()
        #         else:
        #             chstr = f"UPDATE route SET Seats_AC2 = Seats_AC2 + 1 WHERE Route_id={i[0]};"
        #             mycursor.execute(chstr);
        #             mydb.commit()

        main_delete = f"DELETE FROM passenger WHERE Ticket_id={ticket_id};"
        mycursor.execute(main_delete)
        mydb.commit();






        return render_template("ticket_cancelled.html", thisuser = current_user, thispasswd = pasw)

if __name__ == '__main__':
    app.run()

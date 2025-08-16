from flask import Flask,render_template, request, redirect, url_for, flash
from application.database import db
from application.models import *

app=Flask(__name__)
app.config['SECRET_KEY'] = 'your-unique-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)
app.app_context().push()

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists
        existing_user = users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('userlogin'))

        # Create a new user (no password hashing for simplicity)
        new_user = users(email=email, password_hash=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Signup successful. You can now log in.', 'success')
        return redirect(url_for('userlogin'))

    return render_template('signup.html')

@app.route('/registered')
def registered():
    return render_template('registered.html')

@app.route('/headlogin', methods=['GET', 'POST'])
def headlogin():
    if request.method == 'POST':
        email = request.form['heademail']
        password = request.form['headpassword']
        
        if email == 'adminhead@gmail.com' and password == 'adminhead':
            flash('Head login successful!', 'success')
            return redirect(url_for('head_home', user_type='Head'))
        else:
            flash('Invalid head credentials. Please try again.', 'danger')
            return redirect(url_for('headlogin'))
    
    return render_template('headlogin.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['adminemail']
        login_key = request.form['adminpassword']

        admin = officials.query.filter_by(email=email, login_key=login_key).first()
        if admin:
            return redirect(url_for('admin_home', user_type='Admin'))
        else:
            flash('Invalid admin credentials. Please try again.', 'danger')
            return redirect(url_for('adminlogin'))

    return render_template('adminlogin.html')

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        email = request.form['useremail']
        password = request.form['userpassword']
        
        user = users.query.filter_by(email=email, password_hash=password).first()
        
        if user:
            flash('Login successful!', 'success')
            return redirect(url_for('user_home', user_type='User'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('userlogin'))
    
    return render_template('userlogin.html')

@app.route('/admins', methods=['GET', 'POST'])
def admins():
    if request.method == 'POST':
        email = request.form['newadminemail']
        login_key = request.form['newadminpassword']

        # Check if admin email already exists
        existing_admin = officials.query.filter_by(email=email).first()
        if existing_admin:
            flash('An admin with this email already exists.', 'danger')
            return redirect(url_for('admins'))

        # Create a new admin entry
        new_admin = officials(email=email, login_key=login_key, registered_by_head=True)
        db.session.add(new_admin)
        db.session.commit()

        flash('New admin added successfully.', 'success')
        return redirect(url_for('registered'))

    return render_template('admins.html')

@app.route('/admin_home')
def admin_home():
    return render_template('admin_home.html', user_type='Admin')

@app.route('/head_home')
def head_home():
    return render_template('head_home.html', user_type='Head')

@app.route('/user_home')
def user_home():
    return render_template('user_home.html', user_type='User')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/home/case_details')
def case_details():
    return render_template('case_details.html')

@app.route('/home/filter_cases')
def filter():
    return render_template('filter.html')

@app.route('/submission_success')
def submission_success():
    return render_template('submission_success.html')

@app.route('/updation_success')
def updation_success():
    return render_template('updation_success.html')

@app.route('/home/create_a_new_case',methods=['GET','POST'])
def new_case():
    if request.method=='POST':
        # Adding a new CaseDetails record
        cnr_no = request.form.get('cnr_no')
        case_no = request.form.get('case_no')
        status_id = request.form.get('status_id')
        status = request.form.get('status')
        fir_no = request.form.get('fir_no')
        file_name = request.form.get('file_name')
        new_case_details = Case_details(cnr_no=cnr_no, case_no=case_no, status_id=status_id, status=status, fir_no=fir_no, file_name=file_name)
        db.session.add(new_case_details)

        # Adding a new Prosecutor record
        prosecutor_name = request.form.get('prosecutor_name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        address = request.form.get('address')
        new_prosecutor = prosecutor(cnr_no=cnr_no, name=prosecutor_name, age=age, sex=sex, address=address, file_name=file_name)
        db.session.add(new_prosecutor)

        # Adding associated phone numbers for the Prosecutor
        phone_numbers_list = request.form.getlist('phone_number[]')
        for phone_number in phone_numbers_list:
            new_phone_number = phone_numbers(number=phone_number, file_name=file_name)
            db.session.add(new_phone_number)

        # Adding a new PoliceStation record
        station_name = request.form.get('station_name')
        inspector_name = request.form.get('inspector_name')
        fir_date_str = request.form.get('fir_date')
        fir_date = datetime.strptime(fir_date_str, '%Y-%m-%d').date()
        new_police_station = police_station(cnr_no=cnr_no, station_name=station_name, inspector_name=inspector_name, fir_date=fir_date, fir_no=fir_no)
        db.session.add(new_police_station)

        # Adding a new CaseHistory record
        incident_date_str = request.form.get('incident_date')
        incident_time_str = request.form.get('incident_time')
        incident_date = datetime.strptime(incident_date_str, "%Y-%m-%d").date()
        incident_time = datetime.strptime(incident_time_str, "%H:%M").time()
        incident_location = request.form.get('incident_location')
        defence_name = request.form.get('defence_name')
        new_case_history = case_history(status_id=status_id, cnr_no=cnr_no, incident_date=incident_date, incident_time=incident_time, incident_location=incident_location, defence_name=defence_name)
        db.session.add(new_case_history)

        # Adding new Acts associated with the CaseHistory
        act_names = request.form.getlist('act_name[]')
        for act_name in act_names:
            new_act = acts(status_id=status_id, act_name=act_name)
            db.session.add(new_act)

        # Adding new Sections associated with the CaseHistory
        section_names = request.form.getlist('section_name[]')
        for section_name in section_names:
            new_section = sections(status_id=status_id, section_name=section_name)
            db.session.add(new_section)

        # Adding new Witnesses associated with the CaseHistory
        witness_names = request.form.getlist('witness_name[]')
        for witness_name in witness_names:
            new_witness = witnesses(name=witness_name, status_id=status_id)
            db.session.add(new_witness)

        # Adding a new CourtDetails record
        court_id = request.form.get('court_id')
        lawyer_id = request.form.get('lawyer_id')
        judge_id = request.form.get('judge_id')
        hearing_date_str = request.form.get('hearing_date')
        hearing_date = datetime.strptime(hearing_date_str, "%Y-%m-%d").date()
        court_location = request.form.get('court_location')
        new_court_details = court_details(case_no=case_no, cnr_no=cnr_no, court_id=court_id, lawyer_id=lawyer_id, judge_id=judge_id, hearing_date=hearing_date, court_location=court_location)
        db.session.add(new_court_details)

        # Commit the session to save all records
        db.session.commit()
        return redirect(url_for('submission_success'))
    
    return render_template('new_case.html')

@app.route('/home/search_case', methods=['GET', 'POST'])
def search_case():
    if request.method == 'POST':
        # Get the CNR number from the form
        cnr_no = request.form.get('cnr_no')
        
        # Search for the case in the database by CNR number
        case_details = Case_details.query.get(cnr_no)
        
        # Check if the case exists
        if case_details:
            # If case exists, redirect to the update case page with the CNR number
            return redirect(url_for('update_case', cnr_no=cnr_no))
        else:
            # If case doesn't exist, show a message (optional)
            flash('Case not found. Please check the CNR number and try again.', 'danger')
            return render_template('search_case.html')
    
    # Render the search page
    return render_template('search_case.html')

@app.route('/home/update_case/<cnr_no>', methods=['GET', 'POST'])
def update_case(cnr_no):
    # Fetch the case details using the provided CNR number
    case_details = Case_details.query.filter_by(cnr_no=cnr_no).first()
    prosecutor_details = prosecutor.query.filter_by(cnr_no=cnr_no).first()
    police_station_details = police_station.query.filter_by(cnr_no=cnr_no).first()
    case_history_details = case_history.query.filter_by(cnr_no=cnr_no).first()
    c_details = court_details.query.filter_by(cnr_no=cnr_no).first()
    phone_numbers_details = phone_numbers.query.filter_by(file_name=case_details.file_name).all()

    # Cache current status_id before updating
    old_status_id = case_details.status_id

    if request.method == 'POST':
        # Update case details
        case_details.case_no = request.form['case_no']
        case_details.status = request.form['status']
        case_details.fir_no = request.form['fir_no']
        case_details.file_name = request.form['file_name']
        case_details.status_id = request.form['status_id']
        
        # Update prosecutor details
        prosecutor_details.name = request.form['prosecutor_name']
        prosecutor_details.age = request.form['age']
        prosecutor_details.sex = request.form['sex']
        prosecutor_details.address = request.form['address']
        
        # Update police station details
        police_station_details.station_name = request.form['station_name']
        police_station_details.inspector_name = request.form['inspector_name']
        fir_date_str = request.form['fir_date']
        police_station_details.fir_date = datetime.strptime(fir_date_str, '%Y-%m-%d').date()
        
        # Update case history details
        incident_date_str = request.form['incident_date']
        incident_time_str = request.form['incident_time']
        case_history_details.incident_date = datetime.strptime(incident_date_str, "%Y-%m-%d").date()
        try:
            # Try parsing with seconds first
            case_history_details.incident_time = datetime.strptime(incident_time_str, "%H:%M:%S").time()
        except ValueError:
            # Fallback to parsing without seconds if seconds are missing
            case_history_details.incident_time = datetime.strptime(incident_time_str, "%H:%M").time()

        case_history_details.incident_location = request.form['incident_location']
        case_history_details.defence_name = request.form['defence_name']
        
        # Update or add phone numbers
        new_phone_numbers = request.form.getlist('phone_number[]')
        for i, phone_number in enumerate(new_phone_numbers):
            if i < len(phone_numbers_details):
                phone_numbers_details[i].number = phone_number
            else:
                new_phone = phone_numbers(number=phone_number, file_name=case_details.file_name)
                db.session.add(new_phone)

        # Remove extra phone numbers if the new list is shorter
        if len(new_phone_numbers) < len(phone_numbers_details):
            for j in range(len(new_phone_numbers), len(phone_numbers_details)):
                db.session.delete(phone_numbers_details[j])
        
        # Update court details
        c_details.court_id = request.form['court_id']
        c_details.lawyer_id = request.form['lawyer_id']
        c_details.judge_id = request.form['judge_id']
        hearing_date_str = request.form['hearing_date']
        c_details.hearing_date = datetime.strptime(hearing_date_str, "%Y-%m-%d").date()
        c_details.court_location = request.form['court_location']

        # If the status_id has changed, update associated acts, sections, and witnesses
        if old_status_id != case_details.status_id:
            # Delete old associations
            acts.query.filter_by(status_id=old_status_id).delete()
            sections.query.filter_by(status_id=old_status_id).delete()
            witnesses.query.filter_by(status_id=old_status_id).delete()

            # Add new associations
            act_names = request.form.getlist('act_name')
            for act_name in act_names:
                new_act = acts(status_id=case_details.status_id, act_name=act_name)
                db.session.add(new_act)

            section_names = request.form.getlist('section_name')
            for section_name in section_names:
                new_section = sections(status_id=case_details.status_id, section_name=section_name)
                db.session.add(new_section)

            witness_names = request.form.getlist('witness_name')
            for witness_name in witness_names:
                new_witness = witnesses(status_id=case_details.status_id, name=witness_name)
                db.session.add(new_witness)
        else:
            # Update existing associations if status_id hasn't changed
            act_names = request.form.getlist('act_name')
            for act, act_name in zip(acts.query.filter_by(status_id=case_details.status_id).all(), act_names):
                act.act_name = act_name

            section_names = request.form.getlist('section_name')
            for section, section_name in zip(sections.query.filter_by(status_id=case_details.status_id).all(), section_names):
                section.section_name = section_name

            witness_names = request.form.getlist('witness_name')
            for witness, witness_name in zip(witnesses.query.filter_by(status_id=case_details.status_id).all(), witness_names):
                witness.name = witness_name

        db.session.commit()  # Commit changes to the database
        
        return redirect(url_for('updation_success'))

    return render_template(
        'update_case.html',
        case_details=case_details,
        prosecutor_details=prosecutor_details,
        police_station_details=police_station_details,
        case_history_details=case_history_details,
        acts_details=acts.query.filter_by(status_id=case_details.status_id).all(),
        sections_details=sections.query.filter_by(status_id=case_details.status_id).all(),
        witnesses_details=witnesses.query.filter_by(status_id=case_details.status_id).all(),
        court_details=c_details,
        phone_numbers_details=phone_numbers_details
    )  # Redirect to the same page to see updated data

@app.route('/cnr_number', methods=['GET', 'POST'])
def cnr_number():
    if request.method == 'POST':
        # Get the CNR number from the form
        cnr_no = request.form.get('cnr_no')  # corrected to match input name

        # Search for the case in the database by CNR number
        case_details = Case_details.query.filter_by(cnr_no=cnr_no).first()

        if case_details:
            #cnr_no = case_details.cnr_no
            prosecutor_data = prosecutor.query.filter_by(cnr_no=cnr_no).first()
            police_station_data = police_station.query.filter_by(cnr_no=cnr_no).first()
            case_history_data = case_history.query.filter_by(cnr_no=cnr_no).first()
            acts_data = acts.query.filter_by(status_id=case_details.status_id).all()
            sections_data = sections.query.filter_by(status_id=case_details.status_id).all()
            witnesses_data = witnesses.query.filter_by(status_id=case_details.status_id).all()
            court_details_data = court_details.query.filter_by(cnr_no=cnr_no).first()
            phone_numbers_data = phone_numbers.query.filter_by(file_name=case_details.file_name).all()

            return render_template(
                'case_info.html',
                case_details=case_details,
                prosecutor=prosecutor_data,
                police_station=police_station_data,
                case_history=case_history_data,
                acts=acts_data,
                sections=sections_data,
                witnesses=witnesses_data,
                court_details=court_details_data,
                phone_numbers=phone_numbers_data
            )
        else:
            flash('No matching case found for the provided CNR number.', 'danger')
            return redirect(url_for('cnr_number'))

    return render_template('cnr_number.html')

@app.route('/case_number', methods=['GET', 'POST'])
def case_number():
    if request.method == 'POST':
        case_no = request.form.get('case_no')

        # Search for the case by Case Number
        case_details = Case_details.query.filter_by(case_no=case_no).first()

        if case_details:
            prosecutor_data = prosecutor.query.filter_by(cnr_no=case_details.cnr_no).first()
            police_station_data = police_station.query.filter_by(cnr_no=case_details.cnr_no).first()
            case_history_data = case_history.query.filter_by(cnr_no=case_details.cnr_no).first()
            acts_data = acts.query.filter_by(status_id=case_details.status_id).all()
            sections_data = sections.query.filter_by(status_id=case_details.status_id).all()
            witnesses_data = witnesses.query.filter_by(status_id=case_details.status_id).all()
            court_details_data = court_details.query.filter_by(cnr_no=case_details.cnr_no).first()
            phone_numbers_data = phone_numbers.query.filter_by(file_name=case_details.file_name).all()

            return render_template(
                'case_info.html',
                case_details=case_details,
                prosecutor=prosecutor_data,
                police_station=police_station_data,
                case_history=case_history_data,
                acts=acts_data,
                sections=sections_data,
                witnesses=witnesses_data,
                court_details=court_details_data,
                phone_numbers=phone_numbers_data
            )
        else:
            flash('No matching case found for the provided Case Number.', 'danger')
            return redirect(url_for('case_number'))

    return render_template('case_number.html')

@app.route('/file_name', methods=['GET', 'POST'])
def file_name():
    if request.method == 'POST':
        file_name = request.form.get('file_name')

        # Search for the case by File Name
        case_details = Case_details.query.filter_by(file_name=file_name).first()

        if case_details:
            prosecutor_data = prosecutor.query.filter_by(cnr_no=case_details.cnr_no).first()
            police_station_data = police_station.query.filter_by(cnr_no=case_details.cnr_no).first()
            case_history_data = case_history.query.filter_by(cnr_no=case_details.cnr_no).first()
            acts_data = acts.query.filter_by(status_id=case_details.status_id).all()
            sections_data = sections.query.filter_by(status_id=case_details.status_id).all()
            witnesses_data = witnesses.query.filter_by(status_id=case_details.status_id).all()
            court_details_data = court_details.query.filter_by(cnr_no=case_details.cnr_no).first()
            phone_numbers_data = phone_numbers.query.filter_by(file_name=case_details.file_name).all()

            return render_template(
                'case_info.html',
                case_details=case_details,
                prosecutor=prosecutor_data,
                police_station=police_station_data,
                case_history=case_history_data,
                acts=acts_data,
                sections=sections_data,
                witnesses=witnesses_data,
                court_details=court_details_data,
                phone_numbers=phone_numbers_data
            )
        else:
            flash('No matching case found for the provided File Name.', 'danger')
            return redirect(url_for('file_name'))
    return render_template('file_name.html')

@app.route('/fir_number', methods=['GET', 'POST'])
def fir_number():
    if request.method == 'POST':
        fir_no = request.form.get('fir_no')

        # Search for the case by FIR Number
        case_details = Case_details.query.filter_by(fir_no=fir_no).first()

        if case_details:
            prosecutor_data = prosecutor.query.filter_by(cnr_no=case_details.cnr_no).first()
            police_station_data = police_station.query.filter_by(cnr_no=case_details.cnr_no).first()
            case_history_data = case_history.query.filter_by(cnr_no=case_details.cnr_no).first()
            acts_data = acts.query.filter_by(status_id=case_details.status_id).all()
            sections_data = sections.query.filter_by(status_id=case_details.status_id).all()
            witnesses_data = witnesses.query.filter_by(status_id=case_details.status_id).all()
            court_details_data = court_details.query.filter_by(cnr_no=case_details.cnr_no).first()
            phone_numbers_data = phone_numbers.query.filter_by(file_name=case_details.file_name).all()

            return render_template(
                'case_info.html',
                case_details=case_details,
                prosecutor=prosecutor_data,
                police_station=police_station_data,
                case_history=case_history_data,
                acts=acts_data,
                sections=sections_data,
                witnesses=witnesses_data,
                court_details=court_details_data,
                phone_numbers=phone_numbers_data
            )
        else:
            flash('No matching case found for the provided FIR Number.', 'danger')
            return redirect(url_for('fir_number'))
    return render_template('fir_number.html')

@app.route('/status_id', methods=['GET', 'POST'])
def status_id():
    if request.method == 'POST':
        status_id = request.form.get('status_id')

        # Search for the case by Status ID
        case_details = Case_details.query.filter_by(status_id=status_id).first()

        if case_details:
            prosecutor_data = prosecutor.query.filter_by(cnr_no=case_details.cnr_no).first()
            police_station_data = police_station.query.filter_by(cnr_no=case_details.cnr_no).first()
            case_history_data = case_history.query.filter_by(cnr_no=case_details.cnr_no).first()
            acts_data = acts.query.filter_by(status_id=case_details.status_id).all()
            sections_data = sections.query.filter_by(status_id=case_details.status_id).all()
            witnesses_data = witnesses.query.filter_by(status_id=case_details.status_id).all()
            court_details_data = court_details.query.filter_by(cnr_no=case_details.cnr_no).first()
            phone_numbers_data = phone_numbers.query.filter_by(file_name=case_details.file_name).all()

            return render_template(
                'case_info.html',
                case_details=case_details,
                prosecutor=prosecutor_data,
                police_station=police_station_data,
                case_history=case_history_data,
                acts=acts_data,
                sections=sections_data,
                witnesses=witnesses_data,
                court_details=court_details_data,
                phone_numbers=phone_numbers_data
            )
        else:
            flash('No matching case found for the provided Status ID.', 'danger')
            return redirect(url_for('status_id'))
    return render_template('status_id.html')

if __name__=='__main__':
    app.run(debug=True)


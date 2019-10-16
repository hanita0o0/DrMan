from flask import Flask,jsonify,request
from peewee import *
from argon2 import PasswordHasher
from flask_cors import CORS
import datetime
import jwt
import uuid
from functools import wraps
import json
import os

#confige param
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
app = Flask(__name__)
app.debug = True
cors = CORS(app, resources={r"*": {"origins": "*"}})

#//////////////////////////////////////////////////////////////////
DATABASE = MySQLDatabase("drman",user = 'root' ,host = 'localhost')
HASHER = PasswordHasher()
SECRET_KEY = 'gjgvghljgyuk@h&ddd%hlj'

class Type(Model):
    name = CharField(unique= True)

    class Meta():
        database = DATABASE

class Proficiency(Model):
    name = CharField(unique=True)

    class Meta():
        database = DATABASE

class State(Model):
    name = CharField(unique=True)


    class Meta():
        database = DATABASE

class City(Model):
    name = CharField(unique=True)
    state = ForeignKeyField(State)


    class Meta():
        database = DATABASE

class Region(Model):
    name = CharField(unique = True)
    city = ForeignKeyField(City)


    class Meta():
        database = DATABASE

class Institute(Model):
    name = CharField(unique=True)
    tel = CharField()
    state = ForeignKeyField(State)
    city = ForeignKeyField(City)
    region = ForeignKeyField(Region)
    address = TextField()
    email = CharField(null= True,unique=True)
    website =CharField(null= True)
    created_at = DateTimeField(default=datetime.datetime.now)
    type = ForeignKeyField(Type)

    class Meta():
        database = DATABASE

class Temp_User(Model):
    code = CharField()
    username = CharField(unique=True)
    password = CharField()
    name = CharField()
    family = CharField()
    public_id = CharField(max_length=50, unique=True)
    mobile = CharField()
    tel = CharField(null = True)
    birth_year = IntegerField()
    gender = BooleanField(default = 0)
    state = IntegerField()
    city = IntegerField()
    region = IntegerField()
    address = TextField(null=True)
    email = CharField(null=True)
    path = TextField(null =True)
    type_id = IntegerField()
    temp_institute =  TextField(null =True)
    temp_proficiency = TextField(null =True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta():
        database = DATABASE

    @classmethod
    def Create(cls, code, username, password, name, family, mobile, tel, birth_year, gender,
               state, city, region, address, email, type_id,path,temp_institute,temp_proficiency):
        if email:
            email = email.lower()
        try:
            cls.select().where(
                (cls.username == username)
            ).get()
            query = User.select().where(User.username == username)
        # there is not exist user in database so create
        except cls.DoesNotExist:
            new = cls(code=code, username=username, name=name, family=family, mobile=mobile,
                      tel=tel, birth_year=birth_year, gender=gender, state=state, city=city, region=region,
                      address=address, email=email, type_id=type_id,path =path,temp_institute = temp_institute,
                      temp_proficiency = temp_proficiency,
                      public_id=str(uuid.uuid4()))
            new.password = new.set_password(password)
            new.save()
            return new
        else:
            return 1


    @staticmethod
    def set_password(password):
        return HASHER.hash(password)
class User(Model):
    code = CharField()
    username = CharField(unique=True)
    password = CharField()
    name = CharField()
    family = CharField()
    public_id = CharField(max_length=50, unique=True)
    mobile = CharField()
    tel = CharField(null = True)
    birth_year = IntegerField()
    gender = BooleanField(default = 0)
    state =  ForeignKeyField(State)
    city = ForeignKeyField(City)
    region = ForeignKeyField(Region)
    address = TextField(null=True)
    email = CharField(null=True)
    path = TextField(null =True)
    type = ForeignKeyField(Type)
    active = BooleanField(default = 1)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta():
        database = DATABASE
    @classmethod
    def Create(cls, code, username, password, name, family, mobile, tel, birth_year, gender,
               state, city,region,address,email, type_id,path):
        if email:
          email = email.lower()
        try:
            cls.select().where(
                (cls.username == username)
            ).get()
        # there is not exist user in database so create
        except cls.DoesNotExist:
            new = cls(code = code, username = username,name = name,family = family, mobile = mobile,
             tel = tel, birth_year = birth_year, gender = gender, state = state, city = city, region = region, address = address,
                      email = email,type_id = type_id,path = path,
                      public_id =str(uuid.uuid4()) )
            new.password = new.set_password(password)
            new.save()
            return new
        else:
            return 1

    @staticmethod
    def set_password(password):
        return HASHER.hash(password)
class Proficiency_User(Model):
    user = ForeignKeyField(User)
    proficiency = ForeignKeyField(Proficiency)

    class Meta():
        database = DATABASE

    @classmethod
    def Create(cls, proficiency_id, user_id):
        new = cls(proficiency_id=proficiency_id, user_id=user_id)
        new.save()
        return True

class Institute_User(Model):
     user = ForeignKeyField(User)
     institute = ForeignKeyField(Institute)

     class Meta():
         database = DATABASE

     @classmethod
     def Create(cls, institute_id, user_id):
         new = cls(institute_id=institute_id, user_id = user_id)
         new.save()
         return True

class Prescription(Model):
    body = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    lab_take_at=DateTimeField(null = True)
    lab_result_at = DateTimeField(null = True)
    result = TextField(null=True)
    description =TextField(null=True)
    agree = BooleanField(default = 0)

    class Meta():
        database = DATABASE

    @classmethod
    def Cteate(cls,body):
        new=cls(body = body)
        new.save()
        return new


    @classmethod
    def Delete(cls,prescription_id):
        q = Prescription.delete().where(Prescription.id == prescription_id)
        q.execute()

        return True

    @classmethod
    def Update_Pre_Clinic(cls,prescription_id,body):
        new = (Prescription
               .update(body = body)
               .where(Prescription.id == prescription_id)
               .execute()
               )
        # if new.update():
        return True


    @classmethod
    def Update_Pre_Lab(cls,prescription_id,lab_take_at,lab_result_at,result,description,agree):
        new = (Prescription
               .update(lab_take_at = lab_take_at, lab_result_at = lab_result_at,result = result,
                       description =description, agree = agree)
               .where(Prescription.id == prescription_id)
               .execute()
               )
        # if new.update():
        return True


    @classmethod
    def Create_Result(cls, prescription_id, lab_take_at, lab_result_at):
        new = (Prescription
       .update(lab_take_at=lab_take_at,lab_result_at = lab_result_at)
       .where(Prescription.id == prescription_id)
       .execute())
        # if new.update():
        return True

    @classmethod
    def Edit_Result(cls, prescription_id, result):
        new = (Prescription
               .update(result = result)
               .where(Prescription.id == prescription_id)
               .execute())
        # if new.update():
        return True

    @classmethod
    def Submit_Result(cls, prescription_id, description,agree):
        new = (Prescription
               .update(description = description,agree = agree)
               .where(Prescription.id == prescription_id)
               .execute())
        # if new.update():
        return True

class Prescription_User(Model):
    user= ForeignKeyField(User)
    prescription = ForeignKeyField(Prescription)

    class Meta():
        database = DATABASE

    @classmethod
    def Create(cls, user_id, prescription_id):
        new = cls(user_id=user_id, prescription_id=prescription_id)
        if new.save():
            return True
    @classmethod
    def Delete(cls,prescription_id):
        q = Prescription_User.delete().where(Prescription_User.prescription_id == prescription_id)
        q.execute()
        return True

    @classmethod
    def Update(cls,patient_id,user_id,prescription_id):
        new = (Prescription_User
               .update(user_id = user_id)
               .where((Prescription_User.prescription_id == prescription_id )& (Prescription_User.user_id == patient_id))
               .execute()
               )
        # if new.update():
        return True

class Prescription_institute(Model):
    institute = ForeignKeyField(Institute)
    prescription = ForeignKeyField(Prescription)

    class Meta():
        database = DATABASE

    @classmethod
    def Create(cls,institute_id,prescription_id):
        new = cls(institute_id=institute_id,prescription_id=prescription_id)
        if new.save():
            return True

    @classmethod
    def Update(cls,id,institute_id):
        new = (Prescription_institute
               .update(institute_id = institute_id)
               .where(Prescription_institute.id == id)
               .execute()
               )

        return True

    @classmethod
    def Delete(cls,prescription_id):
        q = Prescription_institute.delete().where(Prescription_institute.prescription_id == prescription_id)
        q.execute()
        return True

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Type,Institute,User,Temp_User,Prescription,Prescription_User,Prescription_institute,Institute_User,State,
                            City,Region,Proficiency,Proficiency_User], safe = True)
    DATABASE.close()

#////////////////////////////authentication //////////////
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):

        token = None
        if 'api_token' in request.headers:
            token = request.headers['api_token']
        if not token:
            return jsonify({'message':'Token is missing'}),401
        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = User.get(User.public_id == data['public_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}),401
        #token is valid and  have a user
        return  f(current_user,*args, **kwargs)
    return decorated

# /////////////////////////////////////////////////////////
def provide_directory(username):

    parent_dir = os.getcwd()


    path = parent_dir + '\\' + 'Uploads'

    # get time
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    file_path = directory(path, year, month, username)
    return file_path

def directory(path = None ,year = None,month = None,username =None):
    list = []
    if not (os.path.exists(path)):
        os.mkdir(path)

    if not(os.path.exists(path + '\\'  + year)):
        os.mkdir(path + '\\'  + year )
    if not (os.path.exists(path + '\\'  + year + '\\' + month )):
        os.mkdir(path + '\\'  + year + '\\' + month)
    if not (os.path.exists(path + '\\'  + year + '\\' + month + '\\'  + username)):
        os.mkdir(path + '\\'  + year + '\\' + month +  '\\' + username)
    list.append(path + '\\' + year + '\\' + month + '\\' + username)
    list.append('Uploads' + '\\' + year + '\\' + month + '\\' + username)
    return list

def create_filename(type_file):

    now = datetime.datetime.now()
    now_string = str(now.strftime('(%Y-%m-%d)(%H-%M-%S)'))
    filename = now_string   + type_file
    return filename

# //////////////////////////////////
@app.route('/login',methods=['POST'])
def Login():

        json_data = request.get_json(force=True)
        if json_data['username'] and json_data['password'] and json_data['institute_name'] :

             input = json_data['username']
             password = json_data['password']
             institute_name = json_data['institute_name']
             institute_id = None
             institute_type_id= None
             institute_type_name =None
             user_Type_name =None
             user_pass = None
             user_id =None
             user_type_id =None
             user_public_id =None
             query1 = User.select().where( User.username == input)
             if query1:
                for g in query1:
                       user_id = g.id
                       user_pass = g.password
                       user_type_id = g.type_id
                       user_public_id = g.public_id
                try:
                     HASHER.verify(user_pass, password)

                     query = Institute.select().where(Institute.name == institute_name)
                     if query:
                         for i in query:
                             institute_id = i.id
                             institute_type_id =i.type_id
                         query2 = Institute_User.select().where((Institute_User.institute_id == institute_id)
                                                                & (Institute_User.user_id ==  user_id))
                         if query2:
                             query3 = Type.select().where(Type.id ==  institute_type_id)
                             for n in query3:
                                 institute_type_name = n.name
                             query4 = Type.select().where(Type.id == user_type_id)
                             for s in query4:
                                 user_Type_name = s.name
                             token = jwt.encode(
                                 {'public_id': user_public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                 SECRET_KEY)
                             return jsonify(
                                 {'token': token.decode('UTF-8'), 'institute_id': institute_id,
                                  'institute_type_name' :institute_type_name ,'user_Type_name':user_Type_name})
                         else:
                             # invalid institute
                             return jsonify(1)
                     else:
                         #invalid institute
                         return jsonify(1)
                except:
                     return jsonify(0)
             else:
                 #username wrong
                 return jsonify(0)


        else:
            # not input enough
            return jsonify(0)



#//////////////////////////////////////////////////////////

@app.route('/ListTypeUser',methods = ['GET'])
def List_TypeUser():

    query = Type.select().where((Type.name != "clinic") &(Type.name != 'lab') & (Type.name != 'other') &
                                (Type.name != 'admin') )
    list = []
    if query:
        for i in query:
           dict ={}
           dict["name"] = i.name
           dict["id"] = i.id
           list.append(dict)
        return jsonify(list)


@app.route('/CreateUser' , methods=['POST'])
def CreateUser():

    if  request.form['code'] and request.form['name'] and request.form['family'] and request.form['username'] and request.form['password']\
             and request.form['mobile'] and request.form['state'] and request.form['city'] and request.form['gender'] and request.form['birth_year'] and \
             request.form['region'] and request.form['type_id'] and request.form['institute_id'] and request.form['proficiency_id'] :

        query = Type.select().where((Type.name != "clinic") & (Type.name != 'lab') & (Type.name != 'other') &
                                    (Type.name != 'admin'))
        list = []
        if query:
           for i in query:
                list.append(i.id)

           if int(request.form['type_id']) in list:
                    code = request.form['code']
                    username = request.form['username']
                    password = request.form['password']
                    name = request.form['name']
                    family = request.form['family']
                    mobile = request.form['mobile']
                    if request.form['tel']:
                       tel = request.form['tel']
                    else:
                        tel = None
                    state = request.form['state']
                    city = request.form['city']
                    region = request.form['region']
                    if request.form['address']:
                       address = request.form['address']
                    else:
                        address = None
                    birth_year = request.form['birth_year']
                    gender = request.form['gender']
                    if request.form['email']:
                       email = request.form['email']
                    else:
                        email = None
                    type_id = int(request.form['type_id'])
                    institute_id = request.form['institute_id']
                    proficiency_id = request.form['proficiency_id']
                    # convert string to list
                    institute_id = institute_id.split(',')
                    proficiency_id = proficiency_id.split(',')

                    for i in institute_id:
                       query2 = Institute.select().where(Institute.id == i)
                       if not query2 :
                           # invalid inistite_id
                           return jsonify(4)
                    # convert list to string
                    institute_id = ','.join(institute_id)

                    for k in proficiency_id:
                        query3 = Proficiency.select().where(Proficiency.id == k)
                        if not query3:
                            # invalid proficiency_id
                            return jsonify(5)
                    # convert list to string
                    proficiency_id = ','.join(proficiency_id)

                    row = Type.select().where(Type.name == 'patient').get()
                    row1 = Type.select().where((Type.name == 'drclinic') | (Type.name == 'drlab'))
                    row2 = Type.select().where((Type.name == 'secretaryclinic') | (Type.name == 'secretarylab'))

                    list_dr_id = []

                    for i in row1:
                        list_dr_id.append(i.id)
                    if type_id in list_dr_id:
                        # so be dr
                        if  not request.files['file'] :
                            # please enter file
                            return jsonify(3)
                        else:
                         file = request.files['file']
                         file_name = file.filename
                         extension = os.path.splitext(file_name)[1]
                         file_name = create_filename(extension)
                         file_path = provide_directory(username)
                         path_local = file_path[0]
                         path_db = file_path[1]
                         path_db = path_db + '\\' + file_name
                         # save file
                         file.save(path_local + '\\' + file_name)
                         new1 = Temp_User.Create(code, username, password, name, family, mobile, tel, birth_year, gender,
                              state, city, region, address, email, type_id, path_db, institute_id, proficiency_id)
                         if new1 == 1:
                             # user with that username exist
                             return jsonify(6)
                         # dr created
                         return jsonify(0)

                    patient_id = row.id
                    if type_id == patient_id:

                      #so be patient
                      path = None
                      new1 = User.Create(code, username, password, name, family, mobile, tel, birth_year, gender,
                                              state, city, region, address, email, type_id,path)
                      if new1 == 1:
                          # user with that username exist
                          return jsonify(6)
                      # dr created
                      return jsonify(0)

                    list_sec_id = []
                    for i in row2:
                        list_sec_id.append(i.id)
                    if type_id in  list_sec_id:
                        #so be sec
                        path = None
                        new1 = Temp_User.Create(code, username, password, name, family, mobile, tel, birth_year, gender,
                                                state, city, region, address, email, type_id, path, institute_id,
                                                proficiency_id)

                        if new1 == 1:
                            # user with that username exist
                            return jsonify(6)
                            # dr created
                        return jsonify(0)



           else :
                #invalid type_id
                return jsonify(2)
    else :
        # not input enough
        return jsonify(1)

@app.route('/CreatePrescription' , methods=['POST'])
@token_required
def CreatePrescription(current_user):
   type_id_user = None
   type_id_lab = None
   type_name_lab =None
   type_name_user = None
   #user info
   query1 = User.select().where(User.id ==  current_user.id)
   for i in query1:
       type_id_user = i.type_id
   #check user be doctorclinic
   query2 = Type.select().where(Type.id == type_id_user)
   for j in query2 :
       type_name_user = j.name
   if type_name_user == 'drclinic':
       json_data = request.get_json(force=True)
       if json_data['patient_id'] and json_data['body'] and json_data['lab_id'] and json_data['clinic_id']:
           lab_id = json_data['lab_id']
           #lab info
           query3 = Institute.select().where(Institute.id == lab_id)
           if query3:
               for j in query3:
                   type_id_lab = j.type_id
               #check Institute is lab
               query4 = Type.select().where(Type.id == type_id_lab)
               for n in query4:
                     type_name_lab =n.name
               if type_name_lab == 'lab':
                   patient_id = json_data['patient_id']
                   #check patient be in db
                   query5 = User.select().where(User.id == patient_id)
                   if query5:
                       body = json_data['body']
                       body = json.dumps(body)
                       query6 = Institute_User.select().where(
                           (Institute_User.user_id == current_user.id) & (Institute_User.institute_id == json_data['clinic_id']))
                       if query6 :
                           #insert new prescription
                           new1 = Prescription.Cteate(body)
                           # insert doctor clinic for prescription
                           new2 = Prescription_User.Create(current_user.id,new1.id)
                           # insert clinic for prescription
                           new3 = Prescription_institute.Create(json_data['clinic_id'],new1.id)
                           #insert lab for prescription
                           new4 = Prescription_institute.Create(lab_id,new1.id)
                           # insert patient for prescription
                           new5 = Prescription_User.Create(patient_id, new1.id)
                           return jsonify({"id":new1.id})

                       else :
                           # clinic not found
                           return jsonify(4)
                   else:
                       #patient not found
                       return jsonify(3)
               else:
                   # lab not found
                   return jsonify(2)
           else:
               #lab not found
               return  jsonify(2)

       else :
           # not enough inputs
           return jsonify(1)

   else :
       # you are not doctor
       return jsonify(0)

@app.route('/ListPrescription',methods=['GET'])
@token_required
def ListPrescription(current_user):
    if not request.args['institute_id'] and not request.args['limit'] and not request.args['skip']:
        # please enter params
        return jsonify(1)

    type_clinic_id = None
    type_lab_id = None
    init_id =None
    name =None
    limit = int(request.args['limit'])
    skip = int(request.args['skip'])

    que = Institute.select().where(Institute.id == request.args['institute_id'])
    if que :
        # check user that login authorized for institute_id
        gg = Institute_User.select().where((Institute_User.user_id == current_user.id) &
                                           (Institute_User.institute_id == request.args['institute_id']))
        if gg :
            q1 = Type.select().where(Type.name == 'clinic')
            q2 = Type.select().where(Type.name == 'lab')
            for h in q1:
                type_clinic_id = h.id
            for w in q2:
                type_lab_id = w.id

            for bb in que:
                type_institute_id = bb.type_id
                if type_institute_id == type_clinic_id:
                    #so clinic
                    name = bb.name
                if  type_institute_id == type_lab_id:
                    #so be lab
                    name = bb.name
            # dr lab param
            type_Dr_Lab_id = None
            ww = Type.select().where(Type.name == 'drlab')
            for z in ww:
                type_Dr_Lab_id = z.id
            #dr clinic param
            type_Dr_Clinic_id = None

            q = Type.select().where(Type.name == 'drclinic')
            for s in q:
                type_Dr_Clinic_id = s.id

            #patient param
            type_patient_id  = None
            z = Type.select().where(Type.name == 'patient')
            for p in z:
                type_patient_id = p.id


            #list prescriptions for special lab and clinic
            query1 = Prescription_institute.select().where(
                Prescription_institute.institute_id == request.args['institute_id']
            ).order_by(Prescription_institute.id.desc()).limit(limit).offset(skip)

            if query1 :

                list_prescription_id = []
                for k in query1:
                   list_prescription_id.append(k.prescription_id)

                list = []
                # prescription info
                for j in list_prescription_id:

                        i = Prescription.select().where(Prescription.id == j).get()

                        dict = {}
                        # ba tavajoh be nooe institute digar etelaate khodash ra dar list neshan nemidahad
                        qq = Prescription_institute.select().where((Prescription_institute.prescription_id == j) &
                                                                   (Prescription_institute.institute_id != request.args['institute_id'])).get()

                        init_id = qq.institute_id
                        dd = Institute.select().where(Institute.id == init_id).get()
                        type_init_id = dd.type_id
                        if type_init_id ==  type_clinic_id  :
                            # so be clinic
                            dict['clinic_id'] = init_id
                            dict['clinic_name'] = dd.name
                        # so be lab
                        else :

                            dict['lab_id'] = init_id
                            dict['lab_name'] =dd.name


                        dict['id'] = i.id
                        dict['description']=i.description
                        dict['lab_take_at'] =i.lab_take_at
                        dict['lab_result_at'] = i.lab_result_at
                        result = i.result
                        if result == None:
                            dict['result'] =None
                        else:
                            result = json.loads(result)
                            dict['result'] = result

                        dict['agree'] = i.agree
                        dict['created_at'] =i.created_at
                        # body
                        body = i.body
                        if body ==None:
                            dict['body'] =None
                        else:
                            body = json.loads(body)
                            dict['body'] = body

                        # Users info
                        query4 = Prescription_User.select().where(Prescription_User.prescription_id == i.id)
                        list_users = []
                        for k in query4:
                            list_users.append(k.user_id)
                        for m in list_users:
                          query5 = User.select().where(User.id == m)
                          for l in query5:
                            if l.type_id == type_Dr_Clinic_id :
                                dict['drclinic_id'] = l.id
                                dict['drclinic_name'] = l.name
                                dict['drclinic_family'] = l.family

                            if l.type_id == type_Dr_Lab_id :
                                dict['drlab_id'] = l.id
                                dict['drlab_name'] = l.name
                                dict['drlab_family'] = l.family

                            if l.type_id == type_patient_id :
                                dict['patient_id'] = l.id
                                dict['patient_name'] = l.name
                                dict['patient_family'] = l.family
                                dict['patient_birth_year'] = l.birth_year
                                dict['patient_national_code'] = l.code
                                dict['patient_mobile'] = l.mobile
                                dict['patient_tel'] = l.tel

                        list.append(dict)

                return jsonify(list)

            else:
                #no prescription
                return jsonify(0)

        else:
            #no access
            return jsonify(2)
    else :
        # invalid institute_id
        return jsonify(1)

@app.route('/Search_Patient_Name',methods=['GET'])
def Search_Patient_Name():
     if request.args['patient_name'] :
         patient_name = request.args['patient_name']
         query1 = User.select().where(User.name.startswith(patient_name))
         list_patient_name =[]
         if query1:
             for i in query1:
                 dict={}
                 dict['name'] = i.name
                 list_patient_name.append(dict)
             return jsonify(list_patient_name)
         else:
             # not found
             return jsonify(1)
     else:
         # no enough input
         return jsonify(0)

@app.route('/Search_Patient_Family',methods=['GET'])
def Search_Patient_Family():
     if request.args['patient_family'] :
         patient_family = request.args['patient_family']
         query1 = User.select().where(User.family.startswith(patient_family))
         list_patient_family =[]
         if query1:
             for i in query1:
                 dict={}
                 dict['family'] = i.family
                 list_patient_family.append(dict)
             return jsonify(list_patient_family)
         else:
             # not found
             return jsonify(1)
     else:
         # no enough input
         return jsonify(0)

@app.route('/Search_Patient_FullName',methods=['GET'])
def Search_Patient_FullName():
     if request.args['patient_name'] and request.args['patient_family']:
         patient_name = request.args['patient_name']
         patient_family = request.args['patient_family']
         query1 = User.select().where((User.name == patient_name) and (User.family == patient_family))
         list_patient =[]
         if query1:
             for i in query1:
                 dict={}
                 dict['id'] = i.id
                 dict['name'] = i.name
                 dict['family'] = i.family
                 dict['national_code'] = i.code
                 dict['birth_year'] = i.birth_year
                 list_patient.append(dict)
             return jsonify(list_patient)
         else:
             # not found
             return jsonify(1)
     else:
         # no enough input
         return jsonify(0)


@app.route('/Search_City',methods=['GET'])
def Search_City():
    if request.args['city']:
       city = request.args['city']
       query = City.select().where(City.name.startswith(city))
       list_city = []
       if query:
           for i in query:
               dict = {}
               dict['id'] = i.id
               dict['name'] = i.name
               list_city.append(dict)
           return jsonify(list_city)
       else:
           # not found
           return jsonify(1)
    else:
        # not enough input
        return jsonify(0)


@app.route('/Search_Region',methods=['GET'])
def Search_Region():
    if request.args['region'] and request.args['city_id']:
       region = request.args['region']
       city = int(request.args['city_id'])

       query = Region.select().where((Region.city_id == city) & (Region.name.startswith(region)))
       list_region = []
       if query:
           for i in query:
               dict = {}
               dict['id'] = i.id
               dict['name'] = i.name
               list_region.append(dict)
           return jsonify(list_region)
       else:
           # not found
           return jsonify(1)
    else:
        # not enough input
        return jsonify(0)



#/////////////////////////////////////////////search lab
@app.route('/Search_Lab_Region',methods=['GET'])
def Search_Lab_Region():
     if request.args['region_id']:
         type_lab_id = None
         region_id = request.args['region_id']
         query1 = Type.select().where(Type.name == 'lab')
         if query1:
             for j in query1:
                 type_lab_id = j.id
         query2 = Institute.select().where((Institute.region_id == region_id )& (Institute.type_id == type_lab_id))
         list_lab_name =[]
         if query2:
             for i in query2:
                 dict={}
                 dict['id'] = i.id
                 dict['name'] = i.name
                 dict['address'] = i.address
                 list_lab_name.append(dict)
             return jsonify(list_lab_name)
         else:
             # not found
             return jsonify(1)
     else:
         #not enough input
         return jsonify(0)

@app.route('/Search_Lab_Name',methods=['GET'])
def Search_Lab_Name():
     if request.args['lab_name']:
         type_lab_id = None
         lab_name = request.args['lab_name']
         query1 = Type.select().where(Type.name == 'lab')
         if query1:
             for j in query1:
                 type_lab_id = j.id
         query2 = Institute.select().where((Institute.name.startswith(lab_name) )& (Institute.type_id == type_lab_id))
         list_lab_name =[]
         if query2:
             for i in query2:
                 query3 = City.select().where(City.id == int(i.city_id)).get()
                 query4 = Region.select().where(Region.id == int(i.region_id)).get()
                 dict={}
                 dict['id'] = i.id
                 dict['name'] = i.name
                 dict['city'] = query3.name
                 dict['region'] = query4.name
                 dict['address'] = i.address
                 list_lab_name.append(dict)
             return jsonify(list_lab_name)
         else:
             # not found
             return jsonify(1)
     else:
         #not enough input
         return jsonify(0)


#//////////////////////////////////////////////search clinic
@app.route('/Search_Clinic_Region',methods=['GET'])
def Search_Clinic_Region():
     if request.args['region_id']:
         type_clinic_id = None
         region_id = request.args['region_id']
         query1 = Type.select().where(Type.name == 'clinic')
         if query1:
             for j in query1:
                 type_clinic_id = j.id
         query2 = Institute.select().where((Institute.region_id == region_id ) & (Institute.type_id == type_clinic_id))
         list_clinic_name =[]
         if query2:
             for i in query2:
                 dict={}
                 dict['id'] = i.id
                 dict['name'] = i.name
                 dict['address'] = i.address
                 list_clinic_name.append(dict)
             return jsonify(list_clinic_name)
         else:
             # not found
             return jsonify(1)
     else:
         #not enough input
         return jsonify(0)


@app.route('/Search_Clinic_Name',methods=['GET'])
def Search_Clinic_Name():
     if request.args['clinic_name']:
         type_clinic_id = None
         clinic_name = request.args['clinic_name']
         query1 = Type.select().where(Type.name == 'clinic')
         if query1:
             for j in query1:
                 type_clinic_id = j.id
         query2 = Institute.select().where((Institute.name.startswith(clinic_name) )& (Institute.type_id == type_clinic_id))
         list_clinic_name =[]
         if query2:
             for i in query2:
                 query3 = City.select().where(City.id == int(i.city_id)).get()
                 query4 = Region.select().where(Region.id == int(i.region_id)).get()
                 dict={}
                 dict['id'] = i.id
                 dict['name'] = i.name
                 dict['city'] = query3.name
                 dict['region'] = query4.name
                 dict['address'] = i.address
                 list_clinic_name.append(dict)
             return jsonify(list_clinic_name)
         else:
             # not found
             return jsonify(1)
     else:
         #not enough input
         return jsonify(0)


@app.route('/Search_Prescription',methods=['GET'])
@token_required
def Search_Prescription(current_user):
    if not request.args['institute_id'] and request.args['national_code']:
        # please enter inputs
        return jsonify(1)

    type_clinic_id = None
    type_lab_id = None
    init_id =None
    name =None

    patient_id = None
    national_code = request.args['national_code']
    query = User.select().where(User.code == national_code)
    if query:
        for i in query:
            patient_id = i.id
        que = Institute.select().where(Institute.id == request.args['institute_id'])
        if que :
            # check user that login authorized for institute_id
            gg = Institute_User.select().where((Institute_User.user_id == current_user.id) &
                                               (Institute_User.institute_id == request.args['institute_id']))
            if gg :
                q1 = Type.select().where(Type.name == 'clinic')
                q2 = Type.select().where(Type.name == 'lab')
                for h in q1:
                    type_clinic_id = h.id
                for w in q2:
                    type_lab_id = w.id

                for bb in que:
                    type_institute_id = bb.type_id
                    if type_institute_id == type_clinic_id:
                        #so clinic
                        name = bb.name
                    if  type_institute_id == type_lab_id:
                        #so be lab
                        name = bb.name

                # dr lab param
                type_Dr_Lab_id = None
                ww = Type.select().where(Type.name == 'drlab')
                for z in ww:
                    type_Dr_Lab_id = z.id
                #dr clinic param
                type_Dr_Clinic_id = None

                q = Type.select().where(Type.name == 'drclinic')
                for s in q:
                    type_Dr_Clinic_id = s.id

                # patient param
                type_patient_id = None
                z = Type.select().where(Type.name == 'patient')
                for p in z:
                    type_patient_id = p.id

                #list prescriptions for special lab and clinic and patient_id
                row1 = Prescription_User.select().where(Prescription_User.user_id == patient_id)
                if row1:
                    list_prescription_id=[]
                    list_pre_id = []
                    for i in row1:
                        list_pre_id.append(i.prescription_id)

                    for j in list_pre_id:

                        query1 = Prescription_institute.select().where(
                            (Prescription_institute.institute_id == request.args['institute_id']) &
                            (Prescription_institute.prescription_id == j)
                        )

                        if query1 :

                            for k in query1:
                                list_prescription_id.append(k.prescription_id)

                    list = []
                    # prescription info
                    for j in list_prescription_id:

                      row = Prescription.select().where(Prescription.id == j)

                      for i in row :
                        print(i)
                        dict = {}
                        # ba tavajoh be nooe institute digar etelaate khodash ra dar list neshan nemidahad
                        qq = Prescription_institute.select().where((Prescription_institute.prescription_id == j) &
                                                                   (Prescription_institute.institute_id != request.args[
                                                                       'institute_id'])).get()

                        init_id = qq.institute_id
                        dd = Institute.select().where(Institute.id == init_id).get()
                        type_init_id = dd.type_id
                        if type_init_id == type_clinic_id:
                            # so be clinic
                            dict['clinic_id'] = init_id
                            dict['clinic_name'] = dd.name
                        # so be lab
                        else:

                            dict['lab_id'] = init_id
                            dict['lab_name'] = dd.name


                        dict['id'] = i.id
                        dict['description'] = i.description
                        dict['lab_take_at'] = i.lab_take_at
                        dict['lab_result_at'] = i.lab_result_at
                        result = i.result
                        if result == None:
                            dict['result'] = None
                        else:
                            result = json.loads(result)
                            dict['result'] = result
                        dict['agree'] = i.agree
                        # body
                        body = i.body
                        if body == None:
                            dict['body'] = None
                        else:
                            body = json.loads(body)
                            dict['body'] = body
                        dict['created_at'] = i.created_at

                        # Doctors info
                        query4 = Prescription_User.select().where(Prescription_User.prescription_id == i.id)
                        list_doctors=[]
                        for k in query4:
                            list_doctors.append(k.user_id)
                        for m in list_doctors:
                          query5 = User.select().where(User.id == m)
                          for l in query5:
                            if l.type_id == type_Dr_Clinic_id :
                                dict['drclinic_id'] = l.id
                                dict['drclinic_name'] = l.name
                                dict['drclinic_family'] = l.family

                            if l.type_id == type_Dr_Lab_id:
                                dict['drlab_id'] = l.id
                                dict['drlab_name'] = l.name
                                dict['drlab_family'] = l.family

                            if l.type_id == type_patient_id:
                                dict['patient_id'] = l.id
                                dict['patient_name'] = l.name
                                dict['patient_family'] = l.family
                                dict['patient_birth_year'] = l.birth_year
                                dict['patient_national_code'] = l.code
                                dict['patient_mobile'] = l.mobile
                                dict['patient_tel'] = l.tel

                        list.append(dict)


                    return jsonify(list)

                else:
                    #no prescription
                    return jsonify(0)

            else:
                #no access
                return jsonify(2)
        else :
            # invalid institute_id
            return jsonify(1)
    else :
        # not found patient
        return jsonify(3)


@app.route('/Create_Result',methods=['POST'])
@token_required
def Create_Result(current_user):
    json_data = request.get_json(force=True)
    if  not json_data['lab_id'] and json_data['prescription_id'] and json_data['lab_take_at'] and \
        json_data['lab_result_at']:
        # please enter inputs
        return jsonify(3)

    type_lab_id = None

    q = Type.select().where(Type.name == 'lab')
    for i in q:
        type_lab_id = i.id
    que = Institute.select().where((Institute.id ==json_data['lab_id']) & (Institute.type_id == type_lab_id))
    if que :
        # check user that login authorized for institute_id
        gg = Institute_User.select().where((Institute_User.user_id == current_user.id) &
                                           (Institute_User.institute_id == json_data['lab_id']))
        if gg :
           prescription_id = json_data['prescription_id']
           lab_take_at = json_data['lab_take_at']
           lab_result_at = json_data['lab_result_at']
           query1 = Prescription.select().where(Prescription.id == prescription_id)
           if query1:
               new = Prescription.Create_Result(prescription_id,lab_take_at,lab_result_at)
               if new:
                     return jsonify(4)
               return "no create"
           else:
               #no found prescription
               return jsonify(0)
        else:
            #no access
            return jsonify(2)
    else :
        # invalid institute_id
        return jsonify(1)


@app.route('/Edit_Result',methods=['POST'])
@token_required
def Edit_Result(current_user):
    json_data = request.get_json(force=True)
    if  not json_data['lab_id'] and json_data['prescription_id'] and json_data['result'] :
        # please enter inputs
        return jsonify(3)

    type_lab_id = None

    q = Type.select().where(Type.name == 'lab')
    for i in q:
        type_lab_id = i.id
    que = Institute.select().where((Institute.id ==json_data['lab_id']) & (Institute.type_id == type_lab_id))
    if que :
        # check user that login authorized for institute_id
        gg = Institute_User.select().where((Institute_User.user_id == current_user.id) &
                                           (Institute_User.institute_id == json_data['lab_id']))
        if gg :
           prescription_id = json_data['prescription_id']
           result = json_data['result']
           if result == None :
               result = None
           else:
               result = json.dumps(result)
           query1 = Prescription.select().where(Prescription.id == prescription_id)
           if query1:
               new = Prescription.Edit_Result(prescription_id,result)
               if new:
                     return jsonify(4)
               return "no update"
           else:
               #no found prescription
               return jsonify(0)
        else:
            #no access
            return jsonify(2)
    else :
        # invalid institute_id
        return jsonify(1)

@app.route('/Submit_Result',methods=['POST'])
@token_required
def Submit_Result(current_user):
    json_data = request.get_json(force=True)
    if  not json_data['lab_id'] and json_data['prescription_id'] and json_data['description'] and json_data['agree'] :
        # please enter inputs
        return jsonify(1)

    type_lab_id = None
    type_drlab_id = None
    q = Type.select().where(Type.name == 'lab')

    for i in q:
        type_lab_id = i.id
    que = Institute.select().where((Institute.id ==json_data['lab_id']) & (Institute.type_id == type_lab_id))
    if que :
        # check user that login authorized for institute_id
        gg = Institute_User.select().where((Institute_User.user_id == current_user.id) &
                                           (Institute_User.institute_id == json_data['lab_id']))
        if gg :
            # check user just drlab
            quee = Type.select().where(Type.name == 'drlab')
            for j in quee:
                type_drlab_id = j.id
            quer = User.select().where((User.type_id == type_drlab_id) & (User.id == current_user.id))
            if quer:

               prescription_id = json_data['prescription_id']
               description = json_data['description']
               agree = json_data['agree']
               if agree == 0:
                   # please agree==1
                   return jsonify(3)
               else:
                   query1 = Prescription.select().where(Prescription.id == prescription_id)
                   if query1:
                       new = Prescription.Submit_Result(prescription_id,description,agree)
                       if new:
                           # set dr lab in Prescription_User table
                           query2 = Prescription_User.Create(current_user.id ,prescription_id )
                           if query2:
                              return jsonify(4)
                       return "no submit"
                   else:
                       #no found prescription
                       return jsonify(0)
            else :
                # no access
                return jsonify(2)
        else:
            #no access
            return jsonify(2)
    else :
        # invalid institute_id
        return jsonify(1)


@app.route('/Show_Prescription',methods = ['GET'])
@token_required
def Show_Prescription(current_user):
    if not request.args['institute_id'] and request.args['prescription_id']:
        # please enter inputs
        return jsonify(1)

    type_clinic_id = None
    type_lab_id = None
    init_id = None
    name = None
    dict = {}
    que = Institute.select().where(Institute.id == request.args['institute_id'])
    if que:
        # check user that login authorized for institute_id
        gg = Institute_User.select().where((Institute_User.user_id == current_user.id) &
                                           (Institute_User.institute_id == request.args['institute_id']))
        if gg:
            q1 = Type.select().where(Type.name == 'clinic')
            q2 = Type.select().where(Type.name == 'lab')
            for h in q1:
                type_clinic_id = h.id
            for w in q2:
                type_lab_id = w.id

            for bb in que:
                type_institute_id = bb.type_id
                if type_institute_id == type_clinic_id:
                    # so clinic
                    name = bb.name
                if type_institute_id == type_lab_id:
                    # so be lab
                    name = bb.name
            # dr lab param
            type_Dr_Lab_id = None
            ww = Type.select().where(Type.name == 'drlab')
            for z in ww:
                type_Dr_Lab_id = z.id
            # dr clinic param
            type_Dr_Clinic_id = None

            q = Type.select().where(Type.name == 'drclinic')
            for s in q:
                type_Dr_Clinic_id = s.id

            # patient param
            type_patient_id = None
            z = Type.select().where(Type.name == 'patient')
            for p in z:
                type_patient_id = p.id

            # prescription info
            query2 = Prescription.select().where(Prescription.id == request.args['prescription_id'])
            if query2:

                # check prescription id authorized for inistitue
                for i in query2:

                    qq = Prescription_institute.select().where((Prescription_institute.prescription_id == i.id) &
                                                               (Prescription_institute.institute_id != request.args[
                                                                   'institute_id']))
                    for ee in qq:
                        init_id = ee.institute_id
                    dd = Institute.select().where(Institute.id == init_id)
                    for hh in dd:
                        type_init_id = hh.type_id
                        if type_init_id == type_clinic_id:
                            dict['clinic_id'] = init_id
                            dict['clinic_name'] = hh.name

                        else:
                            dict['lab_id'] = init_id
                            dict['lab_name'] = hh.name


                    dict['id'] = i.id
                    dict['description'] = i.description
                    dict['lab_take_at'] = i.lab_take_at
                    dict['lab_result_at'] = i.lab_result_at
                    result = i.result
                    if result == None:
                        dict['result'] = None
                    else:
                        result = json.loads(result)
                        dict['result'] = result
                    dict['agree'] = i.agree
                    # body
                    body = i.body
                    if body == None:
                        dict['body'] = None
                    else:
                        body = json.loads(body)
                        dict['body'] = body
                    dict['created_at'] = i.created_at

                    # Users info
                    query4 = Prescription_User.select().where(Prescription_User.prescription_id == i.id)
                    list_users = []

                    for k in query4:
                        list_users.append(k.user_id)
                    for m in list_users:
                        query5 = User.select().where(User.id == m)
                        for l in query5:
                            if l.type_id == type_Dr_Clinic_id:
                                dict['drclinic_id'] = l.id
                                dict['drclinic_name'] = l.name
                                dict['drclinic_family'] = l.family

                            if l.type_id == type_Dr_Lab_id:
                                dict['drlab_id'] = l.id
                                dict['drlab_name'] = l.name
                                dict['drlab_family'] = l.family

                            if l.type_id == type_patient_id:
                                dict['patient_id'] = l.id
                                dict['patient_name'] = l.name
                                dict['patient_family'] = l.family
                                dict['patient_birth_year'] = l.birth_year
                                dict['patient_national_code'] = l.code
                                dict['patient_mobile'] = l.mobile
                                dict['patient_tel'] = l.tel


                return jsonify(dict)

            else:
                # no prescription
                return jsonify(0)

        else:
            # no access
            return jsonify(2)
    else:
        # invalid institute_id
        return jsonify(1)

@app.route('/Update_Prescription_Clinic',methods=['POST'])
@token_required
def Update_Prescription_Clinic(current_user):

    # untill update prescription by clinic that not accepted by lab
    if not request.args['prescription_id']:
        # please enter inputs
        return jsonify(1)
    json_data = request.get_json(force=True)
    if json_data['body'] and json_data ['patient_id'] and json_data['lab_id'] and json_data['clinic_id']:
        #find prescription
        row = Prescription.select().where(Prescription.id == request.args['prescription_id'])
        if row:
            lab_result_at = None
            lab_take_at = None
            result = None
            description = None
            agree = None

            for i in row:
                # features be null then can update prescription
                lab_take_at = i.lab_take_at
                lab_result_at = i.lab_result_at
                result = i.result
                description = i.description
                agree = i.agree
            if (lab_take_at == None) and (lab_result_at == None) and (result == None) and \
                    (description == None) and (agree == 0):

                # check authorized user for update prescription
                query1 = Prescription_User.select().where((Prescription_User.user_id == current_user.id) &
                                                          (Prescription_User.prescription_id == request.args[
                                                              'prescription_id']))
                if query1:

                    # find type_id clinic
                    row3 = Type.select().where(Type.name == 'clinic').get()
                    type_id = row3.id
                    row4 = Institute.select().where(Institute.id == json_data['clinic_id'])
                    if row4:
                        institute_type = None
                        for j in row4:
                            institute_type = j.type_id
                        if institute_type == type_id:
                            # so be clinic
                            # check prescription be for The desired clinic
                            row5 = Prescription_institute.select().where(
                                (Prescription_institute.institute_id == json_data['clinic_id']) &
                                (Prescription_institute.prescription_id == request.args['prescription_id']))
                            if row5:
                                # patient param
                                patient_id = None
                                type_patient_id = None
                                z = Type.select().where(Type.name == 'patient')
                                for p in z:
                                    type_patient_id = p.id
                                    # Users info
                                    query4 = Prescription_User.select().where(Prescription_User.prescription_id == request.args['prescription_id'])
                                    list_users = []

                                    for k in query4:
                                        list_users.append(k.user_id)
                                    for m in list_users:
                                        query5 = User.select().where(User.id == m)
                                        for l in query5:

                                            if l.type_id == type_patient_id:
                                               patient_id = l.id

                                body = json_data['body']
                                body = json.dumps(body)
                                # update prescription
                                if Prescription.Update_Pre_Clinic(request.args['prescription_id'], body):
                                    if  json_data ['patient_id'] != patient_id :
                                        Prescription_User.Update(patient_id,json_data ['patient_id'],request.args['prescription_id'])
                                        # find id from table prescription_institute
                                        row2 = Prescription_institute.select().where(
                                            (Prescription_institute.institute_id != json_data['clinic_id']) &
                                            (Prescription_institute.prescription_id == request.args['prescription_id'])).get()
                                        if row2:
                                            if Prescription_institute.Update(row2.id, json_data['lab_id']):
                                                #updated
                                                return jsonify(0)

                            else:
                                # not prescription for the desired clinic
                                return jsonify(7)
                        else:
                            # institute not be clinic type
                            return jsonify(6)
                    else:
                        # no found clinic
                        return jsonify(5)
                else:
                    # no access
                    return jsonify(3)

            else:
                # not possible to update because prescription accepted from lab
                return jsonify(4)

        else:
            # not found prescription
            return jsonify(2)
    else:
        #please enter inputs
        return jsonify(1)

@app.route('/Delete_Prescription' ,methods=['GET'])
@token_required
def Delete_Prescription(current_user):
    # untill delete prescription by clinic that not accepted by lab
    if not request.args['prescription_id']:
        # please enter inputs
        return jsonify(1)

        # find prescription
    row = Prescription.select().where(Prescription.id == request.args['prescription_id'])
    if row:
        lab_result_at =None
        lab_take_at =None
        result =None
        description =None
        agree =None

        for i in row:
            # features be null then can delete prescription
            lab_take_at =i.lab_take_at
            lab_result_at = i.lab_result_at
            result = i.result
            description = i.description
            agree = i.agree
        if (lab_take_at == None) and (lab_result_at == None) and (result == None) and \
                (description == None) and (agree == 0):
            # check authorized user for delete prescription
            query1 = Prescription_User.select().where((Prescription_User.user_id == current_user.id) &
                                                      (Prescription_User.prescription_id == request.args[
                                                          'prescription_id']))
            if query1:
                # delete prescription

                    # delete row of prescription_user and prescription_institute
                    Prescription_User.Delete(request.args['prescription_id'])
                    Prescription_institute.Delete(request.args['prescription_id'])
                    Prescription.Delete(request.args['prescription_id'])
                    # deleted
                    return jsonify(0)
            else:
                # no access
                return jsonify(1)
        else:
            # not possible to update because prescription accepted from lab
            return jsonify(2)

    else:
        # not found prescription
        return jsonify(3)

@app.route('/Update_Prescription_Lab',methods=['POST'])
@token_required
def Update_Prescription_Lab(current_user):

    if not request.args['prescription_id']:
        # please enter inputs
        return jsonify(1)
    json_data = request.get_json(force=True)
    if json_data['lab_id']:

        result = json_data['result']
        if result == None:
            result = None
        else:
            result = json.dumps(result)

        lab_take_at = json_data['lab_take_at']
        lab_result_at =json_data['lab_result_at']
        agree = json_data['agree']
        # find prescription
        row = Prescription.select().where(Prescription.id == request.args['prescription_id'])
        if row:

            q1 = Type.select().where(Type.name == 'drlab').get()
            type_id_drlab = q1.id
            q2 = Type.select().where(Type.name == 'secretarylab').get()
            type_id_seclab = q2.id

            # check type of login user
            q3 = User.select().where(User.id == current_user.id).get()
            type_id_user = q3.type_id

            if type_id_user == type_id_drlab:
                # so be drlab
                # check authorized drlab for update prescription
                query1 = Prescription_User.select().where((Prescription_User.user_id == current_user.id) &
                                                          (Prescription_User.prescription_id == request.args[
                                                              'prescription_id']))
                if query1:
                    if  agree == None and \
                        result == None and lab_take_at ==None and lab_result_at == None :
                        # enter correct inputs
                        return jsonify(8)
                    else:

                        if Prescription.Update_Pre_Lab(request.args['prescription_id'], json_data['lab_take_at'],
                                                       json_data['lab_result_at'], result,
                                                       json_data['description'],
                                                       json_data['agree']):
                            # updated
                            return jsonify(0)

                else:
                    # no access
                    return jsonify(3)
            if type_id_user == type_id_seclab :
                # so be secretarylab
                # untill update prescription by secretary lab that not accepted by drlab
                agree = None
                for i in row:
                    # feature be null then can update prescription
                    agree = i.agree
                if  agree == 0:

                    # find type_id lab
                    row3 = Type.select().where(Type.name == 'lab').get()
                    type_id = row3.id
                    row4 = Institute.select().where(Institute.id == json_data['lab_id'])
                    if row4:
                        institute_type = None
                        for j in row4:
                            institute_type = j.type_id
                        if institute_type == type_id:
                            # so be lab
                            # check prescription be for The desired lab
                            row5 = Prescription_institute.select().where(
                                (Prescription_institute.institute_id == json_data['lab_id']) &
                                (Prescription_institute.prescription_id == request.args['prescription_id']))
                            if row5:

                                # check authorized secretary for update prescription
                                q4 = Institute_User.select().where(Institute_User.user_id == current_user.id).get()
                                institute_id = q4.institute_id
                                if institute_id == int(json_data['lab_id']) :
                                    if agree == 1 :
                                        # enter correct inputs
                                        return jsonify(8)

                                    if Prescription.Update_Pre_Lab(request.args['prescription_id'],json_data['lab_take_at'],
                                                              json_data['lab_result_at'],result,json_data['description'],
                                                              json_data['agree']):
                                       # updated
                                       return jsonify(0)

                                # no access
                                return jsonify(3)
                            else:
                                # not prescription for the desired lab
                                return jsonify(7)
                        else:
                            # institute not be lab type
                            return jsonify(6)
                    else:
                        # no found lab
                        return jsonify(5)

                else:
                    # not possible to update because prescription accepted by drlab
                    return jsonify(4)

        else:
            # not found prescription
            return jsonify(2)
    else:
        # please enter inputs
        return jsonify(1)

if __name__ == '__main__':
    initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)


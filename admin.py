from flask import Flask,jsonify,request
from peewee import *
from argon2 import PasswordHasher
from flask_cors import CORS
import datetime
import jwt
import uuid
from functools import wraps



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

    @classmethod
    def Create(cls, name,tel,state,city,region,address,email,website,type_id):
        new = cls(name = name, tel = tel, state = state, city = city, region = region , address = address,
                  email = email,website = website,type_id = type_id)
        new.save()
        return new

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


#///////////////////////////////////routs

@app.route('/loginadmin',methods=['POST'])
def loginadmin():
        row = Type.select().where(Type.name == "admin").get()
        type_admin_id = row.id
        json_data = request.get_json(force=True)
        if json_data['username'] and json_data['password'] :

             input = json_data['username']
             password = json_data['password']
             user_pass = None
             user_type_id =None
             user_public_id =None

             query1 = User.select().where( User.username == input)
             if query1:
                for g in query1:
                       user_pass = g.password
                       user_type_id = g.type_id
                       user_public_id = g.public_id
                if type_admin_id ==  user_type_id  :

                     try:
                             HASHER.verify(user_pass, password)
                             token = jwt.encode(
                                 {'public_id': user_public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                 SECRET_KEY)
                             return jsonify(
                                 {'token': token.decode('UTF-8')
                                  })

                     except:
                         # password wrong
                          return jsonify(0)
                else:
                    # no access
                    return jsonify(2)

             else:
                 #username wrong
                 return jsonify(0)


        else:
            # not input enough
            return jsonify(1)

@app.route('/ListTypeInstitute',methods = ['GET'])
def ListTypeInstitute():

    query = Type.select().where((Type.name == "clinic") |(Type.name == 'lab') )
    list = []
    if query:
        for i in query:
           dict ={}
           dict["name"] = i.name
           dict["id"] = i.id
           list.append(dict)
        return jsonify(list)

@app.route('/CreateInstitute', methods=['POST'])
@token_required
def CreateInstitute(current_user):
    # just admin can create institute
    row = Type.select().where(Type.name == "admin").get()
    admin_id = row.id
    if current_user.type_id == admin_id :
        json_data = request.get_json(force=True)
        if json_data['name'] and json_data['tel'] and json_data['state'] and json_data['city'] \
                and json_data['region'] and json_data['address']  and json_data['type_id']:

            query1 = Type.select().where(Type.name == 'lab').get()
            type_id_lab = query1.id
            query2 = Type.select().where(Type.name == 'clinic').get()
            type_id_clinic = query2.id
            if  json_data['type_id'] == type_id_lab or json_data['type_id'] == type_id_clinic :

                name = json_data['name']
                tel = json_data['tel']
                state = json_data['state']
                city = json_data['city']
                region = json_data['region']
                address = json_data['address']
                type_id = json_data['type_id']
                email = json_data['email']
                website = json_data['website']

                if  json_data['type_id'] == type_id_lab :
                    # so create lab
                    query3 = Institute.select().where((Institute.name == name) & Institute.type_id == type_id_lab )
                    if query3:
                        # institute already exists
                        return jsonify(3)
                    else :
                        new1 = Institute.Create(name,tel,state,city,region,address,email,website,type_id)
                        # created
                        return jsonify(0)
                if json_data['type_id'] == type_id_clinic:
                    # so be clinic
                    new1 = Institute.Create(name, tel, state, city, region, address, email, website, type_id)
                    # created
                    return jsonify(0)

            else:
                # invalid type_id
                return jsonify(2)
        else:
            # not input enough
            return jsonify(1)
    else:
        # no access
        return jsonify(4)


@app.route('/create' , methods=['POST'])
def Create():
    json_data = request.files
    if (json_data):
        return "ok"
    else:
        return "no"


if __name__ == '__main__':
    initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)

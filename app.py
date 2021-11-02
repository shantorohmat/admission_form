import mysql.connector as mysql
from numpy import double
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib
import uuid
import yaml
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
from db_connection import get_database_connection
# import yaml
# from db_connection import get_database_connection
st.set_page_config(
    page_title="Admission form",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded",
)
with open('credintials.yml', 'r') as f:
    credintials = yaml.load(f, Loader=yaml.FullLoader)
    db_credintials = credintials['db']
    system_pass = credintials['system_pass']['admin']
    email_sender = credintials['email_sender']
# def get_database_connection():
#     db = mysql.connect(host = "localhost",
#                       user = "root",
#                       passwd = "shanto",
#                       database = "lab",
#                      )
#     cursor = db.cursor()
 
#     return cursor, db
 
cursor, db = get_database_connection()
 
# cursor.execute("show columns from student_information")
# databases = cursor.fetchall() ## it returns a list of all databases present
# st.write(databases)

# cursor.execute("show tables from project")
# tables = cursor.fetchall()
# st.write(tables)

# if 'login' not in st.session_state:
#     st.session_state.login = False
#     # driver()

# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False

# cursor.execute('''CREATE TABLE  STUDENT_INFORMATION (start_date date,end_date date,NAME VARCHAR(60) NOT NULL , EMAIL VARCHAR(60) NOT NULL,INSTITUTION VARCHAR(60) NOT NULL , PHONE numeric NOT NULL , ADDRESS VARCHAR(60) NOT NULL , GENDER VARCHAR(60) NOT NULL , cgpa double,STATUS VARCHAR(60),ID int AUTO_increment,PRIMARY KEY (ID) ''')

	
# 										id int AUTO_increment PRIMARY KEY,
#                                       name varchar(255),
#                                       nickname varchar(255),
#                                       email varchar(255),
#                                       dept varchar(255),
#                                       status varchar(255),
#                                       joining_date date,
#                                       account_number varchar(255),
#                                       gross_salary int)''')



					   
def driver():
	with st.form(key='member_form'):
		start_date = st.date_input("When you want to start your Bootcamp?")
		end_date = st.date_input("When you want to complete your Bootcamp?")
		st.write(start_date)
		name = st.text_input("Name")
		email = st.text_input("E-mail")
		institution = st.text_input("Institution")
		phone = st.text_input("Mobile Number")
		address = st.text_area("Address")
		gender = st.radio('select',('select','male','female'))
		cgpa = st.text_input("current_CGPA:")
		status = st.selectbox('status',('In_progress','wait'))
		submit_result = st.form_submit_button("Submit")

		if submit_result:
			# st.sidebar.markdown("Your registration is complete")
			st.write('submit successfully')
			query = '''INSERT INTO student_information (start_date, end_date, name,  email, institution, phone, 
			address, gender,cgpa,status) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)'''
			values = (start_date, end_date, name,  email, institution, phone, 
			address, gender,cgpa,status)
			cursor.execute(query, values)
			db.commit()
			st.success(f'{name} info inserted successfully')

		
def admin():
	st.sidebar.title('Navigation')
	username = st.sidebar.text_input('Username', 'Enter your email', key='user')
	password = st.sidebar.text_input("Enter a password", type="password", key='pass')
	st.session_state.login = st.sidebar.checkbox('login')
	if st.session_state.login:
		if username.split('@')[-1]=="gmail.com" and password == "admin":
			st.write('login seccessfull')
			start_date = st.date_input('start_date')
			end_date = st.date_input('end_date')
			cursor.execute(f"select * from student_information where start_date between '{start_date}' and '{end_date}' and end_date between '{start_date}' and '{end_date}'")
			tables =cursor.fetchall()
			for i in tables:
				x = st.write(f"id: {i[10]}::name: {i[2]} :: cgpa:{i[8]}")
			dx = st.text_input("put your id")
			# st.write(type(dx))
			
			z = st.radio('select',('select','accept','reject'))
			if z == 'accept':
				
				st.write(f'{dx} is accepted by admin ')
				# st.write('accepted')
				cursor.execute(f"Update student_information set status='Accepted' where id='{dx}'")
				db.commit()
			if z == 'reject':
				
				st.write(f'{dx} is rejected by admin ')
				cursor.execute(f"Update student_information set status='Rejected' where id='{dx}'")
				db.commit()
				
				
				# if x:
				# 	accept = st.button("accept",key=i[9])
				# 	if accept:
						# st.write(i[2])
						# st.write('is accepted by admin ')
						# # st.write('accepted')
						# cursor.execute(f"Update student_information set status='Accepted' where id='{i[10]}'")
						# db.commit()
				# 		reject = st.button("reject",key=i[9])
				# 	if reject:
						# st.write(i[2])
						# st.write('is rejected by admin ')
						# cursor.execute(f"Update student_information set status='Rejected' where id='{i[10]}'")
						# db.commit()

				
		else: 
			st.warning('Wrong Credintials')

def info():
	z = st.selectbox('select',('select','information','status'))
	if(z == 'status'):
		# v = st.text_input("id",key = 1)
		st.write("Which id is yours?")
		cursor.execute(f"Select name,id from student_information  ")
		hh=cursor.fetchall()
		# for i in hh:
		# 	x = st.write(f"id: {i[10]}::name: {i[2]} :: cgpa:{i[8]}")
		df = pd.DataFrame(hh, columns=[
                          'name','id'])
		st.write(df)
		# cursor.fetchall()
		# for i in tables:
		# 	x = st.write(f"id: {i[10]}::name: {i[2]} ")
		
		id = st.text_input("put your id")
		cursor.execute(f"Select status from student_information where id='{id}'")
		table=cursor.fetchall()
		df = pd.DataFrame(table, columns=[
                          'status'])
		st.write(df)
	if z == 'information':
		st.write("Which id is yours?")
		cursor.execute(f"Select name,id from student_information  ")
		hh=cursor.fetchall()

		df = pd.DataFrame(hh, columns=[
                          'name','id'])
		st.write(df)


		id = st.text_input("put your id")
		cursor.execute(f"Select * from student_information where id='{id}'")
		table=cursor.fetchall()
		df = pd.DataFrame(table, columns=['start_date', 'end_date', 'name',  'email', 'institution', 'phone', 
		'address', 'gender','cgpa','status','id'])
		st.write(df)
		
	
		
def main():
	st.title("Diploma in Data Science Admission Portal")
	x = st.sidebar.selectbox('select',('select','Admin','Registration','info'))
	if x == 'Admin':
		admin()
	if x == 'Registration':
		# st.sidebar.markdown("hello you are tring to register in our program")
		driver()

	if x == 'info':
		info()

	

if __name__ == '__main__':
    main()





from PyQt5 import  QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow
from library_gui import Ui_MainWindow
import pyodbc as odbc




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_addNewMember.clicked.connect(self.add_new_member)
        self.ui.pushButton_addNewCIty.clicked.connect(self.add_new_city)
        self.ui.pushButton_addNewAuthor.clicked.connect(self.add_new_author)
        self.ui.pushButton_addNewBook.clicked.connect(self.add_new_book)
        self.ui.pushButton_addNewAuthBook.clicked.connect(self.add_new_auth_book)
        self.ui.pushButton_addNewPub.clicked.connect(self.add_new_pub)
        self.ui.pushButton_addNewLoan.clicked.connect(self.add_new_loan)

        self.ui.pushButton_loanDetails.clicked.connect(self.show_loan_details)
        self.ui.pushButton_showMembers.clicked.connect(self.show_members)
        self.ui.pushButton_authorsBooks.clicked.connect(self.show_authors_books)
        self.ui.pushButton_showAvailable.clicked.connect(self.show_available)
        self.ui.pushButton_showAllMembers.clicked.connect(self.show_all_members)
        self.ui.pushButton_renewal.clicked.connect(self.do_renewal)
        self.ui.pushButton_return.clicked.connect(self.do_return)

        self.ui.lineEdit_nameMemb.textChanged.connect(self.show_member_by_name)
        self.ui.lineEdit_nameAuth.textChanged.connect(self.show_author_by_name)
        self.ui.lineEdit_titleBook.textChanged.connect(self.show_book_by_title)

        self.ui.pushButton_deleteMemb.clicked.connect(self.delete_member)
        self.ui.pushButton_deleteBook.clicked.connect(self.delete_book)
    
    def perform_insertion(self,insert_q,values):
        try:
            cursor=connection.cursor()
            cursor.execute(insert_q,values)
            connection.commit()        
        except odbc.Error as e:
            print("Error during insertion:",e)
        finally:
            cursor.close()

    def clear_widgets(self,widgets):
        for widget in  widgets:
            widget.clear()

    def add_new_member(self):
        first_name = self.ui.lineEdit_mfn.text()
        last_name = self.ui.lineEdit_mln.text()
        date_memb = self.ui.dateEdit_memb.text()
        date_paym = self.ui.dateEdit_paym.text()
        type=''
        postal_code=self.ui.lineEdit_mpc.text()
        if(self.ui.radioButton_p1.isChecked()):
            type='U'
        elif(self.ui.radioButton_s1.isChecked()):
            type='S'
        elif(self.ui.radioButton_r1.isChecked()):
            type='R'
        
        widgets=[self.ui.lineEdit_mfn,self.ui.lineEdit_mln,self.ui.lineEdit_mpc]
        
        if first_name!="" and last_name!="" and date_memb !="" and\
           date_paym!="" and type!="" and postal_code!="":
            insert_q="INSERT INTO LIB_MEMBER (FIRST_NAME, LAST_NAME, DATE_OF_MEMBERSHIP, DATE_OF_PAYMENT, TYPE_MEMBER, PBR) VALUES(?,?,?,?,?,?)"
            values= (first_name,last_name,date_memb,date_paym,type,postal_code)
            self.perform_insertion(insert_q,values)
            self.clear_widgets(widgets)


    def add_new_city(self):
        city=self.ui.lineEdit_city.text()
        postal_code = self.ui.lineEdit_pc.text()
        
        widgets=[self.ui.lineEdit_city,self.ui.lineEdit_pc]
        if city!="" and postal_code!="":
            insert_q="INSERT INTO CITY (PBR, CITY_NAME) VALUES(?,?)"
            values = (postal_code,city)
            self.perform_insertion(insert_q,values)
            self.clear_widgets(widgets)
    
    def add_new_author(self):
        first_name = self.ui.lineEdit_afn.text()
        last_name = self.ui.lineEdit_aln.text()
        date_birth = self.ui.dateEdit_birth.text()
        
        widgets=[self.ui.lineEdit_afn,self.ui.lineEdit_aln]
        if first_name!="" and last_name!="" and date_birth!="":
            insert_q="INSERT INTO AUTHOR (FIRST_NAME, LAST_NAME, DATE_OF_BIRTH) VALUES(?,?,?)"
            values = (first_name,last_name,date_birth)
            self.perform_insertion(insert_q,values)
            self.clear_widgets(widgets)

    def add_new_book(self):
        isbn=self.ui.lineEdit_isbn.text()
        number=self.ui.lineEdit_availNum.text()
        title=self.ui.lineEdit_title.text()
        date_publish=self.ui.dateEdit_publish_2.text()
        type = self.ui.lineEdit_type.text()
        pub=self.ui.lineEdit_pubID.text()

        widgets=[self.ui.lineEdit_isbn,self.ui.lineEdit_availNum,self.ui.lineEdit_title,
                 self.ui.lineEdit_type,self.ui.lineEdit_pubID]
        if isbn!="" and number!="" and title!="" and date_publish!="" and type!="" and pub!="":
            insert_q="INSERT INTO BOOK (ISBN,NUMBER_AVAILABLE,TITLE,PUBLISH_DATE,NAME_TYPE,ID_PUBLISHER) VALUES(?,?,?,?,?,?)"
            values = (isbn,number,title,date_publish,type,pub)
            self.perform_insertion(insert_q,values)
            self.clear_widgets(widgets)

    def add_new_auth_book(self):
        book_id=self.ui.lineEdit_IDBook.text()
        auth_id=self.ui.lineEdit_IDAuth.text()

        widgets=[self.ui.lineEdit_IDBook,self.ui.lineEdit_IDAuth]
        if book_id!="" and auth_id!="":
            insert_q="INSERT INTO WRITES (ID_AUTHOR,ID_BOOK) VALUES(?,?)"
            values=(auth_id,book_id)
            self.perform_insertion(insert_q,values)
            self.clear_widgets(widgets)


    def add_new_pub(self):
        pub = self.ui.lineEdit_Pub.text()
        
        widgets=[self.ui.lineEdit_Pub]
        if pub!="":
            insert_q="INSERT INTO PUBLISHER (PUB_NAME) VALUES(?)"
            values=(pub)
            self.perform_insertion(insert_q,values)
            self.clear(widgets)

    def add_new_loan(self):
        memb_id=self.ui.lineEdit_IDMem.text()
        book_id=self.ui.lineEdit_IDBook_2.text()
        date_loan=self.ui.dateEdit_loan.text()
        date_deadline=self.ui.dateEdit_deadline.text()

        widgets=[self.ui.lineEdit_IDMem, self.ui.lineEdit_IDBook_2]
        if memb_id!="" and book_id!="" and date_loan!="" and date_deadline!="":
            insert_q="INSERT INTO LOAN (ID_M,ID_BOOK,DATE_LOAN,DATE_DEADLINE) VALUES(?,?,?,?)"
            values=(memb_id,book_id,date_loan,date_deadline)
            self.perform_insertion(insert_q,values)
            self.clear_widgets(widgets)
    
    def populate_table_view(self,headers,rows):
        model = QtGui.QStandardItemModel(self)
        model.setHorizontalHeaderLabels(headers)
        for row in rows:
            item_row = [QtGui.QStandardItem(str(item)) for item in row]
            model.appendRow(item_row)

        self.ui.tableView.setModel(model)

    def show_loan_details(self):
        memb_id = self.ui.lineEdit_IDLoanMemb.text()
        if memb_id!="":
            cursor = connection.cursor()
            cursor.execute("EXECUTE PRINT_LOAN_DETAILS @idmember=?", memb_id)
            rows = cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            self.populate_table_view(headers,rows)
            cursor.close()

    def show_book_by_title(self):
        text = self.ui.lineEdit_titleBook.text()
        if text!="":
            cursor=connection.cursor()
            cursor.execute("EXECUTE PRINT_BOOK_BY_TITLE ?",text)
            rows = cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            self.populate_table_view(headers,rows)
            cursor.close()

    def show_members(self):
        type=''
        if(self.ui.radioButton_p2.isChecked()):
            type='U'
        elif(self.ui.radioButton_s2.isChecked()):
            type='S'
        elif(self.ui.radioButton_r2.isChecked()):
            type='R'
        
        if type!='':
            cursor=connection.cursor()
            cursor.execute("EXECUTE PRINT_MEMBERS_OF_TYPE ?",(type,))
            rows=cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            self.populate_table_view(headers,rows)
            cursor.close()
    
    def show_authors_books(self):
        auth_id = self.ui.lineEdit_IDAuthorsBooks.text()
        if auth_id!="":
            cursor=connection.cursor()
            cursor.execute("EXECUTE PRINT_BOOKS_OF_AUTHOR ?",auth_id)
            rows=cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            self.populate_table_view(headers,rows)
            cursor.close()


    def show_available(self):
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM AVAILABLE_BOOK')
        rows=cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        self.populate_table_view(headers,rows)
        cursor.close()

    def show_all_members(self):
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM MEMBERS')
        rows=cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        self.populate_table_view(headers,rows)
        cursor.close()

    def do_renewal(self):
        memb_id = self.ui.lineEdit_IDMembRenewal.text()
        if  memb_id!="":
            cursor = connection.cursor()
            cursor.execute('EXECUTE MEMBERSHIP_RENEWAL ?',memb_id)
            connection.commit()
            cursor.close()

    def do_return(self):
        book_id = self.ui.lineEdit_IDBookReturn.text()
        memb_id = self.ui.lineEdit_IDMemberReturn.text()

        if book_id!="" and memb_id!="":
            cursor = connection.cursor()
            cursor.execute('EXECUTE BOOK_RETURN_ENTRY @idBook=?, @idMember=?',(book_id,memb_id))
            connection.commit()
            cursor.close()

            cursor = connection.cursor()
            cursor.execute('EXECUTE CHANGE_AVAILABLE_NUMBER_BY @idBook=?,@n=1', book_id)
            connection.commit()
            cursor.close()

    def show_member_by_name(self):
        text = self.ui.lineEdit_nameMemb.text()
        if text!="":
            cursor=connection.cursor()
            cursor.execute("EXECUTE PRINT_MEMBERS_BY_NAME ?",text)
            rows = cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            self.populate_table_view(headers,rows)
            cursor.close()
    
    def show_author_by_name(self):
        text = self.ui.lineEdit_nameAuth.text()
        if text!="":
            cursor=connection.cursor()
            cursor.execute("EXECUTE PRINT_AUTHOR_BY_NAME ?",text)
            rows = cursor.fetchall()
            headers = [column[0] for column in cursor.description]
            self.populate_table_view(headers,rows)
            cursor.close()

    def delete_member(self):
        ID = self.ui.lineEdit_IDMembDelete.text()
        if ID!="":
            cursor=connection.cursor()
            cursor.execute("EXECUTE REMOVE_MEMBER ?",ID)
            connection.commit()
            cursor.close()

    def delete_book(self):
        ID = self.ui.lineEdit_IDBookDelete.text()
        if ID!="":
            cursor=connection.cursor()
            cursor.execute("EXECUTE REMOVE_BOOK ?",ID)
            connection.commit()
            cursor.close()

if __name__=='__main__':
    DRIVER_NAME='SQL Server'
    SERVER_NAME='DESKTOP-QA0KJU8\SQLEXPRESS'
    DATABASE_NAME='master'

    connection_string = f'DRIVER={{{DRIVER_NAME}}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;'
    connection = odbc.connect(connection_string)

    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
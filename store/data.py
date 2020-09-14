# import sqlite3
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','store.settings')
# import django
# django.setup()
# from django.contrib.auth.models import User
# from basicapp.models import UserProfileInfo,UserDealers,UserStock

# class Store:
#     def __init__(self):
#         self.conn=sqlite3.connect("store.db")
#         self.cur=self.conn.cursor()
#         self.cur.execute("CREATE TABLE IF NOT EXISTS STORE(id INTEGER PRIMARY KEY,dealer text,name text,rate real,mrp real)")
#         self.conn.commit()
#     def insert(self,dealer,name,rate,mrp):
#         self.cur.execute("INSERT INTO STORE VALUES(NULL,?,?,?,?)",(dealer,name,rate,mrp))
#         self.conn.commit()
#     def view(self):
#         self.cur.execute("SELECT * FROM STORE ORDER BY dealer")
#         rows=self.cur.fetchall()
#         return rows
#     def viewdealer(self):
#         self.cur.execute("SELECT DISTINCT dealer FROM STORE")
#         rows=self.cur.fetchall()
#         return rows
#     def search(self,id=-1,dealer="",name="",rate=-1,mrp=-1):
#         self.cur.execute("SELECT * FROM STORE WHERE id=? OR dealer=? OR name LIKE ? OR rate=? OR mrp=? ORDER BY dealer",(id,dealer,name,rate,mrp))
#         rows=self.cur.fetchall()
#         return rows
#     def delete(self,id):
#         self.cur.execute("DELETE FROM STORE WHERE id=?",(id,))
#         self.conn.commit()
#     def update(self,id,dealer,name,rate,mrp):
#         self.cur.execute("UPDATE STORE SET dealer=?,name=?,rate=?,mrp=? WHERE id=?",(dealer,name,rate,mrp,id))
#         self.conn.commit()
#     def __del__(self):
#         self.conn.close()

# store=Store()
# # x=0
# # for row in store.view():
# #     x+=1
# #     print(x,row)

# # df1=pandas.DataFrame(store.view(),columns=["id","Dealer","Item","Rate","Mrp"])
# # del  df1["id"]
# # with open("order"+".txt","a+") as f:
# #     f.write(df1.to_string()+"\n")

# def userd():
#     user = User.objects.create_user('umesh', 'muffersoft@gmail.com', 'qwerty123')
#     user.first_name = 'umesh'
#     user.save()
#     return user

# d1 = {}
# u = userd()
# def dealerd():
#     for row in store.viewdealer():
#         d=row[0]
#         dealerdet=UserDealers.objects.get_or_create(owner=u,dealer=d)[0]
#         d1.update({d: dealerdet})

# def itemadd():
#     for row in store.view():
#         itemname=row[2]
#         dealername=row[1]
#         itemrate=row[3]
#         itemmrp=row[4]
#         if itemrate=='':
#             itemrate=0
#         if itemmrp == '':
#             itemmrp = 0
#         itemin=UserStock.objects.get_or_create(owner=u, dealer=d1[dealername],item=itemname,rate=itemrate,mrp=itemmrp)[0]

# if __name__ == "__main__":
#     dealerd()
#     itemadd()
#     print("populated")

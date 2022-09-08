from flask import Flask,redirect, render_template, request, session,flash 
import sqlite3 as sql
import os
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.static_folder = 'static'

conn = sql.connect('otel.db')
conn.execute('CREATE TABLE IF NOT EXISTS  users (userId INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL , email TEXT , password TEXT NOT NULL, role TEXT NOT NULL)')
conn.execute('CREATE TABLE IF NOT EXISTS  rezervasyonlar (id INTEGER PRIMARY KEY AUTOINCREMENT,uyeadi TEXT,adsoyad TEXT, odatipi TEXT, giristarihi TEXT, cikistarihi TEXT, yetiskinsayi TEXT, cocuksayi TEXT,telno TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS  odalar (oda_id INTEGER PRIMARY KEY AUTOINCREMENT, oda_tipi TEXT, oda_sayisi INTEGER)')
conn.close()


@app.route('/', methods=['GET'])
def home():
   return render_template("/index.html") 
@app.route('/silsil/<id>')
def urunsil(id):
   db_uri =  'sqlite:///otel.db'
   engine = create_engine(db_uri)
   conn = engine.connect()
   sql = 'DELETE FROM rezervasyonlar WHERE id=?'
   conn.execute(sql, (id,))
   db_uri =  'sqlite:///otel.db'
   engine = create_engine(db_uri)
   conn = engine.connect()
   return admin()
@app.route('/rezsil/<id>')
def rezsil(id):
   db_uri =  'sqlite:///otel.db'
   engine = create_engine(db_uri)
   conn = engine.connect()
   sql = 'DELETE FROM rezervasyonlar WHERE id=?'
   conn.execute(sql, (id,))
   db_uri =  'sqlite:///otel.db'
   engine = create_engine(db_uri)
   conn = engine.connect()
   return purchasingHistory()
@app.route('/admin')
def admin():
   if not session.get('loggedIn'):
      flash("Kullanıcı Girişi Yapılmadan Alışveriş Geçmişi Görüntülenemez")
      return redirect('login')
      #oturum kontrolu
   con=sql.connect('otel.db')
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM rezervasyonlar")
   joinRows=cur.fetchall()
   pHistory = []
   cur.execute("SELECT * FROM odalar")
   odalarr=cur.fetchall()
   pHistoryy = []
   for row in joinRows:
      pHistory.append(row)
   for oda in odalarr:
      pHistoryy.append(oda)
   return render_template("/admin.html" , rows = pHistory, oda=pHistoryy)
@app.route('/odalar')
def odalar():
   if not session.get('loggedIn'):
      flash("Kullanıcı Girişi Yapılmadan Alışveriş Geçmişi Görüntülenemez")
      return redirect('login')
      #oturum kontrolu
   con=sql.connect('otel.db')
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM odalar")
   joinRows=cur.fetchall()
   pHistory = []
   for row in joinRows:
      pHistory.append(row)
   return render_template("/odalar.html" , rows = pHistory)
@app.route('/uyegiris', methods=['POST'])
def authentication():
   con=sql.connect('otel.db')
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM users")
   # Tüm kullanıcılar çekilir
   userRows=cur.fetchall()
   for row in userRows:
      if request.form['name'] == row['name'] and check_password_hash(row['password'],request.form['password']):
         # kullanıcı adı ve şifresi girilen değerlerle uyuşursa aşağıdaki işlemleri gerçekleştir
         session['userName'] = request.form['name']
         session['userId'] = row['userId']
         session['loggedIn'] = True
         # login kontrolu için
         session['role'] = row['role']
         # permission kontrolleri için
         break 
   if not session.get('loggedIn'):
      flash("HATALI KULLANICI")
      return redirect('/login')
   else:
      if session['userName'] == "admin":
         return redirect('/admin')
      else:
         return redirect('/')
@app.route('/degistir/<id>',methods = ['POST', 'GET'])
def degistir(id):
   if request.method == 'POST':   
      try:
         adsoyad = request.form['adsoyad']
         odatipi = request.form['odatipi']
         giristarihi = request.form['giristarihi']
         cikistarihi = request.form['cikistarihi']
         yetiskinsayi = request.form['yetiskinsayi']
         cocuksayi = request.form['cocuksayi']
         telno = request.form['telno']
         # formdan gelen veriler tutularak update için veri tabanına yollanır
         with sql.connect("otel.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE rezervasyonlar SET adsoyad = ? , odatipi = ?, giristarihi = ? , cikistarihi = ? , yetiskinsayi = ? , cocuksayi = ? , telno = ? WHERE id=?", (adsoyad, odatipi, giristarihi, cikistarihi, yetiskinsayi, cocuksayi, telno, id))
            con.commit()
            flash("Güncelleme başarılı")   
      except:
         con.rollback()
         flash("Güncelleme işlemi sırasında  bir hata oluştu , tekrar deneyiniz")
      
      finally:
         con.close()
         return admin()
@app.route('/kdegistir/<id>',methods = ['POST', 'GET'])
def kdegistir(id):
   if request.method == 'POST':   
      try:
         adsoyad = request.form['adsoyad']
         odatipi = request.form['odatipi']
         giristarihi = request.form['giristarihi']
         cikistarihi = request.form['cikistarihi']
         yetiskinsayi = request.form['yetiskinsayi']
         cocuksayi = request.form['cocuksayi']
         telno = request.form['telno']
         # formdan gelen veriler tutularak update için veri tabanına yollanır
         with sql.connect("otel.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE rezervasyonlar SET adsoyad = ? , odatipi = ?, giristarihi = ? , cikistarihi = ? , yetiskinsayi = ? , cocuksayi = ? , telno = ? WHERE id=?", (adsoyad, odatipi, giristarihi, cikistarihi, yetiskinsayi, cocuksayi, telno, id))
            con.commit()
            flash("Güncelleme başarılı")   
      except:
         con.rollback()
         flash("Güncelleme işlemi sırasında  bir hata oluştu , tekrar deneyiniz")
      
      finally:
         con.close()
         return purchasingHistory()
@app.route('/odaguncelle',methods = ['POST', 'GET'])
def odaguncelle():
   if request.method == 'POST':   
      try:
         odaid = request.form['odaid']
         odasayisi = request.form['odasayisi']
         # formdan gelen veriler tutularak update için veri tabanına yollanır
         with sql.connect("otel.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE odalar SET oda_sayisi = ? WHERE oda_id=?", (odasayisi, odaid))
            con.commit()
            flash("Güncelleme başarılı")   
      except:
         con.rollback()
         flash("Güncelleme işlemi sırasında  bir hata oluştu , tekrar deneyiniz")
      
      finally:
         con.close()
         return admin()
@app.route('/ekle'  , methods=['POST'])
def buyCart():
      try:
         userId = session.get('userName')
         odatipii = request.form['odatipi']
         telno = request.form['telno']
         giristarihi = request.form['giristarihi']
         cikistarihi = request.form['cikistarihi']
         yetiskinsayi = request.form['yetiskinsayi']
         cocuksayi = request.form['cocuksayi']
         adsoyad = request.form['adsoyad']
         if odatipii == 'Tekli Oda':
            azalt=1;
         elif odatipii == 'Aile Odasi':
            azalt=2;
         elif odatipii == 'Cift Kisilik Oda':
            azalt=3;
         elif odatipii == 'VIP Oda':
            azalt=4;
         else:
            azalt=1;
         with sql.connect("otel.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO rezervasyonlar (uyeadi,adsoyad, odatipi,giristarihi,cikistarihi,yetiskinsayi,cocuksayi,telno) VALUES (?,?,?,?,?,?,?,?)", (userId,adsoyad,odatipii,giristarihi,cikistarihi,yetiskinsayi,cocuksayi,telno))
            cur.execute("UPDATE odalar SET oda_sayisi=oda_sayisi-1 WHERE oda_id=?",(azalt,))
            # kullanıcı satın al  butonuna bastıktan sonra saledProducts tablosuna insert işlemi yapılır 
            con.commit()
      except:
         con.rollback()
         flash("Satın alma sırasında bir hata meydana geldi")
         return redirect('/HATA')
      finally:
         con.close()
         return redirect('/rezervasyongecmisi')
         flash("satın alma işlemi başarılı")     
@app.route('/rezervasyongecmisi')
def purchasingHistory():
   if not session.get('loggedIn'):
      flash("Kullanıcı Girişi Yapılmadan Alışveriş Geçmişi Görüntülenemez")
      return redirect('login')
      #oturum kontrolu
   con=sql.connect('otel.db')
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM rezervasyonlar")
   joinRows=cur.fetchall()
   pHistory = []
   for row in joinRows:
      if row['uyeadi'] == session.get('userName'):
         # eğer oturum açan kullanıcının id si ile eşleşen veriler varsa listeye alıp profile.html'e prop olarak yollarız.
         pHistory.append(row)
   return render_template("/listele.html" , rows = pHistory)
@app.route('/duzenle/<idd>', methods = ['POST', 'GET'])
def duzenle(idd):
   con=sql.connect('otel.db')
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM rezervasyonlar WHERE id=?",(idd,))
   joinRows=cur.fetchall()
   pHistory = []
   for row in joinRows:
         pHistory.append(row)
   con.close()
   return render_template("/rezduzenle.html" , rows = pHistory)

@app.route('/kduzenle/<idd>', methods = ['POST', 'GET'])
def kduzenle(idd):
   con=sql.connect('otel.db')
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("SELECT * FROM rezervasyonlar WHERE id=?",(idd,))
   joinRows=cur.fetchall()
   pHistory = []
   for row in joinRows:
         pHistory.append(row)
   con.close()
   return render_template("/krezduzenle.html" , rows = pHistory)
@app.route('/login')
def login():
   return render_template('/login.html')

@app.route("/logout")
def logout():
    session['loggedIn'] = False
    session['userName']="";
    # kullanıcı çıkış yaptığında loggedIn kontrolu ve sepet sıfırlanır
    return home()

@app.route('/kayit')
def kayit():
   return render_template('/kayit.html')
@app.route('/gir')
def girrr():
   return render_template('/login.html')
@app.route('/kayit_ekle',methods = ['POST', 'GET'])
def kayit_ekle():
   if request.method == 'POST':
      try:
         name = request.form['name']
         email = request.form['email']
         passw = generate_password_hash(request.form['password'])
         # kullanıcının girdiği şifreyi hashleyerek kaydeder
         role="user"
         # kullanıcı role'u default olarak user'dır bir kullanıcı rol seçemez
         with sql.connect("otel.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (name,email,password,role) VALUES (?,?,?,?)", (name,email,passw,role))
            # Girilen verileri user tablosuna insert eder
            con.commit()
            msg = "Kayıt başarılı , giriş yapabilirsiniz"
      except:
         con.rollback()
         msg = "Kayıt işlemi sırasında  bir hata oluştu , tekrar deneyiniz"
      
      finally:
         con.close()
         msg="Kayıt Basarılı Giriş Yapabilirsiniz"
         return render_template("login.html",msg = msg)


if __name__ == '__main__':
   app.secret_key = os.urandom(12)
   app.run(host='127.0.0.1', port=5005, debug=True)
   app.run(debug = True)
#!/usr/bin/python
import re
import string
import MySQLdb
from flask import Flask, render_template, request, session, redirect,url_for
from flask_mysqldb import MySQL
from flask_qrcode import QRcode
import random
from flask_mail import Mail,Message
import bcrypt
import json

app = Flask(__name__,static_url_path='/static')
mail = Mail(app)

app.secret_key = 'geebang'
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'geebang_db'

app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'quentin.dubois72@hotmail.fr'
app.config['MAIL_PASSWORD'] = 'Legendaires'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

mysql = MySQL(app)
QRcode(app)

@app.route('/', methods=['GET', 'POST'])
def accueil():
    return render_template("accueil.html",msg="")

@app.route('/restaurateur', methods=['GET', 'POST'])
def restaurateur():
    return render_template("page_restaurateur.html",msg="")

@app.route('/interface_restaurateur', methods=['GET', 'POST'])
def interface_restau():
    if request.method == 'POST':
        donnees = request.form
        nbr_points = donnees['points']
        description = donnees['description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO promotions_db(restaurant,points_necessaires,description,nb_scan) VALUES (%s, %s, %s,%s)",
                    (session['restaurant'], nbr_points, description, int(0)))
        mysql.connection.commit()

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM promotions_db WHERE restaurant = %s', (session['restaurant'],))
    mysql.connection.commit()
    data = cursor.fetchall()

    return render_template("interface_restaurateur.html",data=data,msg=session['restaurant'])

@app.route('/delete_promo/<int:index>')
def delete_promo(index):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM promotions_db WHERE id_promo = %s",(index,))
    mysql.connection.commit()
    return redirect(url_for('interface_restau'))

@app.route('/modif_promo', methods=['POST'])
def modif_promo():
    details = request.form
    pts = details['points_modif']
    desc = details['description_modif']
    id = details['id_modif']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE promotions_db SET points_necessaires = %s, description = %s WHERE id_promo = %s", (pts,desc,id,))
    mysql.connection.commit()
    return redirect(url_for('interface_restau'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        #Recupere les données envoyées par le form et check si le mail est conforme
        details = request.form
        mail = details['mail']
        if(CheckEmail(mail) is False):
            error = 'Mail invalide'
            return render_template('accueil.html', msg=error)

        #Check si le mail existe
        motdepasse = details['motdepasse']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users_db WHERE mail = %s', (mail,))
        mysql.connection.commit()
        account = cursor.fetchone()

        #si mail existe, test le mdp
        if account:
            hash_pw = "".join(account[3]).encode('utf8')
            motdepasse_enc = motdepasse.encode('utf8')
            if bcrypt.checkpw(motdepasse_enc,hash_pw):
                session['login'] = True
                session['mail'] = mail

                # Recuperer le nombre de points de l'User
                new_tuple = tuple(map(str, account))
                session['points'] = " ".join(new_tuple[4])

                # Recuperer le prenom de l'User
                session['prenom'] = "".join(account[1])

                #Tester si c'est un Admin
                test_admin = False
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT prenom FROM admin_db WHERE mail = %s', (mail,))
                mysql.connection.commit()
                admin = cursor.fetchone()
                if admin:
                    test_admin = True

                # Tester si c'est un restaurateur
                cursor.execute('SELECT nom_restau FROM restaurateurs_db WHERE mail = %s', (mail,))
                mysql.connection.commit()
                restaurateur = cursor.fetchone()
                if restaurateur:
                    session['restaurant'] = "".join(restaurateur[0])
                    return redirect(url_for('interface_restau'))
                return render_template('accueil.html',msg = "Bienvenue " + session['prenom'] + ", vous avez actuellement "+session['points']+" points sur Geebang !")
            else:
                error = 'Mot de Passe invalide'
                return render_template('accueil.html', msg=error)
        else:
            error = 'Mail invalide'
            return render_template('accueil.html', msg=error)

    return render_template('loginform.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        details = request.form
        cursor = mysql.connection.cursor()
        mail = details['mail']
        if (CheckEmail(mail) is False):
            error = 'Mail invalide'
            return render_template('accueil.html', msg="Email invalide")

    #####################   RESTAURATEUR    ###################

        code_restau = details['code_restaurateur']
        if code_restau is not None:
            cursor.execute('SELECT * FROM restaurants_db WHERE code_restau = %s ', (code_restau,))
            mysql.connection.commit()
            if cursor is not None:
                data = cursor.fetchone()
                try:
                    motdepasse = details['motdepasse']
                    mdp_hash =bcrypt.hashpw(motdepasse.encode('utf-8'), bcrypt.gensalt())
                    prenom = details['prenom']
                    session['prenom'] = prenom
                    nom = details['nom']

                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO users_db(nom,prenom,mail,motdepasse,points) VALUES (%s, %s, %s, %s,%s)",
                                (nom, prenom, mail, mdp_hash,int(0)))
                    mysql.connection.commit()

                    restaurant = "".join(data[0])
                    cur.execute("INSERT INTO restaurateurs_db(nom,prenom,mail,motdepasse,nom_restau) VALUES (%s, %s, %s, %s,%s)",
                                (nom, prenom, mail, mdp_hash,restaurant))
                    mysql.connection.commit()
                    cur.close()
                    return render_template('accueil.html',msg = "Bienvenue " + prenom + ", merci de votre inscription en tant que restaurateur!")
                except Exception:
                    return render_template('404.html',msg = "inscription restaurateur ko")
            cursor.close()

        cursor.execute('SELECT * FROM users_db WHERE mail = %s', (mail,))
        mysql.connection.commit()
        if cursor is not None:
            cursor.close()
            try:
                motdepasse = details['motdepasse']
                mdp_hash = bcrypt.hashpw(motdepasse.encode('utf-8'), bcrypt.gensalt())
                prenom = details['prenom']
                nom = details['nom']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users_db(nom,prenom,mail,motdepasse) VALUES (%s, %s, %s, %s)",
                            (nom,prenom, mail, mdp_hash))
                mysql.connection.commit()
                cur.close()
                return render_template('accueil.html',msg = "Bienvenue " + prenom + ", merci de ton inscription !")
            except Exception:
                return render_template('404.html',msg = "inscription ko")
        return render_template('404.html',msg = "email existant")
    return render_template('register_page.html')

@app.route('/logout')
def logout():
    session.pop('mail',None)
    session.pop('restaurant', None)
    session.pop('prenom', None)
    session.pop('points', None)
    session.pop('restaurateur', None)
    session.pop('admin', None)
    session.pop('login',False)
    return redirect(url_for('accueil'))

@app.route('/DemandeDevis', methods=['GET', 'POST'])
def Devis():
    if request.method == 'POST':
        details = request.form
        msg = Message("Geebang - Demande Devis de "+details["devis_etab"], sender="quentin.dubois72@hotmail.fr", recipients=["quentin.dubois72@hotmail.fr"])
        msg.body = details["devis_message"]+"\n\n"+details["devis_prenom"]+" "+details["devis_nom"]+", "+\
                   details["devis_ville"]+", "+details["devis_etab"]+", "+details["devis_ville"]
        mail.send(msg)

    return render_template('page_restaurateur.html')

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/QRcode', methods=['GET', 'POST'])
def CreationQRCode():
    str = string.ascii_lowercase
    QRcode_string =  ''.join(random.choice(str) for i in range(15))
    print(QRcode_string)
    return render_template("UserInterface.html",code=QRcode_string)

@app.route('/AjouterPoint', methods=['POST'])
def AjouterPoint():
    mail = request.form['javascript_data']
    cur = mysql.connection.cursor()
    cur.execute('SELECT points FROM users_db WHERE mail = %s', (mail,))
    data = cur.fetchone()
    new_tuple = tuple(map(str, data))
    points = " ".join(new_tuple[0])
    new_points = str(int(points)+1)


    cur.execute("UPDATE users_db SET points = %s WHERE mail = %s",(str(new_points),mail))
    mysql.connection.commit()
    return redirect(url_for('accueil'))


def CheckEmail(email):
    if (re.fullmatch(regex, email)):
        return True;
    else:
        return False;
if __name__ == '__main__':
    app.run()
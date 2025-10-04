
import os
from dotenv import load_dotenv
import mercadopago
from flask import Flask, render_template,session, redirect, url_for, request, jsonify, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import requests
from werkzeug.utils import secure_filename
import mercadopago
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

from database import db, Usuario, Categoria, Producto, ProductoImagen, Pedido, PedidoItem

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


MP_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN')
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

#VERIFICACION EMAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Correo de Gmail
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Contraseña de la aplicación
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME') 

# Inicializar Flask-Mail
mail = Mail(app)

# Para generar tokens
serializer = URLSafeTimedSerializer(app.config['MAIL_USERNAME'])


#BASE DE DATOS
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'mi_base.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)
app.app_context().push()  

#RECAPTCHA
RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

#FUNCIONES

def enviar_correo(destinatario, asunto, mensaje):
    msg = Message(asunto,
                  sender='bairescandybox@gmail.com',
                  recipients=[destinatario])
    msg.body = mensaje
    mail.send(msg)


def obtener_productos_por_tipo(tipo):
    if tipo == "candybox":
        return "Candy Box",Producto.query.filter_by(categoria_id=1).all()  
    elif tipo == "activitybox":
        return "Activity Box",Producto.query.filter_by(categoria_id=2).all()  
    elif tipo == "plantillasdigitales":
        return "Plantillas Digitales",Producto.query.filter_by(categoria_id=3).all()
    else:
        return "Eror", [] 

#CONTEXTO GLOBAL
@app.context_processor
def inyectar_usuario():
    usuario_id = session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.query.get(usuario_id)
        return dict(usuario=usuario)
    return dict(usuario=None)


#RUTAS
@app.route('/')
def index():
    usuario = None
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])

    return render_template('home.html', usuario=usuario)

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        mensaje = request.form.get("mensaje")

        try:
            # Email que recibís vos (administrador)
            msg = Message(
                subject=f"Consulta de {nombre}",
                recipients=["bairescandybox@gmail.com"],  
                body=f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"
            )
            mail.send(msg)

            # Respuesta automática al cliente
            respuesta = Message(
                subject="Gracias por tu consulta",
                recipients=[email],
                body=f"Hola {nombre},\n\nRecibimos tu mensaje y te responderemos pronto.\n\nSaludos,\nBairesCandyBox"
            )
            mail.send(respuesta)

            flash("Mensaje enviado con éxito. ¡Gracias por contactarnos!", "success")
        except Exception as e:
            print("Error al enviar correo:", e)
            flash("Hubo un problema al enviar el mensaje.", "danger")

        return redirect(url_for("contacto"))

    return render_template("contacto.html")


@app.route('/como_comprar', methods=['GET'])
def como_comprar(): 
    return render_template('comocomprar.html')

@app.route('/informacion_util', methods=['GET', 'POST'])
def preguntas_frecuentes():
    return render_template('info_util.html')

@app.route('/quien_soy', methods=['GET', 'POST'])
def quien_soy():
    return render_template('quien_soy.html')

@app.route('/usuarios_registrados', methods=['GET', 'POST'])
def usuarios_registrados():
    usuarios = Usuario.query.all()
    return render_template('usuarios_registrados.html', usuarios=usuarios)

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    pedidos = Pedido.query.all()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/eliminar_pedido/<int:pedido_id>', methods=['POST'])
def eliminar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    PedidoItem.query.filter_by(pedido_id=pedido.id).delete()
    db.session.delete(pedido)
    db.session.commit()
    flash('Pedido eliminado correctamente.', 'success')
    return redirect(url_for('pedidos'))

@app.route("/catalogo/<tipo>", methods=["GET"])
def catalogo(tipo):
    tipo_categoria, productos = obtener_productos_por_tipo(tipo)
    
    if len(productos) == 0:
        return render_template('catalogo.html', tipo=tipo_categoria, texto=True)
    else:
        return render_template('catalogo.html', tipo=tipo_categoria, productos=productos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email-login')
        password = request.form.get('password-login')
        
        errores = {}
        
        if not email:
            errores['email'] = '* Ingresa un email valido.'
        if not password:
            errores['password'] = '* Ingresa una contraseña.'
        
        if errores:
            return render_template('login.html', errores=errores)
        else:
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.password, password):
                if not usuario.email_verificado:
                    return render_template('login.html', errores={'email': '* Debes verificar tu email.'})
                
                session['usuario_id'] = usuario.id
                return redirect(url_for('index'))
            else:
                return render_template('login.html', errores={'login': '* Email o contraseña incorrectos.'})
    else:
        return render_template('login.html', errores={})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        nombre = request.form.get('nombre-registro')
        email = request.form.get('email-registro')
        password = request.form.get('password-registro')
        confirm_password = request.form.get('confirm-password-registro')
        recaptcha_response = request.form.get('g-recaptcha-response')
        
        errores = {}
        
        if not nombre:
            errores['nombre'] = '* Ingresa tu nombre.'
        if not email:
            errores['email'] = '* Ingresa un email valido.'
        if not password:
            errores['password'] = '* Ingresa una contraseña.'
        elif len(password) < 8:
            errores['password'] = '* La contraseña debe tener al menos 8 caracteres.'
        if not confirm_password:
            errores['confirm_password'] = '* Confirma tu contraseña.'
        elif password != confirm_password:
            errores['confirm_password'] = '* Las contraseñas no coinciden.'
        if not recaptcha_response:
            errores['recaptcha'] = '* Por favor completa el reCAPTCHA.'
        
        if errores:
            return render_template('register.html', errores=errores, site_key=RECAPTCHA_SITE_KEY)
        else:
            hashed_password = generate_password_hash(password) 
            nuevo_usuario = Usuario(nombre=nombre, email=email, password=hashed_password, email_verificado=False, rol='usuario')
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            usuario = Usuario.query.filter_by(email=email).first()          
            
            # Generar token de verificación
            token = serializer.dumps(email, salt='email-confirm')
            
            # Crear URL de verificación
            confirm_url = url_for('confirm_email', token=token, _external=True)
            
            # Crear y enviar mensaje
            enviar_correo(email, "Confirma tu correo", f'Hola {nombre}, por favor confirmá tu correo haciendo clic en el siguiente enlace:\n{confirm_url}')
            
            flash('Te enviamos un correo para verificar tu cuenta.', 'info')
            return redirect(url_for('login'))
    
    return render_template('register.html', site_key=RECAPTCHA_SITE_KEY, errores={})


     
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)  # 1 hora válido
    except:
        flash('El enlace de verificación expiró o no es válido.', 'danger')
        return redirect(url_for('login'))
    
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        usuario.email_verificado = True
        db.session.commit()
    else:
        flash('Usuario no encontrado.', 'danger')
    return redirect(url_for('login'))

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return f"Usuario con ID {id} eliminado."
    else:
        return "Usuario no encontrado."


     
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(usuario_id)

    return render_template('perfil.html', usuario=usuario)



@app.route('/admin')
def admin():
    return render_template('administrador.html')

@app.route('/admin_producto')
def admin_producto():
    productos_candybox = Producto.query.filter_by(categoria_id=1)
    productos_activity = Producto.query.filter_by(categoria_id=2)
    productos_plantillas = Producto.query.filter_by(categoria_id=3)
    return render_template('admin_producto.html', productos_candybox=productos_candybox, productos_activity=productos_activity, productos_plantillas=productos_plantillas)

@app.route('/eliminar_producto/<int:prod_id>')
def eliminar_producto(prod_id):
    imagenes=ProductoImagen.query.filter_by(producto_id=prod_id)
    for img in imagenes:
        db.session.delete(img)
    
    producto = Producto.query.filter_by(id=prod_id).first()
    db.session.delete(producto)
    db.session.commit()
    
    return redirect(url_for('admin_producto'))

@app.route('/editar_producto/<int:producto_id>')
def editar_producto(producto_id):
    producto = Producto.query.filter_by(id=producto_id).first()
    return render_template('editar_producto.html', producto=producto)

@app.route('/actualizar_producto/<int:producto_id>', methods=['GET', 'POST'])
def actualizar_producto(producto_id):
    if request.method == 'POST':
        producto = Producto.query.filter_by(id=producto_id).first()
        producto.nombre = request.form['nombre']
        precio=float(request.form['precio'])
        producto.precio = precio
        producto.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('admin_producto'))

@app.route('/nuevo_producto')
def nuevo_producto():
    return render_template('agregar_producto.html')

@app.route('/agregar_producto',methods = ['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre=request.form['nombre']
        precio=float(request.form['precio'])
        descripcion=request.form['descripcion']
        if not descripcion:
            descripcion="El producto no tiene descripción"
        id_categoria=request.form['categoria']
        
        imagen_principal = request.files.get('imagen_principal')
        imagenes_secundarias = request.files.getlist('imagenes_secundarias')

        nombre_archivo_principal = secure_filename(imagen_principal.filename)
        ruta_principal = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo_principal)
        imagen_principal.save(ruta_principal)
        
        nuevo_producto=Producto(nombre=nombre,precio=precio,descripcion=descripcion,categoria_id=id_categoria,imagen_principal=nombre_archivo_principal,fecha_creacion=date.today())
        db.session.add(nuevo_producto)
        db.session.commit()
        
        for imagen in imagenes_secundarias:
            if imagen and imagen.filename != '':
                filename = secure_filename(imagen.filename)
                filepath = os.path.join('static/uploads', filename)
                imagen.save(filepath)

                nueva_imagen = ProductoImagen(
                    producto_id=nuevo_producto.id,
                    url=f'uploads/{filename}' 
                )
                db.session.add(nueva_imagen)

        db.session.commit()
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('admin'))

@app.route('/producto/<int:producto_id>',methods=['GET','POST'])
def pagina_producto(producto_id):
    producto = Producto.query.filter_by(id=producto_id).first()
    categoria=""
    if producto.categoria_id==1:
        categoria = "candybox"
    elif producto.categoria_id==2:
        categoria = "activitybox"
    elif producto.categoria_id==3:
        categoria = "plantillasdigitales"
    fotos_secundarias = ProductoImagen.query.filter_by(producto_id=producto_id).all()
    return render_template('producto.html',producto=producto, fotos_secundarias=fotos_secundarias, categoria=categoria)


@app.route('/datos-personales/<int:id>', methods=['POST','GET'])
def datos_personales(id):
    usuario_id = session.get('usuario_id')
    producto = Producto.query.filter_by(id=id).first()
    if not usuario_id:
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(usuario_id)
    
    if request.method =='GET':
        cantidad = request.args.get('cantidad', type=int)    
        total= producto.precio * cantidad
        return render_template('confirmar-compra.html', usuario=usuario, total=total, producto=producto, cantidad=cantidad)


@app.route('/datos-personales-agregar', methods=['POST'])
def agregar_datos_compra():
    usuario_id = session.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)
    valido=True


    if not usuario_id:
        return redirect(url_for('login'))
    
    if request.method=='POST':
        email_compra=request.form.get('email-compra')
        if not email_compra:
            valido=False
        nombre_compra=request.form.get('nombre-compra')
        if not nombre_compra:
            valido=False
        apellido_compra=request.form.get('apellido-compra')
        if not apellido_compra:
            valido=False
        telefono_compra=request.form.get('telefono-compra')
        if not telefono_compra:
            valido=False
        postal_compra=request.form.get('postal-compra')
        if not postal_compra or len(postal_compra)>4:
            valido=False
        otra_persona = bool(request.form.get('otra-persona'))
        nombre_compra_retira=request.form.get('nombre-compra-retira')
        apellido_compra_retira=request.form.get('apellido-compra-retira')
        
        if not otra_persona:
            nombre_compra_retira = nombre_compra
            apellido_compra_retira = apellido_compra
        elif otra_persona:
            if not nombre_compra_retira:
                valido=False
            if not apellido_compra_retira:
                valido=False
        provincia_compra=request.form.get('provincia-compra')
        if not provincia_compra:
            valido=False
        ciudad_compra=request.form.get('ciudad-compra')
        if not ciudad_compra:
            valido=False
        barrio_compra=request.form.get('barrio-compra')
        if not barrio_compra:
            valido=False
        calle_compra=request.form.get('calle-compra')
        if not calle_compra:
            valido=False
        numero_calle_compra=request.form.get('numero-calle-compra')
        if not numero_calle_compra:
            valido=False
        dapartamento_compra=request.form.get('dapartamento-compra')
        precio_unitario = request.form.get('precio_unitario')
        cantidad = int(request.form.get('cantidad_compra_final'))
        producto_id = int(request.form.get('id_producto_compra'))
        producto = Producto.query.filter_by(id=producto_id).first()
        nombre_producto = producto.nombre
        
        if valido:
            pedido = Pedido(
                        usuario_id=usuario_id,
                        email=email_compra,
                        nombre=nombre_compra,
                        apellido=apellido_compra,
                        telefono=telefono_compra,
                        codigo_postal=postal_compra,
                        provincia=provincia_compra,
                        ciudad=ciudad_compra,
                        barrio=barrio_compra,
                        calle=calle_compra,
                        numero_calle=numero_calle_compra,
                        departamento=dapartamento_compra,
                        retira_otro=otra_persona,
                        nombre_retira=nombre_compra_retira,
                        apellido_retira=apellido_compra_retira,
                        total=precio_unitario*cantidad
            )
            db.session.add(pedido)
            db.session.commit()

            pedido_item = PedidoItem(
                pedido_id=pedido.id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            db.session.add(pedido_item)
            db.session.commit()
            
            return redirect(url_for('crear_pago', pedido_id=pedido.id))
        else:
            return redirect(url_for('datos_personales',id=producto_id, cantidad=cantidad))        

# MERCADO PAGO
@app.route("/crear_pago")
def crear_pago():
    pedido_id = int(request.args.get("pedido_id"))
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        return "Pedido no encontrado", 404

    # Crear preferencia de Mercado Pago
    preference_data = {
        "items": [
            {
                "title": f"Pedido #{pedido.id} - {pedido.nombre}",
                "quantity": 1,
                "unit_price": pedido.total,
            }
        ],
        "back_urls": {
            "success": "https://45428033c30a.ngrok-free.app/",
            "failure": "https://45428033c30a.ngrok-free.app/",
            "pending": "https://45428033c30a.ngrok-free.app/"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    # Guardar el payment_id en el pedido
    pedido.pago_id = preference["id"]
    db.session.commit()

    # Redirigir al checkout de Mercado Pago
    return redirect(preference["init_point"])


# Solicitar restablecimiento
@app.route('/olvido_password', methods=['GET', 'POST'])
def olvido_password():
    if request.method == 'POST':
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario:
            # Generar token temporal de 1 hora
            token = serializer.dumps(email, salt='password-reset')
            reset_url = url_for('reset_password', token=token, _external=True)
            
            msg = Message(
                subject='Restablecer contraseña',
                recipients=[email],
                body=f"Hola {usuario.nombre},\n\n"
                     f"Para cambiar tu contraseña haz clic en el siguiente enlace:\n{reset_url}\n\n"
                     f"Si no solicitaste esto, ignora este correo."
            )
            mail.send(msg)
            
            flash('Te enviamos un enlace para restablecer tu contraseña.', 'success')
            return redirect(url_for('login'))
        else:
            flash('No se encontró un usuario con ese email.', 'danger')
            return render_template('olvido_password.html')
    
    return render_template('olvido_password.html')


# Formulario para nueva contraseña
@app.route('/reset_password/<token>', methods=['GET'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except:
        flash('El enlace ha expirado o no es válido.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

# Guardar nueva contraseña
@app.route('/reset_password_submit/<token>', methods=['POST'])
def reset_password_submit(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except:
        flash('El enlace ha expirado o no es válido.', 'danger')
        return redirect(url_for('login'))
    
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not password or password != confirm_password:
        flash('Las contraseñas no coinciden o están vacías.', 'danger')
        return redirect(url_for('reset_password', token=token))
    
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        usuario.password = generate_password_hash(password)
        db.session.commit()
        flash('Contraseña actualizada correctamente.', 'success')
    else:
        flash('Usuario no encontrado.', 'danger')
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    
    app.run(debug=True, port=5500)
   
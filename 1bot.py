import json
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
from datetime import datetime

TOKEN = "8383696890:AAHBxVs9t0CqQ7R9pkve76CVvUT243kVYnU"
ADMIN_ID = 7957443258

USUARIOS_FILE = "usuarios.json"
INTENTOS_FILE = "intentos.json"
FUNCION17_FILE = "funcion17.json"
PEDIDOS_FILE = "pedidos.json"


# ------------------------
# JSON
# ------------------------

def cargar_json(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return default


def guardar_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)


usuarios = set(cargar_json(USUARIOS_FILE, []))
intentos = cargar_json(INTENTOS_FILE, {})
funcion17 = cargar_json(FUNCION17_FILE, {})
pedidos = cargar_json(PEDIDOS_FILE, [])


# ------------------------
# BASICO
# ------------------------

def es_admin(uid):
    return uid == ADMIN_ID


def esta_autorizado(uid):
    return str(uid) in usuarios or es_admin(uid)


def esta_bloqueado(uid):
    return intentos.get(str(uid), 0) >= 3


# ------------------------
# MENU
# ------------------------

menu_text = """âââââââââââââ
OPCIONES DISPONIBLESð®

1. Cromar calipers.
2. Cromar luces.
3. Ventanas GG.
4. Modificar 1 HP.
5. Cromar rines.
6. Cromar aleron.
7. Traspasar auto.
8. Modificar shiftime.
9. Quitar parachoques.
10. Auto 6 segundos.
11. Modificar ID.
12. 30k / 50M.
13. Comprar casas.
14. Cuenta full.
15. Auto Full GG.
16. FULL GG PREMIUM
17. Cuentas/DiseÃ±os.
18. ðComandos (ðAdmin.)
19. ðComandos (ðAdmin.)



âââââââââââââ"""
menu_admin = """âââââââââââââ
ð PANEL ADMIN

1. Cromar calipers
2. Cromar luces
3. Ventanas GG
4. Modificar 1 HP
5. Cromar rines
6. Cromar aleron
7. Traspasar auto
8. Modificar shiftime
9. Quitar parachoques
10. Auto 6 segundos
11. Modificar ID
12. 30k / 50M
13. Comprar casas
14. Cuenta full
15. Auto Full GG
16. FULL GG PREMIUM
17. Cuentas/DiseÃ±os

âââââââââââââ
â ADMIN

18. Panel Admin
19. Ver Pedidos
âââââââââââââ
"""
FORMULARIOS = {
"1":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta","ð Modelo del vehÃ­culo"],
"2":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta","ð Modelo del vehÃ­culo"],
"3":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta","ð Modelo del vehÃ­culo"],
"4":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"5":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta","ð Modelo del vehÃ­culo"],
"6":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta","ð Modelo del vehÃ­culo"],
"7":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"8":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"9":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"10":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"11":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta", "Nuevo ID:"],
"12":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"13":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"14":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta"],
"15":["ð§ Correo electrÃ³nico","ð ContraseÃ±a de la cuenta","ð ID DEL AUTO"],
"16":[
"ð§ Correo electrÃ³nico",
"ð ContraseÃ±a de la cuenta",
"ð Modelo del vehÃ­culo"
],
"17":[],
}

OPCIONES_CON_COLOR={"1","2","3","5","6","15"}
OPCION_FULL_GG = "16"

user_states={}


# ------------------------
# START
# ------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    uid = user.id
    uid_str = str(uid)

    if esta_bloqueado(uid):
        return

    # USUARIOS AUTORIZADOS
    if esta_autorizado(uid):

        if es_admin(uid):
            await update.message.reply_text(menu_admin)
        else:
            await update.message.reply_text(menu_text)

        await update.message.reply_text(
            "Elige una funciÃ³n respondiendo con el nÃºmero correspondiente:"
        )
        return

    # USUARIO NO AUTORIZADO
    intentos[uid_str] = intentos.get(uid_str, 0) + 1
    guardar_json(INTENTOS_FILE, intentos)

    if intentos[uid_str] >= 3:

        await update.message.reply_text(
            "ð« Has sido bloqueado permanentemente por intentar explotar el bot. Si crees que es un error, contacta al administrador."
        )

        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")

        texto = f"""ð«âââââââââââââââââð«
      ð«  USUARIO BLOQUEADO  ð«
ð«âââââââââââââââââð«

ð¤  NOMBRE
ââ¤ {user.first_name}

ð  USUARIO
ââ¤ @{user.username}

ð  ID DEL USUARIO
ââ¤ {user.id}

ð  FECHA
ââ¤ {fecha}

â°  HORA
ââ¤ {hora}

â ï¸ ACCESO DENEGADO
Este usuario se encuentra en la
lista de usuarios bloqueados.
"""

        fotos = await context.bot.get_user_profile_photos(uid)

        if fotos.total_count > 0:
            file = fotos.photos[0][-1].file_id
            await context.bot.send_photo(ADMIN_ID, file, caption=texto)
        else:
            await context.bot.send_message(ADMIN_ID, texto)

        return

    await update.message.reply_text(
        "ð« No tienes acceso a este bot. Contacta al administrador @drillscars para solicitar acceso."
    )
# ------------------------
# MANEJO FORMULARIOS
# ------------------------

async def manejar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.effective_user.id
    texto = update.message.text.strip()

    opciones_validas = list(FORMULARIOS.keys()) + ["17","18","19"]

    if texto not in opciones_validas and uid not in user_states:
        await update.message.reply_text("â Ese comando no existe")
        return


    # ð¹ OPCION 18
    if texto == "18":

        tiempo = funcion17.get(str(uid))

        if not tiempo or tiempo < time.time():
            await update.message.reply_text("â No tienes acceso a funciÃ³n 17")
            return

        await update.message.reply_text("ðÂ¡Bienvenido Admin!")

        botones = [[
            InlineKeyboardButton("ð¢ Canal", url="https://t.me/bot_multifunciones_cpm_drill_bot"),
            InlineKeyboardButton("ðÂ¡Comandos Admin!", callback_data="comando"),
            InlineKeyboardButton("respuestas", callback_data="respuestas")
        ]]

        teclado = InlineKeyboardMarkup(botones)

        await update.message.reply_text(
            "âï¸ Panel de la funciÃ³n 17",
            reply_markup=teclado
        )
        return


    # ð¹ OPCION 19
    if texto == "19":

        if not es_admin(uid):
            await update.message.reply_text("â Solo admin puede usar esto")
            return

        if not pedidos:
            await update.message.reply_text("ð¦ No hay pedidos pendientes")
            return

        for i, p in enumerate(pedidos):

            mensaje = f"""ð¦ PEDIDO #{i+1}

ð¤ Usuario: @{p['usuario']}
ð ID: {p['id']}

ð OpciÃ³n: {p['opcion']}
ð§ Correo: {p['correo']}
ð¨ Color: {p['color']}

ð {p['fecha']}  â° {p['hora']}

ââââââââââââââââââ
{p['datos']}
"""

            botones = [[
                InlineKeyboardButton("â Completar", callback_data=f"completar_{i}")
            ]]

            await update.message.reply_text(
                mensaje,
                reply_markup=InlineKeyboardMarkup(botones)
            )

        return


    # ð¹ OPCION 17
    if texto == "17":

        await update.message.reply_text("Â¡Selecciona Un Bot!")

        botones = [[
            InlineKeyboardButton("Bot Cuentas", url="https://t.me/bot_acuunts_drills_bot"),
            InlineKeyboardButton("Bot DiseÃ±os", url="https://t.me/personalizados_drills_bot")
        ]]

        teclado = InlineKeyboardMarkup(botones)

        await update.message.reply_text(
            "Bots Disponibles:",
            reply_markup=teclado
        )
        return


    # ð¹ FORMULARIOS
    if texto in FORMULARIOS:

        user_states[uid] = {
            "opcion": texto,
            "preguntas": FORMULARIOS[texto],
            "respuestas": [],
            "paso": 0
        }

        await update.message.reply_text(FORMULARIOS[texto][0] + ":")
        return


    
    # ð¹ PROCESO DE RESPUESTAS
    if uid in user_states:

        estado = user_states[uid]

    # VALIDAR CORREO
    if estado["paso"] == 0:
        if "@" not in texto or "." not in texto:
            await update.message.reply_text(
                "â Correo invÃ¡lido.\n\nDebe contener @ y .\nEjemplo: correo@gmail.com"
            )
            return

    # VALIDAR CONTRASEÃA
    if estado["paso"] == 1:
        if len(texto) < 6:
            await update.message.reply_text(
                "â ContraseÃ±a invÃ¡lida.\n\nDebe tener mÃ­nimo 6 caracteres."
            )
            return

    # VALIDAR MODELO DEL AUTO (SOLO NÃMEROS)
    if estado["paso"] == 2:
        if not texto.isdigit():
            await update.message.reply_text(
                "â Modelo invÃ¡lido.\n\nSolo se permiten nÃºmeros."
            )
            return

    estado["respuestas"].append(texto)
    estado["paso"] += 1

    if estado["paso"] < len(estado["preguntas"]):
        await update.message.reply_text(
            estado["preguntas"][estado["paso"]] + ":"
        )
        return

    opcion = estado["opcion"]


        # â­ OPCION 16 FULL GG PREMIUM
    if opcion == "16":

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ð´ Rojo",callback_data="aleron_rojo"),
                    InlineKeyboardButton("ðµ Azul",callback_data="aleron_azul")
                ],
                [
                    InlineKeyboardButton("ð¢ Verde",callback_data="aleron_verde"),
                    InlineKeyboardButton("âª Blanco",callback_data="aleron_blanco")
                ]
            ])

            estado["paso_color"] = "aleron"

            await update.message.reply_text(
                "ð¨ Selecciona color del alerÃ³n",
                reply_markup=keyboard
            )
            return

        # ð¹ OPCIONES NORMALES CON COLOR
    if opcion in OPCIONES_CON_COLOR:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("ð´ Rojo",callback_data="color_rojo"),
                    InlineKeyboardButton("ðµ Azul",callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("ð¢ Verde",callback_data="color_verde"),
                    InlineKeyboardButton("ðµAzul Claro",callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("ð Naranja",callback_data="color_naranja"),
                    InlineKeyboardButton("ð©·rosa",callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("ð£Purpura",callback_data="color_purpura"),
                    InlineKeyboardButton("âªBlanco",callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("ð¡Amarillo",callback_data="color_amarillo"),
                    InlineKeyboardButton("ð£Violeta Obscuro",callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("ðµTurqueza",callback_data="color_turqueza"),
                    InlineKeyboardButton("ð¦Azul Marino",callback_data="color_azul-marino")
                ]
            ])

            estado["esperando_color"] = True

            await update.message.reply_text(
                "ð¨ Selecciona color",
                reply_markup=keyboard
            )
            return

    await enviar_admin(update, context, estado, "N/A")

    del user_states[uid]
# ------------------------
# COLOR
# ------------------------

async def color(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    uid = query.from_user.id
    data = query.data

    # Siempre responder al callback
    await query.answer()

    if uid not in user_states:
        await query.answer("â ï¸ La sesiÃ³n expirÃ³. Usa el menÃº otra vez.", show_alert=True)
        return

    estado = user_states[uid]

    # -------------------------
    # ALERON
    # -------------------------
    if data.startswith("aleron_"):

        color = data.replace("aleron_", "")
        estado["color_aleron"] = color

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ð´ Rojo", callback_data="luces_rojo"),
                InlineKeyboardButton("ðµ Azul", callback_data="luces_azul")
            ],
            [
                InlineKeyboardButton("ð¢ Verde", callback_data="luces_verde"),
                InlineKeyboardButton("âª Blanco", callback_data="luces_blanco")
            ]
        ])

        await query.edit_message_text(f"AlerÃ³n seleccionado: {color}")

        await context.bot.send_message(
            chat_id=uid,
            text="ð¡ Selecciona color de luces",
            reply_markup=keyboard
        )
        return

    # -------------------------
    # LUCES
    # -------------------------
    if data.startswith("luces_"):

        color = data.replace("luces_", "")
        estado["color_luces"] = color

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ð´ Rojo", callback_data="calipers_rojo"),
                InlineKeyboardButton("ðµ Azul", callback_data="calipers_azul")
            ],
            [
                InlineKeyboardButton("ð¢ Verde", callback_data="calipers_verde"),
                InlineKeyboardButton("âª Blanco", callback_data="calipers_blanco")
            ]
        ])

        await query.edit_message_text(f"Luces seleccionadas: {color}")

        await context.bot.send_message(
            chat_id=uid,
            text="ð Selecciona color de calipers",
            reply_markup=keyboard
        )
        return

    # -------------------------
    # CALIPERS
    # -------------------------
    if data.startswith("calipers_"):

        color = data.replace("calipers_", "")
        estado["color_calipers"] = color

        await query.edit_message_text(f"Calipers seleccionados: {color}")

        colores = f"""
AlerÃ³n: {estado['color_aleron']}
Luces: {estado['color_luces']}
Calipers: {estado['color_calipers']}
"""

        await enviar_admin(query, context, estado, colores)

        del user_states[uid]
        return

    # -------------------------
    # OPCIONES NORMALES color_
    # -------------------------
    if data.startswith("color_"):

        color = data.replace("color_", "")

        await query.edit_message_text(f"Color seleccionado: {color}")

        await enviar_admin(query, context, estado, color)

        del user_states[uid]
        return
# ------------------------
# ENVIAR ADMIN
# ------------------------

async def enviar_admin(update_or_query, context, estado, color):

    if hasattr(update_or_query, "effective_user"):
        user = update_or_query.effective_user
    else:
        user = update_or_query.from_user

    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")

    datos = ""

    for p, r in zip(estado["preguntas"], estado["respuestas"]):
        datos += f"{p}: {r}\n"

    pedido = {
        "usuario": user.username,
        "id": user.id,
        "opcion": estado["opcion"],
        "correo": estado["respuestas"][0] if estado["respuestas"] else "N/A",
        "color": color,
        "fecha": fecha,
        "hora": hora,
        "datos": datos
    }

    pedidos.append(pedido)
    guardar_json(PEDIDOS_FILE, pedidos)

    await context.bot.send_message(
        ADMIN_ID,
        f"""ð¦ ââââã NUEVO PEDIDO ãââââ ð¦

ð¤ Usuario: @{user.username}
ð ID: {user.id}

ð OpciÃ³n: {estado['opcion']}
ð¨ Color: {color}

ð Fecha: {fecha}
â° Hora: {hora}

ââââââââââââââââââ
{datos}
"""
    )

    await context.bot.send_message(user.id,"â Pedido enviado")
    await context.bot.send_message(user.id,menu_text)
    await update_or_query.message.reply_text(
"Elige una funciÃ³n respondiendo con el nÃºmero correspondiente:"
)
# ------------------------
# PUBLICACIONES
# ------------------------

async def publicar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("â Responde al mensaje que quieres publicar")
        return

    try:
        with open("usuarios.json","r") as f:
            usuarios = json.load(f)
    except:
        await update.message.reply_text("â No hay usuarios guardados")
        return

    enviados = 0
    mensaje = update.message.reply_to_message

    for uid in usuarios:
        try:
            await context.bot.copy_message(
                chat_id=uid,
                from_chat_id=update.message.chat_id,
                message_id=mensaje.message_id
            )
            enviados += 1
        except:
            pass

    await update.message.reply_text(f"â Publicado a {enviados} usuarios")



#COMPLETAR#

# ------------------------
# FUNCION 17
# ------------------------
async def completar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    i = int(query.data.split("_")[1])

    if i >= len(pedidos):
        await query.edit_message_text("â Pedido no encontrado")
        return

    pedido = pedidos[i]

    # mensaje al usuario
    await context.bot.send_message(
        pedido["id"],
        f"""â TU PEDIDO HA SIDO COMPLETADO

ð FunciÃ³n: {pedido['opcion']}
ð§ Correo: {pedido['correo']}

Gracias por usar el bot."""
    )

    pedidos.pop(i)
    guardar_json(PEDIDOS_FILE, pedidos)

    await query.edit_message_text("â Pedido completado y eliminado")

async def opcion_comando_17(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    uid=context.args[0]

    keyboard=InlineKeyboardMarkup([
[InlineKeyboardButton("5 min",callback_data=f"f17_{uid}_300")],
[InlineKeyboardButton("10 min",callback_data=f"f17_{uid}_600")],
[InlineKeyboardButton("1 dÃ­a",callback_data=f"f17_{uid}_86400")],
[InlineKeyboardButton("1 semana",callback_data=f"f17_{uid}_604800")],
[InlineKeyboardButton("1 mes",callback_data=f"f17_{uid}_2592000")],
[InlineKeyboardButton("1 aÃ±o",callback_data=f"f17_{uid}_31536000")]
])

    await update.message.reply_text(
        "Selecciona tiempo",
        reply_markup=keyboard
    )




async def activar17(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    _,uid,seg=query.data.split("_")

    funcion17[uid]=time.time()+int(seg)

    guardar_json(FUNCION17_FILE,funcion17)

    await query.edit_message_text("FunciÃ³n 17 activada")


async def quitar_funcion17(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    uid=context.args[0]

    if uid in funcion17:
        del funcion17[uid]

    guardar_json(FUNCION17_FILE,funcion17)

    await update.message.reply_text("FunciÃ³n 17 eliminada")


# ------------------------
# ADMIN USUARIOS
# ------------------------

async def agregar(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("â  Usa: /agregar ID")
        return

    uid=context.args[0]

    usuarios.add(str(uid))
    guardar_json(USUARIOS_FILE,list(usuarios))

    await update.message.reply_text("â Usuario agregado")

    # MENSAJE AL USUARIO
    try:
        await context.bot.send_message(
            chat_id=int(uid),
            text="ð Has sido agregado al bot.\n\nUsa /start para comenzar."
        )
    except:
        await update.message.reply_text(
            "â  No se pudo enviar mensaje al usuario.\nEl usuario debe iniciar el bot con /start primero."
        )


async def eliminar(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    uid=context.args[0]

    if str(uid) in usuarios:
        usuarios.remove(str(uid))

    guardar_json(USUARIOS_FILE,list(usuarios))

    await update.message.reply_text("Usuario eliminado")


async def ver_usuarios(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    lista="\n".join(usuarios)

    await update.message.reply_text(f"Usuarios:\n{lista}")


async def ver_bloqueados(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    bloqueados=[u for u,n in intentos.items() if n>=3]

    await update.message.reply_text("\n".join(bloqueados))


async def desbloquear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("â ï¸ Usa el comando asÃ­:\n/desbloquear ID")
        return

    uid = context.args[0]

    intentos[uid] = 0

    guardar_json(INTENTOS_FILE, intentos)

    await update.message.reply_text("â Usuario desbloqueado")

async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.effective_user.id == ADMIN_ID:
        return

    await update.message.reply_text("â Ese comando no existe")
##########RARO#########
async def raro(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.effective_user
    msg=update.message

    tipo="archivo"

    if msg.sticker:
        tipo="sticker"
    elif msg.voice:
        tipo="audio de voz"
    elif msg.video:
        tipo="video"
    elif msg.audio:
        tipo="audio"
    elif msg.document:
        tipo="documento"

    fecha=datetime.now().strftime("%d/%m/%Y")
    hora=datetime.now().strftime("%H:%M:%S")
    
    texto = f"""
ð¨ ðððð¥ð§ð ðð ð ð¢ð©ðð ððð¡ð§ð¢ ð¦ð¢ð¦ð£ðððð¢ð¦ð¢

ð¤ ð¨ððð®ð¿ð¶ð¼: {user.first_name}
ð ð¨ðð²ð¿ð»ð®ðºð²: @{user.username}
ð ðð: {user.id}

ð¦ Tipo: {tipo}

ð ðð²ð°ðµð®: {fecha}
â° ðð¼ð¿ð®: {hora}

â ï¸ Verifica esta actividad inmediatamente.
"""

    # STICKER
    if update.message.sticker:
        file = update.message.sticker.file_id
        await context.bot.send_sticker(ADMIN_ID, file)
        await context.bot.send_message(ADMIN_ID, texto)

    # FOTO
    elif update.message.photo:
        file = update.message.photo[-1].file_id
        await context.bot.send_photo(ADMIN_ID, file, caption=texto)

    # VOZ
    elif update.message.voice:
        file = update.message.voice.file_id
        await context.bot.send_voice(ADMIN_ID, file, caption=texto)

    # AUDIO
    elif update.message.audio:
        file = update.message.audio.file_id
        await context.bot.send_audio(ADMIN_ID, file, caption=texto)

    # VIDEO
    elif update.message.video:
        file = update.message.video.file_id
        await context.bot.send_video(ADMIN_ID, file, caption=texto)

    # DOCUMENTO
    elif update.message.document:
        file = update.message.document.file_id
        await context.bot.send_document(ADMIN_ID, file, caption=texto)

    # Aviso al usuario
    await update.message.reply_text(
        "â  Accion identificada como extraÃ±a (Notificada al administrador @drillscars), por favor utiliza el bot correctamente."
    )
# ------------------------
# BOTON MANTENIMIENTO
# ------------------------

async def boton_comandos_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "comando":
        await query.message.reply_text("ââââââââââââââââââââââââââââââââ\n"
"        ð PANEL DE ADMIN ð\n"
"ââââââââââââââââââââââââââââââââ\n\n"

"âï¸ CONTROL DEL BOT\n"
"ââââââââââââââââââââ\n\n"

"ð COMANDOS PRINCIPALES\n\n"

"â¶ï¸ /start\n"
"Iniciar el bot\n\n"

"ð¤ /agregar\n"
"Agregar usuario autorizado\n\n"

"â /eliminar\n"
"Eliminar usuario del sistema\n\n"

"ð /ver_usuarios\n"
"Ver usuarios registrados\n\n"

"ð /desbloquear\n"
"Desbloquear usuario bloqueado\n\n"

"ð /ver_bloqueados\n"
"Ver usuarios bloqueados\n\n"

"ââââââââââââââââââââ\n\n"

"ð¢ PUBLICACIONES\n\n"

"ð¡ /publicar\n"
"Enviar mensaje a todos los usuarios\n\n"

"ââââââââââââââââââââ\n\n"

"ð§© FUNCIÃN 17\n\n"

"ð¢ /opcion_comando_17\n"
"Dar acceso a funciÃ³n 17\n\n"

"ð´ /quitar_funcion17\n"
"Quitar acceso a funciÃ³n 17\n\n"

"ââââââââââââââââââââ\n"
"ð¡ Solo para administrador")
        
async def boton_respuestas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "respuestas":
        await query.message.reply_text("ââââââââââââââââââââââââââââââââ\n"
"ð Respuestas\n"
"âââââââââââââââââââ\n"
"â Proceso Finalizado\n"
"ð§ð ð½ð¿ð¼ð°ð²ðð¼ ð±ð² ð¹ð® ð°ðð²ð»ðð® () ðµð® ðð¶ð±ð¼ ð°ð¼ðºð½ð¹ð²ðð®ð±ð¼.\n"
"ââââââââââââââââââââ\n"
"â Agregar usuario\n"
"ð§ð ð°ðð²ð»ðð® ðµð® ðð¶ð±ð¼ ð°ð¿ð²ð®ð±ð® ðð! ð£ðð²ð±ð²ð ððð®ð¿ ð¹ð®ð ð³ðð»ð°ð¶ð¼ð»ð²ð ð°ð¼ð» ð²ð¹ ð°ð¼ðºð®ð»ð±ð¼ /start.\n"
"ââââââââââââââââââââ\n"
"ð Desbloquear usuario\n"
"ðð®ð ðð¶ð±ð¼ ð±ð²ðð¯ð¹ð¼ð¾ðð²ð®ð±ð¼! ðð®ð¯ð¹ð® ð°ð¼ð» ð²ð¹ ð®ð±ðºð¶ð»ð¶ððð¿ð®ð±ð¼ð¿ @drillscars ð½ð®ð¿ð® ð¾ðð² ðð² ð®ð´ð¿ð²ð´ðð².\n"
"ââââââââââââââââââââ\n"
)


        

# ------------------------
# MAIN
# ------------------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("agregar", agregar))
app.add_handler(CommandHandler("eliminar", eliminar))
app.add_handler(CommandHandler("ver_usuarios", ver_usuarios))
app.add_handler(CommandHandler("ver_bloqueados", ver_bloqueados))
app.add_handler(CommandHandler("desbloquear", desbloquear))

app.add_handler(CommandHandler("publicar", publicar))

app.add_handler(CommandHandler("opcion_comando_17", opcion_comando_17))
app.add_handler(CommandHandler("quitar_funcion17", quitar_funcion17))

# DETECTAR COSAS RARAS
app.add_handler(
    MessageHandler(
        filters.Sticker.ALL | filters.VOICE | filters.AUDIO | filters.VIDEO | filters.Document.ALL,
        raro
    )
)


# TEXTO NORMAL
app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar))


print("BOT DE DRILLS ACTIVO ")
















print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")





























print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78sijwhegfvbhnjdkijufhyueiw8734t5yhjkoe9i8ury75ghrjki398ut4yghfnjmshdgfbnmlpÃ±aos09i8duy7ctgfbnjko987ey6rtfgbhnjksoiu8y7dtcgbhndksi83u76t45fgchbnjxkoi9283u74y6tycghxnjki8736t4ghnjki873y6g")



























































print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")

print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")

print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")

print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")

print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")

print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")
print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")

print("juhr3koiudyhh9764yiwwuhygdbhsju87364ty83746fdhjuidfhgbi3u7ygfhkmdjnhfbdjskisjdcfhydusiosi9d8u7y6d3890swidchuygt6y7w8uiaeshdy6e78si")




































print("BOT ACTIVOOO DE DRILLS")
app.add_handler(CallbackQueryHandler(color, pattern="^(color_|aleron_|luces_|calipers_)"))
app.add_handler(CallbackQueryHandler(activar17, pattern="^f17_"))
app.add_handler(CallbackQueryHandler(completar_pedido, pattern="^completar_"))
app.add_handler(CallbackQueryHandler(boton_comandos_admin, pattern="comando"))
app.add_handler(CallbackQueryHandler(boton_respuestas, pattern="respuestas"))

app.run_polling()

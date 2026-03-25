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

TOKEN = "8527070285:AAGsLZy6Gff0IYbXLLpvAFM-6P-S0Jki_nc"
ADMIN_ID = 7957443258

USUARIOS_FILE = "usuarios.json"
INTENTOS_FILE = "intentos.json"
FUNCION17_FILE = "funcion17.json"
PEDIDOS_FILE = "pedidos.json"

MANTENIMIENTO = False
estado_admin = {}
estado_admin = {}
usuarios = set()
bloqueados = set()
opcion17 = set()

stats = {
    "bloqueados": [],
    "desbloqueados": [],
    "agregados": [],
    "eliminados": [],
    "mantenimiento": 0,
    "publicaciones": 0
}
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

menu_text = """━━━━━━━━━━━━━
OPCIONES DISPONIBLES🎮

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
17. Cuentas/Diseños.
18. 🔒Comandos (👑Admin.)
19. 🔒Comandos (👑Admin.)
20. 🔒Comandos (👑Admin.)
━━━━━━━━━━━━━"""
menu_admin = """━━━━━━━━━━━━━
👑 PANEL ADMIN

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
17. Cuentas/Diseños

━━━━━━━━━━━━━
⚙ ADMIN

18. Panel Admin
19. Ver Pedidos
20. Mantenimiento of on 
━━━━━━━━━━━━━
"""

NOMBRES_OPCIONES = {
    "1": "Cromar calipers",
    "2": "Cromar luces",
    "3": "Ventanas GG",
    "4": "Modificar 1 HP",
    "5": "Cromar rines",
    "6": "Cromar aleron",
    "7": "Traspasar auto",
    "8": "Modificar shiftime",
    "9": "Quitar parachoques",
    "10": "Auto 6 segundos",
    "11": "Modificar ID",
    "12": "30k / 50M",
    "13": "Comprar casas",
    "14": "Cuenta full",
    "15": "Auto Full GG",
    "16": "FULL GG PREMIUM",
    "17": "Cuentas/Diseños",
    "18": "🔒Comandos (👑Admin.)",
    "19": "🔒Comandos (👑Admin.)",
    "20": "🔒Comandos (👑Admin.)"
}

FORMULARIOS = {
"1":["📧 Correo electrónico","🔐 Contraseña de la cuenta","🚗 Modelo del vehículo"],
"2":["📧 Correo electrónico","🔐 Contraseña de la cuenta","🚗 Modelo del vehículo"],
"3":["📧 Correo electrónico","🔐 Contraseña de la cuenta","🚗 Modelo del vehículo"],
"4":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"5":["📧 Correo electrónico","🔐 Contraseña de la cuenta","🚗 Modelo del vehículo"],
"6":["📧 Correo electrónico","🔐 Contraseña de la cuenta","🚗 Modelo del vehículo"],
"7":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"8":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"9":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"10":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"11":["📧 Correo electrónico","🔐 Contraseña de la cuenta", "Nuevo ID:"],
"12":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"13":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"14":["📧 Correo electrónico","🔐 Contraseña de la cuenta"],
"15":["📧 Correo electrónico","🔐 Contraseña de la cuenta","🚗 ID DEL AUTO"],
"16":[
"📧 Correo electrónico",
"🔐 Contraseña de la cuenta",
"🚗 Modelo del vehículo"
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

    uid = update.effective_user.id

    if MANTENIMIENTO and not es_admin(uid):
        await update.message.reply_text("🛠 Bot en mantenimiento, intenta más tarde")
        return

    user = update.effective_user
    uid = user.id
    uid_str = str(uid)

    if esta_bloqueado(uid):
        return
    # 🔥 CANCELAR FORMULARIO SI EXISTE
    if uid in user_states:
        del user_states[uid]
    # 🔹 BOTÓN
    botones = [
        [InlineKeyboardButton("👥 Grupo oficial", url="https://t.me/+RrL593ltDKgwMDJh")]
    ]
    teclado = InlineKeyboardMarkup(botones)

    # 🔥 USUARIOS AUTORIZADOS
    if esta_autorizado(uid):

        # 1️⃣ MENÚ + BOTÓN
        if es_admin(uid):
            await update.message.reply_text(menu_admin, reply_markup=teclado)
        else:
            await update.message.reply_text(menu_text, reply_markup=teclado)

        # 2️⃣ MENSAJE FINAL (YA BIEN COLOCADO)
        await update.message.reply_text(
            "Elige una función respondiendo con el número correspondiente:"
        )

        return

    # ❌ USUARIO NO AUTORIZADO
    intentos[uid_str] = intentos.get(uid_str, 0) + 1
    guardar_json(INTENTOS_FILE, intentos)

    if intentos[uid_str] >= 3:

        await update.message.reply_text(
            "🚫 Has sido bloqueado permanentemente por intentar explotar el bot."
        )

        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")

        texto = f"""🚫══════════════════🚫
🚫  USUARIO BLOQUEADO  🚫
🚫══════════════════🚫

👤 {user.first_name}
🔗 @{user.username}
🆔 {user.id}

📅 {fecha}
⏰ {hora}
"""

        fotos = await context.bot.get_user_profile_photos(uid)

        if fotos.total_count > 0:
            file = fotos.photos[0][-1].file_id
            await context.bot.send_photo(ADMIN_ID, file, caption=texto)
        else:
            await context.bot.send_message(ADMIN_ID, texto)

        return

    await update.message.reply_text(
        "🚫 No tienes acceso. Contacta al admin.",
       
    )
    
# ------------------------
# MANEJO FORMULARIOS
# ------------------------

async def manejar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    uid = update.effective_user.id
    texto = update.message.text.strip()

    # 🔥 RESPUESTAS DEL ADMIN (PRIORIDAD)
    if uid in estado_admin:

        accion = estado_admin[uid]

        # 🔥 CASO ESPECIAL: UPDATE GLOBAL
        if accion == "esperando_update":

            detalles = texto

            mensaje = f"""🟢 BOT FUNCIONANDO DE NUEVO

✨ ACTUALIZACIÓN:

{detalles}

🚀 Gracias por tu paciencia.
"""

            for u in usuarios:
                try:
                    await context.bot.send_message(int(u), mensaje)
                except:
                    pass

            del estado_admin[uid]
            await update.message.reply_text("✅ Actualización enviada")
            return

        # 🔥 VALIDAR ID
        if not texto.isdigit():
            await update.message.reply_text("❌ ID inválido")
            return

        target = int(texto)

        if accion == "agregar":
            usuarios.add(target)
            stats["agregados"].append(target)
            await update.message.reply_text("✅ Usuario agregado")

        elif accion == "eliminar":
            usuarios.discard(target)
            stats["eliminados"].append(target)
            await update.message.reply_text("❌ Usuario eliminado")

        elif accion == "bloquear":
            bloqueados.add(target)
            stats["bloqueados"].append(target)
            await update.message.reply_text("🚫 Usuario bloqueado")

        elif accion == "desbloquear":
            bloqueados.discard(target)
            stats["desbloqueados"].append(target)
            await update.message.reply_text("✅ Usuario desbloqueado")

        elif accion == "add17":
            opcion17.add(target)
            await update.message.reply_text("⭐ Opción 17 agregada")

        elif accion == "remove17":
            opcion17.discard(target)
            await update.message.reply_text("❌ Opción 17 quitada")

        del estado_admin[uid]
        return

    # 🔥 MANTENIMIENTO
    if MANTENIMIENTO and not es_admin(uid):
        await update.message.reply_text("🛠 Bot en mantenimiento, intenta más tarde")
        return

    # 🔥 FORMULARIOS (PRIORIDAD ALTA)
    if uid in user_states:

        estado = user_states[uid]

        # VALIDACIONES
        if estado["paso"] == 0:
            if "@" not in texto or "." not in texto:
                await update.message.reply_text("❌ Correo inválido")
                return

        elif estado["paso"] == 1:
            if len(texto) < 6:
                await update.message.reply_text("❌ Contraseña muy corta")
                return

        elif estado["paso"] == 2:
            if not texto.isdigit():
                await update.message.reply_text("❌ Solo números en modelo")
                return

        estado["respuestas"].append(texto)
        estado["paso"] += 1

        # SIGUIENTE PREGUNTA
        if estado["paso"] < len(estado["preguntas"]):
            await update.message.reply_text(
                estado["preguntas"][estado["paso"]] + ":"
            )
            return

        opcion = estado["opcion"]

        # ⭐ OPCIÓN 16
        if opcion == "16":

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔴 Rojo", callback_data="aleron_rojo"),
                    InlineKeyboardButton("🔵 Azul", callback_data="aleron_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde", callback_data="aleron_verde"),
                    InlineKeyboardButton("⚪ Blanco", callback_data="aleron_blanco")
                ]
            ])

            await update.message.reply_text(
                "🎨 Selecciona color del alerón",
                reply_markup=keyboard
            )
            return

        # 🔹 OPCIONES CON COLOR
        if opcion in OPCIONES_CON_COLOR:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔴 Rojo", callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul", callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde", callback_data="color_verde"),
                    InlineKeyboardButton("⚪ Blanco", callback_data="color_blanco")
                ]
            ])

            await update.message.reply_text(
                "🎨 Selecciona color",
                reply_markup=keyboard
            )
            return

        # 🔹 SIN COLOR
        await enviar_admin(update, context, estado, "N/A")
        del user_states[uid]
        return

    # ---------------------------
    # 🔽 AQUÍ YA VAN LOS COMANDOS
    # ---------------------------


    opciones_validas = list(FORMULARIOS.keys()) + ["17", "18", "19", "20", "21"]

    # ❌ comando inválido
    if texto not in opciones_validas and uid not in user_states:
            await update.message.reply_text("❌ Ese comando no existe")
            return
    
    # 🔹 OPCION 20 (MANTENIMIENTO)
    # 🔹 OPCION 20 (MANTENIMIENTO)
    if texto == "21":

        if not es_admin(uid):
            await update.message.reply_text("❌ Solo admin")
            return

        botones = [
        [InlineKeyboardButton("➕ Agregar", callback_data="admin_agregar"),
         InlineKeyboardButton("➖ Eliminar", callback_data="admin_eliminar")],

        [InlineKeyboardButton("🚫 Bloquear", callback_data="admin_bloquear"),
         InlineKeyboardButton("✅ Desbloquear", callback_data="admin_desbloquear")],

        [InlineKeyboardButton("⭐ Dar opción 17", callback_data="admin_add17"),
         InlineKeyboardButton("❌ Quitar opción 17", callback_data="admin_remove17")],

        [InlineKeyboardButton("👥 Ver usuarios", callback_data="admin_ver")],
        [InlineKeyboardButton("📊 Estadísticas", callback_data="admin_stats")]
    ]

        await update.message.reply_text(
        "⚙️ Panel Admin",
        reply_markup=InlineKeyboardMarkup(botones)
    )
        return
    # 🔹 OPCION 18
    if texto == "18":

        tiempo = funcion17.get(str(uid))

        if not tiempo or tiempo < time.time():
            await update.message.reply_text("❌ No tienes acceso a función 17")
            return

        botones = [[
            InlineKeyboardButton("📢 Canal", url="https://t.me/bot_multifunciones_cpm_drill_bot"),
            InlineKeyboardButton("👑 Comandos Admin", callback_data="comando"),
            InlineKeyboardButton("Respuestas", callback_data="respuestas")
        ]]

        await update.message.reply_text(
            "⚙️ Panel de la función 17",
            reply_markup=InlineKeyboardMarkup(botones)
        )
        return

    # 🔹 OPCION 19
    if texto == "19":

        if not es_admin(uid):
            await update.message.reply_text("❌ Solo admin puede usar esto")
            return

        if not pedidos:
            await update.message.reply_text("📦 No hay pedidos pendientes")
            return

    # 🔹 MOSTRAR PEDIDOS
        for i, p in enumerate(pedidos):
            mensaje = f"""📦 PEDIDO #{i+1}

👤 Usuario: @{p['usuario']}
🆔 ID: {p['id']}

📌 Opción: {p['opcion']}
📧 Correo: {p['correo']}
🎨 Color: {p['color']}

📅 {p['fecha']} ⏰ {p['hora']}

━━━━━━━━━━━━━━━━━━
{p['datos']}
"""

            botones = [[
                InlineKeyboardButton("✅ Completar", callback_data=f"completar_{i}")
        ]]

            await update.message.reply_text(
                mensaje,
                reply_markup=InlineKeyboardMarkup(botones)
        )

        # 🔥 ESTADÍSTICAS
        total = len(pedidos)

        # 📊 Función más usada
        conteo_opciones = {}
        for p in pedidos:
            op = p["opcion"]
            conteo_opciones[op] = conteo_opciones.get(op, 0) + 1

        if conteo_opciones:
            mas_usada = max(conteo_opciones, key=conteo_opciones.get)
            nombre_funcion = NOMBRES_OPCIONES.get(mas_usada, f"Opción {mas_usada}")
            veces_opcion = conteo_opciones[mas_usada]
        else:
            mas_usada = "N/A"
            veces_opcion = 0

    # 👤 Usuario más activo
        conteo_usuarios = {}
        for p in pedidos:
            user = p["usuario"] or "Sin username"
            conteo_usuarios[user] = conteo_usuarios.get(user, 0) + 1

        if conteo_usuarios:
            top_user = max(conteo_usuarios, key=conteo_usuarios.get)
            veces_user = conteo_usuarios[top_user]
        else:
            top_user = "N/A"
            veces_user = 0

    # 🧾 MENSAJE FINAL
        mensaje_stats = f"""📊 ESTADÍSTICAS

📦 Total pedidos: {total}
🔥 Función más usada: {nombre_funcion} ({veces_opcion} veces)

👑 Usuario más activo: @{top_user}
📨 Pedidos realizados: {veces_user}
"""

        await update.message.reply_text(mensaje_stats)

    # 🔥 BOTÓN BORRAR TODOS
        keyboard = [[
            InlineKeyboardButton("🗑 Borrar TODOS los pedidos", callback_data="borrar_todos")
    ]]

        await update.message.reply_text(
            "⚠️ Acción peligrosa",
            reply_markup=InlineKeyboardMarkup(keyboard)
    )

        return
    # 🔹 OPCION 19
    if texto == "19":

        if not es_admin(uid):
            await update.message.reply_text("❌ Solo admin puede usar esto")
            return

        if not pedidos:
            await update.message.reply_text("📦 No hay pedidos pendientes")
            return

    # 🔹 MOSTRAR PEDIDOS
        for i, p in enumerate(pedidos):
            mensaje = f"""📦 PEDIDO #{i+1}

👤 Usuario: @{p['usuario']}
🆔 ID: {p['id']}

📌 Opción: {p['opcion']}
📧 Correo: {p['correo']}
🎨 Color: {p['color']}

📅 {p['fecha']} ⏰ {p['hora']}

━━━━━━━━━━━━━━━━━━
{p['datos']}
"""

            botones = [[
                InlineKeyboardButton("✅ Completar", callback_data=f"completar_{i}")
        ]]

            await update.message.reply_text(
                mensaje,
                reply_markup=InlineKeyboardMarkup(botones)
        )

        # 🔥 ESTADÍSTICAS
        total = len(pedidos)

        # 📊 Función más usada
        conteo_opciones = {}
        for p in pedidos:
            op = p["opcion"]
            conteo_opciones[op] = conteo_opciones.get(op, 0) + 1

        if conteo_opciones:
            mas_usada = max(conteo_opciones, key=conteo_opciones.get)
            nombre_funcion = NOMBRES_OPCIONES.get(mas_usada, f"Opción {mas_usada}")
            veces_opcion = conteo_opciones[mas_usada]
        else:
            mas_usada = "N/A"
            veces_opcion = 0

    # 👤 Usuario más activo
        conteo_usuarios = {}
        for p in pedidos:
            user = p["usuario"] or "Sin username"
            conteo_usuarios[user] = conteo_usuarios.get(user, 0) + 1

        if conteo_usuarios:
            top_user = max(conteo_usuarios, key=conteo_usuarios.get)
            veces_user = conteo_usuarios[top_user]
        else:
            top_user = "N/A"
            veces_user = 0

    # 🧾 MENSAJE FINAL
        mensaje_stats = f"""📊 ESTADÍSTICAS

📦 Total pedidos: {total}
🔥 Función más usada: {nombre_funcion} ({veces_opcion} veces)

👑 Usuario más activo: @{top_user}
📨 Pedidos realizados: {veces_user}
"""

        await update.message.reply_text(mensaje_stats)

    # 🔥 BOTÓN BORRAR TODOS
        keyboard = [[
            InlineKeyboardButton("🗑 Borrar TODOS los pedidos", callback_data="borrar_todos")
    ]]

        await update.message.reply_text(
            "⚠️ Acción peligrosa",
            reply_markup=InlineKeyboardMarkup(keyboard)
    )

        return

    # 🔹 OPCION 17
    if texto == "17":

        botones = [[
            InlineKeyboardButton("Bot Cuentas", url="https://t.me/bot_acuunts_drills_bot"),
            InlineKeyboardButton("Bot Diseños", url="https://t.me/personalizados_drills_bot")
        ]]

        await update.message.reply_text(
            "Bots disponibles:",
            reply_markup=InlineKeyboardMarkup(botones)
        )
        return

    # 🔹 FORMULARIOS
    if texto in FORMULARIOS:

        user_states[uid] = {
            "opcion": texto,
            "preguntas": FORMULARIOS[texto],
            "respuestas": [],
            "paso": 0
        }

        if FORMULARIOS[texto]:
            await update.message.reply_text(FORMULARIOS[texto][0] + ":")
        return

    # 🔹 RESPUESTAS
    if uid in user_states:

        estado = user_states[uid]

        # VALIDACIONES
        if estado["paso"] == 0:
            if "@" not in texto or "." not in texto:
                await update.message.reply_text("❌ Correo inválido")
                return

        if estado["paso"] == 1:
            if len(texto) < 6:
                await update.message.reply_text("❌ Contraseña muy corta")
                return

        if estado["paso"] == 2:
            if not texto.isdigit():
                await update.message.reply_text("❌ Solo números en modelo")
                return

        estado["respuestas"].append(texto)
        estado["paso"] += 1

        # siguiente pregunta
        if estado["paso"] < len(estado["preguntas"]):
            await update.message.reply_text(
                estado["preguntas"][estado["paso"]] + ":"
            )
            return

        opcion = estado["opcion"]

        # ⭐ OPCION 16 FULL GG PREMIUM
        if opcion == "16":

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔴 Rojo", callback_data="aleron_rojo"),
                    InlineKeyboardButton("🔵 Azul", callback_data="aleron_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde", callback_data="aleron_verde"),
                    InlineKeyboardButton("⚪ Blanco", callback_data="aleron_blanco")
                ]
            ])

            await update.message.reply_text(
                "🎨 Selecciona color del alerón",
                reply_markup=keyboard
            )
            return

        # 🔹 OPCIONES CON COLOR
        if opcion in OPCIONES_CON_COLOR:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔴 Rojo", callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul", callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde", callback_data="color_verde"),
                    InlineKeyboardButton("⚪ Blanco", callback_data="color_blanco")
                ]
            ])

            await update.message.reply_text(
                "🎨 Selecciona color",
                reply_markup=keyboard
            )
            return

        # 🔹 SIN COLOR
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

    # 🔹 detectar usuario correctamente
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

    # 🔥 MENSAJE AL ADMIN (ARREGLADO SIN BUG DE CARACTERES)
    mensaje_admin = f"""📦 ━━━━【 NUEVO PEDIDO 】━━━━ 📦

👤 Usuario: @{user.username}
🆔 ID: {user.id}

📌 Opción: {estado['opcion']}
🎨 Color: {color}

📅 Fecha: {fecha}
⏰ Hora: {hora}

━━━━━━━━━━━━━━━━━━
{datos}
"""

    await context.bot.send_message(ADMIN_ID, mensaje_admin)

    # 🔥 CONFIRMACIÓN AL USUARIO
    await context.bot.send_message(user.id, "✅ Pedido enviado")

    # 🔥 MENÚ CORRECTO SEGÚN USUARIO
    if es_admin(user.id):
        await context.bot.send_message(user.id, menu_admin)
    else:
        await context.bot.send_message(user.id, menu_text)

    # 🔥 MENSAJE FINAL SEGURO (sirve para message y callback)
    if hasattr(update_or_query, "message") and update_or_query.message:
        await update_or_query.message.reply_text(
            "Elige una función respondiendo con el número correspondiente:"
        )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    uid = query.from_user.id
    data = query.data

    # 🔹 AGREGAR
    if data == "admin_agregar":
        estado_admin[uid] = "agregar"
        await query.message.reply_text("🆔 Envía el ID a agregar")

    elif data == "admin_eliminar":
        estado_admin[uid] = "eliminar"
        await query.message.reply_text("🆔 Envía el ID a eliminar")

    elif data == "admin_bloquear":
        estado_admin[uid] = "bloquear"
        await query.message.reply_text("🆔 ID a bloquear")

    elif data == "admin_desbloquear":
        estado_admin[uid] = "desbloquear"
        await query.message.reply_text("🆔 ID a desbloquear")

    elif data == "admin_add17":
        estado_admin[uid] = "add17"
        await query.message.reply_text("🆔 ID para opción 17")

    elif data == "admin_remove17":
        estado_admin[uid] = "remove17"
        await query.message.reply_text("🆔 ID para quitar opción 17")

    # 👥 VER USUARIOS
    elif data == "admin_ver":

        for u in usuarios:
            try:
                fotos = await context.bot.get_user_profile_photos(int(u))

                if fotos.total_count > 0:
                    file = fotos.photos[0][-1].file_id
                    await context.bot.send_photo(uid, file, caption=f"ID: {u}")
                else:
                    await context.bot.send_message(uid, f"ID: {u}")
            except:
                pass

    # 📊 ESTADÍSTICAS
    elif data == "admin_stats":

        mensaje = f"""📊 ESTADÍSTICAS

👥 Agregados: {len(stats['agregados'])}
🚫 Bloqueados: {len(stats['bloqueados'])}
✅ Desbloqueados: {len(stats['desbloqueados'])}
➖ Eliminados: {len(stats['eliminados'])}

🛠 Mantenimiento usado: {stats['mantenimiento']}
📢 Publicaciones: {stats['publicaciones']}
"""

        await query.message.reply_text(mensaje)

        # 🔥 RESETEAR
        stats["agregados"].clear()
        stats["bloqueados"].clear()
        stats["desbloqueados"].clear()
        stats["eliminados"].clear()
        stats["mantenimiento"] = 0
        stats["publicaciones"] = 0
    # 🟢 ACTIVAR
async def mantenimiento_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global MANTENIMIENTO

    query = update.callback_query
    uid = query.from_user.id
    data = query.data

    await query.answer()

    if not es_admin(uid):
        return

    # 🟢 ACTIVAR
    if data == "mantenimiento_on":

        MANTENIMIENTO = True

        await query.edit_message_text("🛠 Bot en mantenimiento ACTIVADO")

        # avisar usuarios
        for u in usuarios:
            try:
                await context.bot.send_message(
                    chat_id=int(u),
                    text="🛠 El bot está en mantenimiento\nIntenta más tarde."
                )
            except:
                pass

    # 🔴 DESACTIVAR
    elif data == "mantenimiento_off":

        MANTENIMIENTO = False

        botones = [[
            InlineKeyboardButton("✅ Sí hubo actualización", callback_data="update_si"),
            InlineKeyboardButton("❌ No", callback_data="update_no")
        ]]

        await query.edit_message_text(
            "🟢 Bot funcionando nuevamente\n\n¿Hubo actualización?",
            reply_markup=InlineKeyboardMarkup(botones)
        )

async def actualizacion_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    uid = query.from_user.id
    data = query.data

    await query.answer()

    if not es_admin(uid):
        return

    # ✅ SI HUBO UPDATE
    if data == "update_si":

        estado_admin[uid] = "esperando_update"

        await query.message.reply_text("✍️ Escribe los detalles de la actualización")

    # ❌ NO HUBO
    elif data == "update_no":

        await query.edit_message_text("🟢 Bot activo nuevamente")

        for u in usuarios:
            try:
                await context.bot.send_message(
                    chat_id=int(u),
                    text="🟢 El bot ya está activo nuevamente"
                )
            except:
                pass

async def borrar_pedidos_botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # 🔥 CONFIRMAR BORRADO
    if query.data == "borrar_todos":

        keyboard = [
            [
                InlineKeyboardButton("✅ Sí", callback_data="confirmar_borrar"),
                InlineKeyboardButton("❌ No", callback_data="cancelar_borrar")
            ]
        ]

        await query.message.reply_text(
            "⚠️ ¿Seguro que quieres borrar TODOS los pedidos?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 🔥 BORRAR
    elif query.data == "confirmar_borrar":

        pedidos.clear()
        guardar_json(PEDIDOS_FILE, pedidos)

        await query.message.reply_text("🗑 Todos los pedidos fueron eliminados")

    # 🔥 CANCELAR
    elif query.data == "cancelar_borrar":

        await query.message.reply_text("❌ Operación cancelada")
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
app.add_handler(CallbackQueryHandler(mantenimiento_botones, pattern="mantenimiento_"))
app.add_handler(CallbackQueryHandler(actualizacion_botones, pattern="update_"))
app.add_handler(CallbackQueryHandler(borrar_pedidos_botones, pattern="^(borrar_todos|confirmar_borrar|cancelar_borrar)$"))
app.add_handler(CallbackQueryHandler(admin_panel))

app.run_polling()

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
estado_soporte = {}

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

menu_text = """
━━━━━━━━━━━━━
OPCIONES DISPONIBLES🎮

1. Cromar calipers.
2. Cromar luces.
3. Ventanas GG.
4. Modificar 1 HP.
5. Cromar rines.
6. Cromar aleron.
7. Traspasar auto.
8. Modificar Shiftime.
9. Remover Parachoques.
10. Hacer Auto 6 segundos.
11. Modificar ID.
12. Poner 30k / 50M.
13. Comprar casas.
14. Chetar Cuenta.
15. Full GG 1 color.
16. Full GG Colores Distintos.
17. Bot de Diseños/Cuentas al azar.
18. Enviar problemas o ideas.
━━━━━━━━━━━━━
"""
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
18. REPORTES IDEAS 
━━━━━━━━━━━━━
⚙ ADMIN

19. Panel Admin
20. Ver Pedidos
21. Mantenimiento of on 
22. ver reportes o ideas 
/publicar
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
    
}

FORMULARIOS = {
"1":["¡Seleccionaste “Cromar Calipers”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:","🚗 Ingresa el numero del vehículo"],
"2":["¡Seleccionaste “Cromar Luces”!\n✉️Ingresa el correo de tu cuenta","🔐 🔐Ingresa lá contraseña de tu cuenta:","🚗 Ingresa el numero del vehículo"],
"3":["¡Seleccionaste “Ventanas GG”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:","🚗 Ingresa el numero del vehículo"],
"4":["¡Seleccionaste “Modificar Un HP”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"5":["¡Seleccionaste “Cromar Rines”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:","🚗 Ingresa el numero del vehículo"],
"6":["¡Seleccionaste “Cromar Aleron”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:","🚗 Ingresa el numero del vehículo"],
"7":["¡Seleccionaste “Transpasar Auto”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"8":["¡Seleccionaste “Modificar Shiftime”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"9":["¡Seleccionaste “Remover Parachoques”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"10":["¡Seleccionaste “Hacer 6 segundos”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"11":["¡Seleccionaste “Modificar ID”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:", "Ingresa el nuevo 🆔"],
"12":["¡Seleccionaste “Poner 30k/50m”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"13":["¡Seleccionaste “Comprar Casas”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"14":["¡Seleccionaste “Chetar Cuenta”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:"],
"15":["¡Seleccionaste “Full gg 1 Color”!\n✉️Ingresa el correo de tu cuenta","🔐Ingresa lá contraseña de tu cuenta:","🚗 Ingresa el numero del vehículo"],
"16":[
"¡Seleccionaste “Full GG Varios Colores”!\n✉️Ingresa el correo de tu cuenta",
"🔐Ingresa lá contraseña de tu cuenta:",
"🚗 Ingresa el numero del vehículo"
],
"17":[],
}
OPCIONES_CON_COLOR={"1","2","3","5","6","15"}
OPCION_FULL_GG = "16"

user_states={}
estado_reportes = {}  # Para problemas de usuarios
estado_ideas = {}     # Para ideas de usuarios
estado_reportes_global = {}  # {uid: "texto del reporte"}
estado_ideas_global = {}     # {uid: "texto de la idea"}
# 🔹 LISTAS PARA GUARDAR TODOS LOS REPORTES E IDEAS
todos_reportes = []  # Guarda todos los reportes/problemas
todas_ideas = []     # Guarda todas las ideas
estado_publicar = {}
tipo_publicar = {}
usuarios_seleccionados = {}
seleccion_publicar = {}
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

    # ⚠️ Evitar error si no es mensaje (ej: botón)
    if not update.message:
        return

    msg = update.message

    # 🔥 TEXTO SEGURO (NO CRASHEA)
    texto = msg.text.strip() if msg.text else None

    # ===============================
    # 🔹 USUARIO REPORTES (problemas)
    # ===============================
    if uid in estado_reportes:

        if not texto:
            await msg.reply_text("❌ Ingresa texto válido")
            return

        todos_reportes.append(f"👤 @{update.effective_user.username} ({uid}): {texto}")

        botones = [
            [InlineKeyboardButton("✅ Enviar", callback_data="enviar_problema")],
            [InlineKeyboardButton("❌ Rechazar", callback_data="rechazar_problema")]
        ]

        await msg.reply_text(
            f"Tu reporte:\n\n{texto}\n\nElige una opción:",
            reply_markup=InlineKeyboardMarkup(botones)
        )
        return

    # ===============================
    # 🔹 USUARIO IDEAS
    # ===============================
    if uid in estado_ideas:

        if not texto:
            await msg.reply_text("❌ Ingresa texto válido")
            return

        todas_ideas.append(f"💡 @{update.effective_user.username} ({uid}): {texto}")

        botones = [
            [InlineKeyboardButton("✅ Enviar", callback_data="enviar_idea")],
            [InlineKeyboardButton("❌ Rechazar", callback_data="rechazar_idea")]
        ]

        await msg.reply_text(
            f"Tu idea:\n\n{texto}\nElige una opción:",
            reply_markup=InlineKeyboardMarkup(botones)
        )
        return

    # ===============================
    # 🔥 AQUÍ SIGUE TU /PUBLICAR
    # ===============================

    # Ejemplo detección (IMPORTANTE)
    if uid in tipo_publicar:

        tipo = tipo_publicar[uid]

        # 📸 FOTO
        if tipo == "foto":
            if not msg.photo:
                await msg.reply_text("❌ Seleccionaste FOTO, envía una foto")
                return

        # 🎥 VIDEO
        elif tipo == "video":
            if not msg.video:
                await msg.reply_text("❌ Seleccionaste VIDEO, envía un video")
                return

        # 🎧 AUDIO
        elif tipo == "audio":
            if not msg.audio and not msg.voice:
                await msg.reply_text("❌ Seleccionaste AUDIO, envía un audio")
                return

        # 📁 ARCHIVO
        elif tipo == "archivo":
            if not msg.document:
                await msg.reply_text("❌ Seleccionaste ARCHIVO, envía un archivo")
                return

        # ✅ GUARDAR MENSAJE
        # 👉 GUARDAR MENSAJE
        estado_publicar[uid] = msg

# 👉 INICIALIZAR SELECCIÓN
        usuarios_seleccionados[uid] = set()

# 👉 CARGAR USUARIOS
        try:
            with open("usuarios.json", "r") as f:
                lista_usuarios = json.load(f)
        except:
            await msg.reply_text("❌ Error cargando usuarios")
            return

# 👉 CREAR BOTONES
        botones = []

        for u in lista_usuarios:
            botones.append([
                InlineKeyboardButton(f"👤 Usuario {u}", callback_data=f"user_{u}")
    ])

# 👉 BOTONES FINALES
        botones.append([
    InlineKeyboardButton("✅ Enviar seleccionados", callback_data="send_selected")
])

        botones.append([
    InlineKeyboardButton("🌍 Enviar a TODOS", callback_data="send_all")
])

        await msg.reply_text(
    "👥 Selecciona usuarios:",
            reply_markup=InlineKeyboardMarkup(botones)
)

        return

    # 🔥 RESPUESTAS DEL ADMIN
    if uid in estado_admin:

        accion = estado_admin[uid]

        # 🔥 UPDATE GLOBAL
        if accion == "esperando_update":

            detalles = texto

            mensaje = f"""🟢 BOT FUNCIONANDO DE NUEVO

✨ ACTUALIZACIÓN:

{detalles}

🚀 Gracias por tu paciencia.
Abajo te aparecera un boton que puuedes usar en caso de tener un desacuerdo o probllema con el bot. :)
"""

            # ✅ BOTÓN
            botones = [
                [InlineKeyboardButton("⚠️ Reporte", callback_data="reportar_problema")]
            ]

            teclado = InlineKeyboardMarkup(botones)

            # ✅ ENVIAR A TODOS
            for u in usuarios:
                try:
                    await context.bot.send_message(
                        int(u),
                        mensaje,
                        reply_markup=teclado
                    )
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

        # ➕ AGREGAR
        if accion == "agregar":
            usuarios.add(str(target))
            await update.message.reply_text("✅ Usuario agregado")

            try:
                await context.bot.send_message(
                    chat_id=target,
                    text="🎉 Has sido agregado al bot"
                )
            except:
                pass

        # ❌ ELIMINAR
        elif accion == "eliminar":
            usuarios.discard(str(target))
            stats["eliminados"].append(target)
            await update.message.reply_text("❌ Usuario eliminado")

        # 🚫 BLOQUEAR
        elif accion == "bloquear":
            bloqueados.add(str(target))
            stats["bloqueados"].append(target)
            await update.message.reply_text("🚫 Usuario bloqueado")

            try:
                await context.bot.send_message(
                    chat_id=target,
                    text="🚫 Has sido bloqueado del bot"
                )
            except:
                pass

        # ✅ DESBLOQUEAR
        elif accion == "desbloquear":
            bloqueados.discard(str(target))
            stats["desbloqueados"].append(target)
            await update.message.reply_text("✅ Usuario desbloqueado")

            try:
                await context.bot.send_message(
                    chat_id=target,
                    text="✅ Has sido desbloqueado, ya puedes usar el bot"
                )
            except:
                pass

        # ⭐ OPCION 17
        elif accion == "add17":
            opcion17.add(str(target))
            await update.message.reply_text("⭐ Opción 17 agregada")

        elif accion == "remove17":
            opcion17.discard(str(target))
            await update.message.reply_text("❌ Opción 17 quitada")

        # 🔥 LIMPIAR ESTADO
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
                    InlineKeyboardButton("🔴 Rojo",callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul",callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde",callback_data="color_verde"),
                    InlineKeyboardButton("🔵Azul Claro",callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("🟠Naranja",callback_data="color_naranja"),
                    InlineKeyboardButton("🩷rosa",callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("🟣Purpura",callback_data="color_purpura"),
                    InlineKeyboardButton("⚪Blanco",callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("🟡Amarillo",callback_data="color_amarillo"),
                    InlineKeyboardButton("🟣Violeta Obscuro",callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("🔵Turqueza",callback_data="color_turqueza")
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
                    InlineKeyboardButton("🔴 Rojo",callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul",callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde",callback_data="color_verde"),
                    InlineKeyboardButton("🔵Azul Claro",callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("🟠Naranja",callback_data="color_naranja"),
                    InlineKeyboardButton("🩷rosa",callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("🟣Purpura",callback_data="color_purpura"),
                    InlineKeyboardButton("⚪Blanco",callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("🟡Amarillo",callback_data="color_amarillo"),
                    InlineKeyboardButton("🟣Violeta Obscuro",callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("🔵Turqueza",callback_data="color_turqueza")
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


    opciones_validas = list(FORMULARIOS.keys()) + ["17", "18", "19", "20", "21", "22"]

    # ❌ comando inválido
    if texto not in opciones_validas and uid not in user_states:
            await update.message.reply_text("❌ Ese comando no existe")
            return
    
    # 🔹 OPCION 20 (MANTENIMIENTO)
    if texto == "18":
        botones = [
        [InlineKeyboardButton("🛠 Problemas con el bot ", callback_data="reportes_problemas"),
        InlineKeyboardButton("💡 Ideas para el bot", callback_data="reportes_ideas")]
    ]
        await update.message.reply_text(
        "📌 SECCIÓN DE REPORTES\nElige una opción:",
        reply_markup=InlineKeyboardMarkup(botones)
    )
        return
    # 🔹 OPCION 21 (MANTENIMIENTO)
    if texto == "21":

        if not es_admin(uid):
            await update.message.reply_text("❌ Solo admin")
            return

        botones = [
        [InlineKeyboardButton("🟢 Activar mantenimiento", callback_data="mantenimiento_on"),
        InlineKeyboardButton("🔴 Desactivar mantenimiento ", callback_data="mantenimiento_off")]
        ]

        await update.message.reply_text(
            "⚙️ Panel de mantenimiento",
            reply_markup=InlineKeyboardMarkup(botones)
            )
        return
    # 🔹 OPCION 19
    if texto == "19":

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
    # 🔹 COMANDO ADMIN 22 - REVISIÓN DE REPORTES/IDEAS
    # 🔹 COMANDO ADMIN 22 - REVISIÓN DE REPORTES/IDEAS
    # 🔹 COMANDO ADMIN 22 - REVISIÓN DE REPORTES/IDEAS
    if texto == "22" and uid == ADMIN_ID:
        botones = [
            [InlineKeyboardButton("📝 Ver reportes/problemas", callback_data="ver_reportes")],
            [InlineKeyboardButton("💡 Ver ideas", callback_data="ver_ideas")]
    ]
        teclado = InlineKeyboardMarkup(botones)
        await update.message.reply_text(
            "⚡ Revisión de reportes e ideas",
            reply_markup=teclado
        )
        return
    # 🔹 OPCION 20
    if texto == "20":

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
    # 🔹 OPCION 20
    if texto == "20":

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
                    InlineKeyboardButton("🔴 Rojo",callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul",callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde",callback_data="color_verde"),
                    InlineKeyboardButton("🔵Azul Claro",callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("🟠Naranja",callback_data="color_naranja"),
                    InlineKeyboardButton("🩷rosa",callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("🟣Purpura",callback_data="color_purpura"),
                    InlineKeyboardButton("⚪Blanco",callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("🟡Amarillo",callback_data="color_amarillo"),
                    InlineKeyboardButton("🟣Violeta Obscuro",callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("🔵Turqueza",callback_data="color_turqueza")
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
                    InlineKeyboardButton("🔴 Rojo",callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul",callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde",callback_data="color_verde"),
                    InlineKeyboardButton("🔵Azul Claro",callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("🟠Naranja",callback_data="color_naranja"),
                    InlineKeyboardButton("🩷rosa",callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("🟣Purpura",callback_data="color_purpura"),
                    InlineKeyboardButton("⚪Blanco",callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("🟡Amarillo",callback_data="color_amarillo"),
                    InlineKeyboardButton("🟣Violeta Obscuro",callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("🔵Turqueza",callback_data="color_turqueza")
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

async def soporte(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    uid = query.from_user.id

    estado_soporte[uid] = True

    await query.message.reply_text("✍️ Escribe tu problema con el bot:")
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
                    InlineKeyboardButton("🔴 Rojo",callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul",callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde",callback_data="color_verde"),
                    InlineKeyboardButton("🔵Azul Claro",callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("🟠Naranja",callback_data="color_naranja"),
                    InlineKeyboardButton("🩷rosa",callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("🟣Purpura",callback_data="color_purpura"),
                    InlineKeyboardButton("⚪Blanco",callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("🟡Amarillo",callback_data="color_amarillo"),
                    InlineKeyboardButton("🟣Violeta Obscuro",callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("🔵Turqueza",callback_data="color_turqueza")
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
                    InlineKeyboardButton("🔴 Rojo",callback_data="color_rojo"),
                    InlineKeyboardButton("🔵 Azul",callback_data="color_azul")
                ],
                [
                    InlineKeyboardButton("🟢 Verde",callback_data="color_verde"),
                    InlineKeyboardButton("🔵Azul Claro",callback_data="color_azul_claro")
                ],
                [
                    InlineKeyboardButton("🟠Naranja",callback_data="color_naranja"),
                    InlineKeyboardButton("🩷rosa",callback_data="color_rosa")
                ],
                [
                    InlineKeyboardButton("🟣Purpura",callback_data="color_purpura"),
                    InlineKeyboardButton("⚪Blanco",callback_data="color_blanco")
                ],
                [
                    InlineKeyboardButton("🟡Amarillo",callback_data="color_amarillo"),
                    InlineKeyboardButton("🟣Violeta Obscuro",callback_data="color_violeta__obscuro")
                ],
                [
                    InlineKeyboardButton("🔵Turqueza",callback_data="color_turqueza")
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
                    text="🛠 El bot está en mantenimiento intenta más tarde."
                )
            except:
                pass

    # 🔴 DESACTIVAR
    elif data == "mantenimiento_off":

        MANTENIMIENTO = False

        botones = [[
            InlineKeyboardButton("✅ Sí hubo actualización", callback_data="update_si"),
            InlineKeyboardButton("❌ No hubo actualizacion", callback_data="update_no")
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
        

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    botones = [
    [InlineKeyboardButton("➕ Agregar", callback_data="admin_agregar")],
    [InlineKeyboardButton("➖ Eliminar", callback_data="admin_eliminar")],
    [InlineKeyboardButton("🚫 Bloquear", callback_data="admin_bloquear")],
    [InlineKeyboardButton("✅ Desbloquear", callback_data="admin_desbloquear")],
    [InlineKeyboardButton("📊 Estadísticas", callback_data="admin_stats")],
    [InlineKeyboardButton("👥 Usuarios", callback_data="admin_users")],
    [InlineKeyboardButton("🚫 Bloqueados", callback_data="admin_blocked")],
    [InlineKeyboardButton("⭐ Agregar Opción 17", callback_data="admin_add17")],
    [InlineKeyboardButton("❌ Quitar Opción 17", callback_data="admin_remove17")],
]

    await update.message.reply_text(
        "⚙️ PANEL ADMIN",
        reply_markup=InlineKeyboardMarkup(botones)
    )
# ------------------------
# PUBLICACIONES
# ------------------------

async def publicar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    botones = [
        [InlineKeyboardButton("📸 Foto", callback_data="pub_foto")],
        [InlineKeyboardButton("🎥 Video", callback_data="pub_video")],
        [InlineKeyboardButton("📁 Archivo", callback_data="pub_doc")],
        [InlineKeyboardButton("🎧 Audio", callback_data="pub_audio")]
    ]

    await update.message.reply_text(
        "📢 ¿Qué quieres enviar?",
        reply_markup=InlineKeyboardMarkup(botones)
    )

async def tipo_envio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    uid = query.from_user.id
    data = query.data

    tipo = data.replace("pub_", "")

    tipo_publicar[uid] = tipo

    await query.edit_message_text(
        f"📤 Envía el {tipo} que deseas publicar"
    )

#COMPLETAR#

async def seleccion_envio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    uid = query.from_user.id
    data = query.data

    if uid not in estado_publicar:
        return

    # 👤 SELECCIONAR
    if data.startswith("user_"):
        u = data.split("_")[1]

        usuarios_seleccionados[uid].add(u)

        lista = "\n".join(usuarios_seleccionados[uid])

        await query.message.reply_text(
            f"👥 Usuarios seleccionados:\n{lista}"
        )
        return

    # ✅ ENVIAR SELECCIONADOS
    if data == "send_selected":

        mensaje = estado_publicar.pop(uid)
        seleccion = usuarios_seleccionados.pop(uid)

        enviados = 0

        for u in seleccion:
            try:
                await context.bot.copy_message(
                    chat_id=u,
                    from_chat_id=query.message.chat.id,
                    message_id=mensaje.message_id
                )
                enviados += 1
            except:
                pass

        await query.message.reply_text(f"✅ Enviado a {enviados}")
        return

    # 🌍 ENVIAR A TODOS
    if data == "send_all":

        mensaje = estado_publicar.pop(uid)
        usuarios_seleccionados.pop(uid)

        with open("usuarios.json","r") as f:
            usuarios = json.load(f)

        enviados = 0

        for u in usuarios:
            try:
                await context.bot.copy_message(
                    chat_id=u,
                    from_chat_id=query.message.chat.id,
                    message_id=mensaje.message_id
                )
                enviados += 1
            except:
                pass

        await query.message.reply_text(f"🌍 Enviado a todos ({enviados})")


# ------------------------
# FUNCION 17
# ------------------------
async def completar_pedido(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    i = int(query.data.split("_")[1])

    if i >= len(pedidos):
        await query.edit_message_text("Pedido no encontrado")
        return

    pedido = pedidos[i]

    # 🔥 TRADUCIR OPCIÓN A NOMBRE
    nombre_funcion = NOMBRES_OPCIONES.get(
        pedido["opcion"],
        f"Opción {pedido['opcion']}"
    )

    # 🔥 MENSAJE AL USUARIO
    await context.bot.send_message(
        pedido["id"],
        f"""✅ TU PEDIDO HA SIDO COMPLETADO

📌 Función: {nombre_funcion}
📧 Correo: {pedido['correo']}

Gracias por usar el bot."""
    )

    # 🔥 ELIMINAR PEDIDO
    pedidos.pop(i)
    guardar_json(PEDIDOS_FILE, pedidos)

    await query.edit_message_text("✅ Pedido completado y eliminado")

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

    await query.edit_message_text("Funcionn 17 activada")


async def quitar_funcion17(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    uid=context.args[0]

    if uid in funcion17:
        del funcion17[uid]

    guardar_json(FUNCION17_FILE,funcion17)

    await update.message.reply_text("Funcion 17 eliminada")


# ------------------------
# ADMIN USUARIOS
# ------------------------

async def agregar(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if not es_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("Usa: /agregar ID")
        return

    uid=context.args[0]

    usuarios.add(str(uid))
    guardar_json(USUARIOS_FILE,list(usuarios))

    await update.message.reply_text("Usuario agregado")

    # MENSAJE AL USUARIO
    try:
        await context.bot.send_message(
            chat_id=int(uid),
            text="🎉 Has sido agregado al bot.Usa /start para comenzar."
        )
    except:
        await update.message.reply_text(
            "⚠ No se pudo enviar mensaje al usuario.\nEl usuario debe iniciar el bot con /start primero."
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
        await update.message.reply_text("Usa el comando \n/desbloquear ID")
        return

    uid = context.args[0]

    intentos[uid] = 0

    guardar_json(INTENTOS_FILE, intentos)

    await update.message.reply_text("Usuario desbloqueado")

async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.effective_user.id == ADMIN_ID:
        return

    await update.message.reply_text("Ese comando no existe")

async def reportes_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    if data == "reportes_problemas":
        estado_reportes[uid] = True
        await query.message.reply_text("✍️ Ingresa los problemas que has tenido con el bot:")
    elif data == "reportes_ideas":
        estado_ideas[uid] = True
        await query.message.reply_text("✍️ Ingresa tus ideas para próximas actualizaciones del bot:")

async def enviar_reporte_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    data = query.data

    # 🔹 ENVIAR PROBLEMA
    if data == "enviar_problema" and uid in estado_reportes:
        problema = estado_reportes.pop(uid)
        await context.bot.send_message(
            ADMIN_ID,
            f"⚠️ NUEVO REPORTE\n\n👤 @{query.from_user.username} ({uid})\n📝 {problema}"
        )
        await query.message.reply_text("✅ Tu reporte fue enviado")
        await query.message.reply_text(menu_text if not es_admin(uid) else menu_admin)
        await query.message.reply_text("Elige una función respondiendo con el número correspondiente:")
        return

    # 🔹 RECHAZAR PROBLEMA
    if data == "rechazar_problema" and uid in estado_reportes:
        estado_reportes.pop(uid)
        await query.message.reply_text("❌ Tu reporte fue cancelado")
        await query.message.reply_text(menu_text if not es_admin(uid) else menu_admin)
        await query.message.reply_text("Elige una función respondiendo con el número correspondiente:")
        return

    # 🔹 ENVIAR IDEA
    if data == "enviar_idea" and uid in estado_ideas:
        idea = estado_ideas.pop(uid)
        await context.bot.send_message(
            ADMIN_ID,
            f"💡 NUEVA IDEA\n\n👤 @{query.from_user.username}\n({uid})\n📝 {idea}"
        )
        await query.message.reply_text("✅ Tu idea fue enviada")
        await query.message.reply_text(menu_text if not es_admin(uid) else menu_admin)
        await query.message.reply_text("Elige una función respondiendo con el número correspondiente:")
        return

    # 🔹 RECHAZAR IDEA
    if data == "rechazar_idea" and uid in estado_ideas:
        estado_ideas.pop(uid)
        await query.message.reply_text("❌ Tu idea fue cancelada")
        await query.message.reply_text(menu_text if not es_admin(uid) else menu_admin)
        await query.message.reply_text("Elige una función respondiendo con el número correspondiente:")
        return

async def ver_reportes_o_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ver_reportes":
        if not estado_reportes_global:
            await query.message.reply_text("No hay reportes aún.")
            return

        mensaje = "📝 **Reportes/Problemas recibidos:**\n\n"
        for uid, texto in estado_reportes_global.items():
            mensaje += f"ID: {uid}\nTexto: {texto}\n\n"
        await query.message.reply_text(mensaje)

    elif query.data == "ver_ideas":
        if not estado_ideas_global:
            await query.message.reply_text("No hay ideas aún.")
            return

        mensaje = "💡 **Ideas recibidas:**\n\n"
        for uid, texto in estado_ideas_global.items():
            mensaje += f"ID: {uid}\nTexto: {texto}\n\n"
        await query.message.reply_text(mensaje)

async def boton_revision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ver_reportes":
        if todos_reportes:
            await query.message.reply_text("\n\n".join(todos_reportes))
        else:
            await query.message.reply_text("❌ No hay reportes aún.")

    elif query.data == "ver_ideas":
        if todas_ideas:
            await query.message.reply_text("\n\n".join(todas_ideas))
        else:
            await query.message.reply_text("❌ No hay ideas aún.")
##########RARO#########
async def raro(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    msg = update.message

    if not msg:
        return

    uid = user.id

    # 🔥 IGNORAR ADMIN
    if es_admin(uid):
        return

    # 🔥 IGNORAR CUANDO ESTÁ PUBLICANDO
    if uid in tipo_publicar or uid in estado_publicar or uid in seleccion_publicar:
        return

    # 🔥 IGNORAR TEXTO NORMAL
    if msg.text:
        return

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
🚨 𝗔𝗟𝗘𝗥𝗧𝗔 𝗗𝗘 𝗠𝗢𝗩𝗜𝗠𝗜𝗘𝗡𝗧𝗢 𝗦𝗢𝗦𝗣𝗘𝗖𝗛𝗢𝗦𝗢

👤 Usuario: {user.first_name}
🔗 Username: @{user.username}
🆔 ID: {user.id}

📦 Tipo: {tipo}

📅 Fecha: {fecha}
⏰ Hora: {hora}

⚠️ Verifica esta actividad inmediatamente.
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
         "⚠ Acción identificada como extraña (Notificada al administrador), usa el bot correctamente."
    )
# ------------------------
# BOTON MANTENIMIENTO
# ------------------------

async def boton_comandos_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "comando":
        await query.message.reply_text("╔══════════════════════════════╗\n"
"        👑 PANEL DE ADMIN 👑\n"
"╚══════════════════════════════╝\n\n"

"⚙️ CONTROL DEL BOT\n"
"━━━━━━━━━━━━━━━━━━━━\n\n"

"🚀 COMANDOS PRINCIPALES\n\n"

"▶️ /start\n"
"Iniciar el bot\n\n"

"👤 /agregar\n"
"Agregar usuario autorizado\n\n"

"❌ /eliminar\n"
"Eliminar usuario del sistema\n\n"

"📋 /ver_usuarios\n"
"Ver usuarios registrados\n\n"

"🔓 /desbloquear\n"
"Desbloquear usuario bloqueado\n\n"

"🔓 /ver_bloqueados\n"
"Ver usuarios bloqueados\n\n"

"━━━━━━━━━━━━━━━━━━━━\n\n"

"📢 PUBLICACIONES\n\n"

"📡 /publicar\n"
"Enviar mensaje a todos los usuarios\n\n"

"━━━━━━━━━━━━━━━━━━━━\n\n"

"🧩 FUNCIÓN 17\n\n"

"🟢 /opcion_comando_17\n"
"Dar acceso a función 17\n\n"

"🔴 /quitar_funcion17\n"
"Quitar acceso a función 17\n\n"

"━━━━━━━━━━━━━━━━━━━━\n"

"🧩 MANTENIMIENTO ON/OF\n\n"

"🟢 /mantenimiento_on\n"
"Poner bot en mantenimiento\n\n"

"🔴 /mantenimiento_off\n"
"Poner bot activo (quitar mantenimiento)\n\n"

"━━━━━━━━━━━━━━━━━━━━\n"

"🛡 Solo para administrador")
        
async def boton_respuestas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "respuestas":
        await query.message.reply_text("╔══════════════════════════════╗\n"
"📌 Respuestas\n"
"───────────────────\n"
"✅ Proceso Finalizado\n"
"𝗧𝘂 𝗽𝗿𝗼𝗰𝗲𝘀𝗼 𝗱𝗲 𝗹𝗮 𝗰𝘂𝗲𝗻𝘁𝗮 () 𝗵𝗮 𝘀𝗶𝗱𝗼 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗮𝗱𝗼.\n"
"────────────────────\n"
"➕ Agregar usuario\n"
"𝗧𝘂 𝗰𝘂𝗲𝗻𝘁𝗮 𝗵𝗮 𝘀𝗶𝗱𝗼 𝗰𝗿𝗲𝗮𝗱𝗮 🏁🎉! 𝗣𝘂𝗲𝗱𝗲𝘀 𝘂𝘀𝗮𝗿 𝗹𝗮𝘀 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗲𝘀 𝗰𝗼𝗻 𝗲𝗹 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /start.\n"
"────────────────────\n"
"🔓 Desbloquear usuario\n"
"𝗛𝗮𝘀 𝘀𝗶𝗱𝗼 𝗱𝗲𝘀𝗯𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼! 𝗛𝗮𝗯𝗹𝗮 𝗰𝗼𝗻 𝗲𝗹 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 @drillscars 𝗽𝗮𝗿𝗮 𝗾𝘂𝗲 𝘁𝗲 𝗮𝗴𝗿𝗲𝗴𝘂𝗲.\n"
"────────────────────\n"
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
app.add_handler(CommandHandler("admin", admin_menu))

# 🔥 CALLBACKS (ORDEN IMPORTANTE)
app.add_handler(CallbackQueryHandler(soporte, pattern="reportar_problema"))
app.add_handler(CallbackQueryHandler(boton_revision, pattern="ver_reportes|ver_ideas"))
app.add_handler(CallbackQueryHandler(ver_reportes_o_ideas, pattern="^(ver_reportes|ver_ideas)$"))
app.add_handler(CallbackQueryHandler(reportes_handler, pattern="reportes_.*"))
app.add_handler(CallbackQueryHandler(enviar_reporte_idea, pattern="enviar_.*|rechazar_.*"))
app.add_handler(CallbackQueryHandler(color, pattern="^(color_|aleron_|luces_|calipers_)"))
app.add_handler(CallbackQueryHandler(activar17, pattern="^f17_"))
app.add_handler(CallbackQueryHandler(tipo_envio, pattern="^pub_"))
app.add_handler(CallbackQueryHandler(seleccion_envio, pattern="^(user_|send_)"))
app.add_handler(CallbackQueryHandler(completar_pedido, pattern="^completar_"))
app.add_handler(CallbackQueryHandler(boton_comandos_admin, pattern="comando"))
app.add_handler(CallbackQueryHandler(boton_respuestas, pattern="respuestas"))
app.add_handler(CallbackQueryHandler(mantenimiento_botones, pattern="^mantenimiento_"))
app.add_handler(CallbackQueryHandler(actualizacion_botones, pattern="^update_"))
app.add_handler(CallbackQueryHandler(borrar_pedidos_botones, pattern="^(borrar_todos|confirmar_borrar|cancelar_borrar)$"))
app.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_"))

# 🔥 PRIMERO detectar cosas raras
app.add_handler(
    MessageHandler(
        filters.Sticker.ALL | filters.VOICE | filters.AUDIO | filters.VIDEO | filters.Document.ALL,
        raro
    )
)

# 🔥 LUEGO texto normal
app.add_handler(MessageHandler(filters.ALL, manejar))

# 🔥 AL FINAL comandos desconocidos
app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))

# TEXTO
app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar))

print("BOT ACTIVOOO DE DRILLS")

app.run_polling()
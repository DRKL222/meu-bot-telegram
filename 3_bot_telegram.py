import os
import logging
import datetime
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_TOKEN", "8737068584:AAEpqTSPQbIJafyiLHNhkkf-KsN3XDg3s-c")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── RESPOSTAS HUMANIZADAS ────────────────────────────────────────────────────

SAUDACOES_RESPOSTAS = [
    "Oi! Tudo bem? Em que posso te ajudar hoje? 😊",
    "Olá! Que bom te ver por aqui! Como posso te ajudar?",
    "Oi oi! Pode falar, tô aqui pra isso 😄",
    "Ei, olá! Me diz, o que você precisa?",
]

DESPEDIDAS_RESPOSTAS = [
    "Tchau! Qualquer coisa é só chamar 👋",
    "Até mais! Foi um prazer te ajudar 😊",
    "Até logo! Estarei por aqui se precisar de algo.",
    "Falou! Cuida-se bem 😄",
]

AGRADECIMENTOS_RESPOSTAS = [
    "De nada! Fico feliz em ter ajudado 😊",
    "Imagina, pra isso tô aqui!",
    "Disponha! Se precisar de mais alguma coisa, é só falar.",
    "Que isso, sem problema nenhum! 😄",
]

NAOENTENDI_RESPOSTAS = [
    "Hmm, não entendi muito bem... Pode reformular?",
    "Eita, essa eu não peguei 😅 Tenta me perguntar de outro jeito!",
    "Não consegui entender direito. Me diz de outra forma?",
    "Desculpa, não entendi! Pode ser mais específico?",
]

FAQ = {
    "horario":     "Funcionamos de segunda a sexta, das 8h às 18h. Mas pode me mandar mensagem a qualquer hora que eu respondo! 😄",
    "preco":       "Os preços variam de acordo com o produto. Quer que eu te mostre o catálogo completo?",
    "preço":       "Os preços variam de acordo com o produto. Quer que eu te mostre o catálogo completo?",
    "contato":     "Pode nos chamar por aqui mesmo, ou se preferir:\n📧 contato@empresa.com\n☎️ (11) 9999-9999",
    "localizacao": "Estamos na Rua Exemplo, 123 — São Paulo, SP. Bem fácil de achar! 📍",
    "localização": "Estamos na Rua Exemplo, 123 — São Paulo, SP. Bem fácil de achar! 📍",
    "entrega":     "O prazo de entrega é de 3 a 7 dias úteis, dependendo da sua região. Quer saber o frete?",
    "pagamento":   "Aceitamos Pix (sem taxinha!), cartão de crédito/débito e boleto bancário 💳",
    "catalogo":    "Aqui tá o nosso catálogo completo 👉 https://exemplo.com/catalogo",
    "catálogo":    "Aqui tá o nosso catálogo completo 👉 https://exemplo.com/catalogo",
}

PALAVRAS_SAUDACAO  = {"oi", "olá", "ola", "hello", "hi", "hey", "bom dia", "boa tarde", "boa noite", "eai", "eaí", "e aí"}
PALAVRAS_DESPEDIDA = {"tchau", "bye", "até logo", "ate logo", "adeus", "flw", "vlw", "até mais", "ate mais", "xau"}
PALAVRAS_OBRIGADO  = {"obrigado", "obrigada", "vlw", "valeu", "thanks", "grato", "grata", "obg", "mt obg", "muito obrigado", "muito obrigada"}
PALAVRAS_PIADA     = {"piada", "me conta uma piada", "faz uma piada", "conta uma piada", "me faz rir"}

PIADAS = [
    "Por que o computador foi ao médico?\nPorque estava com vírus 😂",
    "O que o zero disse pro oito?\nQue cinto bonito! 😆",
    "Por que o Python é ótimo na cozinha?\nPorque sabe usar o django! 🐍",
    "O que o programador disse pra namorada?\nVou te amar por (while) True! ❤️",
    "Por que o banco de dados foi ao psicólogo?\nPorque tinha muita coluna! 😂",
    "Como o programador abre uma porta?\nEle dá um push! 😄",
    "O que o HTML disse pro CSS?\nPara de estilizar minha vida! 😅",
]

# ─── MENU PRINCIPAL ───────────────────────────────────────────────────────────

def montar_menu():
    teclado = [
        [InlineKeyboardButton("🕐 Horário de atendimento", callback_data="horario")],
        [InlineKeyboardButton("💰 Preços",                 callback_data="preco"),
         InlineKeyboardButton("📦 Catálogo",               callback_data="catalogo")],
        [InlineKeyboardButton("🚚 Entrega",                callback_data="entrega"),
         InlineKeyboardButton("💳 Formas de pagamento",    callback_data="pagamento")],
        [InlineKeyboardButton("📞 Contato",                callback_data="contato"),
         InlineKeyboardButton("📍 Onde ficamos",           callback_data="localizacao")],
    ]
    return InlineKeyboardMarkup(teclado)


# ─── COMANDOS ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    hora_atual = datetime.datetime.now().hour
    if hora_atual < 12:     periodo = "Bom dia"
    elif hora_atual < 18:   periodo = "Boa tarde"
    else:                   periodo = "Boa noite"

    await update.message.reply_text(
        f"{periodo}, {user.first_name}! 👋\n\n"
        "Sou o assistente da empresa e tô aqui pra te ajudar.\n"
        "Pode me perguntar qualquer coisa ou escolher uma opção abaixo:",
        reply_markup=montar_menu(),
    )


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Pode me mandar mensagem normalmente e eu te respondo!\n\n"
        "Se preferir, use o menu com /start ou pergunte sobre:\n"
        "horário, preço, entrega, pagamento, contato, catálogo 😊"
    )


async def hora_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    agora = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
    await update.message.reply_text(f"Agora são {agora} ⏰")


# ─── BOTÕES INLINE ────────────────────────────────────────────────────────────

async def botao_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    chave = query.data
    resposta = FAQ.get(chave, "Hmm, não encontrei essa informação agora 😅")
    await query.edit_message_text(
        text=f"{resposta}\n\n‹ Use /start pra voltar ao menu",
    )


# ─── MENSAGENS DE TEXTO ───────────────────────────────────────────────────────

async def responder_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = update.message.text.lower().strip()

    # Saudação
    if any(s in texto for s in PALAVRAS_SAUDACAO):
        await update.message.reply_text(random.choice(SAUDACOES_RESPOSTAS))
        return

    # Despedida
    if any(d in texto for d in PALAVRAS_DESPEDIDA):
        await update.message.reply_text(random.choice(DESPEDIDAS_RESPOSTAS))
        return

    # Agradecimento
    if any(o in texto for o in PALAVRAS_OBRIGADO):
        await update.message.reply_text(random.choice(AGRADECIMENTOS_RESPOSTAS))
        return

    # Piada
    if any(p in texto for p in PALAVRAS_PIADA):
        await update.message.reply_text(random.choice(PIADAS))
        return

    # FAQ por palavras-chave
    for chave, resposta in FAQ.items():
        if chave in texto:
            await update.message.reply_text(resposta)
            return

    # Não entendeu — mostra o menu junto
    await update.message.reply_text(
        random.choice(NAOENTENDI_RESPOSTAS) + "\n\nSe quiser, escolhe uma opção aqui 👇",
        reply_markup=montar_menu(),
    )


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("🤖 Iniciando bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("hora",  hora_cmd))
    app.add_handler(CallbackQueryHandler(botao_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensagem))

    print("✅ Bot online!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

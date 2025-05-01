import telebot
import random
import json

TOKEN = '7848430240:AAFQeHAG5dg0myQbll4I8XqfnL7p4p_3Ras'  
bot = telebot.TeleBot(TOKEN)

oyuncular = {}

kategori_map = {
    '1': 'Genel Kültür',
    '2': 'Bilim',
    '3': 'Sinema',
    '4': 'Spor',
    '5': 'Edebiyat',
    '6': 'Coğrafya',
    '7': 'Müzik',
    '8': 'Teknoloji',
    '9': 'Tarih'
}

@bot.message_handler(func=lambda m: m.text in kategori_map)
def kategori_sec(message):
    user_id = message.from_user.id
    secilen_kategori = kategori_map[message.text]
    oyuncular[user_id]['kategori'] = secilen_kategori
    bot.send_message(message.chat.id, f"📚 {secilen_kategori} kategorisini seçtiniz. Hadi ilk soruya geçelim!")
    yeni_soru_gonder(message)

def yeni_soru_gonder(message):
    user_id = message.from_user.id
    kategori = oyuncular[user_id]['kategori']
    uygun_sorular = [s for s in tum_sorular if s['kategori'].lower() == kategori.lower()]
    if not uygun_sorular:
        bot.send_message(message.chat.id, f"😕 Bu kategoride soru bulunamadı.")
        return
    soru = random.choice(uygun_sorular)
    oyuncular[user_id]['soru'] = soru
    bot.send_message(message.chat.id, f"🧠 Soru: {soru['soru']}")






def sorulari_yukle():
    with open('sorular.json', 'r', encoding='utf-8') as f:
        return json.load(f)

tum_sorular = sorulari_yukle()

@bot.message_handler(commands=['start', 'basla'])
def baslat(message):
    user_id = message.from_user.id
    oyuncular[user_id] = {'puan': 0}
    bot.send_message(message.chat.id, f"🎉 Trivia oyununa hoş geldin! Hangi kategoriyle oynamak istersin?")
    bot.send_message(message.chat.id, "Kategori seç: \n1. Genel Kültür\n2. Bilim\n3. Sinema\n4. Spor\n5. Edebiyat\n6. Coğrafya\n7. Müzik\n8. Teknoloji\n9. Tarih")

@bot.message_handler(func=lambda m: m.text.lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
def kategori_sec(message):
    user_id = message.from_user.id
    kategori_secimi = None
    
kategori_dict = {
    '1': 'Genel Kültür',
    '2': 'Bilim',
    '3': 'Sinema',
    '4': 'Spor',
    '5': 'Edebiyat',
    '6': 'Coğrafya',
    '7': 'Müzik',
    '8': 'Teknoloji',
    '9': 'Tarih'
}

@bot.message_handler(func=lambda m: m.text in kategori_dict)
def kategori_sec(message):
    user_id = message.from_user.id
    kategori_secimi = kategori_dict[message.text]  
    oyuncular[user_id]['kategori'] = kategori_secimi  
    bot.send_message(message.chat.id, f"{kategori_secimi} kategorisini seçtiniz. İlk soruya geçelim.")
    yeni_soru_gonder(message)

    if kategori_secimi:
        oyuncular[user_id]['kategori'] = kategori_secimi
        bot.send_message(message.chat.id, f"{kategori_secimi} kategorisini seçtiniz. İlk soruya geçelim.")
        yeni_soru_gonder(message)

def yeni_soru_gonder(message):
    user_id = message.from_user.id
    kategori = oyuncular[user_id]['kategori']
    
    filtrelenmis_sorular = [s for s in tum_sorular if s['kategori'] == kategori]
    
    if filtrelenmis_sorular:
        soru = random.choice(filtrelenmis_sorular)
        oyuncular[user_id]['soru'] = soru
        bot.send_message(message.chat.id, f"🧠 Soru: {soru['soru']}")
    else:
        bot.send_message(message.chat.id, f"❌ {kategori} kategorisinde soru bulunmamaktadır.")

@bot.message_handler(commands=['puan'])
def puan_goster(message):
    user_id = message.from_user.id
    puan = oyuncular.get(user_id, {}).get('puan', 0)
    bot.send_message(message.chat.id, f"🎯 Şu anki puanın: {puan}")

@bot.message_handler(func=lambda m: True)
def cevap_kontrol(message):
    user_id = message.from_user.id
    if user_id in oyuncular and 'soru' in oyuncular[user_id]:
        verilen = message.text.strip().lower()
        dogru = oyuncular[user_id]['soru']['cevap'].lower()
        if verilen == dogru:
            oyuncular[user_id]['puan'] += 1
            bot.send_message(message.chat.id, f"✅ Doğru! Puanın: {oyuncular[user_id]['puan']}")
        else:
            bot.send_message(message.chat.id, f"❌ Yanlış! Doğru cevap: {dogru}")
        yeni_soru_gonder(message)

@bot.message_handler(commands=['bitir'])
def oyunu_bitir(message):
    user_id = message.from_user.id
    if user_id in oyuncular:
        del oyuncular[user_id]  # Kullanıcı verisi temizlenir
        bot.send_message(message.chat.id, "🛑 Oyun sona erdi. Tekrar oynamak istersen /basla yazman yeterli!")
    else:
        bot.send_message(message.chat.id, "❗ Zaten aktif bir oyununuz yok.")



bot.polling()

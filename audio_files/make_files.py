from gtts import gTTS

dice_1_text = "You rolled a one. That sucks..."
dice_2_text = "You rolled a two. That sucks slightly less..."
dice_3_text = "You rolled a three. Okay, halfway there..."
dice_4_text = "You rolled a four. Not bad..."
dice_5_text = "You rolled a five. So close..."
dice_6_text = "You rolled a six. Lucky..."

language = "en"

dice_1 = gTTS(text=dice_1_text, lang=language, slow=False)
dice_2 = gTTS(text=dice_2_text, lang=language, slow=False)
dice_3 = gTTS(text=dice_3_text, lang=language, slow=False)
dice_4 = gTTS(text=dice_4_text, lang=language, slow=False)
dice_5 = gTTS(text=dice_5_text, lang=language, slow=False)
dice_6 = gTTS(text=dice_6_text, lang=language, slow=False)

dice_1.save("dice_1.mp3")
dice_2.save("dice_2.mp3")
dice_3.save("dice_3.mp3")
dice_4.save("dice_4.mp3")
dice_5.save("dice_5.mp3")
dice_6.save("dice_6.mp3")
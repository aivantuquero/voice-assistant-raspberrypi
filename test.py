text = "small letter"

text = text.upper()

print(text)


# # Define your message
# message = "My doggy is super smart. He knows how to sit, stay, and shake. I love him so much"

# # Create a TextBlob object
# blob = TextBlob(message)

# # Analyze sentiment
# sentiment_score = blob.sentiment.polarity

# # Categorize the sentiment based on the polarity score
# if sentiment_score > 0.2:
#     tone = "happy"
# elif sentiment_score < -0.2:
#     tone = "sad"
# else:
#     tone = "neutral or other"

# # Print the result
# print(f"The tone of the message is {tone}")




# nlp = spacy.load("en_core_web_sm")

# txt = "What is the price for LINGMEI RACKET?"

# doc = nlp(txt)

# # Print the entities in the doc
# for ent in doc.ents:
#     print(ent.text, ent.label_)

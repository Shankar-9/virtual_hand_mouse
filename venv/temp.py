import textstat
text = "This is a sample text for readability analysis."
flesch_score = textstat.flesch_reading_ease(text)
print("Flesch Reading Ease Score:", flesch_score)

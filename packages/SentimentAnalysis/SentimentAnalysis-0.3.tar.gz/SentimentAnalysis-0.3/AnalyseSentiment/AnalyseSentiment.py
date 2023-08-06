from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class AnalyseSentiment:
    def __init__(self, sentence):
        self.sentence = str(sentence).replace("please ","")
        self.sentence = str(sentence).replace("pls ","")
        self.sentence = str(sentence).replace("plz ","")
        self.sentence = str(sentence).replace("pl ","")

    
    def Analyse(self):
        sentiment = {
            "sentence":self.sentence,
            "overall_sentiment":"",
            "overall_sentiment_score":0.00,
            "scores":[]
        }
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(self.sentence)
        if sentiment_dict['compound'] >= 0.05:
            sentiment["overall_sentiment"] = "Positive"
            sentiment["overall_sentiment_score"] = sentiment_dict['compound']
            sentiment["scores"].append({"positive":sentiment_dict['pos'], "negative":sentiment_dict['neg'],"neutral":sentiment_dict['neu']})
        elif sentiment_dict['compound'] <= - 0.05:
            sentiment["overall_sentiment"] = "Negative"
            sentiment["overall_sentiment_score"] = sentiment_dict['compound']
            sentiment["scores"].append({"positive":sentiment_dict['pos'], "negative":sentiment_dict['neg'],"neutral":sentiment_dict['neu']})
        else:
            sentiment["overall_sentiment"] = "Neutral"
            sentiment["overall_sentiment_score"] = sentiment_dict['compound']
            sentiment["scores"].append({"positive":sentiment_dict['pos'], "negative":sentiment_dict['neg'],"neutral":sentiment_dict['neu']})
        return sentiment

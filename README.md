Hillary Clinton's Email Viewer

Uses Artificial Intelligence to both cluster Hillary Clinton's emails into relevant groups and a sentiment (happy/sad) classifier for each individual email.

Displays a "Meme" for each email corresponding with the AI's perceived sentiment. A random happy photo is displayed for any email with a positive predicted sentiment, and a sad one any email with a negative predicted sentiment.

Machine generated clusters make it easy to view the thousands of leaked emails by filtering emails in terms of similarity.

Algorithms:
	Clustering (KMeans)
	Sentiment Analysis (SVC)


Setup Instructions:
sudo chmod +x ./setup.sh
sudo ./setup.sh

Made during Fall '15 UH CodeRED

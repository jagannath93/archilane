#!/bin/bash
cd /home/archilane/webapps/projects/archilane/archifeed/xml_files
#cd /home/vjag/channel-i/news_feeds/xml_files

wget "http://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=w&output=rss";

#The Hindu
wget "http://www.thehindu.com/news/international/?service=rss";
wget "http://www.thehindu.com/news/national/?service=rss";
wget "http://www.thehindu.com/sport/?service=rss";
wget "http://www.thehindu.com/features/?service=rss";

mv "news?pz=1&cf=all&ned=in&hl=en&topic=w&output=rss" google_int.xml

mv "index.html?service=rss" hindu_int.xml
mv "index.html?service=rss.1" hindu_nat.xml
mv "index.html?service=rss.2" hindu_sports.xml
mv "index.html?service=rss.3" hindu_entertainment.xml


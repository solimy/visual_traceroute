# visual_traceroute
Simple python script to render traceroute output inside google map.

# setup

- install python 3.8 or later version.
- sign up into https://ipstack.com/ and get your api key.
- create a google api key and enable google map js api.
    - https://developers.google.com/maps/documentation/javascript/get-api-key
    - https://console.cloud.google.com/apis/library/maps-backend.googleapis.com?q=Google%20Maps%20JavaScript%20API
- install traceroute.
- pip install -r requirements.txt.

# Traceroute results

To view the results, simply open the traceroute.html (generated by traceroute.py) in your browser.

# Run

<code>
$>export IPSTACK_KEY='your ipstack api key'
<br/>
$>export GMPLOT_KEY='your google api key'
<br/>
</code>
<br/>
<code>
$>python traceroute.py host
<br/>
</code>
<br/>
<code>
$>traceroute host | python traceroute.py
<br/>
</code>
<br/>
<code>
$>traceroute host > route.txt
<br/>
$>python traceroute.py < route.txt
<br/>
</code>
<br/>


# Traceroute results

To view the results, simply open the traceroute.html (generated by traceroute.py) in your browser.

***Warning : do not share your traceroute.html, as the google api key is hardcoded inside it by gmplot.***

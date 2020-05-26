var reqURL = "https://api.rss2json.com/v1/api.json?rss_url=" + encodeURIComponent("https://www.youtube.com/feeds/videos.xml?channel_id=");
var channelID = 'UCrhdp1UfyUQG7GYJSF7xUVQ';
var apiKey = 'AIzaSyDchLsIgc903isuUh9BnVHMyAJE7CwK8i0';

function loadVideo(iframe) {
  $.getJSON(reqURL + iframe.getAttribute('cid'),
    function(data) {
      var videoNumber = (iframe.getAttribute('vnum') ? Number(iframe.getAttribute('vnum')) : 0);
      console.log(videoNumber);
      var link = data.items[videoNumber].link;
      id = link.substr(link.indexOf("=") + 1);
      iframe.setAttribute("src", "https://youtube.com/embed/" + id + "?controls=0&autoplay=0");

      var url = 'https://www.youtube.com/channel/' + channelID_tuttle;
      $.getJSON('https://www.googleapis.com/youtube/v3/videos?id=' + id + '&key=' + apiKey_tuttle + '&fields=items(snippet(title))&part=snippet', {format: 'json', url: url}, function (data) {
        var h2s = $("h4")
        console.log(data.items)
        $(h2s[videoNumber]).html(data.items[0].snippet.title)

      });
    }
  );
}

var iframes = document.getElementsByClassName('latestVideoEmbed');
for (var i = 0, len = iframes.length; i < len; i++) {
  loadVideo(iframes[i]);
}

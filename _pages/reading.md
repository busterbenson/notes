---
title: "Reading"
layout: fullscreen
---

{% assign cards = site.data.tarot.cards %}

<script>
	function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
	}
	
	console.log(findGetParameter('card1'));
	console.log(findGetParameter('card2'));
	console.log(findGetParameter('card3'));
</script>
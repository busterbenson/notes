---
title: "Daily Card"
layout: fullscreen
---

{% assign cards = site.data.tarot.cards %}

<script>
function goto_random_card() {
  var cards = [{% for c in cards  %}'{{c}}',{% endfor %}];
  var random_card = cards[Math.floor(Math.random() * cards.length)];
  window.location.href = "/tarot/"+random_card;
}
goto_random_card();
</script>
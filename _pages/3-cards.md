---
title: "3 Cards"
layout: fullscreen
---

{% assign cards = site.data.tarot.cards %}

<script>
function get_three_cards() {
  var cards = [{% for c in cards  %}'{{c}}',{% endfor %}];
  var three_indexes_hash = {};
  var three_indexes_array = [];
  while (three_indexes_array.length < 3) {
    var random_index = Math.floor(Math.random() * cards.length);
    if (three_indexes_hash[random_index] == null) {
      three_indexes_array.push(cards[random_index]);
      three_indexes_hash[cards[random_index]] = 1;
    }
  }
  window.location.href = "/reading?card1="+three_indexes_array[0]+'&card2='+three_indexes_array[1]+'&card3='+three_indexes_array[2];
}
get_three_cards();
</script>
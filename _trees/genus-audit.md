# California Tree Genus Classification Audit

## Summary of Current Issues

1. **Duplicate Genus Assignment**: Blue Oak (Quercus douglasii) is currently assigned to both:
   - White Oak genus (fagaceae.white-oak.yml)
   - Black Oak genus (fagaceae.black-oak.yml)

2. **Incomplete Genus Assignments**: We have 165 unique trees but only 30 trees are explicitly included in genus profiles. The remaining 135 trees need proper genus assignments.

## Genus Classification Summary

Each tree species should be assigned to exactly one genus file. Below is a proposed organization of all trees by genus.

### Trees With Existing Genus Files

#### 1. White Oak Genus (fagaceae.white-oak.yml)
- Valley Oak (Quercus lobata)
- Oregon White Oak (Quercus garryana)
- Blue Oak (Quercus douglasii)
- Engelmann Oak (Quercus engelmannii)
- Cork Oak (Quercus suber)

#### 2. Black Oak Genus (fagaceae.black-oak.yml)
- California Black Oak (Quercus kelloggii)
- Scrub Oak (Quercus berberidifolia)

#### 3. Live Oak Genus (fagaceae.live-oak.yml)
- Coast Live Oak (Quercus agrifolia)
- Canyon Live Oak (Quercus chrysolepis)
- Interior Live Oak (Quercus wislizeni)

#### 4. Cypress Genus (cupressaceae.cypress.yml)
- Monterey Cypress (Cupressus macrocarpa)
- Arizona Cypress (Cupressus arizonica)
- Italian Cypress (Cupressus sempervirens)

#### 5. Cedar Genus (cupressaceae.cedar.yml)
- Alaska Cedar (Callitropsis nootkatensis)
- Incense Cedar (Calocedrus decurrens)
- Atlantic White Cedar (Chamaecyparis thyoides)
- Western Redcedar (Thuja plicata)
- Port Orford Cedar (Chamaecyparis lawsoniana)
- Northern White Cedar (Thuja occidentalis)
- Japanese Cedar (Cryptomeria japonica)
- Eastern Redcedar (Juniperus virginiana)

#### 6. Pine Genus (pinaceae.pine.yml)
- Ponderosa Pine (Pinus ponderosa)
- Jeffrey Pine (Pinus jeffreyi)
- Sugar Pine (Pinus lambertiana)
- Torrey Pine (Pinus torreyana)
- Bishop Pine (Pinus muricata)
- Gray Pine (Pinus sabiniana)
- Knobcone Pine (Pinus attenuata)
- Lodgepole Pine (Pinus contorta)
- Monterey Pine (Pinus radiata)
- Western White Pine (Pinus monticola)
- Spruce Pine (Pinus glabra)

#### 7. Fir Genus (pinaceae.fir.yml)
- California Red Fir (Abies magnifica)
- California White Fir (Abies concolor)
- Grand Fir (Abies grandis)
- Noble Fir (Abies procera)
- Pacific Silver Fir (Abies amabilis)
- Subalpine Fir (Abies lasiocarpa)
- Bristlecone Fir (Abies bracteata)
- Balsam Fir (Abies balsamea)
- Caucasian Fir (Abies nordmanniana)
- European Silver Fir (Abies alba)
- Fraser Fir (Abies fraseri)
- Nikko Fir (Abies homolepis)

#### 8. Spruce Genus (pinaceae.spruce.yml)
- Sitka Spruce (Picea sitchensis)
- Brewer Spruce (Picea breweriana)
- Engelmann Spruce (Picea engelmannii)
- Black Spruce (Picea mariana)
- Blue Spruce (Picea pungens)
- Norway Spruce (Picea abies)
- Oriental Spruce (Picea orientalis)
- Red Spruce (Picea rubens)
- Serbian Spruce (Picea omorika)
- White Spruce (Picea glauca)

#### 9. Hemlock Genus (pinaceae.hemlock.yml)
- Western Hemlock (Tsuga heterophylla)
- Mountain Hemlock (Tsuga mertensiana)

#### 10. Maple Genus (sapindaceae.maple.yml)
- Bigleaf Maple (Acer macrophyllum)
- Canyon Maple (Acer grandidentatum)
- Rocky Mountain Maple (Acer glabrum)
- Vine Maple (Acer circinatum)
- Red Maple (Acer rubrum)
- Silver Maple (Acer saccharinum)
- Norway Maple (Acer platanoides)
- Japanese Maple (Acer palmatum)
- Sycamore Maple (Acer pseudoplatanus)
- Black Maple (Acer nigrum)
- Amur Maple (Acer ginnala)
- Chalk Maple (Acer leucoderme)
- Fullmoon Maple (Acer japonicum)
- Hedge Maple (Acer campestre)
- Mountain Maple (Acer spicatum)
- Paperbark Maple (Acer griseum)
- Shantung Maple (Acer truncatum)
- Striped Maple (Acer pensylvanicum)
- Tatarian Maple (Acer tataricum)
- Trident Maple (Acer buergerianum)

#### 11. Birch Genus (betulaceae.birch.yml)
- Paper Birch (Betula papyrifera)
- River Birch (Betula nigra)
- Water Birch (Betula occidentalis)
- Downy Birch (Betula pubescens)
- Gray Birch (Betula populifolia)
- Heartleaf Birch (Betula cordifolia)
- Kenai Birch (Betula kenaica)
- Manchurian Birch (Betula platyphylla)
- Murrays Birch (Betula murrayana)
- Resin Birch (Betula neoalaskana)
- Sweet Birch (Betula lenta)
- Virginia Birch (Betula uber)
- Yellow Birch (Betula alleghaniensis)

#### 12. Aspen Genus (salicaceae.aspen.yml)
- Quaking Aspen (Populus tremuloides)
- Bigtooth Aspen (Populus grandidentata)
- European Aspen (Populus tremula)
- Fremont Cottonwood (Populus fremontii)
- Balm of Gilead Poplar (Populus × jackii)
- Balsam Poplar (Populus balsamifera)
- White Poplar (Populus alba)

#### 13. Walnut Genus (juglandaceae.walnut.yml)
- California Black Walnut (Juglans californica)
- Northern California Walnut (Juglans hindsii)

#### 14. Ash Genus (oleaceae.ash.yml)
- Oregon Ash (Fraxinus latifolia)
- Olive (Olea europaea)

#### 15. Locust Genus (fabaceae.locust.yml)
- Black Locust (Robinia pseudoacacia)
- New Mexico Locust (Robinia neomexicana)
- Bristly Locust (Robinia hispida)
- Clammy Locust (Robinia viscosa)
- Honeylocust (Gleditsia triacanthos)
- Waterlocust (Gleditsia aquatica)

#### 16. Madrone Genus (ericaceae.madrone.yml)
- Pacific Madrone (Arbutus menziesii)
- Strawberry Tree (Arbutus unedo)

#### 17. Redbud Genus (fabaceae.redbud.yml)
- California Redbud (Cercis occidentalis)

#### 18. Eucalyptus Genus (myrtaceae.eucalyptus.yml)
- Blue Gum Eucalyptus (Eucalyptus globulus)
- Red Gum Eucalyptus (Eucalyptus camaldulensis)
- Silver Dollar Gum (Eucalyptus polyanthemos)

#### 19. Sycamore Genus (platanaceae.sycamore.yml)
- California Sycamore (Platanus racemosa)
- London Plane Tree (Platanus × acerifolia)

### Trees Needing New Genus Files

#### 20. True Cedar Genus (pinaceae.true-cedar.yml) - New
- Atlas Cedar (Cedrus atlantica)
- Deodar Cedar (Cedrus deodara)
- Lebanon Cedar (Cedrus libani)

#### 21. Douglas-fir Genus (pinaceae.douglas-fir.yml) - New
- Coast Douglas-fir (Pseudotsuga menziesii var. menziesii)
- Rocky Mountain Douglas-fir (Pseudotsuga menziesii var. glauca)
- Bigcone Douglas-fir (Pseudotsuga macrocarpa)

#### 22. Redwood Genus (cupressaceae.redwood.yml) - New
- Coast Redwood (Sequoia sempervirens)
- Giant Sequoia (Sequoiadendron giganteum)
- Dawn Redwood (Metasequoia glyptostroboides)

#### 23. Juniper Genus (cupressaceae.juniper.yml) - New
- Western Juniper (Juniperus occidentalis)
- Eastern Redcedar (Juniperus virginiana)

#### 24. Alder Genus (betulaceae.alder.yml) - New
- Red Alder (Alnus rubra)
- White Alder (Alnus rhombifolia)
- Arizona Alder (Alnus oblongifolia)
- European Alder (Alnus glutinosa)
- Green Alder (Alnus viridis)
- Italian Alder (Alnus cordata)
- Seaside Alder (Alnus maritima)
- Smooth Alder (Alnus serrulata)
- Speckled Alder (Alnus incana)
- Thinleaf Speckled Alder (Alnus incana ssp. tenuifolia)

#### 25. Elm Genus (ulmaceae.elm.yml) - New
- American Elm (Ulmus americana)
- Cedar Elm (Ulmus crassifolia)
- Chinese Elm (Ulmus parvifolia)
- Dutch Elm (Ulmus × hollandica)
- September Elm (Ulmus serotina)
- Siberian Elm (Ulmus pumila)
- Slippery Elm (Ulmus rubra)
- Water Elm (Planera aquatica)
- Winged Elm (Ulmus alata)
- Wych Elm (Ulmus glabra)

#### 26. Buckeye Genus (sapindaceae.buckeye.yml) - New
- California Buckeye (Aesculus californica)
- Western Soapberry (Sapindus saponaria var. drummondii)

#### 27. Palm Genus (arecaceae.palm.yml) - New
- California Fan Palm (Washingtonia filifera)

#### 28. Beech Genus (fagaceae.beech.yml) - New
- American Beech (Fagus grandifolia)
- European Beech (Fagus sylvatica)
- Tanoak (Notholithocarpus densiflorus)

#### 29. Rosaceae Genera - New
- Bradford Pear (Pyrus calleryana) - rosaceae.pear.yml
- Purple Leaf Plum (Prunus cerasifera) - rosaceae.plum.yml
- Western Serviceberry (Amelanchier alnifolia) - rosaceae.serviceberry.yml
- Alder Whitebeam (Sorbus intermedia) - rosaceae.whitebeam.yml
- Alderleaf Cercocarpus (Cercocarpus montanus) - rosaceae.cercocarpus.yml

#### 30. Miscellaneous Genera - New
- Pacific Dogwood (Cornus nuttallii) - cornaceae.dogwood.yml
- California Laurel (Umbellularia californica) - lauraceae.laurel.yml
- Pacific Bayberry (Morella californica) - myricaceae.bayberry.yml
- Chinese Pistache (Pistacia chinensis) - anacardiaceae.pistache.yml
- Pacific Yew (Taxus brevifolia) - taxaceae.yew.yml
- California Torreya (Torreya californica) - taxaceae.torreya.yml
- Joshua Tree (Yucca brevifolia) - asparagaceae.yucca.yml
- Crape Myrtle (Lagerstroemia indica) - lythraceae.crape-myrtle.yml
- Southern Magnolia (Magnolia grandiflora) - magnoliaceae.magnolia.yml
- Ginkgo (Ginkgo biloba) - ginkgoaceae.ginkgo.yml
- American Basswood (Tilia americana) - malvaceae.basswood.yml
- Sweet Gum (Liquidambar styraciflua) - altingiaceae.sweet-gum.yml
- Brisbane Box (Lophostemon confertus) - myrtaceae.lophostemon.yml
- Birchleaf False Buckthorn (Frangula californica) - rhamnaceae.buckthorn.yml
- Desert Willow (Chilopsis linearis) - bignoniaceae.desert-willow.yml
- Jacaranda (Jacaranda mimosifolia) - bignoniaceae.jacaranda.yml
- Palo Verde (Parkinsonia species) - fabaceae.palo-verde.yml

## Next Steps

1. **Fix Blue Oak Duplication**: Remove the Blue Oak entry from the Black Oak genus file, keeping it only in the White Oak genus file.

2. **Create Missing Genus Files**: Based on the above classification, create the additional genus files needed to properly categorize all tree species.

3. **Update tree-tracking.md**: Update the tracking file to reflect the correct number of trees in each genus.
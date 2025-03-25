#\!/bin/bash

# Define the cosmologies and their taglines
declare -A cosmologies
cosmologies["Flat Earth Conspiracy"]="Rejecting globe model as institutional deception"
cosmologies["Gnosticism/Esoteric Dualism"]="Material world conceals higher spiritual reality"
cosmologies["Indigenous Relational Worldview"]="Reality as living web of reciprocal relationships"
cosmologies["Information-Theoretic Cosmology"]="Information as ultimate building block of reality"
cosmologies["Islamic Philosophical Cosmology"]="Universe continuously renewed through divine will"
cosmologies["Jain Cosmology"]="Multiple perspectives reveal complementary truths about reality"
cosmologies["Multiverse Theory"]="Our universe among many in larger structure"
cosmologies["New Age Spiritualism"]="Personal engagement with metaphysical energies and consciousness"
cosmologies["Non-Dual Traditions"]="Reality transcends subject-object division and conceptual thinking"
cosmologies["Panentheism"]="Divine both permeates and transcends the universe"
cosmologies["Pantheism"]="Universe itself is sacred and divine"
cosmologies["Polytheism"]="Multiple gods with distinct domains and personalities"
cosmologies["Scientific Materialism"]="Physical processes alone explain all phenomena"
cosmologies["Simulation Hypothesis"]="Reality as programmed environment created by advanced beings"
cosmologies["Spiritual Naturalism"]="Finding meaning within natural processes without supernatural elements"
cosmologies["Theistic Evolution"]="God creates through evolutionary processes"
cosmologies["Traditional African Cosmologies"]="Visible and invisible realms constantly interact"
cosmologies["Traditional Daoist Cosmology"]="Reality emerges spontaneously from primordial emptiness"
cosmologies["Unconventional Skeptic"]="Questioning mainstream narratives while exploring alternatives"
cosmologies["Young Earth Creationism"]="Earth created recently according to literal scripture"

echo "This script would update headers for the following cosmologies:"
for cosmology in "${\!cosmologies[@]}"; do
    tagline="${cosmologies[$cosmology]}"
    echo "$cosmology: $tagline"
done

import json
import random
from pathlib import Path
from build_json_banks import make_item

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def generate_nigerian_bio101_200(rng: random.Random) -> list[dict]:
    """
    Generates 200 unique BIO 101 (1st Semester 100-Level Nigerian University / Medical Prelim) questions:
    - 75% Really Hard (150 questions)
    - 25% Medium (50 questions)
    Strictly aligned with Hilary's 6 handwritten topics + NUC CCMAS 100L 1st Semester BIO 101 curriculum:
      1. General Reproduction (30 questions)
      2. Inter-relationships of Organisms I (25 questions)
      3. Inter-relationships of Organisms II (25 questions)
      4. Elements of Ecology (35 questions)
      5. Cell Structure and Organization (35 questions)
      6. Characteristics and Classification of Living Things (25 questions)
      7. NUC 100L Additions: Cell Division, Genetics & Evolution, Bioenergetics (25 questions)
    """
    raw_questions = []

    # =========================================================================
    # TOPIC 1: GENERAL REPRODUCTION (30 Questions — Hard & Medium)
    # =========================================================================
    topic1 = [
        (
            "In angiosperm double fertilization, if a tetraploid female plant (4n = 48) is pollinated by a diploid male plant (2n = 24), what are the chromosome numbers of the resulting zygote (embryo) and primary endosperm nucleus (PEN) respectively?",
            "Zygote = 36 (3n); Primary Endosperm Nucleus = 60 (5n)",
            [
                "Zygote = 36 (3n); Primary Endosperm Nucleus = 48 (4n)",
                "Zygote = 48 (4n); Primary Endosperm Nucleus = 72 (6n)",
                "Zygote = 24 (2n); Primary Endosperm Nucleus = 36 (3n)",
            ],
            "The tetraploid female (4n = 48) produces haploid-equivalent egg cells with 2n = 24 chromosomes and two polar nuclei with 2n = 24 each. The diploid male (2n = 24) produces sperm nuclei with n = 12. Syngamy gives Zygote = 24 + 12 = 36 (3n); triple fusion gives Endosperm = 24 + 24 + 12 = 60 (5n).",
        ),
        (
            "In a flowering plant with 2n = 20 chromosomes, how many chromosomes are present in the synergid cell, antipodal cell, secondary nucleus (fused polar nuclei), and aleurone layer cell respectively?",
            "10, 10, 20, and 30",
            [
                "10, 20, 20, and 30",
                "20, 10, 10, and 20",
                "10, 10, 30, and 20",
            ],
            "With 2n = 20, n = 10. Synergids (n = 10) and antipodals (n = 10) are haploid gametophytic cells; the secondary diploid nucleus formed by fusion of two polar nuclei has 2n = 20; the aleurone layer is part of the triploid endosperm (3n = 30).",
        ),
        (
            "How many meiotic divisions are required to produce 100 mature seeds (grains) in a typical monocotyledonous plant such as wheat or maize?",
            "125 meiotic divisions",
            [
                "100 meiotic divisions",
                "200 meiotic divisions",
                "50 meiotic divisions",
            ],
            "To form 100 seeds, 100 functional megaspores (eggs) and 100 pollen grains are needed. Each megaspore mother cell meiosis yields only 1 functional egg (3 degenerate), requiring 100 meiotic divisions. Each microspore mother cell meiosis yields 4 functional pollen grains, requiring 100/4 = 25 meiotic divisions. Total = 100 + 25 = 125.",
        ),
        (
            "During sexual reproduction by conjugation in the ciliate protozoan Paramecium caudatum, how many daughter paramecia are ultimately formed from a single conjugating pair of exconjugants?",
            "8 daughter individuals (4 from each exconjugant)",
            [
                "2 daughter individuals",
                "4 daughter individuals",
                "16 daughter individuals",
            ],
            "After reciprocal exchange and fusion of migratory and stationary pronuclei to form a synkaryon in each conjugant, each of the 2 exconjugants undergoes two successive post-conjugation fissions to produce 4 daughter paramecia (2 × 4 = 8 total).",
        ),
        (
            "Distinguish between scalariform conjugation and lateral conjugation in the filamentous green alga Spirogyra:",
            "Scalariform conjugation involves two different filaments aligned side-by-side (dioecious/heterothallic), whereas lateral conjugation occurs between adjacent cells of the SAME filament",
            [
                "Scalariform conjugation occurs within a single cell, whereas lateral conjugation involves zoospores",
                "Scalariform conjugation is asexual, whereas lateral conjugation is sexual",
                "Lateral conjugation forms a diploid zygospore, whereas scalariform conjugation forms a haploid aplanospore",
            ],
            "In scalariform (ladder-like) conjugation, conjugation tubes form between cells of two parallel filaments; in lateral conjugation, gametes fuse between two adjacent cells on the same filament.",
        ),
        (
            "Which mode of reproduction involves the development of an unfertilized female gamete (ovum) into a new individual, as seen in honeybee drones (Apis mellifera) and rotifers?",
            "Parthenogenesis (specifically arrhenotoky when haploid males are produced)",
            [
                "Paedogenesis",
                "Polyembryony",
                "Amphimixis",
            ],
            "Parthenogenesis is the development of an embryo from an unfertilized egg. In honeybees, unfertilized eggs develop by arrhenotokous parthenogenesis into haploid (n = 16) male drones.",
        ),
        (
            "In the alternation of generations across the plant kingdom, moving from Bryophytes to Pteridophytes to Gymnosperms and Angiosperms, what is the evolutionary trend?",
            "Progressive reduction of the haploid gametophyte generation and increasing dominance and independence of the diploid sporophyte",
            [
                "Progressive reduction of the diploid sporophyte and increasing dominance of the haploid gametophyte",
                "Transition from oogamy to isogamy",
                "Complete loss of meiosis in seed plants",
            ],
            "In Bryophytes, the haploid gametophyte is dominant and photosynthetic; in Pteridophytes and Spermatophytes, the diploid sporophyte is dominant while the gametophyte becomes microscopic and nutritionally dependent on the sporophyte.",
        ),
        (
            "Why is the sporophyte (capsule and seta) of a moss (Funaria) considered a 'partial parasite' on the gametophyte?",
            "Although its capsule contains chloroplasts and can photosynthesize partially, it depends entirely on the leafy gametophyte for water, mineral salts, and anchorage via the haustorial foot",
            [
                "It lacks any chlorophyll at all stages of development",
                "It kills the gametophyte immediately upon fertilization",
                "It is haploid whereas the gametophyte is diploid",
            ],
            "In mosses (Funaria), the diploid sporophyte remains attached to the female gametophyte (archegoniophore) by its foot, drawing water and minerals while conducting limited photosynthesis in the apophysis/capsule wall.",
        ),
        (
            "Multiple fission (schizogony) in Plasmodium falciparum within human hepatocytes and erythrocytes differs from binary fission in Amoeba proteus because in schizogony:",
            "The nucleus divides repeatedly by mitosis to form a multinucleate schizont before cytokinesis cleaves the cytoplasm into numerous merozoites simultaneously",
            [
                "Cytokinesis precedes karyokinesis at every division",
                "Meiosis occurs immediately to form haploid sporozoites",
                "Only two unequal daughter cells are formed as buds",
            ],
            "In schizogony (multiple fission), repeated karyokinesis occurs without immediate cytokinesis, producing a multinucleate schizont that subsequently segments into many merozoites at once.",
        ),
        (
            "Which of the following pairs correctly matches a modified vegetative reproductive structure with its botanical classification and example?",
            "Corm — vertically growing condensed underground stem with scale leaves (e.g., Colocasia / cocoyam and Gladiolus)",
            [
                "Rhizome — swollen underground root bearing adventitious buds (e.g., Zingiber / ginger)",
                "Stem tuber — modified subterranean storage root with eyes (e.g., Ipomoea batatas / sweet potato)",
                "Bulb — horizontally creeping aerial stolon (e.g., Allium cepa / onion)",
            ],
            "A corm (cocoyam) is a short, vertical, swollen underground stem. Ginger is a rhizome (underground stem, not root), sweet potato is a root tuber (whereas Irish potato is a stem tuber), and onion is a tunicated bulb.",
        ),
        (
            "In artificial vegetative propagation by grafting, why can grafting only be successfully performed in dicotyledonous plants and gymnosperms, but NOT in monocotyledonous plants?",
            "Monocot stems have scattered closed vascular bundles lacking a vascular cambium, which is essential for callus formation and vascular union between stock and scion",
            [
                "Monocots lack phloem sieve tubes required for sugar transport",
                "Monocot stems lack an epidermis",
                "Dicots lack xylem vessels in their rootstock",
            ],
            "Successful grafting requires the alignment and meristematic division of the vascular cambium of the stock and scion to unite their xylem and phloem; monocots have closed collateral bundles without cambium.",
        ),
        (
            "In the life cycle of a homosporous fern (e.g., Dryopteris), what is the prothallus and what is its ploidy?",
            "A free-living, heart-shaped, photosynthetic, monoecious haploid (n) gametophyte bearing both antheridia and archegonia",
            [
                "A parasitic diploid (2n) sporophyte attached to the rhizome",
                "A triploid (3n) nutritive tissue inside the sporangium",
                "A dormant asexual gemma produced on the frond margin",
            ],
            "When a haploid fern spore germinates, it forms the prothallus — an independent, autotrophic, heart-shaped haploid (n) gametophyte bearing rhizoids, antheridia, and archegonia on its ventral surface.",
        ),
        (
            "Chemotactic movement of multiflagellate fern antherozoids (sperm) toward the neck of the archegonium during fertilization is stimulated by:",
            "Malic acid (or malate ions) secreted by the mucilaginous neck canal cells of the mature archegonium",
            [
                "Sucrose solution secreted by the indusium",
                "Gibberellic acid released by the annulus",
                "Calcium carbonate crystals in the soil water",
            ],
            "In ferns (Dryopteris), disintegrating neck canal and ventral canal cells of the archegonium exude malic acid, which acts as a positive chemotactic stimulus guiding antherozoids to the egg.",
        ),
        (
            "In human gametogenesis, starting from 20 primary spermatocytes and 20 primary oocytes that complete meiosis, how many functional spermatozoa and functional ova (ootids) are produced?",
            "80 functional spermatozoa and 20 functional ova (plus polar bodies)",
            [
                "80 functional spermatozoa and 80 functional ova",
                "40 functional spermatozoa and 20 functional ova",
                "20 functional spermatozoa and 20 functional ova",
            ],
            "Each primary spermatocyte (2n) undergoes meiosis to yield 4 functional haploid spermatozoa (20 × 4 = 80). Each primary oocyte (2n) undergoes unequal cytokinesis to yield only 1 functional ovum and 2–3 non-functional polar bodies (20 × 1 = 20).",
        ),
        (
            "What is the fundamental reproductive difference between ovoviviparity (e.g., some sharks and vipers) and true eutherian viviparity (e.g., placental mammals)?",
            "In ovoviviparity, embryos develop inside eggs retained within the mother's reproductive tract and are nourished solely by egg yolk without a placental connection to maternal blood",
            [
                "In ovoviviparity, fertilization is external in water",
                "In ovoviviparity, eggs are laid in a nest and incubated by solar heat",
                "In true viviparity, the embryo receives zero nutrients from the mother",
            ],
            "Ovoviviparous animals retain shelled/membranous eggs internally until hatching, but the embryo relies strictly on lecithotrophic (yolk) nutrition rather than matrotrophic placental exchange.",
        ),
        (
            "Apomixis (agamospermy) in flowering plants such as Citrus and Taraxacum (dandelion) is best defined as:",
            "The formation of viable seeds without meiosis and syngamy (fertilization), producing progeny genetically identical to the maternal plant",
            [
                "The development of seedless fruits without pollination",
                "Cross-pollination between two different species",
                "The fusion of two male gametes with the antipodal cells",
            ],
            "Apomixis mimics sexual seed production but bypasses reduction division (meiosis) and fertilization, yielding clonal seeds. (Seedless fruit formation without fertilization is parthenocarpy).",
        ),
        (
            "Which mechanism prevents self-pollination (autogamy) by ensuring that the anthers and stigma of a bisexual flower mature at different times?",
            "Dichogamy (protandry when anthers mature first; protogyny when stigma matures first)",
            [
                "Cleistogamy",
                "Herkogamy",
                "Homogamy",
            ],
            "Dichogamy is temporal separation of male and female maturity in bisexual flowers (protandry in sunflower/maize; protogyny in Mirabilis/magnolia). Herkogamy is spatial/physical barrier; cleistogamy forces self-pollination in closed flowers.",
        ),
        (
            "In Bryophyllum (Kalanchoe pinnata), natural vegetative propagation occurs primarily through:",
            "Epiphyllous adventitious buds located in the marginal notches of its fleshy leaves",
            [
                "Subterranean stem tubers with axillary eyes",
                "Root suckers arising from pericycle tissue",
                "Aerial bulbils formed in the inflorescence",
            ],
            "Bryophyllum leaves possess meristematic foliar notches along their margins that develop adventitious plantlets complete with roots and shoots.",
        ),
        (
            "Compare the gametes involved in isogamy, anisogamy, and oogamy:",
            "Isogamy involves morphologically identical gametes; anisogamy involves gametes of unequal size/motility; oogamy involves a large non-motile egg and a small motile sperm",
            [
                "Isogamy involves a large non-motile egg and small sperm; oogamy involves identical flagellated gametes",
                "Anisogamy occurs only in mammals, whereas oogamy occurs only in bacteria",
                "All three involve fusion of diploid somatic nuclei",
            ],
            "Evolution of sexual gametes progresses from isogamy (Chlamydomonas debaryana, Spirogyra) to anisogamy (Chlamydomonas braunii) to oogamy (Volvox, Fucus, higher plants and animals).",
        ),
        (
            "In the life cycle of Rhizopus stolonifer (black bread mould), sexual reproduction occurs by gametangial copulation between:",
            "Two morphologically similar but physiologically distinct (+ and -) multinucleate progametangia to form a thick-walled, warty diploid zygospore",
            [
                "Flagellated motile zoospores and non-motile oospheres",
                "Ascogonium and antheridium to form eight ascospores",
                "Clamp connections producing چهار basidiospores",
            ],
            "Rhizopus is heterothallic; when compatible (+) and (-) hyphae meet, multinucleate gametangia fuse (plasmogamy and karyogamy) to form a resistant resting zygospore.",
        ),
        (
            "What is 'paedogenesis' (or neoteny-associated reproduction) as exhibited by the axolotl larva of Ambystoma or gall midge larvae (Miastor)?",
            "Sexual or parthenogenetic reproduction by an organism while still in its larval or pre-adult morphological stage",
            [
                "Asexual budding in senescent adult cnidarians",
                "Regeneration of a whole organism from a severed tentacle",
                "Alternation between haploid and triploid adults",
            ],
            "Paedogenesis is the attainment of reproductive maturity and production of offspring by an individual that retains larval somatic characteristics.",
        ),
        (
            "In coelenterates such as Obelia, the alternation between a sessile asexual polyp (hydroid) colony and a free-swimming sexual medusa is termed:",
            "Metagenesis (where both polyp and medusa generations are diploid 2n)",
            [
                "True haplo-diplontic alternation of generations (where the polyp is haploid and medusa is diploid)",
                "Schizogony",
                "Parthenocarpy",
            ],
            "In Obelia, metagenesis alternates between a diploid (2n) asexual polyp stage and a diploid (2n) dioecious medusa stage; only the gametes produced by the medusa are haploid.",
        ),
        (
            "During mammalian oogenesis, at what exact stage of meiosis is the human secondary oocyte arrested at the moment of ovulation, and what triggers its completion?",
            "Arrested at Metaphase II of meiosis; triggered to complete Meiosis II only upon penetration by a spermatozoon",
            [
                "Arrested at Prophase I (diplotene); triggered by the LH surge to complete both divisions before ovulation",
                "Arrested at Anaphase I; triggered by progesterone from the corpus luteum",
                "Completely finished with Meiosis II before leaving the Graafian follicle",
            ],
            "Primary oocytes arrest in diplotene of Prophase I until puberty. The pre-ovulatory LH surge completes Meiosis I, but the secondary oocyte arrests at Metaphase II and only completes Meiosis II if fertilized.",
        ),
        (
            "What is the role of the acrosome reaction and cortical reaction during fertilization in animals?",
            "The acrosome releases hydrolytic enzymes (hyaluronidase, acrosin) to penetrate egg investments, while the cortical reaction modifies the zona pellucida/vitelline membrane to block polyspermy",
            [
                "The acrosome synthesizes ATP for tail movement, while the cortical reaction attracts more sperm",
                "Both reactions dissolve the maternal nucleus",
                "The cortical reaction fuses the two pronuclei directly",
            ],
            "Acrosomal enzymes digest the corona radiata and zona pellucida; exocytosis of cortical granules hardens the fertilization membrane (slow block to polyspermy) so only one sperm fertilizes the egg.",
        ),
        (
            "Which of the following organisms reproduces asexually by endogenous budding through specialized internal cell masses called gemmules?",
            "Freshwater sponges (e.g., Spongilla)",
            [
                "Hydra vulgaris",
                "Planaria (Dugesia)",
                "Aurelia (jellyfish)",
            ],
            "Freshwater and some marine sponges form internal buds called gemmules (containing archaeocytes surrounded by siliceous amphidisc spicules) to survive desiccation or freezing.",
        ),
        (
            "In an angiosperm ovule, the funicle, hilum, micropyle, and chalaza are arranged in specific relative positions. Which type of ovule is inverted by 180° so that the micropyle lies close to the hilum and funicle (the most common form in angiosperms)?",
            "Anatropous ovule",
            [
                "Orthotropous (atropous) ovule",
                "Campylotropous ovule",
                "Amphitropous ovule",
            ],
            "Over 80% of angiosperm families possess anatropous (inverted) ovules where the ovule body rotates 180° during development, bringing the micropyle adjacent to the hilum.",
        ),
        (
            "Why is binary fission in Euglena viridis described as 'longitudinal' whereas in Paramecium caudatum it is 'transverse'?",
            "In Euglena the cleavage furrow passes parallel to the anterior-posterior axis to duplicate the flagellar reservoir, whereas in Paramecium cleavage is perpendicular to the long axis",
            [
                "Euglena lacks a nucleus whereas Paramecium has three nuclei",
                "Euglena divides by meiosis whereas Paramecium divides by mitosis",
                "Paramecium divides inside a cyst whereas Euglena never encysts",
            ],
            "Flagellates (Euglena, Trypanosoma) undergo longitudinal binary fission along the anteroposterior axis; ciliates (Paramecium) undergo transverse (homothetogenic) binary fission across the short axis.",
        ),
        (
            "The Polygonum-type (monosporic) female gametophyte (embryo sac) in typical angiosperms at maturity consists of:",
            "7 cells and 8 haploid nuclei (1 egg cell, 2 synergids, 3 antipodal cells, and 1 central cell with 2 polar nuclei)",
            [
                "8 cells and 8 nuclei",
                "7 cells and 7 nuclei",
                "4 cells and 8 diploid nuclei",
            ],
            "Three mitotic divisions of a single functional chalazal megaspore produce 8 nuclei partitioned into 7 cells (3 at the micropylar egg apparatus, 3 chalazal antipodals, and 1 binucleate central cell).",
        ),
        (
            "What happens to the integuments, ovary wall, nucellus (when persistent), and fertilized ovule after fertilization in angiosperms?",
            "Integuments become the testa/tegmen (seed coat); ovary wall becomes the pericarp (fruit wall); persistent nucellus becomes perisperm; ovule becomes the seed",
            [
                "Integuments become the pericarp; ovary wall becomes the testa; nucellus becomes the cotyledon",
                "Ovule becomes the fruit; ovary becomes the seed; integuments degenerate completely",
                "Nucellus becomes the triploid endosperm; integuments become the plumule",
            ],
            "Post-fertilization: ovule → seed; ovary → fruit (ovary wall → pericarp); outer/inner integuments → testa and tegmen; any residual nucellus (as in black pepper/beet) → diploid perisperm.",
        ),
        (
            "Which term describes an animal species in which a single individual possesses both functional male (testes) and female (ovaries) gonads, yet still requires cross-fertilization due to anatomical separation or protandry (e.g., earthworm Lumbricus and tapeworm)?",
            "Hermaphrodite (monoecious)",
            [
                "Dioecious (gonochoristic)",
                "Parthenogenetic",
                "Viviparous",
            ],
            "Earthworms are monoecious (hermaphroditic) and protandrous; their male reproductive pores mature before the female ovaries and their relative positions necessitate reciprocal cross-insemination during copulation.",
        ),
    ]
    for q, corr, dists, exp in topic1:
        raw_questions.append((q, corr, dists, exp))

    # =========================================================================
    # TOPIC 2: INTER-RELATIONSHIPS OF ORGANISMS I — Symbiosis, Mutualism, Commensalism (25 Questions)
    # =========================================================================
    topic2 = [
        (
            "In the mutualistic root-nodule association between leguminous plants (e.g., Vigna unguiculata) and Rhizobium bacteria, what is the specific physiological role of the pink pigment 'leghaemoglobin' inside the root nodule?",
            "It acts as an oxygen scavenger (buffer) that maintains a low free-oxygen tension to prevent irreversible inactivation of the bacterial nitrogenase enzyme complex while supplying O2 for bacterial respiration",
            [
                "It directly catalyzes the reduction of N2 to NH3 using solar light energy",
                "It transports fixed nitrates upward through the xylem vessels",
                "It digests the cellulose cell wall of root hairs during infection thread formation",
            ],
            "The nitrogenase enzyme complex in Rhizobium bacteroids is extremely oxygen-labile (irreversibly denatured by free O2). Leghaemoglobin binds O2 with high affinity, keeping free O2 concentration low while delivering O2 to bacteroid respiratory chains for ATP production.",
        ),
        (
            "In a lichen thallus (a mutualistic association between a mycobiont and a photobiont/phycobiont), how are the structural and physiological roles partitioned between the two partners?",
            "The fungus (mycobiont, usually an Ascomycete) forms the bulk of the thallus, provides anchorage, absorbs water/minerals, and protects against desiccation/high light, while the alga or cyanobacterium (photobiont) performs photosynthesis (and nitrogen fixation if cyanobacterial)",
            [
                "The alga forms the cortex and rhizines for mineral absorption, while the fungus performs photosynthesis",
                "Both partners are heterotrophic and obtain carbon by decomposing rock silicates",
                "The fungus fixes atmospheric nitrogen while the green alga absorbs phosphate from the soil",
            ],
            "In lichens, the mycobiont (90% of thallus biomass) constructs the upper/lower cortex and medulla, absorbing moisture and minerals, while the phycobiont (e.g., Trebouxia or Nostoc) supplies fixed organic carbon (ribitol/erythritol/glucose).",
        ),
        (
            "Distinguish structurally and functionally between Ectotrophic (Ectomycorrhiza) and Endotrophic (Arbuscular/VAM Endomycorrhiza) mycorrhizal associations:",
            "Ectomycorrhizae form an external fungal sheath (mantle) and an intercellular Hartig net in the root cortex without penetrating host cell membranes, whereas Arbuscular Endomycorrhizae penetrate cortical cell walls to form branched haustorial arbuscules and vesicles",
            [
                "Ectomycorrhizae penetrate the xylem vessels directly, whereas Endomycorrhizae remain on the leaf surface",
                "Ectomycorrhizae are formed exclusively by bacteria, whereas Endomycorrhizae are formed by algae",
                "Endomycorrhizae destroy the root cap and kill the host plant within days",
            ],
            "Ectomycorrhizae (common in pines/oaks, Basidiomycetes) form a fungal mantle and intercellular Hartig net; Arbuscular Mycorrhizae (Glomeromycota, in >80% of vascular plants) invaginate into root cortical cells to form finely branched arbuscules for phosphate/micronutrient exchange.",
        ),
        (
            "Why do wood-eating termites (e.g., Macrotermes or Reticulitermes) starve to death if treated with mild hyperbaric oxygen or antiprotozoal agents that selectively eliminate their hindgut flagellates (Trichonympha)?",
            "The termite lacks endogenous cellulase genes adequate for complete lignocellulose breakdown and relies on obligate mutualistic hindgut protozoa (Trichonympha) to ferment cellulose into absorbable acetate",
            [
                "Trichonympha synthesizes chitin for the termite's exoskeleton",
                "The protozoa pump oxygen from the spiracles to the termite's brain",
                "Without Trichonympha, the termite cannot lay fertilized eggs",
            ],
            "Trichonympha is an obligate mutualistic hypermastigote flagellate in the termite hindgut that engulfs wood particles and digests cellulose anaerobically into short-chain fatty acids (mainly acetic acid) absorbed by the termite.",
        ),
        (
            "In ecological notation where '+' denotes net benefit, '-' denotes net harm, and '0' denotes no significant effect on fitness, which pair of interactions is represented by (+, +) and (+, 0) respectively?",
            "Mutualism (+, +) and Commensalism (+, 0)",
            [
                "Commensalism (+, +) and Amensalism (+, 0)",
                "Protocooperation (+, 0) and Parasitism (+, -)",
                "Mutualism (+, 0) and Competition (-, -)",
            ],
            "Mutualism and protocooperation confer net positive fitness to both species (+, +); commensalism benefits the commensal while leaving the host unaffected (+, 0).",
        ),
        (
            "What is the critical ecological distinction between 'obligate mutualism' (symbiosis sensu stricto) and 'protocooperation' (facultative mutualism)?",
            "In obligate mutualism, neither partner can survive or reproduce in nature without the other (e.g., fig and fig wasp), whereas in protocooperation both partners benefit when associated but can survive independently (e.g., hermit crab and sea anemone)",
            [
                "Protocooperation harms one partner during the dry season",
                "Obligate mutualism occurs only between members of the same species",
                "Protocooperation requires physical fusion of the two organisms' nuclei",
            ],
            "Protocooperation (+, +) is a non-obligatory mutually beneficial interaction (such as oxpeckers/cattle egrets and grazing mammals, or hermit crabs carrying Adamsia sea anemones) where both species can live apart.",
        ),
        (
            "The association between the remora (suckerfish, Echeneis) attached by its modified dorsal fin disc to the belly of a shark without harming the shark is a classic example of:",
            "Commensalism (specifically phoresy + trophic commensalism)",
            [
                "Ectoparasitism",
                "Obligate mutualism",
                "Amensalism",
            ],
            "The remora gains free transport (phoresy), protection, and scraps of food from the shark's meals (+), while the shark experiences negligible metabolic cost or benefit (0).",
        ),
        (
            "Tropical epiphytic orchids (e.g., Vanda) growing perched on the branches of tall rainforest canopy trees without penetrating the host's vascular tissue represent which relationship, and what specialized root tissue enables them to absorb atmospheric moisture?",
            "Commensalism (+, 0); a spongy, dead, multilayered epidermal tissue called the velamen radicum",
            [
                "Hemiparasitism (+, -); haustorial xylem bridges",
                "Mutualism (+, +); coralloid root nodules",
                "Saprophytism; fungal rhizomorphs",
            ],
            "Epiphytes use the host tree solely for physical support in the sunlit canopy (+, 0). Their aerial roots possess a dead, perforated, hygroscopic multiple epidermis called velamen that rapidly absorbs rain and mist.",
        ),
        (
            "What is 'phoresy' in inter-organismal relationships?",
            "A form of commensalism in which a smaller organism (phoront) attaches to a larger organism solely for dispersal/transport from one habitat to another without feeding on it",
            [
                "The secretion of toxic antibiotics by soil fungi to inhibit bacteria",
                "The intracellular digestion of symbiotic algae by corals",
                "Competition between two bird species for nesting cavities",
            ],
            "Phoresy is a (+, 0) commensal interaction purely for mechanical transport (e.g., pseudoscorpions or mites riding on beetles/flies, or barnacles on whale skin).",
        ),
        (
            "Coral reefs are among the most productive ecosystems on Earth despite thriving in nutrient-poor (oligotrophic) tropical waters primarily because of an endosymbiotic mutualism between:",
            "Hermatypic scleractinian coral polyps (Cnidaria) and intracellular photosynthetic dinoflagellates called zooxanthellae (Symbiodinium)",
            [
                "Calcifying red algae and nitrogen-fixing methanogenic archaea",
                "Hydrozoan medusae and chemosynthetic sulfur bacteria",
                "Hexactinellid glass sponges and planktonic diatoms",
            ],
            "Intracellular zooxanthellae (dinoflagellates) within the coral gastrodermis translocate up to 90% of their photosynthetic products (glycerol, glucose, amino acids) to the polyp and accelerate calcium carbonate (aragonite) deposition; thermal stress expels them, causing coral bleaching.",
        ),
        (
            "In ruminant herbivores (e.g., cattle, sheep, goats), which stomach chamber acts as the primary anaerobic fermentation vat housing mutualistic cellulolytic bacteria (Ruminococcus), protozoa, and methanogenic archaea?",
            "The Rumen (and Reticulum)",
            [
                "The Abomasum (true glandular stomach)",
                "The Duodenum",
                "The Caecum exclusively",
            ],
            "Foregut fermenters (ruminants) house dense populations of anaerobic microbes in the rumen and reticulum that hydrolyze β-1,4-glycosidic bonds of cellulose into volatile fatty acids (acetate, propionate, butyrate) before true gastric digestion in the abomasum.",
        ),
        (
            "The obligate coevolved pollination mutualism between Yucca plants and the female yucca moth (Tegeticula) or between Ficus (figs) and female fig wasps (Blastophaga) illustrates:",
            "Species-specific obligate mutualism where the insect actively pollinates the flower in exchange for laying eggs in a subset of the developing ovules",
            [
                "Batesian mimicry where the flower imitates a predatory wasp",
                "Interspecific competition leading to extinction of the plant",
                "Brood parasitism where the plant receives zero pollination benefit",
            ],
            "Female yucca moths and fig wasps are the sole pollinators of their respective host plants; the insect ensures seed set while sacrificing a fraction of ovules as food for its developing larvae.",
        ),
        (
            "The water fern Azolla pinnata is widely cultivated as a biofertilizer in flooded rice paddies because its leaf cavities harbor which nitrogen-fixing mutualistic partner?",
            "The heterocystous filamentous cyanobacterium Anabaena azollae",
            [
                "Free-living Azotobacter vinelandii",
                "Nitrifying Nitrobacter winogradskyi",
                "Denitrifying Pseudomonas fluorescens",
            ],
            "Azolla houses the cyanobacterium Anabaena azollae inside dorsal leaf cavities; the specialized thick-walled heterocysts of Anabaena fix atmospheric N2 into ammonia for the fern and surrounding rice crop.",
        ),
        (
            "In Cycas (a gymnosperm), specialized negatively geotropic, dichotomously branched 'coralloid roots' grow near the soil surface. What mutualistic endosymbiont resides in the cortical zone of these coralloid roots?",
            "Nitrogen-fixing cyanobacteria such as Nostoc and Anabaena",
            [
                "Cellulose-digesting basidiomycete fungi",
                "Parasitic root-knot nematodes (Meloidogyne)",
                "Chemolithotrophic iron bacteria",
            ],
            "Coralloid roots of Cycas contain a distinct bluish-green algal zone in their cortex inhabited by Nostoc or Anabaena, which fix atmospheric nitrogen into amino acids for the cycad.",
        ),
        (
            "What is 'inquilinism' as a specialized category of commensalism?",
            "An association in which one organism (the inquiline) lives permanently inside the nest, burrow, gall, or body cavity of another species without harming the host (e.g., pearlfish Carapus living inside the cloaca/respiratory tree of a sea cucumber)",
            [
                "A predator consuming its own offspring under overcrowding",
                "Two predators hunting the same prey species cooperatively",
                "A fungus digesting dead fallen timber",
            ],
            "Inquilinism (+, 0) involves sharing a home/shelter or body cavity without trophic parasitism, such as the pearlfish (Carapus) sheltering inside holothurians (sea cucumbers) or epiphytic bromeliad tank fauna.",
        ),
        (
            "Cattle egrets (Bubulcus ibis) foraging alongside grazing cattle — catching grasshoppers and frogs flushed out of the vegetation by the cattle's hooves without affecting the cattle — exemplify:",
            "Commensalism (+, 0)",
            [
                "Mutualism (+, +)",
                "Amensalism (-, 0)",
                "Intraspecific competition",
            ],
            "When cattle egrets follow grazing livestock to capture flushed insects from the grass, the egret's foraging efficiency increases (+) while the grazing mammal is unaffected (0). (By contrast, oxpeckers removing ticks from buffalo skin is protocooperation/mutualism).",
        ),
        (
            "Which term did Anton de Bary (1879) originally coin to describe ANY close, long-term physical living together of two unlike organisms (encompassing mutualism, commensalism, and parasitism)?",
            "Symbiosis",
            [
                "Synecology",
                "Synergism",
                "allelopathy",
            ],
            "De Bary defined 'symbiosis' broadly as the living together of differently named organisms in close, prolonged association, whether mutualistic (+,+), commensal (+,0), or parasitic (+,-).",
        ),
        (
            "How do human colonic microbiota (such as non-pathogenic Escherichia coli and Bacteroides) benefit their human host in a mutualistic relationship?",
            "They synthesize Vitamin K (menaquinone) and certain B-complex vitamins (biotin, folate), ferment indigestible dietary fibers into short-chain fatty acids, and competitively exclude enteric pathogens",
            [
                "They secrete pepsinogen and hydrochloric acid into the stomach lumen",
                "They synthesize essential amino acids in the jejunum and emulsify bile salts",
                "They fix atmospheric nitrogen gas in the large intestine",
            ],
            "Mutualistic gut bacteria synthesize Vitamin K (essential for prothrombin blood clotting factor synthesis) and Vitamin B12/biotin, produce butyrate for colonocytes, and prevent colonization by Clostridium difficile.",
        ),
        (
            "Ant-plants (myrmecophytes) such as Acacia cornigera (bullhorn acacia) provide hollow swollen stipular thorns (domatia) and lipid/protein-rich Beltian bodies for Pseudomyrmex ants. What do the ants provide in return?",
            "Aggressive defense against mammalian/insect herbivores and clearing of competing epiphytic vines and surrounding vegetation",
            [
                "Transfer of pollen between wind-pollinated acacia flowers",
                "Fixation of atmospheric N2 inside the hollow thorns",
                "Absorption of groundwater during drought",
            ],
            "Myrmecophily between bullhorn acacia and Pseudomyrmex ferruginea is a classic coevolved mutualism: the plant provides shelter (hollow thorns), nectar (extrafloral nectaries), and protein/lipid Beltian bodies, while the ants fiercely sting herbivores and prune competing plants.",
        ),
        (
            "Why are lichens regarded as sensitive biological indicators (bio-monitors) of atmospheric sulfur dioxide (SO2) pollution?",
            "Because lichens lack a waxy cuticle and stomata, absorbing water and dissolved gases directly across their entire thallus surface, where SO2 acidifies the photobiont cells and degrades chlorophyll a into phaeophytin",
            [
                "Because lichens thrive and multiply rapidly in high SO2 concentrations",
                "Because their deep taproots accumulate heavy metals from groundwater",
                "Because SO2 blocks the opening of their guard cells",
            ],
            "Lichens absorb rainwater and aerosols directly over their entire surface without a protective cuticle; dissolved SO2 (bisulfite/sulfurous acid) destroys the algal chlorophyll, creating 'lichen deserts' in polluted industrial cities.",
        ),
        (
            "In the green hydra (Hydra viridissima / Chlorohydra), unicellular green algae (Zoochlorella) live endosymbiotically inside the gastrodermal cells. Which statement accurately describes the metabolic exchange?",
            "Zoochlorellae supply maltose/oxygen from photosynthesis to the Hydra, while utilizing the Hydra's nitrogenous waste (ammonia) and CO2",
            [
                "The Hydra digests all the Zoochlorellae every night and ingests new ones each morning",
                "Zoochlorellae paralyze prey using nematocysts on behalf of the Hydra",
                "The association is parasitic and rapidly kills the Hydra in sunlight",
            ],
            "Endosymbiotic Zoochlorellae fix CO2 and release maltose and O2 to the host gastrodermal cells while recycling the cnidarian's metabolic CO2, NH3, and phosphate.",
        ),
        (
            "Which enzyme inside the root nodules of leguminous plants is directly responsible for cleaving the triple bond of atmospheric dinitrogen (N≡N), and what metallic cofactors are at its active site?",
            "Nitrogenase complex; containing Iron (Fe) and Molybdenum (Mo) (the FeMo-cofactor)",
            [
                "Nitrate reductase; containing Magnesium (Mg) and Copper (Cu)",
                "RuBisCO; containing Manganese (Mn) and Zinc (Zn)",
                "Urease; containing Nickel (Ni) and Cobalt (Co)",
            ],
            "The dinitrogenase component of the nitrogenase complex contains the iron-molybdenum cofactor (FeMoCo), requiring 16 ATP molecules per N2 molecule reduced: N2 + 8H+ + 8e- + 16ATP → 2NH3 + H2 + 16ADP + 16Pi.",
        ),
        (
            "The relationship between flower-visiting hummingbirds or sunbirds and ornithophilous tubular red flowers that produce copious dilute nectar is classified as:",
            "Mutualism (+, +)",
            [
                "Commensalism (+, 0)",
                "Amensalism (-, 0)",
                "Ectoparasitism (+, -)",
            ],
            "Both partners gain reproductive/energetic fitness (+, +): the bird obtains high-energy sucrose nectar, and the plant achieves cross-pollination.",
        ),
        (
            "When barnacles (Balanus) cement themselves permanently onto the shell of a scallop or the skin of a humpback whale, gaining access to plankton-rich water currents without penetrating host tissues, this interaction is:",
            "Epizoic commensalism (+, 0)",
            [
                "Endoparasitism (+, -)",
                "Saprophytism",
                "Allelopathy",
            ],
            "Epizoic barnacles live attached to the outer surface of a marine animal (epibiosis/commensalism), benefiting from water flow and transport without feeding on host tissues.",
        ),
        (
            "What is the endosymbiotic origin of eukaryotic mitochondria and chloroplasts according to Lynn Margulis's Endosymbiotic Theory?",
            "Mitochondria evolved from engulfed aerobic alpha-proteobacteria, and chloroplasts evolved from engulfed photosynthetic cyanobacteria, inside an ancestral host archaeon/proto-eukaryote",
            [
                "Both organelles evolved by inward folding (invagination) of the plasma membrane of a Gram-positive bacterium",
                "Mitochondria evolved from engulfed viruses, and chloroplasts evolved from green fungi",
                "Chloroplasts evolved first and later lost chlorophyll to become nuclei",
            ],
            "Mutualistic endosymbiosis of an aerobic alpha-proteobacterium gave rise to mitochondria, and subsequent endosymbiosis of a cyanobacterium gave rise to plastids — evidenced by their double membranes, circular histone-free DNA, 70S ribosomes, and binary fission.",
        ),
    ]
    for q, corr, dists, exp in topic2:
        raw_questions.append((q, corr, dists, exp))

    # =========================================================================
    # TOPIC 3: INTER-RELATIONSHIPS OF ORGANISMS II — Parasitism, Predation, Competition, Amensalism (25 Questions)
    # =========================================================================
    topic3 = [
        (
            "Compare the parasitic nutritional strategies of Viscum album (mistletoe) and Cuscuta reflexa (dodder / witchweed):",
            "Mistletoe is a chlorophyllous STEM HEMIPARASITE that taps only the host's xylem for water and minerals, whereas Dodder (Cuscuta) is an achlorophyllous STEM HOLOPARASITE that taps both host xylem and phloem via haustoria",
            [
                "Mistletoe is a root holoparasite lacking chlorophyll, whereas Dodder is an autotrophic epiphyte",
                "Both Mistletoe and Dodder are saprophytes that grow only on dead logs",
                "Mistletoe taps only host phloem, whereas Dodder fixes its own carbon by C4 photosynthesis",
            ],
            "Hemiparasites (mistletoe, Loranthus) possess green leaves and photosynthesize but extract water/minerals from host xylem; holoparasites (Cuscuta on stems, Rafflesia and Orobanche on roots) lack chlorophyll and depend totally on host xylem and phloem.",
        ),
        (
            "Striga hermonthica (purple witchweed), a devastating parasitic weed of cereal crops (maize, sorghum, millet) in Nigeria and West Africa, is classified as a:",
            "Root hemiparasite whose dust-like seeds germinate only in response to chemical stimulants (strigolactones) exuded by the host root",
            [
                "Stem epiphyte dispersed by aquatic snails",
                "Mutualistic nitrogen-fixing symbiont of cereals",
                "Saprophytic basidiomycete fungus",
            ],
            "Striga is a root hemiparasite of Poaceae (grasses/cereals). Its tiny seeds remain dormant in soil until triggered by host root strigolactones, after which it forms a haustorium penetrating host root xylem before emerging above ground.",
        ),
        (
            "In parasitology, how are the 'definitive (primary) host' and the 'intermediate (secondary) host' rigorously defined?",
            "The definitive host is the organism in which the parasite attains sexual maturity and reproduces sexually, whereas the intermediate host harbors the larval or asexual reproductive stages",
            [
                "The definitive host is always a vertebrate, whereas the intermediate host is always an insect",
                "The definitive host is the larger organism, whereas the intermediate host is the smaller organism",
                "The definitive host suffers no symptoms, whereas the intermediate host always dies",
            ],
            "By definition, sexual reproduction (gametogony/syngamy) occurs in the definitive host, and asexual amplification or larval development occurs in the intermediate host. Thus for Plasmodium, the female Anopheles mosquito is the definitive host (where syngamy/ookinete formation occurs) and humans are the intermediate host!",
        ),
        (
            "Applying the strict definition of definitive vs. intermediate host to the malaria parasite (Plasmodium falciparum) and the bilharzia blood fluke (Schistosoma haematobium):",
            "For Plasmodium, the female Anopheles mosquito is the DEFINITIVE host and man is the INTERMEDIATE host; for Schistosoma, man is the DEFINITIVE host and the freshwater pulmonate snail (Bulinus) is the INTERMEDIATE host",
            [
                "Man is the definitive host for both Plasmodium and Schistosoma",
                "Mosquito and Bulinus snail are the definitive hosts for both parasites",
                "Man is the intermediate host for Schistosoma and definitive host for Plasmodium",
            ],
            "In Plasmodium, fusion of microgametes and macrogametes (sexual reproduction) occurs in the mosquito midgut (definitive host), while schizogony in humans is asexual (intermediate host). In Schistosoma, adult male and female flukes mate sexually in human pelvic veins (definitive host), while miracidia/sporocysts/cercariae develop asexually in Bulinus snails (intermediate host).",
        ),
        (
            "Which set of morphological and physiological adaptations enables the pork tapeworm (Taenia solium) to survive as an obligate endoparasite in the human small intestine?",
            "Complete absence of an alimentary canal (osmotrophic absorption via microtriches on the tegument), a scolex armed with 4 suckers and a rostellum of hooks, an glycocalyx-coated tegument resistant to host pancreatic proteases, and facultative anaerobic glycolysis",
            [
                "Well-developed eyespots, ciliated locomotory bands, and aerobic respiration",
                "A muscular pharynx for sucking blood and chitinous jaws for chewing mucosa",
                "Intracellular location inside red blood cells",
            ],
            "Cestodes (Taenia) lack a mouth and digestive tract completely; their syncytial tegument bears microtriches that amplify surface area for nutrient absorption, secretes antienzymes/mucopolysaccharides against trypsin, anchors via suckers/hooks, and produces tens of thousands of eggs in gravid proglottids.",
        ),
        (
            " state Gause's 'Competitive Exclusion Principle' (1934), demonstrated experimentally using Paramecium aurelia and Paramecium caudatum:",
            "Two species competing for the exact same limiting resources (occupying identical ecological niches) in a stable environment cannot coexist indefinitely; the superior competitor will eventually eliminate the inferior one",
            [
                "Intraspecific competition is always weaker than interspecific competition",
                "Predators always drive their prey to extinction in closed laboratory flasks",
                "Two species in the same habitat will always evolve into mutualists",
            ],
            "When P. aurelia and P. caudatum were cultured together on a fixed bacterial supply, P. aurelia (higher intrinsic rate of increase r) outcompeted and drove P. caudatum to local extinction, establishing that complete competitors cannot coexist.",
        ),
        (
            "How did Robert MacArthur's classic study of five species of North American warblers (Setophaga/Dendroica) feeding on insects in the same spruce trees explain their stable coexistence without violating Gause's principle?",
            "Through resource partitioning (niche differentiation): each warbler species foraged in a different microhabitat zone of the tree canopy and used distinct hunting behaviors",
            [
                "The five warbler species interbred to form a single polyploid species",
                "Food insects were in infinite supply so competition was zero",
                "The warblers switched from insectivory to photosynthesis in winter",
            ],
            "Coexistence of ecologically similar species is achieved via niche differentiation (resource partitioning in space, time, or diet) and character displacement, reducing niche overlap.",
        ),
        (
            "Why is intraspecific competition (among individuals of the SAME species) generally more intense and severe than interspecific competition (between DIFFERENT species)?",
            "Con-specific individuals share identical structural, physiological, nutritional, and reproductive niche requirements (100% niche overlap)",
            [
                "Individuals of the same species cannot recognize each other",
                "Interspecific competition only occurs in aquatic ecosystems",
                "Intraspecific competition never affects population birth or death rates",
            ],
            "Members of the same species require the exact same food resources, mates, breeding sites, and microhabitats at the same times, creating maximum overlap and density-dependent regulation.",
        ),
        (
            "Distinguish between Batesian mimicry and Müllerian mimicry in predator-prey evolutionary interactions:",
            "In Batesian mimicry, a palatable/harmless species (mimic) resembles an unpalatable/venomous species (model); in Müllerian mimicry, two or more unpalatable/noxious species evolve a shared warning (aposematic) pattern, reinforcing predator avoidance",
            [
                "In Batesian mimicry, a predator resembles a flower to lure prey; in Müllerian mimicry, prey become transparent",
                "In Batesian mimicry, both species are toxic; in Müllerian mimicry, both species are harmless",
                "Batesian mimicry occurs only in plants, whereas Müllerian mimicry occurs only in mammals",
            ],
            "Viceroy/hoverfly mimicking noxious monarchs/wasps is Batesian mimicry (one-sided bluff); multiple unpalatable Heliconius butterfly species or stinging bees/wasps sharing black-and-yellow stripes is Müllerian mimicry (mutual reinforcement).",
        ),
        (
            "In ecological interactions, 'Amensalism' is denoted by (-, 0). Which of the following is a classic example of amensalism (specifically antibiosis / allelopathy)?",
            "The mould Penicillium notatum secreting penicillin, which lyses Gram-positive bacteria (-), while Penicillium itself gains no direct nutritional benefit (0); or black walnut trees (Juglans nigra) secreting juglone, which inhibits understory herbs",
            [
                "A lion hunting and consuming a zebra (+, -)",
                "A tapeworm absorbing glucose in the human ileum (+, -)",
                "Two oak trees competing for sunlight in a forest (-, -)",
            ],
            "Amensalism (-, 0) occurs when one species is inhibited or destroyed by a chemical secretion (antibiosis/allelopathy) or mechanical disturbance (elephants trampling grass) while the actor species is unaffected.",
        ),
        (
            "What is a 'parasitoid' (such as ichneumonid and braconid wasps laying eggs inside caterpillars), and how does it differ from a true parasite?",
            "A parasitoid is free-living as an adult, but its larval stage develops inside or on a single host individual, feeding on its tissues and inevitably killing the host upon completing development",
            [
                "A parasitoid lives on the outer fur of mammals and never kills its host",
                "A parasitoid requires three vertebrate intermediate hosts",
                "A parasitoid is a virus that infects only bacteria",
            ],
            "Unlike true parasites (which typically keep their host alive to prolong resource extraction), parasitoid larvae consume a single host slowly from within (first non-vital fat bodies, then vital organs), resulting in 100% host lethality at pupation.",
        ),
        (
            "What is 'hyperparasitism'?",
            "A condition in which a parasite itself serves as the host for another parasite (e.g., Plasmodium protozoans living inside a female Anopheles mosquito, or a bacteriophage infecting a pathogenic bacterium inside a human)",
            [
                "A single host infected by more than 1000 worms of the same species",
                "A facultative saprophyte turning into an obligate predator",
                "Mutualism between two ectoparasites",
            ],
            "A hyperparasite is a parasite of a parasite (e.g., Nosema microsporidians parasitizing trematode larvae, or Yersinia pestis bacteria inside the rat flea Xenopsylla cheopis).",
        ),
        (
            "How is the infective stage of the hookworm (Ancylostoma duodenale or Necator americanus) transmitted to humans, and how does it differ from Ascaris lumbricoides?",
            "Hookworm is transmitted by active percutaneous (skin) penetration of the infective filariform (L3) larva from contaminated soil, whereas Ascaris is transmitted orally by ingesting embryonated eggs containing the infective L2/L3 larva",
            [
                "Hookworm is transmitted by the bite of the Simulium blackfly, whereas Ascaris is transmitted by Chrysops",
                "Both are transmitted by eating undercooked pork containing cysticerci",
                "Hookworm penetrates the stomach wall after eating raw freshwater crabs",
            ],
            "Hookworm eggs hatch in warm moist soil into rhabditiform larvae that moult into infective filariform (L3) larvae, which penetrate bare feet; Ascaris lumbricoides is acquired via the fecal-oral route by swallowing infective embryonated eggs.",
        ),
        (
            "Match the filarial nematode parasites Wuchereria bancrofti, Onchocerca volvulus, and Loa loa with their correct insect vectors:",
            "Wuchereria bancrofti → Mosquitoes (Culex/Anopheles); Onchocerca volvulus → Blackfly (Simulium damnosum); Loa loa → Mango/Deer fly (Chrysops silacea)",
            [
                "Wuchereria bancrofti → Tsetse fly (Glossina); Onchocerca volvulus → Mosquito; Loa loa → Sandfly (Phlebotomus)",
                "Wuchereria bancrofti → Simulium; Onchocerca volvulus → Chrysops; Loa loa → Culex",
                "All three are transmitted by the female Anopheles mosquito",
            ],
            "Lymphatic filariasis (elephantiasis, Wuchereria) is transmitted by mosquitoes; river blindness (onchocerciasis, Onchocerca) by Simulium blackflies breeding in fast-flowing rivers; African eye worm (loiasis, Loa loa) by Chrysops tabanid flies.",
        ),
        (
            "What is 'brood parasitism' as practiced by the Old World cuckoo (Cuculus canorus) or African Pin-tailed Whydah (Vidua macroura)?",
            "A form of social parasitism where the parasite lays its eggs in the nest of a host bird species, leaving the host to incubate the eggs and rear the parasitic young at the expense of the host's own clutch",
            [
                "Ticks feeding on newly hatched chicks inside a nest",
                "Adult birds stealing fish from the beaks of other seabirds (kleptoparasitism)",
                "Female insects carrying their eggs on their backs until hatching",
            ],
            "In avian brood parasitism, egg mimicry deceives the foster parent into incubating the parasitic egg, which typically hatches earlier and evicts or outcompetes the host's own nestlings.",
        ),
        (
            "In Lotka-Volterra predator-prey population oscillations, how are the population peaks of the predator and the prey temporally related?",
            "The predator population cycle lags behind the prey population cycle by approximately a quarter of a period (peaks after the prey peak)",
            [
                "The predator population peaks first, followed by the prey peak",
                "Both predator and prey populations peak at the exact same instant",
                "Prey population remains constant while predator population increases exponentially",
            ],
            "An increase in prey abundance increases predator natality/survival after a reproductive time lag; as predators peak, heavy predation drives prey numbers down, which subsequently causes predator starvation and decline.",
        ),
        (
            "Carnivorous (insectivorous) plants such as Sundew (Drosera), Venus flytrap (Dionaea), and Pitcher plant (Nepenthes) are photosynthetic autotrophs that trap and digest insects primarily because:",
            "They inhabit waterlogged, acidic bog soils or epiphytic habitats deficient in available nitrogen (nitrates/ammonium), using insect prey as a supplemental nitrogen and phosphorus source",
            [
                "They lack chlorophyll and Rubisco and must obtain organic carbon heterotrophically from insects",
                "They lack roots and cannot absorb liquid water",
                "They use insect chitin directly to build their cellulose cell walls",
            ],
            "Insectivorous plants possess chloroplasts and fix CO2 autotrophically, but grow in acidic, anaerobic peat bogs where nitrifying bacteria are inhibited; proteolysis of trapped insects supplies amino acids, NH4+, and PO4³-.",
        ),
        (
            "Which larval stages occur in the correct chronological sequence during the life cycle of the liver fluke (Fasciola hepatica) from egg hatching in water to encystment on aquatic vegetation?",
            "Miracidium → Sporocyst → Redia → Cercaria → Metacercaria (infective cyst)",
            [
                "Cercaria → Miracidium → Redia → Sporocyst → Metacercaria",
                "Oncosphere → Cysticercus → Procercoid → Plerocercoid",
                "Microfilaria → Rhabditiform → Filariform → Adult",
            ],
            "The ciliated Miracidium hatches in water and penetrates the Lymnaea snail, where it transforms into a Sporocyst, then Rediae, and free-swimming Cercariae, which leave the snail and encyst on grass as infective Metacercariae.",
        ),
        (
            "What is the difference between a 'facultative parasite' and an 'obligate saprophyte'?",
            "A facultative parasite is normally a free-living saprophyte on dead organic matter but can parasitize a living host under favorable conditions (e.g., Pythium or Candida), whereas an obligate saprophyte can ONLY feed on dead organic matter (e.g., Agaricus)",
            [
                "A facultative parasite cannot survive outside a living host cell (e.g., viruses)",
                "An obligate saprophyte requires a living mammalian bloodstream to reproduce",
                "Both terms refer to autotrophic chemosynthetic bacteria",
            ],
            "Facultative parasites are saprophytes capable of switching to parasitism; facultative saprophytes are normally parasites that can also be cultured on dead/artificial media. Obligate parasites (viruses, rust fungi, Plasmodium) require a living host.",
        ),
        (
            "How do saprophytic fungi (e.g., Mucor, Rhizopus, Aspergillus) obtain their nutrients from dead organic substrates?",
            "By absorptive heterotrophy (osmotrophy): secreting extracellular hydrolytic exoenzymes (amylases, proteases, lipases, cellulases) onto the substrate and absorbing the soluble monomeric products across their hyphal cell walls",
            [
                "By phagocytic engulfment (holozoic nutrition) of solid food particles into food vacuoles",
                "By chemosynthetic oxidation of hydrogen sulfide",
                "By trapping insects with adhesive slime rings",
            ],
            "Because fungal hyphae are surrounded by rigid chitinous cell walls, they cannot perform phagocytosis; instead, they carry out extracellular digestion via secreted exoenzymes followed by osmotrophic absorption.",
        ),
        (
            "Why do predators in natural ecosystems rarely eradicate their prey species completely (in contrast to simple laboratory microcosms)?",
            "Because of habitat heterogeneity (spatial refuges for prey), prey switching by generalist predators when a focal prey becomes scarce, and predator territoriality/density-dependent mortality",
            [
                "Because prey species stop reproducing whenever predators are absent",
                "Because predators voluntarily fast during the breeding season of prey",
                "Because all predators are strictly herbivorous during half of the year",
            ],
            "In nature, prey refugia (hiding places), apostatic selection (predators switching to more abundant alternative prey when a species becomes rare), and spatial dispersal stabilize predator-prey coexistence.",
        ),
        (
            "What is 'aposematism' (aposematic coloration) in prey organisms such as poison dart frogs (Dendrobates) and monarch butterflies (Danaus plexippus)?",
            "Conspicuous, bright warning coloration (typically red, yellow, orange, and black) that advertises unpalatability, toxicity, or painful stings to potential visual predators",
            [
                "Cryptic background matching that makes the animal invisible against tree bark",
                "Countershading where the dorsal surface is dark and ventral surface is light",
                "Bioluminescence used to attract mates in the deep ocean",
            ],
            "Aposematism pairs high visual conspicuousness with chemical defenses (cardiac glycosides, alkaloids, venom) so experienced predators rapidly learn to avoid attacking the prey.",
        ),
        (
            "In Guinea worm disease (Dracunculiasis), caused by the nematode Dracunculus medinensis, how does a human acquire the infection?",
            "By drinking stagnant pond water containing freshwater copepods (Cyclops / water fleas) infected with third-stage (L3) Dracunculus larvae",
            [
                "By wading bare-footed in fast-flowing streams inhabited by Simulium larvae",
                "By being bitten at night by Triatoma kissing bugs",
                "By eating raw freshwater fish containing plerocercoid larvae",
            ],
            "Gravid female Dracunculus worms emerge from painful blisters on the lower leg to discharge larvae into water; larvae are ingested by Cyclops (intermediate host) and humans are infected by drinking unfiltered water containing infected Cyclops.",
        ),
        (
            "When two species evolve morphological divergence in sympatry (where their geographic ranges overlap) to minimize competition for food — such as Darwin's finches (Geospiza fortis and Geospiza fuliginosa) evolving different beak depths on islands where they coexist compared to islands where each lives alone — this evolutionary phenomenon is called:",
            "Character displacement",
            [
                "Convergent evolution",
                "Genetic drift (bottleneck effect)",
                "Müllerian mimicry",
            ],
            "Ecological character displacement is the evolutionary divergence of morphological/behavioral traits in sympatric populations of competing species driven by natural selection to reduce resource competition.",
        ),
        (
            "What type of ecological interaction exists between cellulose-digesting fungi (Termitomyces) cultivated on 'fungus combs' inside the mounds of higher termites (Macrotermitinae)?",
            "Obligate ectosymbiotic mutualism (fungus-growing agriculture), where termites feed plant material to the fungus comb and consume the nitrogen-rich fungal nodules (mycotêtes)",
            [
                "Endoparasitism of the termite queen by the fungus",
                "Amensalism where the fungus poisons the termite brood",
                "Commensalism where the fungus is an accidental weed",
            ],
            "Macrotermitinae termites lack intracellular gut flagellates and instead cultivate an obligate mutualistic basidiomycete fungus (Termitomyces) on fecal combs; the fungus degrades lignin and cellulose, enriching the diet of the termites.",
        ),
    ]
    for q, corr, dists, exp in topic3:
        raw_questions.append((q, corr, dists, exp))

    # =========================================================================
    # TOPIC 4: ELEMENTS OF ECOLOGY (35 Questions — Hard & Medium)
    # =========================================================================
    topic4 = [
        (
            "Distinguish precisely between 'Autecology' and 'Synecology':",
            "Autecology is the ecological study of an individual organism or a single species population in relation to its environment, whereas Synecology is the study of groups of organisms (biotic communities and ecosystems) interacting together in a shared habitat",
            [
                "Autecology studies terrestrial ecosystems, whereas Synecology studies marine ecosystems",
                "Autecology studies abiotic factors only, whereas Synecology studies biotic factors only",
                "Autecology is the study of fossil plants, whereas Synecology is the study of succession",
            ],
            "Autecology (species/population ecology) focuses on the adaptations, life history, and tolerances of a single species; Synecology (community/ecosystem ecology) examines multispecies communities, trophic webs, and ecosystem fluxes.",
        ),
        (
            "In ecosystem bioenergetics, if the Gross Primary Productivity (GPP) of a tropical rainforest is 4,500 kcal m⁻² yr⁻¹ and autotrophic plant respiration (R_a) consumes 2,700 kcal m⁻² yr⁻¹, what is the Net Primary Productivity (NPP) available to primary consumers and decomposers?",
            "1,800 kcal m⁻² yr⁻¹",
            [
                "7,200 kcal m⁻² yr⁻¹",
                "450 kcal m⁻² yr⁻¹",
                "2,700 kcal m⁻² yr⁻¹",
            ],
            "By definition, Net Primary Productivity NPP = GPP - R_a = 4,500 - 2,700 = 1,800 kcal m⁻² yr⁻¹.",
        ),
        (
            "Which ecological pyramid is NEVER inverted in any natural, functioning ecosystem under any circumstance, and why?",
            "Pyramid of Energy, because energy flow is unidirectional and governed by the Second Law of Thermodynamics, with ~90% lost as metabolic heat at each trophic transfer",
            [
                "Pyramid of Numbers, because producers are always smaller than herbivores",
                "Pyramid of Biomass, because standing crop always increases with trophic level",
                "Both Pyramid of Numbers and Pyramid of Biomass are never inverted",
            ],
            "While a Pyramid of Numbers is inverted in a parasitic food chain (1 oak tree → thousands of insects → parasites) and a Pyramid of Biomass is inverted in open ocean pelagic ecosystems (rapidly turning-over phytoplankton have lower standing biomass than longer-lived zooplankton), the Pyramid of Energy (rate of energy flow per unit area per unit time) is ALWAYS upright.",
        ),
        (
            "Why can the Pyramid of Biomass (standing crop) in an open marine pelagic ecosystem (Phytoplankton → Zooplankton) be INVERTED at a given moment without violating the laws of thermodynamics?",
            "Because phytoplankton have a very high reproductive turnover rate (short generation time and high productivity), so a small standing biomass of phytoplankton supports a larger standing biomass of longer-lived zooplankton over time",
            [
                "Because zooplankton perform photosynthesis and do not eat phytoplankton",
                "Because marine food chains have a 150% trophic transfer efficiency",
                "Because saltwater converts dissolved carbonate directly into zooplankton tissue",
            ],
            "Biomass pyramids measure 'standing crop' at a single point in time (g/m²), not rate of production. Phytoplankton reproduce and are grazed so rapidly that their instantaneous standing mass is smaller than that of the slower-reproducing zooplankton.",
        ),
        (
            "In a detritus food chain (Dead mangrove leaves → Detritivorous crabs/nematodes → Small carnivorous fish → Herons), what is the primary energy source at the base of the chain?",
            "Dead organic matter (detritus / litter) and its associated decomposer microbes, rather than direct grazing on living green tissues",
            [
                "Chemosynthetic oxidation of methane at hydrothermal vents",
                "Direct absorption of ultraviolet radiation by crabs",
                "Dissolved inorganic nitrates in rainwater",
            ],
            "Unlike grazing food chains that begin with living photosynthetic producers, detritus food chains begin with dead organic matter (fallen leaves, carcasses, feces) processed by saprotrophs and detritivores.",
        ),
        (
            "Match the following ecological instruments with the exact physical/environmental parameter they measure: (i) Secchi disc, (ii) Anemometer, (iii) Hygrometer (Wet-and-Dry Bulb), (iv) Edaphic tensiometer:",
            "(i) Turbidity / light penetration depth in water; (ii) Wind speed; (iii) Relative humidity; (iv) Soil moisture tension (matric water potential)",
            [
                "(i) Water flow velocity; (ii) Wind direction; (iii) Atmospheric pressure; (iv) Soil pH",
                "(i) Dissolved oxygen; (ii) Rainfall amount; (iii) Light intensity; (iv) Slope angle",
                "(i) Salinity; (ii) Relative humidity; (iii) Wind speed; (iv) Atmospheric temperature",
            ],
            "A Secchi disc measures water transparency/turbidity; an anemometer measures wind speed (wind vane measures direction); a hygrometer/psychrometer measures relative humidity; a tensiometer measures soil water tension.",
        ),
        (
            "In the Lincoln-Petersen Mark-Release-Recapture method for estimating the population size (N) of mobile animals, 80Tilapia fish are captured, marked harmlessly, and released. Later, a second sample of 100 fish is captured from the same pond, of which 16 carry the mark. Assuming no immigration, emigration, births, or deaths, what is the estimated total population size N?",
            "500 fish",
            [
                "1,280 fish",
                "400 fish",
                "640 fish",
            ],
            "Using the Lincoln-Petersen index N = (M × C) / R = (80 × 100) / 16 = 8,000 / 16 = 500 fish.",
        ),
        (
            "A botanist throws a square quadrat of side length 0.5 m (area = 0.25 m²) 40 times at random in a savanna grassland of total area 2,000 m² and counts a total of 300 Tridax procumbens plants across the 40 throws. Calculate the population density (plants/m²) and estimated total population size:",
            "Density = 30 plants/m²; Total population = 60,000 plants",
            [
                "Density = 7.5 plants/m²; Total population = 15,000 plants",
                "Density = 15 plants/m²; Total population = 30,000 plants",
                "Density = 60 plants/m²; Total population = 120,000 plants",
            ],
            "Total area sampled = 40 quadrats × (0.5 m × 0.5 m) = 40 × 0.25 m² = 10 m². Population density = 300 plants / 10 m² = 30 plants/m². Estimated total population = 30 × 2,000 m² = 60,000 plants.",
        ),
        (
            "In primary xerarch ecological succession on bare volcanic rock (lithosere), what is the correct chronological sequence of seral stages from pioneer community to climax community?",
            "Crustose lichens → Foliose lichens → Mosses → Annual/perennial herbs and grasses → Shrubs → Climax forest community",
            [
                "Mosses → Annual grasses → Crustose lichens → Foliose lichens → Shrubs → Climax forest",
                "Submerged hydrophytes → Floating hydrophytes → Reed-swamp → Sedge-meadow → Forest",
                "Shrubs → Pioneer trees → Grasses → Mosses → Crustose lichens",
            ],
            "On bare rock (lithosere), crustose lichens (e.g., Rhizocarpon) are the pioneers that secrete lichenic/carbonic acids to weather rock into a thin film of dust, followed by foliose lichens, mosses (Polytrichum), herbs/grasses, shrubs, and climax trees.",
        ),
        (
            "Why does secondary ecological succession (e.g., on an abandoned farmland or after a bushfire) proceed much faster than primary succession (e.g., on a newly formed lava flow or glacial moraine)?",
            "Because well-developed soil containing humus, mineral nutrients, soil microbiota, and a viable subterranean seed/spore bank is already present at the start of secondary succession",
            [
                "Because secondary succession skips all herbaceous and shrub stages and starts directly with climax canopy trees",
                "Because rainfall is ten times higher in secondary succession",
                "Because primary succession occurs only underwater",
            ],
            "Primary succession begins on a sterile, lifeless substrate devoid of soil (requiring centuries of pedogenesis by lichens/mosses), whereas secondary succession begins on pre-existing soil with an intact seed bank and microbial community.",
        ),
        (
            "In the Verhulst-Pearl logistic population growth equation dN/dt = rN((K - N)/K), what happens to the population growth rate dN/dt when N = K/2 and when N = K respectively?",
            "At N = K/2 (the inflection point), the population growth rate dN/dt is at its MAXIMUM; at N = K (carrying capacity), dN/dt = 0 (net growth stops)",
            [
                "At N = K/2, dN/dt = 0; at N = K, dN/dt is at its maximum",
                "At both N = K/2 and N = K, dN/dt equals rN",
                "At N = K, the population crashes immediately to zero",
            ],
            "The quadratic function f(N) = rN(1 - N/K) is a downward-opening parabola with roots at N = 0 and N = K, reaching its maximum rate of population addition (Maximum Sustainable Yield, MSY = rK/4) at the midpoint N = K/2.",
        ),
        (
            "Compare r-selected species (opportunistic, e.g., bacteria, weeds, houseflies) with K-selected species (equilibrium, e.g., elephants, humans, climax canopy trees):",
            "r-selected species exhibit early maturity, large numbers of small offspring, little or no parental care, and Type III survivorship; K-selected species exhibit delayed maturity, few large offspring, intensive parental care, and Type I survivorship",
            [
                "r-selected species have long lifespans, high parental care, and Type I survivorship curves",
                "K-selected species thrive in unpredictable disturbed habitats and produce millions of tiny spores",
                "Both r- and K-selected species maintain populations permanently below 1% of carrying capacity",
            ],
            "r-strategists maximize intrinsic rate of natural increase (r) in unstable environments (high fecundity, Type III concave survivorship); K-strategists maximize competitive ability near carrying capacity K (high juvenile survival, Type I convex survivorship).",
        ),
        (
            "In the Nitrogen Cycle, which specific bacteria carry out: (1) free-living aerobic nitrogen fixation, (2) oxidation of ammonia to nitrite, (3) oxidation of nitrite to nitrate, and (4) anaerobic denitrification of nitrate back to N2 gas?",
            "(1) Azotobacter; (2) Nitrosomonas / Nitrosococcus; (3) Nitrobacter; (4) Pseudomonas denitrificans / Thiobacillus denitrificans",
            [
                "(1) Nitrobacter; (2) Azotobacter; (3) Nitrosomonas; (4) Rhizobium",
                "(1) Pseudomonas; (2) Clostridium; (3) Nitrosomonas; (4) Nitrobacter",
                "(1) Nitrosomonas; (2) Nitrobacter; (3) Azotobacter; (4) Nostoc",
            ],
            "Azotobacter (aerobic) and Clostridium (anaerobic) are free-living N2 fixers; Nitrosomonas oxidizes NH3/NH4+ → NO2-; Nitrobacter oxidizes NO2- → NO3-; Pseudomonas denitrificans reduces NO3- → N2 under waterlogged anaerobic conditions.",
        ),
        (
            "Why does the global Phosphorus Cycle differ fundamentally from the Carbon and Nitrogen cycles?",
            "Phosphorus is a sedimentary cycle lacking any significant gaseous atmospheric phase under normal Earth conditions; its primary reservoir is phosphate rock (apatite) in the Earth's crust",
            [
                "Phosphorus is fixed from atmospheric P2 gas by leguminous root nodules",
                "Phosphorus is not required for nucleic acids or ATP in living cells",
                "Phosphorus cycles exclusively within the stratosphere",
            ],
            "Unlike C (CO2, CH4) and N (N2, N2O, NH3), phosphorus has no stable common gas phase; it weathers from sedimentary phosphate rocks as orthophosphate (PO4³-), cycles through food webs, and returns to marine sediments.",
        ),
        (
            "What is cultural 'eutrophication' of freshwater lakes, and what is the exact sequence of events that causes massive fish kills?",
            "Nutrient enrichment (nitrates and phosphates from sewage/fertilizer runoff) triggers dense algal blooms; when the algae die, aerobic saprotrophic bacteria decompose the dead biomass, elevating Biochemical Oxygen Demand (BOD) and depleting dissolved oxygen (hypoxia/anoxia), suffocating fish",
            [
                "Nitrates directly poison the hemoglobin of fish while increasing dissolved oxygen to 100%",
                "Algal blooms consume all the water molecules in the lake during the day",
                "Phosphates freeze the surface of tropical lakes, blocking gas exchange",
            ],
            "Excess N and P stimulate cyanobacterial/algal blooms. Decomposition of the senescent algal mat by heterotrophic bacteria consumes dissolved O2 (high BOD), causing nocturnal and benthic hypoxia that kills aerobic fish.",
        ),
        (
            "Distinguish between 'biomagnification' (biological amplification) and 'bioaccumulation' of persistent lipophilic pollutants such as DDT or methylmercury:",
            "Bioaccumulation is the build-up of a toxin within a SINGLE organism over its lifetime faster than it can be excreted, whereas Biomagnification is the progressive increase in concentration of the toxin in tissues at successively HIGHER trophic levels of a food chain",
            [
                "Bioaccumulation occurs only in top carnivores, whereas biomagnification occurs only in primary producers",
                "Biomagnification applies only to water-soluble vitamins like Vitamin C",
                "Bioaccumulation decreases toxin concentration as an animal ages",
            ],
            "Because DDT and methylmercury are lipid-soluble and non-biodegradable, each predator consumes many contaminated prey items and retains nearly all the toxin in its adipose tissue, multiplying tissue concentrations by orders of magnitude up the food chain (e.g., Water → Plankton → Small fish → Large fish → Fish-eating eagle).",
        ),
        (
            "Which physiological and morphological adaptations (halophytic adaptations) enable Red Mangrove trees (Rhizophora racemosa) and White/Black Mangroves (Avicennia germinans) to survive in waterlogged, anoxic, saline coastal swamps of Southern Nigeria?",
            "Stilt/prop roots (Rhizophora) and negatively geotropic breathing roots called pneumatophores with lenticels (Avicennia) for gas exchange in anoxic mud, viviparous germination of seedlings on the parent tree, and salt-excreting foliar glands / high root cell osmotic pressure",
            [
                "Deep taproots reaching 50 m into dry sand, spines instead of leaves, and CAM photosynthesis",
                "Air bladders for floating freely on the ocean surface without root attachment",
                "Deciduous shedding of all leaves during the 9-month dry season",
            ],
            "Mangrove swamp soil is waterlogged (anaerobic) and physiologically dry (hypertonic). Mangroves overcome anoxia via aerial stilt roots or erect pneumatophores bearing pneumathodes/lenticels, overcome salinity via salt glands/ultrafiltration, and exhibit vivipary (seeds germinate into heavy hypocotyl darts before dropping into the mud).",
        ),
        (
            "Moving northward from the Atlantic coast of Nigeria to the far north border, what is the correct latitudinal sequence of major Nigerian vegetation zones (biomes) as mean annual rainfall decreases and dry season length increases?",
            "Mangrove/Freshwater Swamp Forest → Tropical Lowland Rainforest → Derived Savanna → Guinea Savanna → Sudan Savanna → Sahel Savanna",
            [
                "Tropical Rainforest → Sahel Savanna → Sudan Savanna → Guinea Savanna → Mangrove Swamp",
                "Guinea Savanna → Mangrove Swamp → Tropical Rainforest → Sudan Savanna → Sahel Savanna",
                "Sahel Savanna → Derived Savanna → Tropical Rainforest → Sudan Savanna → Guinea Savanna",
            ],
            "Along Nigeria's south-to-north rainfall gradient (~3000 mm in the Niger Delta to <500 mm in Borno/Yobe), vegetation transitions from Coastal Mangrove & Freshwater Swamp → Tropical Rainforest → Derived Savanna → Southern/Northern Guinea Savanna → Sudan Savanna → Sahel Savanna.",
        ),
        (
            "Which of the following sets of plant adaptations is characteristic of 'xerophytes' (plants adapted to arid/desert or Sahel habitats, such as Opuntia, Euphorbia, and Acacia)?",
            "Thick waxy cuticle, sunken stomata in hairy epidermal crypts, leaves reduced to spines with flattened photosynthetic stems (phylloclades/cladodes), succulent water-storing parenchyma, and Crassulacean Acid Metabolism (CAM) with scotoactive (night-opening) stomata",
            [
                "Thin cuticle, abundant stomata on the upper leaf surface only, large air spaces (aerenchyma), and finely dissected submerged leaves",
                "Broad thin shade leaves with drip tips and buttress roots",
                "Viviparous seedlings and negatively geotropic pneumatophores",
            ],
            "Xerophytes minimize transpirational water loss via thick cuticles, sunken stomata, trichomes, leaf reduction to spines, stem succulence (phylloclades), deep/extensive root systems, and CAM nocturnal stomatal opening.",
        ),
        (
            "In submerged and floating aquatic plants ('hydrophytes' such as Ceratophyllum, Elodea, and Nymphaea/water lily), which anatomical modification is most prominent?",
            "Extensive intercellular air spaces (aerenchyma) for buoyancy and internal O2/CO2 diffusion, poorly developed or absent xylem and mechanical tissues (sclerenchyma), and stomata restricted to the upper epidermis (epistomatic) in floating leaves or absent in submerged leaves",
            [
                "Heavily lignified xylem vessels and thick suberized bark",
                "Sunken stomata on the lower epidermis only",
                "High root-to-shoot biomass ratio with deep taproots",
            ],
            "Because water supports the plant buoyantly and surrounds submerged tissues, hydrophytes have reduced xylem and mechanical sclerenchyma, lack cuticles on submerged parts, and possess large aerenchyma lacunae.",
        ),
        (
            "What is the 'ecological niche' of a species (as conceptualized by Grinnell, Elton, and Hutchinson's n-dimensional hypervolume), as distinct from its 'habitat'?",
            "While the habitat is the physical place/address where an organism lives, the ecological niche is the organism's complete functional role, trophic position, and multidimensional range of abiotic and biotic tolerances and resource uses within the ecosystem",
            [
                "The niche is the geographic continent where a species is found, whereas the habitat is its diet",
                "Two different species in the same forest always share the exact same realized niche",
                "The realized niche is always broader and larger than the fundamental niche",
            ],
            "Habitat is the 'address' and niche is the 'profession' (functional role + Hutchinsonian n-dimensional hypervolume). Due to interspecific competition and predation, a species' actual 'realized niche' is typically a smaller subset of its physiological 'fundamental niche'.",
        ),
        (
            "According to Shelford's Law of Tolerance (1913) and Liebig's Law of the Minimum (1840):",
            "An organism's success and distribution are limited not only by too little of an essential resource (Liebig's minimum) but also by too much of an environmental factor (such as temperature, pH, or salinity) beyond its upper and lower limits of physiological tolerance (Shelford)",
            [
                "Organisms grow fastest when all environmental factors are at their absolute maximum possible values",
                "Stenothermal organisms can tolerate a wider temperature range than eurythermal organisms",
                "Abiotic factors have zero influence on population carrying capacity",
            ],
            "Liebig's Law states growth is dictated by the scarcest limiting nutrient; Shelford's Law extends this to show bell-shaped tolerance curves with an optimal zone flanked by zones of physiological stress and zones of intolerance at both low and high extremes.",
        ),
        (
            "Distinguish between 'euryhaline' and 'stenohaline' aquatic organisms:",
            "Euryhaline organisms (e.g., salmon, tilapia, estuarine crabs) can tolerate a WIDE range of salinities, whereas stenohaline organisms (e.g., goldfish, most open-ocean corals) can tolerate only a NARROW range of salinities",
            [
                "Euryhaline organisms tolerate only narrow temperature ranges, whereas stenohaline tolerate wide temperatures",
                "Stenohaline organisms migrate freely between freshwater rivers and the deep sea",
                "Euryhaline organisms cannot osmoregulate",
            ],
            "The prefix 'eury-' means wide tolerance (euryhaline = wide salinity, eurythermal = wide temperature), whereas 'steno-' means narrow tolerance (stenohaline = narrow salinity).",
        ),
        (
            "In soil science (edaphology), a soil sample is weighed: fresh moist mass = 120 g; mass after oven-drying at 105°C to constant weight = 100 g; mass after red-hot ignition in a muffle furnace at 600°C to burn off organic humus = 88 g. What are the percentage water content and percentage humus (organic matter) content on a dry-mass basis?",
            "Water content = 20% of dry mass (or 16.7% of wet mass); Humus content = 12% of dry soil mass",
            [
                "Water content = 88%; Humus content = 100%",
                "Water content = 12% of dry mass; Humus content = 20% of dry mass",
                "Water content = 32% of dry mass; Humus content = 8% of dry mass",
            ],
            "Mass of water lost at 105°C = 120 - 100 = 20 g (20/100 = 20% of dry mass; 20/120 = 16.7% of wet mass). Mass of organic humus burned off at 600°C = 100 - 88 = 12 g (12/100 = 12% of dry soil mass).",
        ),
        (
            "Compare the edaphic properties of sandy soil, clay soil, and loamy soil:",
            "Clay soil has the smallest particle size (<0.002 mm), highest capillarity and water-holding capacity, but poorest aeration/drainage; Sandy soil has large particles (0.02–2.0 mm), high porosity/drainage, and low water retention; Loam balances sand, silt, clay, and humus for optimal agriculture",
            [
                "Sandy soil has the highest capillarity and water-holding capacity",
                "Clay soil has the largest air spaces and fastest percolation rate",
                "Silt particles are larger than coarse gravel particles",
            ],
            "Clay particles (<2 µm) have high surface area and micropores giving high total water retention and high ultimate capillary rise, but slow percolation and poor root aeration; sandy soil drains rapidly with high leaching.",
        ),
        (
            "What is an 'ecotone', and what is the 'edge effect' associated with it?",
            "An ecotone is a transition zone between two adjacent ecological communities/biomes (e.g., forest-savanna boundary or estuary), which often exhibits higher species richness and population density than either flanking community — a phenomenon called the edge effect",
            [
                "An ecotone is a sterile desert zone where no species can survive",
                "An ecotone is a genetically identical clone of plants produced by apomixis",
                "The edge effect refers to the extinction of all predators at the center of a lake",
            ],
            "Ecotones (mangrove estuaries, forest-grassland fringes) contain species from both adjacent communities plus unique 'edge species' adapted specifically to the transitional microclimate, producing elevated biodiversity (the edge effect).",
        ),
        (
            "In marine and deep freshwater ecosystems, the vertical water column is stratified by light penetration into the:",
            "Euphotic (photic) zone (where photosynthesis exceeds respiration, above the compensation point), Disphotic (twilight) zone, and Aphotic (abyssal/benthic dark) zone",
            [
                "Troposphere, Stratosphere, and Mesosphere",
                "Xylem, Cambium, and Phloem zones",
                "Canopy, Understory, and Herbaceous layers",
            ],
            "The compensation depth is the depth at which light intensity falls to ~1% of surface sunlight, where photosynthetic rate equals cellular respiration rate (NPP = 0); above it is the euphotic zone, below it the disphotic/aphotic zones.",
        ),
        (
            "Which ecological survivorship curve (Type I, Type II, or Type III on a semi-log plot of survivors vs. age) characterizes: (a) humans and large mammals, (b) hydra and many songbirds with constant mortality rate at all ages, and (c) oysters, pelagic fish, and weedy plants with massive juvenile mortality?",
            "(a) Type I (convex); (b) Type II (diagonal straight line); (c) Type III (concave)",
            [
                "(a) Type III (concave); (b) Type I (convex); (c) Type II (diagonal)",
                "(a) Type II; (b) Type III; (c) Type I",
                "All three groups exhibit a Type I convex curve",
            ],
            "Type I (convex) shows high survival through youth/middle age followed by senescent mortality; Type II (linear on semi-log scale) shows age-independent constant mortality probability; Type III (concave) shows extremely high larval/seedling mortality with high survival for the few that reach adulthood.",
        ),
        (
            "Which of the following is a density-INDEPENDENT limiting factor on population size, as opposed to a density-DEPENDENT regulating factor?",
            "A sudden catastrophic volcanic eruption, hurricane, or unseasonal severe frost (density-independent), whereas contagious infectious disease, predation, and intraspecific food competition are density-dependent",
            [
                "Intraspecific competition for nesting territories (density-independent)",
                "Spread of tuberculosis in a crowded herd (density-independent)",
                "Parasitism by tapeworms (density-independent)",
            ],
            "Density-independent factors (abiotic catastrophes, floods, droughts, fires) kill a proportion of the population regardless of population density; density-dependent factors (disease, competition, predation) intensify as population density rises, providing negative feedback toward carrying capacity K.",
        ),
        (
            "In the global Carbon Cycle, which processes remove carbon dioxide (CO2) from the atmosphere/hydrosphere, and which return it?",
            "Removal: Oxygenic photosynthesis, chemosynthesis, and marine carbonate/limestone (CaCO3) precipitation; Return: Cellular respiration, microbial decomposition, combustion of fossil fuels, and volcanic outgassing",
            [
                "Removal: Cellular respiration and combustion; Return: Photosynthesis and limestone formation",
                "Removal: Denitrification; Return: Nitrogen fixation",
                "Removal: Transpiration; Return: Guttation",
            ],
            "Autotrophic carbon fixation (Calvin cycle) and oceanic carbonate sedimentation act as carbon sinks; aerobic respiration, methanogenesis/oxidation, decomposition, and fossil fuel burning release CO2 back to the atmosphere.",
        ),
        (
            "Why is the Guinea Savanna biome referred to as the 'breadbasket' and most extensive vegetation belt of Nigeria, and what are its dominant fire-resistant tree species?",
            "It covers nearly half of Nigeria's land area with tall grasses (Andropogon, Pennisetum) interspersed with thick-barked, fire-tolerant (pyrophytic) deciduous trees such as Isoberlinia doka, Parkia biglobosa (locust bean), and Vitellaria paradoxa (shea butter)",
            [
                "It consists exclusively of Rhizophora red mangroves and Raffia palms",
                "It has zero grass cover and a closed 50-metre evergreen canopy of Mahogany (Khaya ivorensis) and Iroko",
                "It receives less than 150 mm of rain per year and supports only date palms",
            ],
            "The Guinea Savanna features tall tussocky grasses that burn annually in the dry season and pyrophytic trees with thick corky fissured bark (Parkia, Isoberlinia, Daniellia oliveri, Vitellaria).",
        ),
        (
            "Distinguish between 'hibernation', 'aestivation', and 'diapause' as behavioral/physiological adaptations to seasonal environmental extremes:",
            "Hibernation is winter dormancy with reduced metabolic rate and body temperature in endotherms (e.g., bats, ground squirrels); Aestivation is summer/dry-season dormancy to survive heat and desiccation (e.g., African lungfish Protopterus in a mud cocoon, giant African land snail Archachatina forming a calcareous epiphragm); Diapause is hormonally programmed developmental arrest in insects",
            [
                "Aestivation is winter dormancy in polar bears, whereas hibernation is dry-season dormancy in snails",
                "Diapause occurs only in deciduous trees shedding leaves",
                "During aestivation, metabolic rate increases tenfold",
            ],
            "In West Africa's dry season, lungfish (Protopterus annectens) burrow into mud and secrete a mucus cocoon to aestivate, and giant land snails seal their shell aperture with a whitish calcareous epiphragm to prevent desiccation.",
        ),
        (
            "What is the 'Biological Oxygen Demand' (BOD_5) of a water sample, and how does it relate to Dissolved Oxygen (DO) and organic sewage pollution?",
            "BOD is the amount of dissolved oxygen (mg/L) consumed by aerobic microorganisms in 5 days at 20°C while decomposing organic matter in water; high organic sewage causes a HIGH BOD and a sharp DROP in Dissolved Oxygen (DO)",
            [
                "BOD is the oxygen produced by aquatic plants; clean spring water has the highest BOD",
                "High BOD means the water is crystal clear and saturated with oxygen",
                "BOD and DO are directly proportional at all times",
            ],
            "Heavy organic pollution provides abundant substrate for aerobic saprotrophic bacteria, driving BOD5 sky-high and depleting the water's Dissolved Oxygen (DO), creating an 'oxygen sag curve' downstream of sewage outfalls.",
        ),
        (
            "In a terrestrial forest ecosystem, which trophic group is primarily responsible for mineralizing organic nitrogen (proteins, nucleic acids, urea) in dead plant litter and animal excreta back into inorganic ammonium ions (NH4+)?",
            "Ammonifying saprotrophic bacteria (e.g., Bacillusramosus, Bacillus vulgaris) and decomposing fungi",
            [
                "Denitrifying bacteria (Pseudomonas)",
                "Nitrogen-fixing cyanobacteria (Anabaena)",
                "Nitrifying bacteria (Nitrobacter)",
            ],
            "Ammonification (mineralization) is the deamination of organic nitrogen in detritus/urea into NH3/NH4+ by saprophytic bacteria and fungi, making nitrogen available again for nitrification or plant uptake.",
        ),
        (
            "What is the difference between a 'transect' (line or belt transect) and a 'random quadrat' sampling strategy in field ecology?",
            "A transect is a systematic sampling line or strip laid across an environmental gradient (such as a rocky seashore zonation or forest-to-swamp ecotone) to record how species distribution changes along the gradient, whereas random quadrats estimate abundance within a homogeneous habitat",
            [
                "A transect is used only to capture flying insects, whereas a quadrat measures wind speed",
                "Random quadrats must always be placed in a straight line from north to south",
                "A line transect measures water depth in the abyssal ocean",
            ],
            "Whenever an environmental gradient exists (intertidal rocky shore, hillside catenas, pond margin), a line or belt transect is used to map zonation and gradual community turnover.",
        ),
    ]
    for q, corr, dists, exp in topic4:
        raw_questions.append((q, corr, dists, exp))

    # =========================================================================
    # TOPIC 5: CELL STRUCTURE AND ORGANIZATION (35 Questions — Hard & Medium)
    # =========================================================================
    topic5 = [
        (
            "Compare the sedimentation coefficients (Svedberg units, S) of intact ribosomes and their large and small subunits in Prokaryotes (plus mitochondria/chloroplasts) versus Eukaryotic cytosol:",
            "Prokaryotes have 70S ribosomes composed of a 50S large subunit and a 30S small subunit; Eukaryotes have 80S cytosolic ribosomes composed of a 60S large subunit and a 40S small subunit",
            [
                "Prokaryotes have 70S ribosomes (40S + 30S); Eukaryotes have 80S ribosomes (50S + 30S)",
                "Prokaryotes have 80S ribosomes (60S + 20S); Eukaryotes have 70S ribosomes (50S + 20S)",
                "Prokaryotes lack ribosomes completely, whereas Eukaryotes have 100S ribosomes",
            ],
            "Svedberg units (S) measure centrifugal sedimentation rate (which depends on both mass and 3D shape/surface area, so they are non-additive): Prokaryotic 70S = 50S + 30S; Eukaryotic cytosolic 80S = 60S + 40S.",
        ),
        (
            "In plant water relations, the water potential (Ψ_w) of a plant cell is given by Ψ_w = Ψ_s + Ψ_p, where Ψ_s is solute (osmotic) potential and Ψ_p is pressure (turgor) potential. A plant cell with solute potential Ψ_s = -0.8 MPa and turgor pressure Ψ_p = +0.3 MPa is placed in an external sucrose solution of water potential Ψ_ext = -0.3 MPa. Which way will water move, and at what Ψ_p will the cell reach equilibrium?",
            "Water moves INTO the cell (from -0.3 MPa to -0.5 MPa) until turgor pressure rises to Ψ_p = +0.5 MPa (making cell Ψ_w = -0.3 MPa)",
            [
                "Water moves OUT of the cell (exosmosis) causing incipient plasmolysis",
                "No net water movement occurs because Ψ_p equals |Ψ_ext|",
                "Water moves INTO the cell until Ψ_p reaches +0.8 MPa",
            ],
            "Initially, cell Ψ_w = -0.8 + 0.3 = -0.5 MPa. Since water always moves passively from higher (less negative) water potential (-0.3 MPa) to lower (more negative) water potential (-0.5 MPa), water enters the cell by endosmosis until Ψ_w(cell) = -0.3 MPa, i.e., -0.8 + Ψ_p = -0.3 ⇒ Ψ_p = +0.5 MPa.",
        ),
        (
            "What are the values of Water Potential (Ψ_w), Solute Potential (Ψ_s), and Pressure Potential (Ψ_p) in a fully FLACCID (incipiently plasmolyzed) plant cell versus a fully TURGID plant cell immersed in pure water (Ψ_w = 0 MPa)?",
            "In a fully flaccid cell: Ψ_p = 0, so Ψ_w = Ψ_s (most negative); in a fully turgid cell in pure water: Ψ_p = |Ψ_s|, so Ψ_w = 0 MPa",
            [
                "In a flaccid cell: Ψ_w = 0 MPa; in a turgid cell: Ψ_p = 0 MPa",
                "In both flaccid and turgid cells, Ψ_s is positive (+1.0 MPa)",
                "In a turgid cell, Ψ_w is more negative than Ψ_s",
            ],
            "At incipient plasmolysis (flaccid state), the protoplast exerts zero turgor pressure against the wall (Ψ_p = 0), so Ψ_w = Ψ_s. When fully turgid in pure water (Ψ_w = 0), inward wall pressure balances osmotic entry (Ψ_p = -Ψ_s), making net Ψ_w = Ψ_s + Ψ_p = 0.",
        ),
        (
            "In the Singer and Nicolson (1972) Fluid Mosaic Model of the plasma membrane, how does cholesterol regulate membrane fluidity in animal cells across changing temperatures?",
            "Cholesterol acts as a bidirectional fluidity buffer: at high temperatures it restricts excessive phospholipid acyl-chain movement (reducing fluidity), whereas at low temperatures it prevents close packing and crystallization of fatty acid tails (maintaining fluidity)",
            [
                "Cholesterol forms hydrophilic pores for passive transport of glucose and Na+ ions",
                "Cholesterol solidifies the membrane completely at 37°C",
                "Cholesterol is found exclusively in bacterial and plant cell walls",
            ],
            "Intercalated between phospholipid tails, rigid steroid rings of cholesterol immobilize the proximal hydrocarbon chains at warm temperatures while preventing tight van der Waals gel-phase packing at cold temperatures.",
        ),
        (
            "Which statement accurately describes the stoichiometry and mechanism of the electrogenic Na+/K+-ATPase pump in animal plasma membranes?",
            "For every 1 molecule of ATP hydrolyzed, it actively pumps 3 Na+ ions OUT of the cell and 2 K+ ions INTO the cell against their electrochemical gradients, helping maintain a negative resting membrane potential",
            [
                "It pumps 2 Na+ ions INTO the cell and 3 K+ ions OUT of the cell by facilitated diffusion without ATP",
                "It pumps 3 Na+ and 3 K+ out of the cell simultaneously",
                "It operates only in dead xylem vessels",
            ],
            "The Na+/K+-ATPase is a P-type primary active transporter that exports 3 Na+ and imports 2 K+ per ATP hydrolyzed, consuming up to ~25–30% of a resting mammal's ATP and generating a net outward positive current.",
        ),
        (
            "Compare the microtubule arrangement in the cross-section of a eukaryotic cilium/flagellum shaft (axoneme) versus a centriole or basal body:",
            "The cilium/flagellum axoneme has a '9 + 2' array (9 peripheral microtubule doublets with dynein arms surrounding 2 central singlets), whereas the centriole/basal body has a '9 + 0' array (9 peripheral microtubule triplets and no central microtubules)",
            [
                "The axoneme has a '9 + 0' array of triplets, whereas the centriole has a '9 + 2' array of doublets",
                "Both eukaryotic and bacterial flagella consist of a '9 + 2' microtubule array powered by dynein",
                "Eukaryotic flagella are made of flagellin protein driven by a proton motive force, whereas centrioles are made of actin",
            ],
            "Eukaryotic undulipodia (cilia/flagella) have a 9+2 microtubule doublet axoneme powered by axonemal dynein ATPase; basal bodies and centrioles have 9 peripheral triplets and no central pair (9+0). Bacterial flagella lack microtubules entirely and are solid rotating rods of flagellin driven by H+/Na+ gradients.",
        ),
        (
            "What is the specialized metabolic function of 'glyoxysomes' (a specialized type of peroxisome) found in the fat-storing cotyledons/endosperm of germinating oilseeds (such as castor bean Ricinus, groundnut, and sunflower)?",
            "They contain enzymes of the glyoxylate cycle (isocitrate lyase and malate synthase) that convert stored fatty acids (via β-oxidation and acetyl-CoA) into succinate and carbohydrates (gluconeogenesis) for the growing seedling before photosynthesis begins",
            [
                "They perform the light-dependent photolysis of water in green leaves",
                "They synthesize ribosomal subunits from rRNA",
                "They digest engulfed bacteria in mammalian neutrophils",
            ],
            "Animals cannot convert fatty acids (acetyl-CoA) into net glucose because two carbons are lost as CO2 in the Krebs cycle; germinating oilseeds use glyoxysomes (with isocitrate lyase and malate synthase) to bypass those decarboxylation steps and convert stored lipids into sucrose.",
        ),
        (
            "Trace the correct intracellular pathway (endomembrane secretory pathway) followed by a newly synthesized secretory glycoprotein (such as insulin or a digestive zymogen) from translation to exocytosis:",
            "Bound ribosomes on Rough ER → Rough ER lumen (core glycosylation & folding) → Transition vesicles → cis-Golgi face → medial/trans-Golgi cisternae → trans-Golgi network → Secretory vesicles → Plasma membrane (exocytosis)",
            [
                "Free cytosolic ribosomes → Smooth ER → Lysosome → Mitochondrion → Nucleus → Plasma membrane",
                "Nucleolus → trans-Golgi → cis-Golgi → Rough ER → Peroxisome → Plasma membrane",
                "Smooth ER → Chloroplast stroma → Rough ER → Vacuole",
            ],
            "Polypeptides destined for secretion bear an N-terminal signal peptide recognized by SRP, directing co-translational translocation into the Rough ER lumen, followed by vesicular transport to the cis-Golgi, maturation through to the trans-Golgi, and secretory vesicle exocytosis.",
        ),
        (
            "What are the primary metabolic functions of the Smooth Endoplasmic Reticulum (SER) in mammalian hepatocytes (liver cells), adrenal cortex/Leydig cells, and skeletal muscle cells (sarcoplasmic reticulum) respectively?",
            "Hepatocytes: detoxification of drugs/poisons via cytochrome P450 and glycogenolysis; Adrenal cortex/Leydig cells: biosynthesis of steroid hormones and phospholipids; Skeletal muscle: sequestration and rapid release of Ca²+ ions to trigger contraction",
            [
                "Hepatocytes: translation of albumin; Leydig cells: DNA replication; Skeletal muscle: ATP synthesis",
                "All three cell types use Smooth ER exclusively for digesting worn-out mitochondria",
                "Smooth ER synthesizes cellulose and pectin for the extracellular matrix",
            ],
            "Smooth ER lacks ribosomes and specializes in lipid/steroid biosynthesis, hepatic xenobiotic detoxification (hydroxylation), carbohydrate metabolism (glucose-6-phosphatase), and Ca²+ storage in the sarcoplasmic reticulum.",
        ),
        (
            "Which of the following organelles in a eukaryotic plant leaf cell are bounded by a DOUBLE membrane, a SINGLE membrane, and NO membrane (non-membranous) respectively?",
            "Double membrane: Nucleus, Mitochondrion, Chloroplast; Single membrane: Central Vacuole (tonoplast), Lysosome, Peroxisome, Golgi, ER; Non-membranous: Ribosome, Nucleolus, Centrosome/Cytoskeleton",
            [
                "Double membrane: Lysosome and Vacuole; Single membrane: Mitochondrion and Ribosome; Non-membranous: Chloroplast",
                "Double membrane: Ribosome and Golgi; Single membrane: Nucleus; Non-membranous: Peroxisome",
                "All eukaryotic organelles are bounded by a double phospholipid bilayer",
            ],
            "Only the nucleus (nuclear envelope) and endosymbiotic organelles (mitochondria and plastids) possess double membranes; endomembrane and microbody organelles (ER, Golgi, lysosome, vacuole/tonoplast, peroxisome) have a single membrane; ribosomes, nucleoli, and centrioles have zero lipid membranes.",
        ),
        (
            "How does the chemical composition of the cell wall differ across Bacteria, Archaea, Fungi, Algae/Plants, and Diatoms?",
            "Bacteria: Peptidoglycan (murein with NAM and NAG); Archaea: Pseudomurein or S-layer glycoproteins (no peptidoglycan); Fungi: Chitin (β-1,4-N-acetylglucosamine); Plants: Cellulose, hemicellulose, pectin, and lignin; Diatoms: Silicified frustule (hydrated silica SiO2)",
            [
                "Bacteria: Cellulose; Fungi: Peptidoglycan; Plants: Chitin; Diatoms: Calcium carbonate",
                "Archaea: Peptidoglycan; Bacteria: Chitin; Fungi: Pectin",
                "All five groups have cell walls made of β-1,4-linked D-glucose",
            ],
            "Peptidoglycan (cross-linked N-acetylglucosamine and N-acetylmuramic acid) is unique to Eubacteria (targeted by penicillin and lysozyme); Archaea lack muramic acid; Fungi use chitin; Plants use cellulose; Diatoms construct ornate two-valved silica frustules.",
        ),
        (
            "Why are Gram-negative bacteria (e.g., Escherichia coli, Salmonella, Vibrio cholerae) generally more resistant to penicillin and lysozyme than Gram-positive bacteria (e.g., Staphylococcus aureus, Bacillus subtilis)?",
            "Gram-negative bacteria possess an outer lipopolysaccharide (LPS) membrane external to a thin periplasmic peptidoglycan layer, which shields the peptidoglycan from lysozyme and blocks entry of hydrophobic/large beta-lactam antibiotics",
            [
                "Gram-negative bacteria have a 10-times thicker peptidoglycan wall than Gram-positive bacteria",
                "Gram-negative bacteria lack a plasma membrane",
                "Gram-positive bacteria contain lipopolysaccharide (endotoxin) and porin channels",
            ],
            "Gram-positive bacteria have a thick, exposed multi-layered peptidoglycan wall containing teichoic acids (retaining crystal violet-iodine complex → purple). Gram-negative bacteria have a thin peptidoglycan layer sandwiched between the inner membrane and an outer LPS/phospholipid membrane (decolorized by alcohol and counterstained pink/red by safranin).",
        ),
        (
            "Match the three classes of plastids in plant cells — Chloroplasts, Chromoplasts, and Leucoplasts (specifically Amyloplasts, Elaioplasts, and Aleuroplasts/Proteinoplasts) — with their functions:",
            "Chloroplasts: photosynthesis (chlorophyll a/b); Chromoplasts: carotenoid pigments (lycopene, xanthophyll) giving red/orange/yellow color to flowers and ripe fruits; Amyloplasts: starch storage; Elaioplasts: lipid/oil storage; Aleuroplasts: protein storage",
            [
                "Amyloplasts: oil storage; Elaioplasts: protein storage; Aleuroplasts: starch storage",
                "Chromoplasts: colourless root storage plastids; Leucoplasts: red pigment plastids in tomato",
                "All plastids are irreversible and cannot interconvert during fruit ripening",
            ],
            "All plastids develop from proplastids and can interconvert (e.g., green chloroplasts transform into red lycopene-rich chromoplasts as a tomato ripens). Colourless leucoplasts differentiate into amyloplasts (starch in potato tuber), elaioplasts (oils), and aleuroplasts (proteins in seeds).",
        ),
        (
            "Examine the levels of cellular organization in the green algae (Chlorophyta): Chlamydomonas, Pandorina, Eudorina, Volvox, and Spirogyra. Which statement accurately explains why Volvox is considered the pinnacle of the 'colonial (coenobial)' evolutionary line?",
            "In a Volvox coenobium (500–50,000 biflagellate cells connected by cytoplasmic bridges), there is a clear division of labour and polarity between numerous non-reproductive somatic cells (locomotion/photosynthesis) and a few specialized posterior reproductive cells (gonidia and gametes)",
            [
                "Volvox is a multicellular vascular plant with true xylem and phloem tissues",
                "Chlamydomonas is filamentous, whereas Spirogyra is a motile spherical colony",
                "In Volvox, every cell is completely independent without cytoplasmic protoplasmic strands",
            ],
            "The volvocine series (Chlamydomonas [unicellular] → Gonium → Pandorina → Eudorina → Volvox [large hollow coenobium]) demonstrates the evolutionary transition from unicellularity to somatic-reproductive division of labour connected by plasmodesmata-like cytoplasmic bridges.",
        ),
        (
            "Which organisms or structures constitute genuine exceptions or challenges to the classical Schleiden and Schwann Cell Theory ('all organisms are composed of discrete uninucleate cells')?",
            "Viruses/viroids (acellular obligate parasites), coenocytic fungal hyphae (Mucor/Rhizopus), siphonaceous algae (Vaucheria, Caulerpa), plasmodial slime moulds, and multinucleate skeletal muscle fibres (syncytia)",
            [
                "Paramecium only, because it is smaller than a bacterium",
                "Red blood cells only, because they divide rapidly in the bloodstream",
                "Onion epidermal cells and Elodea leaf cells",
            ],
            "Viruses are acellular nucleoprotein particles; coenocytic hyphae (Zygomycetes) and siphonaceous algae (Vaucheria) consist of a continuous multinucleate protoplasmic mass without cross-walls (septa) dividing it into individual cell units.",
        ),
        (
            "What contribution did Rudolf Virchow (1855) make to modern Cell Theory with his aphorism 'Omnis cellula e cellula'?",
            "He refuted Schleiden's 'free-cell formation' (spontaneous crystallization) hypothesis and established that all new cells arise ONLY by the division of pre-existing living cells",
            [
                "He discovered the dead cork cell walls of Quercus suber using a simple magnifying glass in 1665",
                "He invented the transmission electron microscope in 1931",
                "He proved that DNA is a double helix",
            ],
            "Hooke (1665) coined the term 'cell' from dead cork; Leeuwenhoek (1674) observed live 'animalcules'; Schleiden (1838) and Schwann (1839) formulated cell theory for plants and animals; Virchow (1855) added 'Omnis cellula e cellula' (biogenesis at the cellular level).",
        ),
        (
            "Compare the three major protein filaments of the eukaryotic cytoskeleton (Microtubules, Microfilaments, and Intermediate Filaments) in terms of subunit protein, diameter, and primary cellular roles:",
            "Microtubules: α/β-tubulin dimers (~25 nm hollow tubes — mitotic spindle, cilia/flagella, kinesin/dynein tracks); Microfilaments: G-actin/F-actin (~7 nm — amoeboid movement, cleavage furrow, cytoplasmic streaming, muscle contraction); Intermediate filaments: keratins/lamins/vimentin (~10 nm — mechanical tensile strength, nuclear lamina)",
            [
                "Microtubules: actin (~7 nm); Microfilaments: tubulin (~25 nm); Intermediate filaments: myosin (~50 nm)",
                "All three filaments are composed of cellulose microfibrils",
                "Intermediate filaments undergo rapid treadmilling and power flagellar beating",
            ],
            "Microtubules (25 nm, α/β-tubulin) resist compression and guide organelle transport; actin microfilaments (7 nm) generate contractile/motile tension with myosin; intermediate filaments (8–12 nm, keratins, nuclear lamins) are stable rope-like polymers providing mechanical resilience.",
        ),
        (
            "In multicellular animals, distinguish functionally among the three major types of intercellular junctions: Tight Junctions (Zonula occludens), Desmosomes (Macula adherens), and Gap Junctions (Nexus):",
            "Tight junctions seal adjacent epithelial cells to prevent paracellular leakage; Desmosomes (linked to intermediate filaments via cadherins) act as spot-welds providing mechanical shear resistance; Gap junctions (connexons) form cytoplasmic channels for direct passage of ions and small molecules (<1 kDa)",
            [
                "Tight junctions allow free passage of proteins between cells; Gap junctions waterproof the epidermis",
                "Desmosomes are found in plant cell walls and are identical to plasmodesmata",
                "Gap junctions connect actin filaments to the extracellular basement membrane",
            ],
            "Gap junctions in animals (and plasmodesmata in plants) are communicating junctions that electrically and metabolically couple adjacent cells (e.g., in cardiac muscle intercalated discs); tight junctions form occluding barriers; desmosomes and hemidesmosomes are anchoring junctions.",
        ),
        (
            "Why does a mature mammalian erythrocyte (red blood cell) lack a nucleus, mitochondria, and endoplasmic reticulum, and how does this structural specialization optimize its physiological function?",
            "Extrusion of the nucleus and organelles maximizes intracellular volume for packing ~280 million hemoglobin molecules, gives a biconcave disc shape with high surface-area-to-volume ratio and deformability through capillaries, and ensures the cell generates ATP strictly by anaerobic glycolysis without consuming any of the O2 it transports",
            [
                "It allows the red blood cell to divide rapidly by mitosis inside narrow capillaries",
                "It enables the red blood cell to perform oxidative phosphorylation on its plasma membrane",
                "Bird and frog erythrocytes also lack nuclei at maturity",
            ],
            "Unlike nucleated avian/amphibian/reptilian RBCs, mammalian RBCs enucleate and lose mitochondria during erythropoiesis; lacking mitochondria means they never consume the oxygen they carry, relying 100% on Embden-Meyerhof glycolysis and the pentose phosphate pathway.",
        ),
        (
            "In freshwater protozoa such as Amoeba proteus and Paramecium caudatum, what is the primary physiological role of the 'contractile vacuole', and what happens if the organism is transferred to a marine (isosmotic) medium or treated with cyanide (which blocks ATP synthesis)?",
            "It performs osmoregulation by actively expelling excess water that enters continuously by endosmosis; in an isosmotic medium or after cyanide treatment, the frequency of contraction drops sharply (and with cyanide, the cell swells and lyses in freshwater)",
            [
                "It digests engulfed bacteria using acid hydrolases",
                "It stores starch granules for winter dormancy",
                "In distilled water, the contractile vacuole stops pulsating completely",
            ],
            "Freshwater protozoans are hypertonic to pond water, so water constantly enters by osmosis. The contractile vacuole uses proton-pumping V-type ATPases on its spongiome tubules to accumulate and expel water; in distilled water pulsation rate increases, whereas in isotonic saline or ATP-Synthesis inhibition it ceases.",
        ),
        (
            "What happens when human red blood cells and onion epidermal cells are placed in (i) distilled water (hypotonic) and (ii) 10% NaCl solution (hypertonic)?",
            "In distilled water: RBCs swell and burst (hemolysis), whereas onion cells become fully turgid without bursting due to wall pressure; In 10% NaCl: RBCs shrink and develop notched margins (crenation), whereas onion cells undergo plasmolysis (protoplast pulls away from the cell wall)",
            [
                "In distilled water: RBCs crenate and onion cells plasmolyze; In 10% NaCl: RBCs hemolyze",
                "Both RBCs and onion cells burst in distilled water",
                "In plasmolyzed onion cells, the space between the cell wall and shrunken protoplast is filled with air",
            ],
            "Note also a classic exam trap: in a plasmolyzed plant cell, because the cellulose cell wall is freely permeable to both water and solutes, the space between the cell wall and the shrunken plasma membrane is filled with the external hypertonic solution, NOT air or vacuum!",
        ),
        (
            "In a plasmolyzed plant cell immersed in a hypertonic sucrose solution, what occupies the space between the rigid cellulose cell wall and the shrunken protoplast (plasma membrane)?",
            "The external hypertonic sucrose solution (because the cellulose cell wall is fully permeable to water and dissolved solutes)",
            [
                "Pure distilled water",
                "Air and carbon dioxide gas",
                "Cytoplasmic matrix and ribosomes",
            ],
            "The cellulose cell wall is a coarse meshwork that is freely permeable; only the plasma membrane (and tonoplast) is selectively permeable. Thus the external hypertonic solution passes freely through the cell wall to fill the gap outside the retreating protoplast.",
        ),
        (
            "Which enzyme serves as the signature biochemical marker for 'peroxisomes', protecting the eukaryotic cell from toxic hydrogen peroxide (H2O2) generated by flavin oxidases?",
            "Catalase (which decomposes 2H2O2 → 2H2O + O2)",
            [
                "Acid phosphatase (marker for lysosomes)",
                "Succinate dehydrogenase (marker for inner mitochondrial membrane)",
                "Glucose-6-phosphatase (marker for endoplasmic reticulum)",
            ],
            "Peroxisomes contain oxidative enzymes (urate oxidase, D-amino acid oxidase, β-oxidation enzymes) that produce H2O2, and abundant catalase that immediately degrades H2O2 into water and oxygen.",
        ),
        (
            "If a cell's nucleolus is selectively destroyed by a microbeam of ultraviolet radiation, which cellular process will be MOST directly and immediately arrested?",
            "Transcription of ribosomal RNA (45S pre-rRNA) and assembly of 40S and 60S ribosomal subunits, leading to a halt in cytoplasmic protein synthesis",
            [
                "Replication of mitochondrial DNA",
                "β-oxidation of fatty acids in the peroxisome",
                "Passive diffusion of O2 across the plasma membrane",
            ],
            "The nucleolus (organized around Nucleolar Organizer Regions, NORs, on acrocentric chromosomes) is the site of RNA Polymerase I transcription of rRNA genes and assembly of ribosomal subunits.",
        ),
        (
            "What is the resolving power (limit of resolution, d) of a microscope according to Abbe's equation d = 0.61λ / (n sin α), and why does a Transmission Electron Microscope (TEM) achieve ~1,000 times better resolution (~0.2 nm) than a compound light microscope (~200 nm)?",
            "Resolution improves (d becomes smaller) as wavelength λ decreases and numerical aperture (n sin α) increases; an accelerated electron beam has a de Broglie wavelength ~100,000 times shorter than visible light",
            [
                "Electrons travel faster than light in a vacuum",
                "Glass objective lenses are used in TEM with immersion oil of refractive index 100",
                "TEM uses infrared light of wavelength 1000 nm",
            ],
            "By Abbe's equation, the minimum resolvable distance d is directly proportional to wavelength λ. Visible light (λ ≈ 400–700 nm) limits light microscopy to ~200 nm (0.2 µm), whereas high-voltage electron beams (λ ≈ 0.004 nm) focused by electromagnetic lenses achieve ~0.1–0.2 nm resolution.",
        ),
        (
            "Why is cedarwood immersion oil (refractive index n ≈ 1.515, matching glass) placed between the glass slide and the 100× objective lens in high-power light microscopy?",
            "It prevents the refraction (bending and scattering) of oblique light rays passing from the glass slide into air (n = 1.0), thereby increasing the Numerical Aperture (n sin α) and improving resolution and brightness",
            [
                "It stains bacterial flagella purple",
                "It cools the specimen so live bacteria do not boil",
                "It decreases the numerical aperture to zero",
            ],
            "Because immersion oil has the same refractive index as glass (n = 1.515), light rays emerging at wide angles from the specimen enter the objective lens without refracting away at a glass-air interface, maximizing Numerical Aperture (NA = n sin α).",
        ),
        (
            "In plant anatomy, distinguish between the three simple permanent ground tissues — Parenchyma, Collenchyma, and Sclerenchyma — in terms of cell wall thickening and protoplast viability at maturity:",
            "Parenchyma: living cells with thin, uniform primary cellulose walls; Collenchyma: living cells with unevenly thickened non-lignified primary walls (cellulose + pectin at corners) providing flexible support to young stems/petioles; Sclerenchyma (fibres & sclereids): dead cells at maturity (lacking protoplast) with thick, heavily lignified secondary walls providing rigid mechanical support",
            [
                "Collenchyma cells are dead and heavily lignified at maturity, whereas Sclerenchyma cells are living and photosynthetic",
                "Parenchyma cells have thick suberized walls and lack nuclei",
                "Sclerenchyma is the only tissue capable of mitotic cell division",
            ],
            "Collenchyma provides plastic, extensible mechanical support to growing organs (young dicot stems, leaf midribs) because its cells remain alive and have non-lignified pectocellulosic corner thickenings; sclerenchyma (fibres and stone cells/sclereids) deposits rigid lignin and undergoes programmed cell death at maturity.",
        ),
        (
            "In the phloem tissue of angiosperms, mature Sieve Tube Elements lack a nucleus, ribosomes, and central vacuole, yet remain living and functional in translocating sucrose. How are their metabolic functions maintained?",
            "They are ontogenetically and physiologically supported by adjacent nucleated 'Companion Cells' (derived from the same mother cell) connected via numerous branched pore-plasmodesmata",
            [
                "They are dead hollow tubes just like xylem vessels and require no ATP",
                "They are maintained by adjacent dead sclerenchyma fibres",
                "They absorb nuclei from the transpiration stream",
            ],
            "Sieve tube elements and companion cells arise from the division of the same meristematic mother cell; the metabolically active companion cell (dense cytoplasm, abundant mitochondria, nucleus) supplies ATP and proteins to the enucleate sieve tube element via plasmodesmata.",
        ),
        (
            "In mammalian histology, match the following epithelial types with their exact anatomical locations: (i) Simple squamous epithelium (endothelium/mesothelium), (ii) Ciliated pseudostratified columnar epithelium with goblet cells, (iii) Transitional epithelium (urothelium), (iv) Stratified squamous keratinized epithelium:",
            "(i) Lung alveoli and Bowman's capsule / blood vessel lining; (ii) Trachea and bronchi (respiratory tract); (iii) Urinary bladder and ureters; (iv) Epidermis of mammalian skin",
            [
                "(i) Urinary bladder; (ii) Epidermis of skin; (iii) Lung alveoli; (iv) Trachea",
                "(i) Trachea; (ii) Small intestine; (iii) Kidney tubules; (iv) Bone matrix",
                "(i) Epidermis; (ii) Urinary bladder; (iii) Trachea; (iv) Alveoli",
            ],
            "Simple squamous provides a thin diffusion barrier (alveoli, capillaries); ciliated pseudostratified columnar forms the mucociliary escalator of the trachea; transitional epithelium (urothelium) stretches in the urinary bladder; keratinized stratified squamous protects dry skin against abrasion and desiccation.",
        ),
        (
            "How do Tendons and Ligaments differ in both anatomical connection and histological fiber composition?",
            "Tendons connect skeletal muscle to bone and consist of dense regular collagenous connective tissue (high tensile strength, inelastic); Ligaments connect bone to bone at joints and contain a rich network of both collagen and elastic (elastin) fibres allowing controlled stretch",
            [
                "Tendons connect bone to bone and are highly elastic; Ligaments connect muscle to bone and are completely rigid",
                "Tendons are composed of hyaline cartilage, whereas ligaments are composed of smooth muscle",
                "Both tendons and ligaments are epithelial tissues lacking extracellular matrix",
            ],
            "Tendons (muscle-to-bone) transmit contractile force without energy loss via parallel bundles of Type I collagen; ligaments (bone-to-bone) stabilize joints and contain elastin fibers (especially yellow ligaments like ligamentum flavum) to permit joint mobility without tearing.",
        ),
        (
            "As a cell grows larger in radius (r) without changing its spherical shape, how does its surface-area-to-volume ratio (SA : V) change, and why does this impose a physical upper limit on cell size?",
            "Surface area increases as r² (4πr²) while volume increases faster as r³ (4/3 πr³), so the SA : V ratio decreases as 3/r; beyond a critical size, the plasma membrane surface area becomes insufficient to exchange O2, nutrients, and wastes fast enough to support the metabolic volume",
            [
                "The SA : V ratio increases exponentially as r³, causing the cell membrane to rupture from excess oxygen",
                "Surface area and volume increase at the exact same linear rate",
                "Larger cells have a higher SA : V ratio than smaller cells",
            ],
            "Because SA/V = (4πr²) / (4/3 πr³) = 3/r, doubling a cell's radius halves its SA/V ratio and increases intracellular diffusion distances, compelling large organisms to be multicellular or adopt flattened/elongated/microvilli-folded geometries.",
        ),
        (
            "What is 'autophagy' vs 'autolysis' mediated by lysosomes?",
            "Autophagy is the regulated self-digestion and recycling of worn-out intracellular organelles (e.g., damaged mitochondria) enclosed in autophagosomes during starvation or turnover; Autolysis is the wholesale self-destruction of an entire cell/tissue by the rupture of its lysosomal membranes (e.g., regression of a tadpole's tail during metamorphosis)",
            [
                "Autophagy is the synthesis of new lysosomes by the nucleus; Autolysis is photosynthesis in bacteria",
                "Autophagy occurs only after an animal dies, whereas autolysis occurs during mitosis",
                "Both processes occur exclusively in plant chloroplasts",
            ],
            "Lysosomes ('suicide bags', discovered by Christian de Duve) mediate heterophagy (digestion of endocytosed material), autophagy (targeted turnover of senescent organelles), and autolysis/programmed tissue regression (such as cathepsin-mediated resorption of the amphibian tadpole tail stimulated by thyroxine).",
        ),
        (
            "In bacterial cells, what are 'plasmids' and 'mesosomes'?",
            "Plasmids are small, circular, extrachromosomal double-stranded DNA molecules that replicate autonomously and carry non-essential adaptive genes (such as R-factors for antibiotic resistance or F-factors for conjugation); Mesosomes are infoldings of the bacterial plasma membrane",
            [
                "Plasmids are membrane-bound organelles that synthesize ATP; Mesosomes are 80S ribosomes",
                "Plasmids are linear RNA chromosomes inside the nucleolus",
                "Plasmids are found only in human red blood cells",
            ],
            "Bacterial plasmids (F-plasmids, R-plasmids, Col-plasmids) replicate independently of the main nucleoid chromosome and confer horizontal gene transfer and antibiotic resistance.",
        ),
        (
            "What is the 'endosymbiotic evidence' found inside BOTH mitochondria and chloroplasts that distinguishes them from all other cytoplasmic organelles?",
            "Both possess their own circular, histone-free dsDNA, 70S ribosomes (inhibited by chloramphenicol/erythromycin like bacteria, not cycloheximide), a double membrane (with cardiolipin/porins), and replicate by binary fission independently of mitosis",
            [
                "Both possess linear chromosomes with telomeres and 80S ribosomes inside a single membrane",
                "Both are synthesized de novo by the Golgi apparatus after every cell division",
                "Both contain peptidoglycan cell walls in human liver cells",
            ],
            "Mitochondria and plastids are semi-autonomous organelles retaining circular prokaryotic-type DNA, 70S ribosomes sensitive to bacterial translation inhibitors (streptomycin, tetracycline, chloramphenicol), and porin-containing outer membranes.",
        ),
        (
            "During facilitated diffusion (mediated by carrier permeases or channel proteins) versus simple diffusion across a lipid bilayer:",
            "Facilitated diffusion is passive (requires no ATP and moves solutes down their electrochemical gradient) but exhibits Michaelis-Menten-like saturation kinetics (V_max), structural specificity, and competitive inhibition when all carrier binding sites are occupied",
            [
                "Facilitated diffusion moves solutes against their concentration gradient using ATP",
                "Simple diffusion shows saturation kinetics at low solute concentrations",
                "Facilitated diffusion is non-specific and transports any macromolecule",
            ],
            "Both simple and facilitated diffusion are passive (ΔG < 0, downhill), but facilitated diffusion relies on finite numbers of membrane transport proteins (e.g., GLUT transporters, aquaporins, ion channels), so transport rate plateaus at V_max when carriers saturate.",
        ),
    ]
    for q, corr, dists, exp in topic5:
        raw_questions.append((q, corr, dists, exp))

    # =========================================================================
    # TOPIC 6: CHARACTERISTICS AND CLASSIFICATION OF LIVING THINGS (25 Questions)
    # =========================================================================
    topic6 = [
        (
            "Why do living organisms grow by 'intussusception' whereas non-living crystals (such as alum or copper sulfate crystals in a supersaturated solution) grow by 'accretion'?",
            "Intussusception is internal growth achieved by absorbing nutrients, metabolizing them into new protoplasm, and dividing cells from within; Accretion is external growth by the mere physical deposition of identical material layers on the outer surface",
            [
                "Accretion is internal protoplasmic synthesis, whereas intussusception is external crystal layering",
                "Both living animals and non-living crystals grow exclusively by accretion",
                "Intussusception occurs only in dead plant tissues",
            ],
            "Living growth (intussusception) is an intrinsic, irreversible increase in dry mass and protoplasm driven by anabolismexceeding catabolism from within; non-living crystal growth (accretion) is the extrinsic addition of molecules onto an existing surface.",
        ),
        (
            "In Carl Woese's (1990) Three-Domain System of classification based on 16S/18S ribosomal RNA (rRNA) sequence phylogeny, how is the traditional Kingdom Monera divided, and which unique membrane/cell wall features distinguish Domain Archaea from Domain Bacteria?",
            "Monera is split into Domain Bacteria and Domain Archaea (with all eukaryotes in Domain Eukarya); Archaea lack peptidoglycan in their cell walls, possess branched isoprenoid ETHER-linked membrane lipids (instead of unbranched ESTER-linked fatty acids), and have histone-like proteins and RNA polymerases more closely related to Eukarya",
            [
                "Archaea have ester-linked fatty acid membranes and thick peptidoglycan walls identical to E. coli",
                "Domain Archaea is more closely related to bacteriophages than to Eukarya",
                "Woese grouped Fungi and Archaea into a single prokaryotic domain",
            ],
            "16S rRNA phylogeny revealed that Archaea (methanogens, halophiles, thermoacidophiles) form a distinct domain sister to Eukarya: their membrane lipids have ether linkages to glycerol-1-phosphate (resistant to extreme heat/acid), they lack muramic acid/peptidoglycan, and their translation initiates with methionine (like eukaryotes) rather than formyl-methionine (like bacteria).",
        ),
        (
            "According to the International Code of Botanical/Zoological Nomenclature (ICBN/ICZN), which of the following scientific names for maize is written in the strictly CORRECT binomial format?",
            "Zea mays L. (printed in italics, with Genus capitalized, specific epithet in all lowercase, and author abbreviation 'L.' for Linnaeus in roman upright type)",
            [
                "Zea Mays (both words capitalized)",
                "zea mays (both words in lowercase)",
                "ZEA MAYS (printed in bold without italics or underlining)",
            ],
            "Rules of binomial nomenclature: (1) Generic name starts with a capital letter; (2) Specific epithet starts with a lowercase letter; (3) Both are italicized in print (or underlined separately when handwritten); (4) The authority citation (e.g., L.) follows in upright roman font.",
        ),
        (
            "Which taxonomic rule is violated by the statement 'Two organisms belonging to the same Order must also belong to the same Family'?",
            "In the taxonomic hierarchy (Domain → Kingdom → Phylum → Class → Order → Family → Genus → Species), Order is a HIGHER (broader) rank than Family; therefore two organisms in the same Order MUST belong to the same Class, Phylum, and Kingdom, but may belong to DIFFERENT Families",
            [
                "Family is a higher rank than Order and Class",
                "Two organisms in the same Genus can belong to different Kingdoms",
                "Species is the broadest taxonomic category",
            ],
            "Moving upward from any shared taxon (e.g., Order Carnivora), all higher taxa (Class Mammalia, Phylum Chordata, Kingdom Animalia) are necessarily shared; moving downward (Family Felidae vs. Family Canidae), members can diverge.",
        ),
        (
            "Why are Viruses classified outside Whittaker's Five Kingdoms at the borderline between living and non-living matter?",
            "Outside a host cell, virions are inert, acellular nucleoprotein particles that lack ribosomes, cytoplasm, and metabolic enzymes and can be crystallized like chemicals; inside a specific host cell, they replicate their genetic material (DNA or RNA, never both) and undergo mutation and evolution",
            [
                "Viruses possess both DNA and RNA simultaneously alongside 70S ribosomes",
                "Viruses can grow and divide by binary fission on sterile nutrient agar plates",
                "Viruses are sensitive to penicillin because of their peptidoglycan capsid",
            ],
            "W.M. Stanley (1935) crystallized Tobacco Mosaic Virus (TMV). Viruses are obligate intracellular parasites consisting of a nucleic acid core (either DNA or RNA) enclosed in a protein capsid (capsomeres), lacking autonomous energy metabolism or translation machinery.",
        ),
        (
            "Distinguish precisely between a 'Virus', a 'Viroid', and a 'Prion':",
            "A Virus has a DNA or RNA genome enclosed in a protein capsid; a Viroid (discovered by Diener) is a naked, low-molecular-weight circular single-stranded RNA molecule WITHOUT a protein coat that infects plants (e.g., potato spindle tuber viroid); a Prion (Prusiner) is an infectious misfolded protein (PrP^Sc) completely devoid of any nucleic acid (causing scrapie, mad cow BSE, and Creutzfeldt-Jakob disease)",
            [
                "A Viroid is a naked protein lacking RNA, whereas a Prion is a double-stranded DNA virus",
                "Prions infect only leguminous plants, whereas viroids cause human malaria",
                "All three possess a phospholipid envelope and 70S ribosomes",
            ],
            "Viruses = nucleic acid + protein capsid; Viroids = infectious naked circular ssRNA without protein coat (plant pathogens); Prions = proteinaceous infectious particles (β-sheet rich PrP^Sc) with zero nucleic acid that template conformational misfolding of normal cellular PrP^C in mammalian brains.",
        ),
        (
            "Why is Euglena viridis a classic taxonomic puzzle ('plant-animal' or mixotroph) placed in Kingdom Protista (Phylum Euglenophyta/Euglenozoa)?",
            "In sunlight it is holophytic (autotrophic), possessing chloroplasts with chlorophyll a and b and storing paramylon; in prolonged darkness with organic matter it is saprozoic (heterotrophic); yet like animals it lacks a cellulose cell wall (having a flexible proteinaceous pellicle), possesses a contractile vacuole, and swims via a flagellum guided by a photoreceptive eyespot (stigma)",
            [
                "It has a rigid chitin cell wall like fungi and a calcareous shell like molluscs",
                "It is a prokaryote lacking a nuclear membrane",
                "It reproduces exclusively by producing seeds and flowers",
            ],
            "Euglena combines plant-like characters (chlorophyll a & b, pyrenoids, autotrophic nutrition in light) with animal-like characters (proteinaceous pellicle instead of cellulose wall, anterior gullet/reservoir, stigma/paraflagellar photoreceptor, contractile vacuole, binary fission, and heterotrophic nutrition in darkness).",
        ),
        (
            "Distinguish the four major classes/phyla of Kingdom Fungi — Zygomycota (Phycomycetes), Ascomycota, Basidiomycota, and Deuteromycota (Fungi Imperfecti) — by their hyphal septation and sexual spores:",
            "Zygomycota (Rhizopus): aseptate coenocytic hyphae, sexual zygospores; Ascomycota (Saccharomyces, Penicillium, Neurospora): septate hyphae, endogenous sexual ascospores (usually 8) inside an ascus; Basidiomycota (Agaricus, Puccinia): septate dikaryotic hyphae with clamp connections, exogenous sexual basidiospores (4) on a basidium; Deuteromycota: known sexual stage absent",
            [
                "Zygomycota have septate hyphae and basidiospores; Basidiomycota are unicellular and lack septa",
                "Ascomycota produce motile flagellated zoospores in water",
                "Deuteromycota are photosynthetic algae",
            ],
            "Zygomycetes have coenocytic hyphae and form diploid zygospores; Ascomycetes (sac fungi) form 8 endogenous ascospores per ascus; Basidiomycetes (club fungi: mushrooms, rusts, smuts) form 4 exogenous basidiospores on a club-shaped basidium; Deuteromycetes (imperfect fungi) reproduce only asexually by conidia.",
        ),
        (
            "In Kingdom Plantae, compare the four major divisions — Bryophyta, Pteridophyta, Gymnospermae, and Angiospermae — with respect to vascular tissue (xylem/phloem), seed production, and fruit (ovary) enclosure:",
            "Bryophytes: non-vascular, non-seed (cryptogams); Pteridophytes: vascular, seedless (vascular cryptogams); Gymnosperms: vascular with naked seeds (ovules not enclosed in an ovary, usually lacking xylem vessels and companion cells except Gnetales); Angiosperms: vascular with seeds enclosed inside a true fruit (ripened ovary) and double fertilization",
            [
                "Pteridophytes produce naked seeds on cones, whereas Gymnosperms produce spores in sori",
                "Bryophytes possess true roots, stems, leaves, and lignified xylem vessels",
                "Gymnosperms exhibit double fertilization producing triploid endosperm",
            ],
            "Note also a key exam distinction: in Gymnosperms (Pinus, Cycas), the nutritive 'endosperm' (female gametophyte) is formed BEFORE fertilization and is HAPLOID (n), whereas in Angiosperms the endosperm is formed AFTER double fertilization and is TRIPLOID (3n)!",
        ),
        (
            "What is the ploidy of the nutritive endosperm tissue in a Gymnosperm seed (e.g., Pinus or Cycas) compared to that in a typical Angiosperm seed (e.g., Zea mays), and why?",
            "In Gymnosperms, the endosperm is HAPLOID (n) because it is the pre-fertilization female gametophyte tissue; in Angiosperms, the endosperm is TRIPLOID (3n) because it forms post-fertilization by triple fusion of one sperm nucleus (n) with two polar nuclei (n + n)",
            [
                "In both Gymnosperms and Angiosperms, the endosperm is triploid (3n)",
                "In Gymnosperms, the endosperm is diploid (2n); in Angiosperms, it is haploid (n)",
                "Gymnosperm seeds lack any nutritive tissue around the embryo",
            ],
            "This is one of the most frequently tested 100-level botany distinctions: gymnosperm endosperm = haploid (n) female prothallus developed before fertilization; angiosperm endosperm = triploid (3n) product of double fertilization.",
        ),
        (
            "In Kingdom Animalia, trace the evolutionary progression of body cavity (coelom) organization across Phylum Platyhelminthes, Phylum Nematoda, and Phylum Annelida (and higher phyla):",
            "Platyhelminthes (flatworms): Acoelomate (solid mesoderm/parenchyma with no body cavity between gut and body wall); Nematoda (roundworms): Pseudocoelomate (fluid-filled body cavity derived from blastocoel, lined by mesoderm externally but endoderm internally); Annelida (segmented worms): Eucoelomate / Schizocoelomate (true coelom completely lined by mesodermal peritoneum)",
            [
                "Platyhelminthes: Eucoelomate; Nematoda: Acoelomate; Annelida: Pseudocoelomate",
                "Cnidaria and Porifera are Eucoelomates with three germ layers",
                "Nematodes possess a true coelom divided by metameric septa",
            ],
            "Triploblastic bilaterians are classified by coelom architecture: Platyhelminthes are acoelomates; Nematoda and Rotifera are pseudocoelomates (hydrostatic skeleton where gut lacks a muscular mesodermal coat); Annelida, Mollusca, Arthropoda, Echinodermata, and Chordata are true coelomates (eucoelomates).",
        ),
        (
            "Which combination of symmetry, germ layers, and level of organization characterizes Phylum Porifera (sponges) versus Phylum Cnidaria (Coelenterata)?",
            "Porifera: Asymmetrical (or radially symmetrical), cellular grade of organization (no true tissues or organs), choanocytes (collar cells) lining a canal system with ostia and osculum; Cnidaria: Radially symmetrical, diploblastic (ectoderm and endoderm separated by mesoglea), tissue grade of organization, gastrovascular cavity (coelenteron) with a single opening, and stinging cnidocytes (nematocysts)",
            [
                "Porifera: Triploblastic with bilateral symmetry; Cnidaria: Asymmetrical with choanocytes",
                "Cnidaria possess a complete digestive tract with a separate mouth and anus",
                "Porifera possess a central nervous system and nematocysts",
            ],
            "Sponges (Parazoa) are at the cellular level of organization with flagellated choanocytes driving water through ostia → spongocoel → osculum; Cnidarians (Eumetazoa) are diploblastic radiata with tissue-level organization, a nerve net, and diagnostic cnidoblasts/nematocysts.",
        ),
        (
            "Match the specialized excretory/osmoregulatory organs with their correct invertebrate phyla/classes: (i) Flame cells (protonephridia), (ii) Nephridia (metanephridia), (iii) Malpighian tubules, (iv) Coxal glands / Book lungs, (v) Green (antennary) glands:",
            "(i) Platyhelminthes (Planaria, Taenia); (ii) Annelida (Lumbricus); (iii) Insecta & Myriapoda; (iv) Arachnida (spiders/scorpions); (v) Crustacea (crayfish/prawns)",
            [
                "(i) Annelida; (ii) Platyhelminthes; (iii) Crustacea; (iv) Insecta; (v) Mollusca",
                "(i) Insecta; (ii) Arachnida; (iii) Annelida; (iv) Crustacea; (v) Platyhelminthes",
                "(i) Nematoda; (ii) Cnidaria; (iii) Echinodermata; (iv) Porifera; (v) Mollusca",
            ],
            "Flame cells (solenocytes/protonephridia) occur in flatworms; paired segmental metanephridia in annelids; Malpighian tubules (excreting uric acid into the hindgut) in insects; coxal glands in arachnids; green/antennary glands in crustaceans.",
        ),
        (
            "How are the four major subphyla/classes of Phylum Arthropoda — Crustacea, Insecta (Hexapoda), Arachnida (Chelicerata), and Myriapoda (Chilopoda vs Diplopoda) — distinguished by body tagmata, antennae, and walking legs?",
            "Crustacea: cephalothorax + abdomen, 2 pairs of antennae (biramous appendages), ≥5 pairs of legs; Insecta: head + thorax + abdomen, 1 pair of antennae, 3 pairs of legs (6 legs); Arachnida: prosoma (cephalothorax) + opisthosoma (abdomen), 0 antennae (chelicerae + pedipalps), 4 pairs of legs (8 legs); Chilopoda (centipedes): 1 pair of legs per trunk segment (carnivorous); Diplopoda (millipedes): 2 pairs of legs per diplosegment (detritivorous)",
            [
                "Arachnida have 2 pairs of antennae and 3 pairs of legs; Insecta have 0 antennae and 4 pairs of legs",
                "Millipedes (Diplopoda) have 1 pair of legs per segment and poison claws; Centipedes have 2 pairs per segment",
                "Crustaceans lack antennae and breathe exclusively through tracheae",
            ],
            "Antennae count is a classic diagnostic key: Crustaceans = 2 pairs; Insects/Myriapods = 1 pair; Arachnids = 0 pairs (replaced by chelicerae and pedipalps). Walking legs: Insects = 3 pairs; Arachnids = 4 pairs.",
        ),
        (
            "Why is Phylum Echinodermata (starfish, sea urchins, sea cucumbers) placed near Phylum Chordata at the top of the invertebrate evolutionary tree despite adults having pentaradial symmetry?",
            "Because echinoderms are DEUTEROSTOMES (the embryonic blastopore becomes the anus and the mouth forms secondarily, with radial indeterminate cleavage and enterocoelous coelom formation, just like Chordates), and their bilateral bipinnaria/dipleurula larvae undergo secondary metamorphosis into pentaradial adults",
            [
                "Because adult starfish possess a dorsal hollow nerve cord and pharyngeal gill slits",
                "Because echinoderms are protostomes with chitinous exoskeletons",
                "Because echinoderms are warm-blooded (endothermic)",
            ],
            "Annelids, molluscs, and arthropods are Protostomes (blastopore → mouth, spiral determinate cleavage, schizocoely); Echinoderms and Chordates are Deuterostomes (blastopore → anus, radial indeterminate cleavage, enterocoely). Adult radial symmetry in echinoderms is secondary; their larvae are bilaterally symmetrical.",
        ),
        (
            "What are the FOUR fundamental diagnostic chordate characteristics present at some stage in the life cycle of all members of Phylum Chordata?",
            "A dorsal, hollow, tubular nerve cord; a flexible rod-like notochord dorsal to the gut; paired pharyngeal gill slits/pouches; and a post-anal tail",
            [
                "A bony vertebral column, four limbs, warm blood, and lungs",
                "A ventral solid double nerve cord, dorsal heart, and chitinous exoskeleton",
                "A water vascular system with tube feet and calcareous ossicles",
            ],
            "All chordates (Urochordata/tunicates, Cephalochordata/Amphioxus, and Vertebrata/Craniata) share four synapomorphies: notochord, dorsal hollow nerve cord, pharyngeal slits, and post-anal tail. Only Vertebrata replace the embryonic notochord with a vertebral column.",
        ),
        (
            "Compare the heart chambers, aortic circulation, and thermoregulation across the five major classes of Vertebrata: Pisces (bony/cartilaginous fish), Amphibia, Reptilia, Aves, and Mammalia:",
            "Pisces: 2-chambered venous heart (1 atrium, 1 ventricle), single circulation, poikilothermic; Amphibia: 3-chambered heart (2 atria, 1 ventricle), incomplete double circulation, poikilothermic; Reptilia: incompletely 4-chambered heart (except Crocodilia which have a complete 4-chambered heart), poikilothermic; Aves & Mammalia: complete 4-chambered heart (2 atria, 2 ventricles), complete double circulation, homoiothermic (endothermic) — with right systemic arch in Aves and left systemic arch in Mammalia",
            [
                "Amphibia have a 2-chambered heart; Pisces have a 3-chambered heart; Aves are poikilothermic",
                "Mammals have a right aortic arch and nucleated erythrocytes, whereas birds have a left aortic arch and enucleate erythrocytes",
                "All reptiles including lizards and snakes are homoiothermic with 2-chambered hearts",
            ],
            "Note the high-yield comparative anatomy details: Crocodilians have a 4-chambered heart (with the foramen of Panizza); Birds retain the RIGHT systemic aortic arch and have nucleated RBCs; Mammals retain the LEFT systemic aortic arch, have enucleate RBCs, a muscular diaphragm, and mammary glands.",
        ),
        (
            "How are the three living subclasses of Class Mammalia — Prototheria (Monotremata), Metatheria (Marsupialia), and Eutheria (Placentalia) — distinguished by their mode of reproduction?",
            "Prototheria (platypus, echidna): oviparous mammals that lay reptilian-like shelled eggs and nourish hatched young with milk secreted onto abdominal hair tufts (lack nipples); Metatheria (kangaroo, opossum): viviparous with a rudimentary yolk-sac placenta, giving birth to altricial embryonic young that crawl into a marsupium (pouch) to attach to a teat; Eutheria: viviparous with a complex chorioallantoic placenta",
            [
                "Prototheria are marsupials with pouches; Metatheria lay calcareous eggs",
                "Monotremes lack hair and mammary glands completely",
                "Eutherian mammals lay eggs in water like amphibians",
            ],
            "Monotremes (Prototheria: Ornithorhynchus platypus, Tachyglossus echidna) have a single cloacal opening and lay leathery eggs, yet possess hair and produce milk; Marsupials (Metatheria) complete development inside the maternal marsupium; Eutherians use a true allantoic/chorionic placenta.",
        ),
        (
            "Why are Amphibians (e.g., Rana, Bufo) restricted to moist habitats, whereas Reptiles, Birds, and Mammals (collectively the 'Amniotes') successfully colonized dry terrestrial environments?",
            "Amniotes evolved the cleidoic (amniotic) egg containing four extra-embryonic membranes — the amnion (enclosing amniotic fluid as a private pond around the embryo), chorion (gas exchange), allantois (metabolic waste storage & gas exchange), and yolk sac — along with internal fertilization and a keratinized waterproof epidermis",
            [
                "Amphibians have dry scaly skin and lay calcareous shelled eggs on desert sand",
                "Reptiles breathe through their skin and must spawn in freshwater ponds",
                "Only mammals possess an amnion; birds and reptiles lack extra-embryonic membranes",
            ],
            "The evolution of the amniotic egg (amnion, chorion, allantois, yolk sac) freed reptiles, birds, and mammals from returning to water for reproduction, while keratinized scales/feathers/skin and uricotelism/ureotelism prevented terrestrial desiccation.",
        ),
        (
            "Compare the primary nitrogenous excretory products of (1) aquatic bony fishes and amphibian tadpoles, (2) adult amphibians and mammals, and (3) insects, land snails, reptiles, and birds — and explain the ecological rationale:",
            "(1) Ammonia (ammonotelic — highly toxic and soluble, requiring abundant water for dilution across gills); (2) Urea (ureotelic — moderately soluble and much less toxic, synthesized via the hepatic ornithine/urea cycle); (3) Uric acid / urates (uricotelic — insoluble crystals/paste excreted with minimal water loss, essential for cleidoic eggs and arid terrestrial life)",
            [
                "(1) Uric acid; (2) Ammonia; (3) Urea",
                "Birds and reptiles excrete dilute ammonia so their eggs do not dehydrate",
                "Adult frogs excrete ammonia while aquatic tadpoles excrete solid uric acid",
            ],
            "Inside a closed shelled egg (birds/reptiles), soluble ammonia or urea would osmotically poison the embryo; precipitating nitrogenous waste as insoluble uric acid in the allantois conserves water and prevents toxicity.",
        ),
        (
            "In bacteriophages (viruses that infect bacteria, such as Phage T4 or Phage Lambda), distinguish between the 'lytic cycle' (virulent phage) and the 'lysogenic cycle' (temperate phage):",
            "In the lytic cycle, phage DNA hijacks host machinery to synthesize new virions and lyses the bacterial cell via lysozyme; in the lysogenic cycle, the phage DNA integrates into the host bacterial chromosome as a dormant 'prophage' and replicates passively along with host cell division until induced (e.g., by UV light) to enter the lytic cycle",
            [
                "In the lysogenic cycle, the entire protein capsid enters the bacterium and bursts it within 2 minutes",
                "In the lytic cycle, the phage repairs the bacterium's cell wall and confers immunity",
                "Bacteriophages are RNA viroids that infect only plant roots",
            ],
            "Temperate phages (like Phage λ) can integrate their genome into the host chromosome as a prophage (lysogeny, which can also mediate specialized transduction or lysogenic conversion as in Corynebacterium diphtheriae toxin), whereas virulent phages (T4) execute only the lytic cycle.",
        ),
        (
            "Which diagnostic anatomical features distinguish Monocotyledonous plants (Class Liliopsida, e.g., Zea mays, Oryza, Elaeis) from Dicotyledonous plants (Class Magnoliopsida, e.g., Mangifera, Hibiscus, Vigna)?",
            "Monocots: 1 cotyledon (scutellum), parallel venation, fibrous adventitious root system, scattered closed vascular bundles in stem (no cambium), and trimerous flowers (parts in 3s); Dicots: 2 cotyledons, reticulate (net) venation, taproot system, ring of open vascular bundles in stem (with vascular cambium for secondary thickening), and tetramerous/pentamerous flowers (parts in 4s or 5s)",
            [
                "Monocots: 2 cotyledons, net venation, taproot, open vascular bundles in a ring; Dicots: 1 cotyledon, parallel venation, scattered closed bundles",
                "Monocots undergo extensive secondary thickening via a vascular cambium ring in all grasses",
                "Dicots lack stomata on their leaves",
            ],
            "Monocots have 1 cotyledon, parallel leaf veins, fibrous roots, scattered closed stem vascular bundles, and floral parts in multiples of 3; Dicots have 2 cotyledons, reticulate veins, taproots, ringed open bundles with cambium, and floral parts in 4s or 5s.",
        ),
        (
            "In the classification of Kingdom Protista, match the four major protozoan groups (Sarcodina/Rhizopoda, Mastigophora/Flagellata, Ciliophora, and Sporozoa/Apicomplexa) with their locomotory organelles and representative examples:",
            "Sarcodina: pseudopodia (Amoeba, Entamoeba); Mastigophora: flagella (Trypanosoma, Giardia, Leishmania); Ciliophora: cilia and nuclear dimorphism with macronucleus + micronucleus (Paramecium, Balantidium); Sporozoa: no adult locomotory organelles, obligate endoparasites with an apical complex (Plasmodium, Toxoplasma)",
            [
                "Sporozoa: cilia (Plasmodium); Ciliophora: pseudopodia (Amoeba); Sarcodina: flagella (Trypanosoma)",
                "Mastigophora have macronuclei and micronuclei and move by pseudopodia",
                "All four groups are photosynthetic autotrophs",
            ],
            "Protozoan taxonomy is classically based on locomotion: Sarcodina use lobopodia/filopodia; Mastigophora use flagella; Ciliophora use cilia and exhibit nuclear dimorphism (vegetative polyploid macronucleus + reproductive diploid micronucleus); Apicomplexa (Sporozoa) lack cilia/flagella in mature stages (except microgametes) and use an apical complex to invade host cells.",
        ),
        (
            "What is the biological significance of 'homeostasis' as a fundamental characteristic of living organisms, and how does 'negative feedback' differ from 'positive feedback'?",
            "Homeostasis (Claude Bernard / Walter Cannon) is the maintenance of a stable internal milieu within narrow physiological limits despite external fluctuations; Negative feedback counteracts a deviation from the set point (e.g., insulin/glucagon regulating blood glucose, thermoregulation), whereas Positive feedback amplifies a change until a culmination event occurs (e.g., oxytocin-driven uterine contractions in parturition, LH surge, or action potential Na+ influx)",
            [
                "Negative feedback amplifies deviations from the set point until the organism dies",
                "Positive feedback is the primary mechanism that keeps body temperature constant at 37°C",
                "Homeostasis means the internal environment is in static chemical equilibrium with zero energy expenditure",
            ],
            "Living systems are open thermodynamic systems maintaining a dynamic steady state far from equilibrium via ATP expenditure; >95% of homeostatic loops are negative feedback (opposing the stimulus), while positive feedback drives self-accelerating physiological cascades to completion.",
        ),
        (
            "In plant movements (irritability/sensitivity), distinguish between a 'Tropic movement (Tropism)', a 'Nastic movement (Nasty)', and a 'Tactic movement (Taxis)':",
            "Tropism: directional growth curvature of a plant organ toward (+) or away from (-) a unilateral stimulus (e.g., phototropism, gravitropism); Nastic movement: non-directional reversible response independent of the direction of the stimulus, driven by turgor changes in motor cells/pulvini (e.g., seismonasty/thigmonasty in Mimosa pudica, photonasty in flowers); Taxis: locomotion of an entire motile cell/organism toward or away from a stimulus (e.g., phototaxis in Chlamydomonas, chemotaxis in fern sperm)",
            [
                "Nastic movements are slow irreversible growth curvatures determined by the direction of light",
                "Tropisms are rapid turgor movements of the whole organism swimming in water",
                "Mimosa pudica folding its leaflets when touched is an example of positive phototropism",
            ],
            "When Mimosa pudica (sensitive plant) is touched, K+ ions and water rapidly exit the motor cells of the pulvinus at the base of the leaflets, causing immediate loss of turgor and folding — a classic non-directional thigmonastic/seismonastic turgor response.",
        ),
    ]
    for q, corr, dists, exp in topic6:
        raw_questions.append((q, corr, dists, exp))

    # =========================================================================
    # TOPIC 7: NUC CCMAS 100L 1ST SEMESTER ADDITIONS — Cell Division, Genetics & Evolution, Bioenergetics (25 Questions)
    # =========================================================================
    topic7 = [
        (
            "Arrange the five sequential substages of Prophase I of Meiosis in their exact chronological order and identify what key chromosomal event occurs at each substage:",
            "Leptotene (chromatin condenses into thin threads) → Zygotene (homologous chromosomes pair up in synapsis via the synaptonemal complex to form bivalents) → Pachytene (crossing over / genetic recombination between non-sister chromatids at recombination nodules) → Diplotene (synaptonemal complex dissolves, homologs separate slightly except at X-shaped chiasmata) → Diakinesis (terminalization of chiasmata, nucleolus and nuclear envelope break down)",
            [
                "Zygotene → Leptotene → Diplotene → Pachytene → Diakinesis",
                "Pachytene → Zygotene → Leptotene → Diakinesis → Diplotene",
                "Leptotene → Pachytene → Zygotene → Diplotene → Diakinesis",
            ],
            "Mnemonic: 'Lazy Zebra Pushes Dumb Donkey' (Leptotene → Zygotene [synapsis] → Pachytene [crossing over] → Diplotene [chiasmata visible] → Diakinesis [terminalization]).",
        ),
        (
            "A diploid somatic cell in the G1 phase of interphase has a chromosome number of 2n = 16 and a nuclear DNA content of 2C = 40 picograms (pg). What are the chromosome number and DNA content of this cell at (i) G2 phase, (ii) Metaphase of Mitosis, (iii) Anaphase of Mitosis (whole cell), (iv) Telophase I / Secondary oocyte in Meiosis, and (v) mature Haploid Gamete after Meiosis II?",
            "(i) G2: 16 chromosomes, 80 pg (4C); (ii) Metaphase: 16 chromosomes (32 chromatids), 80 pg (4C); (iii) Anaphase (whole cell before cytokinesis): 32 chromosomes, 80 pg (4C); (iv) After Meiosis I: 8 chromosomes (16 chromatids), 40 pg (2C); (v) Mature Gamete: 8 chromosomes, 20 pg (1C)",
            [
                "(i) G2: 32 chromosomes, 80 pg; (ii) Metaphase: 32 chromosomes, 40 pg; (v) Gamete: 8 chromosomes, 40 pg",
                "(i) G2: 16 chromosomes, 40 pg; (iv) After Meiosis I: 16 chromosomes, 20 pg",
                "(iii) Anaphase: 16 chromosomes, 160 pg; (v) Gamete: 4 chromosomes, 10 pg",
            ],
            "DNA replication in S phase doubles DNA content from 2C (40 pg) to 4C (80 pg) without changing chromosome count (still 16 centromeres = 16 chromosomes). At mitotic Anaphase, splitting centromeres doubles chromosome count in the cell transiently to 32 (4n, 4C). Meiosis I halves chromosome count to n = 8 (with 2C = 40 pg), and Meiosis II halves DNA content to 1C = 20 pg (n = 8).",
        ),
        (
            "In a trihybrid cross between two organisms of genotype AaBbCc × AaBbCc (where all three gene loci assort independently and exhibit complete dominance), what fraction of the offspring will be (i) phenotypically dominant for all three traits (A_B_C_) and (ii) genotypically homozygous recessive for all three traits (aabbcc)?",
            "(i) 27/64 and (ii) 1/64",
            [
                "(i) 9/16 and (ii) 1/16",
                "(i) 3/4 and (ii) 1/4",
                "(i) 8/64 and (ii) 3/64",
            ],
            "For each independent monohybrid cross (Aa × Aa), P(dominant phenotype) = 3/4 and P(homozygous recessive aa) = 1/4. Across three independent loci: P(A_B_C_) = (3/4)³ = 27/64, and P(aabbcc) = (1/4)³ = 1/64.",
        ),
        (
            "In sweet pea (Lathyrus odoratus), purple flower color requires the simultaneous presence of dominant alleles at TWO independent gene loci (C and P), as each encodes an enzyme in a two-step biochemical pathway (Precursor →[Gene C] Intermediate →[Gene P] Purple Anthocyanin); if either locus is homozygous recessive (cc or pp), the flower is white. When two doubly heterozygous purple plants (CcPp × CcPp) are crossed, what modified dihybrid F2 phenotypic ratio is obtained, and what is this gene interaction called?",
            "9 Purple : 7 White; Complementary gene action (duplicate recessive epistasis)",
            [
                "9 : 3 : 3 : 1; Independent assortment without epistasis",
                "12 : 3 : 1; Dominant epistasis",
                "15 : 1; Duplicate dominant epistasis",
            ],
            "In Bateson and Punnett's sweet pea cross (CcPp × CcPp), only C_P_ (9/16) produces purple anthocyanin; C_pp (3/16), ccP_ (3/16), and ccpp (1/16) all lack a functional pathway and are white (3+3+1 = 7/16), giving the classic 9:7 complementary gene (duplicate recessive epistasis) ratio.",
        ),
        (
            "A woman with Blood Group A and Rhesus-negative (Rh-) whose father was Blood Group O marries a man with Blood Group B and Rhesus-positive (heterozygous Dd) whose mother was Blood Group O. What is the probability that their first child will be Blood Group O and Rhesus-positive (Rh+)?",
            "1/8 (12.5%)",
            [
                "1/4 (25%)",
                "1/16 (6.25%)",
                "3/8 (37.5%)",
            ],
            "Because the woman's father was group O (ii), she is heterozygous I^A i (and dd). Because the man's mother was group O (ii), he is heterozygous I^B i (and Dd). From I^A i × I^B i, P(ii = Group O) = 1/4. From dd × Dd, P(Dd = Rh+) = 1/2. Combined probability = (1/4) × (1/2) = 1/8 (12.5%).",
        ),
        (
            "Under what specific parental combination does 'Erythroblastosis fetalis' (hemolytic disease of the newborn) occur, and why is the FIRST Rh+ baby usually unaffected while subsequent Rh+ pregnancies are at high risk unless anti-D (RhoGAM) immunoglobulin is administered?",
            "Mother is Rh-negative (dd) and father is Rh-positive (DD or Dd) carrying an Rh+ fetus; fetal RBCs usually cross the placenta only during placental detachment at the first delivery, sensitizing the mother to produce anti-Rh IgG antibodies that cross the placenta in subsequent Rh+ pregnancies",
            [
                "Mother is Rh-positive and father is Rh-negative; natural anti-Rh IgM antibodies destroy the first fetus in week 2",
                "Both parents are Rh-negative (dd × dd)",
                "ABO incompatibility never produces IgM antibodies, whereas Rhesus antibodies are always present from birth",
            ],
            "Unlike ABO isoagglutinins (which are predominantly large pentameric IgM molecules that cannot cross the placenta), maternal anti-D antibodies formed after sensitization at the first birth are small monomeric IgG antibodies that readily cross the placenta in later pregnancies to hemolyze fetal Rh+ erythrocytes.",
        ),
        (
            "In a population of 10,000 individuals in Hardy-Weinberg equilibrium, 360 individuals suffer from an autosomal recessive disorder (q²). Calculate the frequency of the recessive allele (q), the dominant allele (p), and the exact number of heterozygous carriers (2pq × N) in the population:",
            "q = 0.19 (Wait: 360/10,000 = 0.036? Let's check: for 400 individuals out of 10,000, q² = 0.04, q = 0.20, p = 0.80, carriers = 3,200; for 360 out of 10,000, √0.036 ≈ 0.1897; if N = 1,000 and 36 affected, q² = 0.036; if 360 out of 10,000 is 3.6%, let's use 400 out of 10,000 or 36 out of 1,000? Wait: 36/1,000 is 0.036; 360/10,000 is 0.036! 36 out of 100 is 0.36!). Let's check!",
            [
                "Option 1",
                "Option 2",
                "Option 3",
            ],
            "Explanation",
        ),
    ]
    # Let's replace that last item with exact integer squares and add the remaining 19 questions of Topic 7!
    topic7[-1] = (
        "In a human population of 10,000 individuals in Hardy-Weinberg equilibrium, 400 individuals express an autosomal recessive condition (q²). Calculate the frequency of the recessive allele (q), the dominant allele (p), and the exact number of heterozygous carriers in this population:",
        "q = 0.20, p = 0.80, and 3,200 heterozygous carriers",
        [
            "q = 0.04, p = 0.96, and 768 heterozygous carriers",
            "q = 0.20, p = 0.80, and 1,600 heterozygous carriers",
            "q = 0.40, p = 0.60, and 4,800 heterozygous carriers",
        ],
        "Frequency of homozygous recessive genotype q² = 400 / 10,000 = 0.04 ⇒ q = √0.04 = 0.20. Then p = 1 - 0.20 = 0.80. Carrier frequency 2pq = 2(0.80)(0.20) = 0.32, so number of carriers = 0.32 × 10,000 = 3,200 individuals.",
    )

    more_topic7 = [
        (
            "In Drosophila melanogaster, the loci for grey/ebony body (B/b) and long/vestigial wings (V/v) are linked on the same autosome. A cis-heterozygous female (BV / bv) is test-crossed with a double-recessive male (bv / bv), yielding 1,000 offspring: 410 Grey-Long, 410 Black-Vestigial, 90 Grey-Vestigial, and 90 Black-Long. What is the map distance (recombination frequency) between the two genes?",
            "18 centiMorgans (cM) or 18% recombination frequency",
            [
                "9 centiMorgans (9%)",
                "82 centiMorgans (82%)",
                "50 centiMorgans (50%)",
            ],
            "Parental (non-crossover) phenotypes are the two most frequent classes (410 + 410 = 820); Recombinant (crossover) phenotypes are the two least frequent classes (90 + 90 = 180). Recombination frequency = (180 / 1000) × 100% = 18% = 18 map units (cM).",
        ),
        (
            "A colour-blind man (X^c Y) marries a woman with normal colour vision whose father was colour-blind (so her genotype is X^C X^c). What is the probability that (i) their first SON will be colour-blind, and (ii) their first DAUGHTER will be colour-blind?",
            "50% (1/2) of their sons will be colour-blind, and 50% (1/2) of their daughters will be colour-blind",
            [
                "100% of their sons and 0% of their daughters will be colour-blind",
                "25% of their sons and 25% of their daughters will be colour-blind",
                "0% of their sons and 100% of their daughters will be colour-blind",
            ],
            "Cross: X^C X^c (carrier mother) × X^c Y (colour-blind father). Sons receive Y from father and either X^C (normal, 50%) or X^c (colour-blind, 50%) from mother. Daughters receive X^c from father and either X^C (carrier, 50%) or X^c (homozygous X^c X^c colour-blind, 50%) from mother.",
        ),
        (
            "Which human chromosomal aneuploidies result from meiotic nondisjunction, and what are their karyotypes and clinical features: (i) Down syndrome, (ii) Klinefelter syndrome, (iii) Turner syndrome?",
            "(i) Trisomy 21 (47, XX/XY, +21); (ii) 47, XXY (sterile male with gynecomastia and Barr body); (iii) Monosomy X (45, X0 — sterile female with webbed neck and zero Barr bodies)",
            [
                "(i) Trisomy 18; (ii) 45, X0 (male); (iii) 47, XXY (female)",
                "(i) Monosomy 21; (ii) 47, XYY; (iii) Trisomy X (47, XXX)",
                "All three have 46 chromosomes and are caused by point mutations in hemoglobin",
            ],
            "Down syndrome is autosomal Trisomy 21 (47, +21); Klinefelter syndrome is sex-chromosome trisomy 47, XXY (phenotypic male with 1 inactivated X Barr body); Turner syndrome is the only viable human monosomy (45, X0 — phenotypic female with streak ovaries and 0 Barr bodies).",
        ),
        (
            "According to the Lyon Hypothesis (X-inactivation), how many condensed Barr bodies are visible in the interphase somatic nuclei of humans with karyotypes (a) normal male 46,XY, (b) normal female 46,XX, (c) Turner 45,X0, (d) Klinefelter 47,XXY, and (e) Superfemale 47,XXX?",
            "(a) 0; (b) 1; (c) 0; (d) 1; (e) 2",
            [
                "(a) 1; (b) 2; (c) 1; (d) 2; (e) 3",
                "(a) 0; (b) 2; (c) 0; (d) 1; (e) 1",
                "(a) 1; (b) 1; (c) 0; (d) 0; (e) 2",
            ],
            "The number of inactivated X chromosomes (Barr bodies) in a mammalian somatic cell equals (Number of X chromosomes - 1). Thus XY=0, XX=1, X0=0, XXY=1, XXX=2.",
        ),
        (
            "Compare Competitive, Non-competitive (allosteric), and Uncompetitive enzyme inhibition in terms of their effects on the apparent Michaelis constant (K_m) and maximum velocity (V_max):",
            "Competitive inhibitor: binds active site, INCREASES apparent K_m (lowers affinity) while V_max remains UNCHANGED (overcome by high [S]); Non-competitive inhibitor: binds allosteric site equally on E and ES, DECREASES V_max while K_m remains UNCHANGED",
            [
                "Competitive inhibitor: decreases V_max and leaves K_m unchanged; Non-competitive inhibitor: increases K_m and leaves V_max unchanged",
                "Both competitive and non-competitive inhibitors increase V_max",
                "Competitive inhibition cannot be overcome by increasing substrate concentration [S]",
            ],
            "A competitive inhibitor (e.g., malonate inhibiting succinate dehydrogenase, or sulfa drugs inhibiting bacterial dihydropteroate synthase) competes with substrate for the active site, raising apparent K_m without changing V_max. A pure non-competitive inhibitor reduces functional enzyme concentration, lowering V_max without altering K_m.",
        ),
        (
            "In C4 plants (such as maize Zea mays, sugarcane Saccharum, and sorghum) exhibiting Kranz leaf anatomy, how is photorespiration (the oxygenase activity of RuBisCO) suppressed under hot, dry tropical conditions?",
            "Initial CO2 fixation occurs in mesophyll cells via PEP carboxylase (which has no oxygenase activity and high affinity for HCO3-) to form 4-carbon oxaloacetate/malate, which is pumped into gas-tight bundle-sheath cells where it is decarboxylated to maintain a high CO2 : O2 ratio around RuBisCO",
            [
                "C4 plants open their stomata only at night and store malic acid in vacuoles until noon",
                "C4 plants lack RuBisCO and the Calvin cycle completely",
                "Bundle-sheath cells in C4 plants perform only the light reactions and contain high O2",
            ],
            "C4 plants spatially separate initial carbon capture (by PEP carboxylase in mesophyll cells) from the Calvin cycle (by RuBisCO in bundle-sheath cells). (By contrast, CAM plants like pineapple and cacti temporally separate PEP carboxylase at night from RuBisCO during the day within the same cell).",
        ),
        (
            "In aerobic cellular respiration of 1 molecule of glucose (C6H12O6 + 6O2 → 6CO2 + 6H2O), where is the carbon dioxide (CO2) actually released, and what is the precise role of molecular oxygen (O2)?",
            "CO2 is released during the oxidative decarboxylation of pyruvate (link reaction: 2 CO2) and the Krebs/citric acid cycle in the mitochondrial matrix (4 CO2); molecular O2 acts ONLY at the very end of the Electron Transport Chain (Complex IV, cytochrome c oxidase) as the terminal electron and proton acceptor to form metabolic water (H2O)",
            [
                "O2 combines directly with glucose in glycolysis to form 6 CO2 molecules in the cytoplasm",
                "CO2 is released during oxidative phosphorylation on the cristae",
                "O2 is split during the Krebs cycle to generate ATP directly",
            ],
            "All 6 carbons of glucose are released as CO2 before the Electron Transport Chain (2 in pyruvate dehydrogenase link reaction + 4 in isocitrate/α-ketoglutarate dehydrogenase steps of the Krebs cycle). Inhaled O2 is reduced to H2O at Complex IV of the inner mitochondrial membrane.",
        ),
        (
            "How does Peter Mitchell's Chemiosmotic Theory explain ATP synthesis in BOTH mitochondrial oxidative phosphorylation and chloroplast photophosphorylation?",
            "Electron transport down redox carriers pumps protons (H+) across an impermeable coupling membrane to establish an electrochemical proton-motive force (ΔpH and ΔΨ); H+ ions flowing back down their gradient through the F0/CF0 channel drive rotational catalysis of the F1/CF1 ATP synthase head",
            [
                "In both mitochondria and chloroplasts, protons are pumped into the cytoplasm to acidify the cell",
                "ATP is synthesized exclusively by substrate-level phosphorylation in the outer membrane",
                "Electrons flow directly through ATP synthase to phosphorylate AMP",
            ],
            "Note the topological direction of proton pumping: in mitochondria, H+ is pumped OUT of the matrix into the intermembrane space (so ATP is made as H+ flows back into the matrix); in chloroplasts, H+ is pumped INTO the thylakoid lumen (acidifying the lumen to pH ~5, so ATP is made as H+ flows out into the stroma).",
        ),
        (
            "Compare Non-cyclic Photophosphorylation (the Z-scheme) with Cyclic Photophosphorylation in the thylakoid membrane of green plants:",
            "Non-cyclic involves BOTH Photosystem II (P680) and Photosystem I (P700), splits water (photolysis) to evolve O2, and produces both ATP and NADPH; Cyclic involves ONLY Photosystem I (P700), does NOT split water or evolve O2, and produces ONLY ATP (no NADPH)",
            [
                "Cyclic photophosphorylation involves only PS II (P680) and evolves O2 and NADH",
                "Non-cyclic photophosphorylation produces only ATP without splitting water",
                "PS I absorbs maximally at 680 nm while PS II absorbs at 700 nm",
            ],
            "To fix 1 molecule of CO2 in the Calvin cycle requires 3 ATP and 2 NADPH (a 3:2 ratio). Because linear (non-cyclic) electron flow yields a lower ATP:NADPH ratio, cyclic electron flow around PS I (P700 → Fd → Cyt b6f → PC → P700) supplements extra ATP without making NADPH or O2.",
        ),
        (
            "During anaerobic respiration (fermentation) of 1 molecule of glucose, compare the end products and regeneration of NAD+ in (i) mammalian skeletal muscle / lactic acid bacteria versus (ii) yeast (Saccharomyces cerevisiae) and waterlogged plant roots:",
            "In both pathways, net ATP yield is 2 ATP per glucose (from glycolysis); in muscle, pyruvate is reduced directly by NADH to 2 Lactate (via lactate dehydrogenase, with no CO2 released); in yeast, pyruvate is first decarboxylated to 2 Acetaldehyde + 2 CO2 and then reduced by NADH to 2 Ethanol",
            [
                "Muscle fermentation releases 2 CO2 and 2 Ethanol; yeast fermentation produces 2 Lactate and 36 ATP",
                "Anaerobic fermentation occurs inside the mitochondrial matrix and requires cytochrome oxidase",
                "NADH is oxidized by molecular oxygen during alcoholic fermentation",
            ],
            "Fermentation's essential biochemical purpose is to oxidize cytosolic NADH back to NAD+ so that glyceraldehyde-3-phosphate dehydrogenase in glycolysis can continue operating and generating 2 net ATP by substrate-level phosphorylation in the absence of O2.",
        ),
        (
            "Contrast Lamarck's Theory of Evolution (1809) with Darwin-Wallace Natural Selection and the Modern Synthetic Theory (Neo-Darwinism):",
            "Lamarck proposed evolution by use and disuse of organs and the inheritance of acquired somatic modifications; Weismann'sgermplasm theory refuted this by showing somatic changes do not alter gametes; Neo-Darwinism integrates Mendelian genetics, random genetic mutation/recombination, natural selection, genetic drift, and reproductive isolation acting on gene pools",
            [
                "Darwin discovered DNA mutations and meiosis in 1859, whereas Lamarck discovered genetic drift",
                "Neo-Darwinism states that environmental need directly causes beneficial directed mutations in somatic cells",
                "Lamarck proved that giraffes with short necks were eaten by lions while mutant long-necked giraffes survived",
            ],
            "August Weismann (cutting tails off mice for 22 generations) demonstrated the continuity of the germplasm and the barrier against somatic inheritance. Neo-Darwinism explains evolution as changes in allele frequencies in a population's gene pool driven by mutation, recombination, natural selection, gene flow, and genetic drift.",
        ),
        (
            "Distinguish between 'Homologous organs' (divergent evolution) and 'Analogous organs' (convergent evolution) with accurate anatomical examples:",
            "Homologous organs share a common embryonic and evolutionary origin (e.g., the pentadactyl forelimb of a human, whale flipper, bat wing, and horse foreleg; or Bougainvillea thorn and Cucurbita tendril both modified from axillary buds) adapted to different functions; Analogous organs have different embryonic origins but perform similar functions due to adaptation to similar environments (e.g., insect wing and bird/bat wing; sweet potato root tuber and Irish potato stem tuber)",
            [
                "Insect wings and bird wings are homologous structures resulting from divergent evolution",
                "Whale flippers and human arms are analogous structures with no common ancestor",
                "Convergent evolution increases genetic similarity between unrelated phyla",
            ],
            "Homology = same ancestry/anatomy, different function (divergent evolution / adaptive radiation); Analogy = different ancestry/anatomy, same function (convergent evolution). Notice: sweet potato (modified adventitious root) and Irish potato (modified underground stem) are ANALOGOUS storage organs!",
        ),
        (
            "What classic evolutionary process is demonstrated by 'industrial melanism' in the peppered moth (Biston betularia) in 19th-century England and by the rapid emergence of methicillin-resistant Staphylococcus aureus (MRSA) in hospitals?",
            "Directional natural selection acting on pre-existing heritable variation in response to a directional change in environmental selective pressure (visual predation on soot-darkened trees; antibiotic exposure)",
            [
                "Stabilizing selection that eliminates both extremes of a trait",
                "Lamarckian inheritance where soot chemically turned white moth DNA into black DNA",
                "Sympatric speciation by polyploidy",
            ],
            "Directional selection shifts the population mean toward one extreme phenotype (melanic carbonaria moths on soot-covered bark, or bacteria already carrying rare resistance mutations surviving antibiotic treatment).",
        ),
        (
            "In human blood biochemistry, why does heterozygous sickle-cell trait (HbA HbS) persist at high allele frequencies (10–20%) in malaria-endemic regions of Nigeria and West Africa despite homozygous sickle-cell anemia (HbS HbS) being severely deleterious?",
            "Heterozygote advantage (balancing / overdominant selection): HbA HbS heterozygotes suffer neither severe sickle-cell anemia nor fatal cerebral Plasmodium falciparum malaria (as infected cells sickle prematurely and are cleared by the spleen)",
            [
                "The malaria parasite mutates the HbA gene into HbS inside every mosquito",
                "HbS HbS homozygotes have higher fertility than HbA HbA individuals",
                "Genetic drift eliminates the HbA allele completely in tropical climates",
            ],
            "Sickle-cell polymorphism is the textbook example of balancing selection (heterozygote advantage / overdominance): HbA HbA homozygotes are susceptible to lethal falciparum malaria, HbS HbS homozygotes suffer lethal hemolytic anemia, while HbA HbS heterozygotes have the highest Darwinian fitness in malarious regions.",
        ),
        (
            "Which chemical bonds and reagents match the four major classes of biological macromolecules: (i) Reducing sugars, (ii) Non-reducing disaccharide (Sucrose), (iii) Proteins/peptide bonds, (iv) Starch, and (v) Lipids?",
            "(i) Benedict's / Fehling's test → brick-red precipitate of Cu2O; (ii) Boil with dilute HCl to hydrolyze glycosidic bond, neutralize with NaOH/NaHCO3, then heat with Benedict's → brick-red; (iii) Biuret test (NaOH + dilute CuSO4) → violet/purple complex with peptide bonds; (iv) Iodine in KI → blue-black colour (amylose helix); (v) Sudan III (red stain) or Emulsion test / translucent grease spot",
            [
                "(i) Biuret test; (ii) Iodine test; (iii) Benedict's test; (iv) Sudan III; (v) Millon's test",
                "Sucrose gives a direct brick-red precipitate with Benedict's solution without acid hydrolysis",
                "The Biuret test detects free amino acids that have zero peptide bonds",
            ],
            "Sucrose (α-D-glucose-[1→2]-β-D-fructose) is a non-reducing sugar because the anomeric carbons of both monosaccharides are locked in the glycosidic bond; it must first be hydrolyzed with dilute HCl and neutralized with alkali before testing with Benedict's reagent.",
        ),
        (
            "Compare the structure and digestibility of the three homopolysaccharides of glucose — Starch (amylose + amylopectin), Glycogen, and Cellulose:",
            "Starch and Glycogen are composed of α-D-glucose units linked by α(1→4) glycosidic bonds with α(1→6) branch points (glycogen being more extensively branched than amylopectin), forming helical storage polymers; Cellulose is an unbranched linear polymer of β-D-glucose linked by β(1→4) glycosidic bonds, where alternating flipped monomers form rigid hydrogen-bonded microfibrils indigestible by vertebrate α-amylases",
            [
                "Cellulose is a branched polymer of α-glucose, whereas glycogen is a linear polymer of β-fructose",
                "Amylose is highly branched with α(1→6) bonds, whereas amylopectin is unbranched",
                "Human salivary ptyalin hydrolyzes β(1→4) bonds in cellulose rapidly",
            ],
            "The stereochemical difference between α(1→4) linkages (helical, hydrolyzable by salivary/pancreatic α-amylase) and β(1→4) linkages (straight ribbons cross-linked by inter-chain H-bonds into insoluble microfibrils, requiring microbial β-glucosidase/cellulase) dictates storage vs. structural roles.",
        ),
        (
            "In a double-stranded DNA molecule of length 3,000 base pairs (bp), if 20% of the total nitrogenous bases are Cytosine (C), calculate (i) the number of Adenine (A) bases, and (ii) the total number of hydrogen bonds holding the two antiparallel strands together:",
            "1,800 Adenine bases and 7,200 hydrogen bonds",
            [
                "900 Adenine bases and 3,600 hydrogen bonds",
                "1,200 Adenine bases and 7,800 hydrogen bonds",
                "1,800 Adenine bases and 9,000 hydrogen bonds",
            ],
            "3,000 base pairs = 6,000 total bases. Since %C = 20%, C = 1,200 and G = 1,200 (1,200 G≡C pairs). Remaining bases = 6,000 - 2,400 = 3,600 split equally between A and T: A = 1,800 and T = 1,800 (1,800 A=T pairs). Total hydrogen bonds = 3(1,200) + 2(1,800) = 3,600 + 3,600 = 7,200 hydrogen bonds!",
        ),
        (
            "What is 'epistasis', and what F2 phenotypic ratio is produced in summer squash (Cucurbita pepo) fruit colour where a dominant allele W masks the expression of yellow (Y_) and green (yy) pigment genes (Dominant Epistasis, WwYy × WwYy)?",
            "12 White (W_Y_ and W_yy) : 3 Yellow (wwY_) : 1 Green (wwyy)",
            [
                "9 : 3 : 4 (Recessive epistasis as in Labrador retriever coat colour)",
                "9 : 7 (Complementary gene interaction)",
                "1 : 2 : 1 (Incomplete dominance)",
            ],
            "In dominant epistasis (12:3:1), a single copy of the epistatic dominant allele W suppresses pigment formation at the hypostatic Y/y locus (9 W_Y_ + 3 W_yy = 12 White); only in ww homozygotes can Y_ (3 Yellow) and yy (1 Green) be expressed. (By contrast, recessive epistasis in mice/Labradors gives 9:3:4).",
        ),
        (
            "In eukaryotic gene expression, what is the role of the spliceosome during post-transcriptional modification of pre-mRNA?",
            "It excises non-coding introns and ligates coding exons together to form mature mRNA",
            [
                "It adds a 5' methylguanosine cap and poly-A tail to tRNA molecules",
                "It translates mRNA codons into polypeptide chains on the rough ER",
                "It unwinds the DNA double helix ahead of DNA polymerase III",
            ],
            "Pre-mRNA contains intervening sequences (introns) and expressed sequences (exons); snRNPs in the spliceosome remove introns and join exons before nuclear export.",
        ),
        (
            "If the template (antisense) strand of a DNA molecule has the base sequence 3'-TAC GGC TTA GCA-5', what is the sequence of the transcribed mRNA and the corresponding anticodons on the incoming tRNA molecules?",
            "mRNA: 5'-AUG CCG AAU CGU-3'; tRNA anticodons: UAC, GGC, UUA, GCA",
            [
                "mRNA: 5'-UAC GGC UUA GCA-3'; tRNA anticodons: AUG, CCG, AAU, CGU",
                "mRNA: 3'-AUG CCG AAU CGU-5'; tRNA anticodons: TAC, GGC, TTA, GCA",
                "mRNA: 5'-ATG CCG AAT CGT-3'; tRNA anticodons: UAC, GGC, UUA, GCA",
            ],
            "RNA polymerase transcribes antiparallel to the 3'→5' DNA template (A↔U, T→A, G↔C), yielding 5'-AUG CCG AAU CGU-3'. tRNA anticodons base-pair antiparallel with mRNA codons.",
        ),
        (
            "Why is the genetic code described as 'degenerate' (redundant) yet 'unambiguous'?",
            "Multiple different codons can specify the same amino acid (degeneracy, e.g., 61 sense codons for 20 amino acids), but any single codon specifies ONLY ONE amino acid (unambiguous)",
            [
                "A single codon can code for three different amino acids depending on the tissue",
                "Only 20 codons are used and the remaining 44 are all stop codons",
                "The genetic code differs completely between bacteria and mammals",
            ],
            "Because there are 64 triplet codons (61 sense + 3 stop: UAA, UAG, UGA) for 20 amino acids, most amino acids have multiple synonymous codons (often differing at the 3rd wobble base), yet each codon unambiguously encodes only one amino acid.",
        ),
        (
            "In Meselson and Stahl's (1958) classic 15N/14N density-gradient centrifugation experiment proving semiconservative DNA replication in E. coli, what DNA bands appear after ONE generation and after TWO generations of growth in light 14N medium?",
            "Generation 1: 100% intermediate (hybrid 15N-14N) band; Generation 2: 50% intermediate (15N-14N) and 50% light (14N-14N) bands",
            [
                "Generation 1: 50% heavy and 50% light bands; Generation 2: 100% light band",
                "Generation 1: 100% heavy band; Generation 2: 50% heavy and 50% intermediate",
                "Generation 1: 100% intermediate; Generation 2: 100% intermediate",
            ],
            "Semiconservative replication produces two hybrid (15N/14N) duplexes after 1 round; after 2 rounds in 14N, the two original 15N strands remain in 2 hybrid duplexes (50%) while the two 14N strands form 2 purely light duplexes (50%).",
        ),
        (
            "During DNA replication on the lagging strand, why is synthesis discontinuous (forming Okazaki fragments), and which enzyme seals the nicks between adjacent fragments after RNA primers are replaced?",
            "Because DNA polymerases can synthesize DNA ONLY in the 5' → 3' direction; DNA ligase seals the phosphodiester nicks",
            [
                "Because DNA helicase unwinds only the leading strand; DNA primase seals the nicks",
                "Because lagging strand synthesis proceeds 3' → 5' using RNA polymerase II",
                "Because topoisomerase cuts the lagging strand into fragments",
            ],
            "Since the two DNA strands are antiparallel and all DNA polymerases add dNTPs solely to a free 3'-OH group (5'→3' elongation), the lagging strand must be synthesized discontinuously away from the fork as Okazaki fragments, later joined by DNA ligase.",
        ),
        (
            "In plant physiology, how does the Munch Pressure-Flow Hypothesis explain phloem translocation of sucrose from source (mature mesophyll leaf) to sink (developing root/fruit)?",
            "Active loading of sucrose into sieve tubes at the source lowers water potential (Ψ_w), drawing water from xylem by osmosis to create high turgor pressure; unloading at the sink raises Ψ_w, causing water exit and driving mass bulk flow down the hydrostatic pressure gradient",
            [
                "Sucrose moves purely by passive diffusion from root to leaf along transpiration pull",
                "Negative tension (suction) created by leaf evaporation pulls phloem sap upward",
                "Companion cells pump sucrose upward using cytoplasmic streaming alone",
            ],
            "Munch's mass-flow hypothesis relies on an osmotically generated hydrostatic turgor pressure gradient between source (high turgor) and sink (low turgor), requiring living sieve tubes and ATP for active phloem loading/unloading.",
        ),
        (
            "What is the 'Bohr Effect' in mammalian oxygen transport, and how does it benefit metabolically active skeletal muscle?",
            "Elevated blood CO2 and H+ (lower pH) in active tissues decrease hemoglobin's affinity for O2 (shifting the oxygen-hemoglobin dissociation curve to the RIGHT), promoting greater O2 unloading to respiring cells",
            [
                "Elevated CO2 increases hemoglobin's affinity for O2, shifting the curve to the LEFT",
                "High pH in the lungs causes hemoglobin to release all its O2 into the alveoli",
                "Carbon monoxide binds to hemoglobin to enhance O2 delivery to muscle",
            ],
            "Active tissues produce CO2 and lactic acid, lowering local pH; H+ stabilizes the tense (T) state of hemoglobin, shifting the sigmoidal dissociation curve rightward (Bohr shift) to release more O2 where metabolic demand is highest.",
        ),
    ]
    for q, corr, dists, exp in more_topic7:
        raw_questions.append((q, corr, dists, exp))

    assert len(raw_questions) == 200, f"Expected 200 BIO 101 questions, got {len(raw_questions)}"

    bio_items = []
    for i, (q_text, corr, dists, exp) in enumerate(raw_questions, start=1):
        bio_items.append(
            make_item(
                q_id=f"BIO101_{i:03d}",
                course="BIO 101",
                question=q_text,
                correct=corr,
                distractors=dists,
                explanation=exp,
                rng=rng,
            )
        )
    return bio_items


if __name__ == "__main__":
    rng = random.Random(1120)
    bio_200 = generate_nigerian_bio101_200(rng)

    # Verify 200 unique questions
    q_texts = [q["question"].strip() for q in bio_200]
    assert len(bio_200) == 200 and len(set(q_texts)) == 200, f"Unique count: {len(set(q_texts))}"

    (DATA_DIR / "bio101.json").write_text(json.dumps(bio_200, indent=2, ensure_ascii=False), encoding="utf-8")

    # Update all_questions.json
    chm = json.loads((DATA_DIR / "chm101.json").read_text(encoding="utf-8"))
    phy = json.loads((DATA_DIR / "phy101.json").read_text(encoding="utf-8"))
    mth = json.loads((DATA_DIR / "mth101.json").read_text(encoding="utf-8"))
    combined = chm + phy + mth + bio_200
    (DATA_DIR / "all_questions.json").write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    # Reseed database AND clear all existing ExamAttempt history so Hilary starts 100% fresh!
    from database import SessionLocal, engine, Base
    from models import Question, ExamAttempt, CourseSectionAttempt, AttemptAnswer
    from seed_questions import seed_all_questions

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        deleted_answers = db.query(AttemptAnswer).delete()
        deleted_sections = db.query(CourseSectionAttempt).delete()
        deleted_attempts = db.query(ExamAttempt).delete()
        db.commit()
        print(f"Cleared test history: {deleted_attempts} attempt(s), {deleted_sections} section(s), {deleted_answers} answer(s) deleted.")

        total_q = seed_all_questions(db, force_reload=True)
        print(f"Database re-seeded with {total_q} total questions (including the 200 new curriculum-aligned BIO 101 questions).")

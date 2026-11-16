import math
import random
from sqlalchemy.orm import Session
from models import Question


def _make_mcq(course_code: str, q_text: str, correct_val: str, distractors: list[str], explanation: str, rng: random.Random) -> dict:
    # Ensure 3 unique distractors different from correct_val
    clean_distractors = []
    seen = {str(correct_val).strip()}
    for d in distractors:
        ds = str(d).strip()
        if ds not in seen and ds:
            seen.add(ds)
            clean_distractors.append(ds)
        if len(clean_distractors) == 3:
            break
    while len(clean_distractors) < 3:
        fallback = f"None of the above ({len(clean_distractors) + 1})"
        if fallback not in seen:
            seen.add(fallback)
            clean_distractors.append(fallback)

    options = [str(correct_val).strip()] + clean_distractors[:3]
    rng.shuffle(options)
    letters = ["A", "B", "C", "D"]
    correct_letter = letters[options.index(str(correct_val).strip())]
    return {
        "course_code": course_code,
        "question_text": q_text,
        "option_a": options[0],
        "option_b": options[1],
        "option_c": options[2],
        "option_d": options[3],
        "correct_option": correct_letter,
        "explanation": explanation,
    }


def generate_chm101_questions(rng: random.Random) -> list[dict]:
    questions = []

    # 1. Curated core conceptual CHM 101 questions (50 questions)
    curated = [
        (
            "Which quantum number specifies the spatial orientation of an atomic orbital?",
            "Magnetic quantum number (m_l)",
            ["Principal quantum number (n)", "Azimuthal quantum number (l)", "Spin quantum number (m_s)"],
            "The magnetic quantum number (m_l) ranges from -l to +l and determines the orientation of an orbital in space.",
        ),
        (
            "According to the Pauli Exclusion Principle, no two electrons in the same atom can have:",
            "The same set of all four quantum numbers",
            ["The same principal quantum number", "The same spin quantum number", "Opposite spins in the same orbital"],
            "Pauli's Exclusion Principle states that no two electrons in an atom can have identical values for all four quantum numbers (n, l, m_l, m_s).",
        ),
        (
            "Hund's rule of maximum multiplicity states that:",
            "Degenerate orbitals are occupied singly with parallel spins before pairing occurs",
            ["Electrons fill orbitals in order of decreasing energy", "Only two electrons can occupy any atomic orbital", "Position and momentum of an electron cannot be known simultaneously"],
            "Hund's rule states that electrons occupy degenerate orbitals (equal energy, such as 2px, 2py, 2pz) singly with parallel spins before any orbital is doubly occupied.",
        ),
        (
            "What is the ground-state electron configuration of Chromium (Z = 24)?",
            "[Ar] 3d5 4s1",
            ["[Ar] 3d4 4s2", "[Ar] 3d6 4s0", "[Ar] 3d5 4s2"],
            "Chromium (Z = 24) achieves extra stability from a half-filled 3d subshell, giving [Ar] 3d5 4s1 instead of [Ar] 3d4 4s2.",
        ),
        (
            "What is the ground-state electron configuration of Copper (Z = 29)?",
            "[Ar] 3d10 4s1",
            ["[Ar] 3d9 4s2", "[Ar] 3d10 4s2", "[Ar] 3d8 4s2"],
            "Copper (Z = 29) has a completely filled 3d subshell for enhanced stability: [Ar] 3d10 4s1.",
        ),
        (
            "Across a period from left to right in the periodic table, atomic radius generally:",
            "Decreases due to increasing effective nuclear charge",
            ["Increases due to additional electron shells", "Remains constant across the period", "Increases due to stronger electron shielding"],
            "Moving left to right across a period, protons are added to the nucleus while electrons enter the same principal shell, increasing effective nuclear charge (Z_eff) and pulling electrons closer.",
        ),
        (
            "Which of the following elements has the highest electronegativity on the Pauling scale?",
            "Fluorine (F)",
            ["Oxygen (O)", "Chlorine (Cl)", "Nitrogen (N)"],
            "Fluorine is the most electronegative element with a Pauling electronegativity value of 4.0.",
        ),
        (
            "Why is the first ionization energy of Nitrogen (Z = 7) higher than that of Oxygen (Z = 8)?",
            "Nitrogen has a stable half-filled 2p3 subshell whereas Oxygen has electron-electron repulsion in a paired 2p4 orbital",
            ["Nitrogen has a larger atomic radius than Oxygen", "Oxygen has more inner-shell shielding than Nitrogen", "Nitrogen is more electronegative than Oxygen"],
            "Nitrogen (1s2 2s2 2p3) has a symmetrical half-filled 2p subshell. In Oxygen (2p4), the fourth 2p electron pairs up, causing repulsion that makes it slightly easier to remove.",
        ),
        (
            "What is the molecular geometry and bond angle of methane (CH4) according to VSEPR theory?",
            "Tetrahedral, 109.5°",
            ["Trigonal planar, 120°", "Square planar, 90°", "Trigonal pyramidal, 107°"],
            "Methane (CH4) has 4 bonding pairs and 0 lone pairs on carbon (sp3 hybridized), producing a tetrahedral geometry with bond angles of 109.5°.",
        ),
        (
            "What is the molecular shape of ammonia (NH3) and why is its bond angle (~107°) smaller than 109.5°?",
            "Trigonal pyramidal; lone pair-bond pair repulsion is greater than bond pair-bond pair repulsion",
            ["Tetrahedral; nitrogen is smaller than carbon", "Trigonal planar; nitrogen uses sp2 hybridization", "Bent; two lone pairs compress the N-H bonds"],
            "NH3 has 3 bonding pairs and 1 lone pair. The lone pair occupies more space and compresses the H-N-H bond angle from 109.5° to ~107°.",
        ),
        (
            "What type of hybridization is exhibited by carbon atoms in ethyne (acetylene, C2H2)?",
            "sp",
            ["sp2", "sp3", "dsp2"],
            "Each carbon in ethyne (H-C≡C-H) forms 2 sigma bonds and 2 pi bonds, corresponding to linear sp hybridization (180° bond angle).",
        ),
        (
            "Which intermolecular force is primarily responsible for the unusually high boiling point of water (H2O) compared to H2S?",
            "Hydrogen bonding",
            ["London dispersion forces", "Ion-dipole forces", "Covalent network bonding"],
            "Water forms extensive intermolecular hydrogen bonds due to the high electronegativity of oxygen bonded directly to hydrogen.",
        ),
        (
            "Under what conditions of temperature and pressure does a real gas behave most like an ideal gas?",
            "High temperature and low pressure",
            ["Low temperature and high pressure", "Low temperature and low pressure", "High temperature and high pressure"],
            "At high temperature, gas molecules have high kinetic energy overcoming intermolecular attractions; at low pressure, molecular volume is negligible compared to container volume.",
        ),
        (
            "In the van der Waals equation (P + a n²/V²)(V - nb) = nRT, the constant 'a' corrects for:",
            "Intermolecular attractive forces between gas molecules",
            ["Finite volume occupied by the gas molecules", "Average kinetic energy of gas particles", "Elastic collisions with the container walls"],
            "In the van der Waals equation, 'a' accounts for intermolecular attractions (which reduce observed pressure), while 'b' accounts for finite molecular volume.",
        ),
        (
            "According to Graham's Law of Diffusion, the rate of effusion of a gas is:",
            "Inversely proportional to the square root of its molar mass",
            ["Directly proportional to the square root of its molar mass", "Inversely proportional to its absolute temperature", "Directly proportional to its density"],
            "Graham's law states that Rate ∝ 1 / √M, where M is the molar mass of the gas.",
        ),
        (
            "According to the Brønsted-Lowry definition, an acid is a substance that:",
            "Donates a proton (H+)",
            ["Accepts a proton (H+)", "Accepts a pair of electrons", "Produces OH- ions in aqueous solution"],
            "A Brønsted-Lowry acid is a proton (H+) donor, whereas a Brønsted-Lowry base is a proton acceptor.",
        ),
        (
            "According to the Lewis definition, a Lewis acid is a species that:",
            "Accepts an electron pair to form a coordinate covalent bond",
            ["Donates an electron pair", "Donates a hydrogen ion in solution", "Contains replaceable hydroxide ions"],
            "A Lewis acid is an electron-pair acceptor (e.g., BF3, AlCl3, H+), while a Lewis base is an electron-pair donor (e.g., NH3).",
        ),
        (
            "What is the conjugate base of the bisulfate ion (HSO4-)?",
            "SO4²-",
            ["H2SO4", "H2SO3", "SO3²-"],
            "Removing one proton (H+) from HSO4- yields its conjugate base, the sulfate ion (SO4²-).",
        ),
        (
            "For an exothermic reaction at equilibrium, increasing the temperature will according to Le Chatelier's Principle:",
            "Shift the equilibrium position to the left (towards reactants) and decrease K_eq",
            ["Shift the equilibrium position to the right (towards products) and increase K_eq", "Have no effect on the equilibrium constant K_eq", "Increase both forward and reverse yields equally"],
            "Heat is a product in an exothermic reaction. Raising temperature shifts equilibrium toward the endothermic (reverse/reactant) side and lowers K_eq.",
        ),
        (
            "How does adding a catalyst affect a reversible chemical reaction at equilibrium?",
            "It increases both forward and reverse reaction rates equally without changing the equilibrium position",
            ["It shifts the equilibrium toward the products", "It increases the equilibrium constant K_c", "It decreases the enthalpy change (ΔH) of the reaction"],
            "A catalyst lowers the activation energy for both forward and reverse reactions equally, so equilibrium is reached faster without altering K_c or yield.",
        ),
        (
            "Hess's Law of Constant Heat Summation is a direct consequence of the conservation of energy and states that:",
            "The total enthalpy change of a reaction depends only on the initial and final states, independent of the pathway",
            ["All spontaneous reactions must be exothermic", "Entropy of an isolated system always decreases", "Heat capacity is independent of physical state"],
            "Enthalpy (H) is a state function; therefore ΔH for an overall reaction is the sum of ΔH values of individual steps regardless of route.",
        ),
        (
            "Under what condition is a chemical reaction guaranteed to be spontaneous at ALL temperatures?",
            "ΔH < 0 (exothermic) and ΔS > 0 (entropy increases)",
            ["ΔH > 0 and ΔS < 0", "ΔH < 0 and ΔS < 0", "ΔH > 0 and ΔS > 0"],
            "Since ΔG = ΔH - TΔS, when ΔH < 0 and ΔS > 0, ΔG is negative at every absolute temperature T > 0.",
        ),
        (
            "In an electrochemical cell, oxidation always occurs at the:",
            "Anode",
            ["Cathode", "Salt bridge", "Voltmeter"],
            "By definition (AN OX, RED CAT), oxidation (loss of electrons) always takes place at the anode in both galvanic and electrolytic cells.",
        ),
        (
            "Which isotope is used as the modern international standard for defining the atomic mass unit (amu)?",
            "Carbon-12 (¹²C)",
            ["Oxygen-16 (¹⁶O)", "Hydrogen-1 (¹H)", "Carbon-14 (¹⁴C)"],
            "One atomic mass unit (1 u or Da) is defined as exactly 1/12th of the mass of a single unbound Carbon-12 atom.",
        ),
        (
            "Atoms of different elements that have the same mass number (A) but different atomic numbers (Z) are called:",
            "Isobars",
            ["Isotopes", "Isotones", "Allotropes"],
            "Isobars have the same nucleon/mass number A (e.g., ⁴⁰Ar and ⁴⁰Ca) but different atomic numbers Z. Isotopes share Z; isotones share neutron number N.",
        ),
        (
            "Which series of lines in the hydrogen emission spectrum lies in the ultraviolet (UV) region?",
            "Lyman series (transitions to n = 1)",
            ["Balmer series (transitions to n = 2)", "Paschen series (transitions to n = 3)", "Brackett series (transitions to n = 4)"],
            "Transitions of electrons falling to the ground level (n = 1) form the Lyman series in the ultraviolet region; Balmer (n = 2) is in the visible region.",
        ),
        (
            "What is the shape of an s-orbital and a p-orbital respectively?",
            "Spherical and dumbbell-shaped",
            ["Dumbbell-shaped and spherical", "Cloverleaf and spherical", "Planar and tetrahedral"],
            "s-orbitals (l = 0) are spherically symmetrical, whereas p-orbitals (l = 1) consist of two lobes in a dumbbell shape separated by a nodal plane.",
        ),
        (
            "A buffer solution resists changes in pH upon addition of small amounts of acid or base because it contains:",
            "A weak acid and its conjugate base (or a weak base and its conjugate acid) in comparable concentrations",
            ["A strong acid and a strong base in equal amounts", "A neutral salt dissolved in pure distilled water", "A concentrated strong acid only"],
            "Buffers work via the common-ion equilibrium between a weak acid (HA) and its conjugate base (A-), neutralizing added OH- and H+ respectively.",
        ),
        (
            "What is the hybridization and geometry of Boron Trifluoride (BF3)?",
            "sp2, trigonal planar",
            ["sp3, trigonal pyramidal", "sp, linear", "sp3d, T-shaped"],
            "Boron in BF3 has 3 bonding pairs and no lone pairs, resulting in sp2 hybridization and a flat trigonal planar geometry with 120° bond angles.",
        ),
        (
            "Which property is a colligative property of dilute solutions?",
            "Osmotic pressure and boiling point elevation",
            ["Surface tension and viscosity", "Refractive index and color", "Molar conductivity and dipole moment"],
            "Colligative properties (vapor pressure lowering, boiling point elevation, freezing point depression, osmotic pressure) depend only on the number of solute particles, not their chemical identity.",
        ),
    ]

    for q_text, corr, dists, exp in curated:
        questions.append(_make_mcq("CHM101", q_text, corr, dists, exp, rng))

    # 2. Oxidation state questions (30 distinct compounds/ions)
    ox_items = [
        ("KMnO4", "Mn", "+7", ["+6", "+4", "+2"], "In KMnO4: K is +1, O is -2. (+1) + Mn + 4(-2) = 0 => Mn = +7."),
        ("K2Cr2O7", "Cr", "+6", ["+3", "+7", "+4"], "In K2Cr2O7: 2(+1) + 2(Cr) + 7(-2) = 0 => 2Cr = +12 => Cr = +6."),
        ("H2SO4", "S", "+6", ["+4", "+2", "-2"], "In H2SO4: 2(+1) + S + 4(-2) = 0 => S = +6."),
        ("Na2S2O3", "S", "+2", ["+4", "+6", "-2"], "In Na2S2O3: 2(+1) + 2(S) + 3(-2) = 0 => 2S = +4 => average oxidation state of S = +2."),
        ("HNO3", "N", "+5", ["+3", "+4", "-3"], "In HNO3: (+1) + N + 3(-2) = 0 => N = +5."),
        ("NH4+", "N", "-3", ["+3", "+5", "-4"], "In NH4+: N + 4(+1) = +1 => N = -3."),
        ("ClO4-", "Cl", "+7", ["+5", "+3", "-1"], "In ClO4-: Cl + 4(-2) = -1 => Cl = +7."),
        ("ClO3-", "Cl", "+5", ["+7", "+3", "+1"], "In ClO3-: Cl + 3(-2) = -1 => Cl = +5."),
        ("H3PO4", "P", "+5", ["+3", "+4", "-3"], "In H3PO4: 3(+1) + P + 4(-2) = 0 => P = +5."),
        ("H3PO3", "P", "+3", ["+5", "+1", "-3"], "In H3PO3: 3(+1) + P + 3(-2) = 0 => P = +3."),
        ("H2O2", "O", "-1", ["-2", "0", "+1"], "In peroxides like H2O2, hydrogen is +1, so 2(+1) + 2(O) = 0 => O = -1."),
        ("OF2", "O", "+2", ["-2", "-1", "+1"], "Because Fluorine is more electronegative (-1), in OF2: O + 2(-1) = 0 => O = +2."),
        ("NaH", "H", "-1", ["+1", "0", "+2"], "In metal hydrides such as NaH, sodium is +1, so hydrogen has an oxidation state of -1."),
        ("CrO4²-", "Cr", "+6", ["+3", "+4", "+2"], "In CrO4²-: Cr + 4(-2) = -2 => Cr = +6."),
        ("MnO4²-", "Mn", "+6", ["+7", "+4", "+2"], "In manganate ion MnO4²-: Mn + 4(-2) = -2 => Mn = +6."),
        ("MnO2", "Mn", "+4", ["+2", "+6", "+7"], "In MnO2: Mn + 2(-2) = 0 => Mn = +4."),
        ("SO3²-", "S", "+4", ["+6", "+2", "-2"], "In sulfite ion SO3²-: S + 3(-2) = -2 => S = +4."),
        ("CO3²-", "C", "+4", ["+2", "-4", "0"], "In carbonate ion CO3²-: C + 3(-2) = -2 => C = +4."),
        ("C2O4²-", "C", "+3", ["+4", "+2", "-2"], "In oxalate ion C2O4²-: 2C + 4(-2) = -2 => 2C = +6 => C = +3."),
        ("NO2-", "N", "+3", ["+5", "+4", "-3"], "In nitrite ion NO2-: N + 2(-2) = -1 => N = +3."),
        ("N2O", "N", "+1", ["+2", "+3", "-1"], "In nitrous oxide N2O: 2N + (-2) = 0 => N = +1."),
        ("Fe(CN)6³-", "Fe", "+3", ["+2", "+4", "+6"], "Since each cyanide (CN-) ligand has a charge of -1: Fe + 6(-1) = -3 => Fe = +3."),
        ("Fe(CN)6⁴-", "Fe", "+2", ["+3", "+4", "0"], "Since each CN- is -1: Fe + 6(-1) = -4 => Fe = +2."),
        ("Ni(CO)4", "Ni", "0", ["+2", "+4", "-2"], "Carbon monoxide (CO) is a neutral ligand, so in neutral Ni(CO)4 the oxidation state of Ni is 0."),
        ("KClO", "Cl", "+1", ["-1", "+3", "+5"], "In KClO (potassium hypochlorite): (+1) + Cl + (-2) = 0 => Cl = +1."),
        ("NaIO3", "I", "+5", ["+7", "+3", "-1"], "In NaIO3: (+1) + I + 3(-2) = 0 => I = +5."),
        ("H4P2O7", "P", "+5", ["+3", "+4", "+6"], "In pyrophosphoric acid H4P2O7: 4(+1) + 2P + 7(-2) = 0 => 2P = +10 => P = +5."),
        ("S4O6²-", "S", "+2.5", ["+2", "+4", "+6"], "In tetrathionate S4O6²-: 4S + 6(-2) = -2 => 4S = +10 => average oxidation state of S = +2.5."),
        ("XeF4", "Xe", "+4", ["+2", "+6", "0"], "In XeF4: Xe + 4(-1) = 0 => Xe = +4."),
        ("XeO3", "Xe", "+6", ["+4", "+3", "+8"], "In XeO3: Xe + 3(-2) = 0 => Xe = +6."),
    ]
    for formula, elem, corr, dists, exp in ox_items:
        q_text = f"What is the oxidation state of {elem} in {formula}?"
        questions.append(_make_mcq("CHM101", q_text, corr, dists, exp, rng))

    # 3. Molarity & Solution Stoichiometry problems (35 questions)
    solutes = [
        ("NaOH", 40.0),
        ("NaCl", 58.5),
        ("KOH", 56.0),
        ("H2SO4", 98.0),
        ("Na2CO3", 106.0),
        ("CaCO3", 100.0),
        ("C6H12O6 (glucose)", 180.0),
    ]
    volumes_ml = [200, 250, 400, 500, 750]
    for solute_name, mm in solutes:
        for vol_ml in volumes_ml:
            moles = rng.choice([0.1, 0.2, 0.25, 0.4, 0.5])
            mass_g = round(moles * mm, 2)
            vol_l = vol_ml / 1000.0
            molarity = round(moles / vol_l, 2)
            q_text = (
                f"What is the molarity of a solution prepared by dissolving {mass_g} g of {solute_name} "
                f"(Molar mass = {mm} g/mol) in enough water to make {vol_ml} mL of solution?"
            )
            corr = f"{molarity:.2f} M"
            dists = [
                f"{round(molarity * 0.5, 2):.2f} M",
                f"{round(molarity * 2.0, 2):.2f} M",
                f"{round(moles, 2):.2f} M",
            ]
            exp = (
                f"Moles of {solute_name} = mass / molar mass = {mass_g} / {mm} = {moles} mol. "
                f"Volume in liters = {vol_ml} / 1000 = {vol_l} L. "
                f"Molarity (M) = {moles} mol / {vol_l} L = {molarity:.2f} M."
            )
            questions.append(_make_mcq("CHM101", q_text, corr, dists, exp, rng))

    # 4. Gas Law problems (Boyle's, Charles's, Ideal Gas Law) (35 questions)
    p1_vals = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    v1_vals = [2.0, 3.0, 4.0, 6.0, 8.0]
    for p1 in p1_vals:
        for v1 in v1_vals:
            factor = rng.choice([2.0, 4.0, 0.5])
            p2 = round(p1 * factor, 2)
            v2 = round((p1 * v1) / p2, 2)
            q_text = (
                f"A sample of an ideal gas occupies {v1} L at a pressure of {p1} atm. "
                f"If the temperature remains constant (Boyle's Law), what volume will the gas occupy at {p2} atm?"
            )
            corr = f"{v2} L"
            dists = [
                f"{round(v1 * factor, 2)} L",
                f"{round(v2 + 1.5, 2)} L",
                f"{round(max(0.2, v2 - 0.5), 2)} L",
            ]
            exp = f"By Boyle's Law, P1V1 = P2V2 => V2 = (P1 × V1) / P2 = ({p1} × {v1}) / {p2} = {v2} L."
            questions.append(_make_mcq("CHM101", q_text, corr, dists, exp, rng))

    # 5. pH and pOH calculations (25 questions)
    h_exponents = range(1, 14)
    for exp_val in h_exponents:
        # Type A: Given [H+], find pH and pOH
        q1 = f"An aqueous solution at 25°C has a hydrogen ion concentration [H+] = 1.0 × 10^-{exp_val} M. What are its pH and pOH respectively?"
        ph = exp_val
        poh = 14 - exp_val
        corr1 = f"pH = {ph}, pOH = {poh}"
        dists1 = [
            f"pH = {poh}, pOH = {ph}",
            f"pH = {ph}, pOH = {ph}",
            f"pH = {max(0, ph - 1)}, pOH = {min(14, poh + 1)}",
        ]
        exp1 = f"pH = -log10[H+] = -log10(10^-{exp_val}) = {ph}. Since pH + pOH = 14 at 25°C, pOH = 14 - {ph} = {poh}."
        questions.append(_make_mcq("CHM101", q1, corr1, dists1, exp1, rng))

    for coeff in [2.0, 4.0, 5.0, 8.0]:
        for power in [2, 3, 4]:
            h_conc = coeff * (10 ** (-power))
            ph_val = round(-math.log10(h_conc), 2)
            q_text = f"Calculate the pH of a monoprotic strong acid solution with [H+] = {coeff} × 10^-{power} M (given log10({int(coeff)}) ≈ {math.log10(coeff):.2f})."
            corr = f"{ph_val:.2f}"
            dists = [f"{round(power + math.log10(coeff), 2):.2f}", f"{round(14 - ph_val, 2):.2f}", f"{round(ph_val + 1.0, 2):.2f}"]
            exp = f"pH = -log10({coeff} × 10^-{power}) = {power} - log10({int(coeff)}) = {power} - {math.log10(coeff):.2f} = {ph_val:.2f}."
            questions.append(_make_mcq("CHM101", q_text, corr, dists, exp, rng))

    # 6. Radioactive Half-life & Nuclear Chemistry (35 questions)
    isotopes = [
        ("Iodine-131", 8),
        ("Phosphorus-32", 14),
        ("Cobalt-60", 5),
        ("Sodium-24", 15),
        ("Radon-222", 4),
        ("Carbon-14", 5730),
        ("Technetium-99m", 6),
        ("Strontium-90", 29),
        ("Cesium-137", 30),
    ]
    for iso_name, half_life in isotopes:
        for num_hl in [1, 2, 3, 4, 5]:
            initial_mass = 64.0
            final_mass = initial_mass / (2 ** num_hl)
            total_time = half_life * num_hl
            q_text = (
                f"A radioactive sample of {iso_name} has a half-life of {half_life} time units. "
                f"Starting with {initial_mass:.0f} g of the isotope, how much remains undecayed after {total_time} time units?"
            )
            corr = f"{final_mass:g} g"
            dists = [
                f"{final_mass * 2:g} g",
                f"{final_mass / 2:g} g",
                f"{round(initial_mass / num_hl, 2):g} g",
            ]
            exp = (
                f"Number of half-lives n = {total_time} / {half_life} = {num_hl}. "
                f"Remaining mass N = N0 × (1/2)^n = {initial_mass:.0f} × (1/2)^{num_hl} = {final_mass:g} g."
            )
            questions.append(_make_mcq("CHM101", q_text, corr, dists, exp, rng))

    return questions[:200]


def generate_phy101_questions(rng: random.Random) -> list[dict]:
    questions = []

    # 1. Curated conceptual PHY 101 questions (50 questions)
    curated = [
        (
            "What are the fundamental SI dimensions of Force?",
            "[M L T^-2]",
            ["[M L^2 T^-2]", "[M L T^-1]", "[M L^-1 T^-2]"],
            "From Newton's second law, Force = mass × acceleration = [M] × [L T^-2] = [M L T^-2].",
        ),
        (
            "What are the SI dimensions of Work, Energy, and Torque?",
            "[M L^2 T^-2]",
            ["[M L T^-2]", "[M L^2 T^-3]", "[M L T^-1]"],
            "Work = Force × distance = [M L T^-2] × [L] = [M L^2 T^-2].",
        ),
        (
            "What are the SI dimensions of Power?",
            "[M L^2 T^-3]",
            ["[M L^2 T^-2]", "[M L T^-3]", "[M^2 L^2 T^-2]"],
            "Power = Work / time = [M L^2 T^-2] / [T] = [M L^2 T^-3].",
        ),
        (
            "Which of the following pairs consists exclusively of vector quantities?",
            "Impulse and Momentum",
            ["Work and Power", "Speed and Displacement", "Electric Potential and Force"],
            "Both impulse (F·Δt) and linear momentum (m·v) have magnitude and direction and obey vector addition.",
        ),
        (
            "At the highest point of a projectile's trajectory (neglecting air resistance), which statement is true?",
            "Its vertical velocity is zero, and its acceleration is g downward",
            ["Both its velocity and acceleration are zero", "Its horizontal velocity is zero, and acceleration is zero", "Its kinetic energy is always zero"],
            "At the apex, vy = 0 while horizontal velocity vx = u cosθ remains constant, and gravitational acceleration g (9.8 m/s² downward) acts continuously.",
        ),
        (
            "For a projectile launched over flat horizontal ground (neglecting air resistance), maximum horizontal range is achieved at a launch angle of:",
            "45°",
            ["30°", "60°", "90°"],
            "Since Range R = (u² sin 2θ) / g, R is maximum when sin 2θ = 1, meaning 2θ = 90° or θ = 45°.",
        ),
        (
            "Two projectiles are launched with the same initial speed u over level ground. Which pair of launch angles produces the exact same horizontal range?",
            "30° and 60°",
            ["30° and 45°", "20° and 60°", "45° and 90°"],
            "Complementary angles θ and (90° - θ) satisfy sin(2θ) = sin(2(90° - θ)), yielding identical horizontal ranges.",
        ),
        (
            "Newton's First Law of Motion defines the property of matter known as:",
            "Inertia",
            ["Impulse", "Elasticity", "Couple"],
            "Newton's First Law (the law of inertia) states that a body remains at rest or in uniform straight-line motion unless acted upon by a net external force.",
        ),
        (
            "In a perfectly inelastic collision between two isolated bodies:",
            "Linear momentum is conserved, kinetic energy is not conserved, and the bodies stick together",
            ["Both kinetic energy and momentum are conserved", "Kinetic energy is conserved, but momentum is lost", "Neither momentum nor total energy is conserved"],
            "Total linear momentum is conserved in all isolated collisions, whereas kinetic energy is partially converted to heat/deformation in inelastic collisions.",
        ),
        (
            "The area under a Force versus Time (F-t) graph represents:",
            "Impulse (or change in linear momentum)",
            ["Work done", "Power developed", "Kinetic energy"],
            "Impulse J = ∫ F dt, which equals the area under the Force-Time curve and equals Δp = mΔv.",
        ),
        (
            "The area under a Force versus Displacement (F-x) graph represents:",
            "Work done by the force",
            ["Impulse", "Linear momentum", "Average power"],
            "Work W = ∫ F dx, which corresponds to the area under the Force-Displacement graph.",
        ),
        (
            "For an object moving in uniform circular motion at constant speed v in a circle of radius r:",
            "Its velocity is tangential and changing, while its centripetal acceleration v²/r is directed toward the center",
            ["Its velocity is constant and its acceleration is zero", "Its acceleration is directed outward away from the center", "The net work done by the centripetal force per revolution is 2πrF"],
            "Because direction changes continuously, velocity changes; the centripetal acceleration a_c = v²/r points radially inward perpendicular to velocity (doing zero work).",
        ),
        (
            "Kepler's Second Law of planetary motion (the law of equal areas) is a direct consequence of the conservation of:",
            "Angular momentum",
            ["Linear momentum", "Mechanical energy", "Mass-energy"],
            "Because gravity is a central force producing zero torque (τ = 0), angular momentum L is constant, so dA/dt = L/(2m) is constant.",
        ),
        (
            "What happens to the period T of a simple pendulum of length L if the mass of the pendulum bob is doubled?",
            "The period remains unchanged",
            ["The period increases by a factor of √2", "The period doubles", "The period decreases by half"],
            "The period of a simple pendulum is T = 2π√(L/g), which is independent of the mass of the bob.",
        ),
        (
            "In Simple Harmonic Motion (SHM), where does the oscillating particle have its maximum speed?",
            "At the equilibrium (mean) position where displacement x = 0",
            ["At the extreme positions where x = ±A", "Halfway between equilibrium and amplitude", "Speed is constant throughout SHM"],
            "Since v = ω√(A² - x²), speed v is maximum (v_max = ωA) when displacement x = 0 at the equilibrium position.",
        ),
        (
            "According to Hooke's Law, the ratio of tensile stress to tensile strain within the proportional limit is called:",
            "Young's Modulus of Elasticity",
            ["Bulk Modulus", "Shear Modulus", "Poisson's Ratio"],
            "Young's Modulus E = Tensile Stress (F/A) / Tensile Strain (ΔL/L).",
        ),
        (
            "What is the elastic potential energy stored in a stretched wire or spring of force constant k extended by a distance x?",
            "½ k x²",
            ["k x²", "½ k x", "2 k x²"],
            "The work done in stretching a spring from 0 to x is W = ∫ kx dx = ½kx².",
        ),
        (
            "Archimedes' Principle states that when a body is wholly or partially immersed in a fluid, it experiences an upthrust equal to:",
            "The weight of the fluid displaced by the body",
            ["The weight of the immersed body itself", "The volume of the body multiplied by its own density", "The atmospheric pressure acting on the fluid surface"],
            "Upthrust (buoyant force) F_b = ρ_fluid × V_displaced × g, which is the weight of the displaced fluid.",
        ),
        (
            "Bernoulli's equation for an incompressible, non-viscous fluid in steady flow is based on the conservation of:",
            "Energy",
            ["Linear momentum", "Angular momentum", "Viscosity"],
            "Bernoulli's equation (P + ½ρv² + ρgh = constant) expresses conservation of mechanical energy per unit volume in a flowing fluid.",
        ),
        (
            "The Continuity Equation (A1 v1 = A2 v2) for an incompressible fluid in steady flow is a statement of the conservation of:",
            "Mass",
            ["Energy", "Momentum", "Pressure"],
            "Since fluid density ρ is constant, mass flow rate ρAv is constant along a streamline, giving A1v1 = A2v2.",
        ),
        (
            "The Zeroth Law of Thermodynamics provides the fundamental basis for defining and measuring:",
            "Temperature",
            ["Internal energy", "Entropy", "Specific latent heat"],
            "The Zeroth Law states that if body A is in thermal equilibrium with C, and B is in thermal equilibrium with C, then A and B are in thermal equilibrium (same temperature).",
        ),
        (
            "In an isothermal expansion of an ideal gas (ΔT = 0), how are the heat added (Q) and the work done by the gas (W) related?",
            "Q = W (since change in internal energy ΔU = 0)",
            ["Q = 0 and W = -ΔU", "W = 0 and Q = ΔU", "Q = -W"],
            "Internal energy U of an ideal gas depends only on temperature T. When ΔT = 0, ΔU = 0, so by the First Law (Q = ΔU + W), Q = W.",
        ),
        (
            "What is the escape velocity v_e from the surface of a planet of mass M, radius R, and surface gravity g?",
            "√(2gR)",
            ["√(gR)", "2√(gR)", "gR²"],
            "Setting ½mv_e² = GMm/R and using GM = gR² gives v_e = √(2GM/R) = √(2gR).",
        ),
        (
            "What is the angular velocity ω of the second hand of a standard analog clock?",
            "π / 30 rad/s",
            ["π / 60 rad/s", "2π rad/s", "π / 1800 rad/s"],
            "The second hand completes one full revolution (2π radians) in T = 60 seconds, so ω = 2π / 60 = π / 30 rad/s.",
        ),
        (
            "When water is heated from 0°C to 10°C, how does its volume change due to the anomalous expansion of water?",
            "It first decreases from 0°C to 4°C (reaching maximum density at 4°C) and then increases from 4°C to 10°C",
            ["It increases uniformly from 0°C to 10°C", "It decreases continuously from 0°C to 10°C", "It remains constant until 4°C and then drops"],
            "Water exhibits anomalous expansion: it contracts between 0°C and 4°C (maximum density of 1000 kg/m³ at 4°C) and expands above 4°C.",
        ),
        (
            "Why does steam at 100°C cause a much more severe burn than an equal mass of boiling water at 100°C?",
            "Steam releases a large amount of latent heat of vaporization when condensing into water at 100°C",
            ["Steam has a higher temperature than boiling water at 100°C", "Steam has a higher density than liquid water", "Water cannot transfer heat by conduction"],
            "Condensing 1 kg of steam at 100°C releases ~2.26 × 10^6 J of latent heat of vaporization before cooling even begins.",
        ),
        (
            "The dot (scalar) product of two non-zero vectors A and B is zero when the angle between them is:",
            "90°",
            ["0°", "45°", "180°"],
            "Since A · B = |A||B| cosθ, the dot product vanishes when cosθ = 0, i.e., θ = 90° (perpendicular vectors).",
        ),
        (
            "The magnitude of the cross (vector) product |A × B| of two non-zero vectors A and B is zero when the vectors are:",
            "Parallel (0°) or antiparallel (180°)",
            ["Perpendicular (90°)", "Inclined at 45°", "Inclined at 60°"],
            "Since |A × B| = |A||B| sinθ, the cross product vanishes when sinθ = 0, which occurs at θ = 0° or 180°.",
        ),
        (
            "Which mode of heat transfer does NOT require a material medium and can occur through a vacuum?",
            "Thermal radiation",
            ["Thermal conduction", "Natural convection", "Forced convection"],
            "Radiation transfers thermal energy via electromagnetic (infrared) waves, which propagate through vacuum at the speed of light.",
        ),
        (
            "What is the relationship between linear expansivity (α), area/superficial expansivity (β), and volume/cubic expansivity (γ) of an isotropic solid?",
            "β = 2α and γ = 3α",
            ["β = α² and γ = α³", "β = α/2 and γ = α/3", "α = 2β = 3γ"],
            "For small thermal expansions of an isotropic solid, superficial expansivity β ≈ 2α and cubic expansivity γ ≈ 3α.",
        ),
    ]

    for q_text, corr, dists, exp in curated:
        questions.append(_make_mcq("PHY101", q_text, corr, dists, exp, rng))

    # 2. Kinematics equations of motion (35 questions)
    u_vals = [0, 4, 6, 8, 10, 12, 15]
    a_vals = [2, 3, 4, 5, 6]
    for u in u_vals:
        for a in a_vals:
            t = rng.choice([3, 4, 5, 6, 8])
            v = u + a * t
            s = u * t + 0.5 * a * (t ** 2)
            q_text = (
                f"A particle starts with an initial velocity of {u} m/s and accelerates uniformly at {a} m/s² "
                f"for {t} s. What are its final velocity and total distance covered?"
            )
            corr = f"v = {v} m/s, s = {s:g} m"
            dists = [
                f"v = {u + a} m/s, s = {u * t + a * (t ** 2):g} m",
                f"v = {v} m/s, s = {v * t:g} m",
                f"v = {a * t} m/s, s = {0.5 * a * t:g} m",
            ]
            exp = (
                f"Using v = u + at = {u} + ({a})({t}) = {v} m/s, and "
                f"s = ut + ½at² = ({u})({t}) + 0.5({a})({t}²) = {s:g} m."
            )
            questions.append(_make_mcq("PHY101", q_text, corr, dists, exp, rng))

    # 3. Newton's Second Law & Kinetic Energy / Momentum (35 questions)
    masses = [2, 4, 5, 8, 10, 12, 20]
    velocities = [3, 5, 6, 8, 10]
    for m in masses:
        for v in velocities:
            ke = 0.5 * m * (v ** 2)
            mom = m * v
            q_text = f"A body of mass {m} kg moves with a uniform speed of {v} m/s. Calculate its kinetic energy (KE) and linear momentum (p)."
            corr = f"KE = {ke:g} J, p = {mom:g} kg·m/s"
            dists = [
                f"KE = {m * (v ** 2):g} J, p = {mom:g} kg·m/s",
                f"KE = {mom:g} J, p = {ke:g} kg·m/s",
                f"KE = {ke:g} J, p = {0.5 * mom:g} kg·m/s",
            ]
            exp = f"Kinetic energy KE = ½mv² = 0.5 × {m} × {v}² = {ke:g} J. Linear momentum p = mv = {m} × {v} = {mom:g} kg·m/s."
            questions.append(_make_mcq("PHY101", q_text, corr, dists, exp, rng))

    # 4. Projectile Motion & Vertical Free Fall (g = 10 m/s²) (30 questions)
    v0_list = [10, 20, 30, 40, 50, 60]
    angles = [(30, 0.5, 0.866), (45, 0.7071, 0.7071), (60, 0.866, 0.5), (90, 1.0, 0.0)]
    for v0 in v0_list:
        for deg, sin_val, _ in angles:
            g = 10.0
            h_max = round(((v0 * sin_val) ** 2) / (2 * g), 1)
            t_flight = round((2 * v0 * sin_val) / g, 2)
            q_text = (
                f"A projectile is launched at an angle of {deg}° to the horizontal with an initial speed of {v0} m/s. "
                f"Taking g = 10 m/s², what is the maximum height reached and the total time of flight?"
            )
            corr = f"H = {h_max:g} m, T = {t_flight:g} s"
            dists = [
                f"H = {round(h_max * 2, 1):g} m, T = {round(t_flight / 2, 2):g} s",
                f"H = {round((v0 ** 2) / (2 * g), 1):g} m, T = {t_flight:g} s",
                f"H = {h_max:g} m, T = {round(t_flight / 2, 2):g} s",
            ]
            exp = (
                f"Maximum height H = (u² sin²θ) / (2g) = ({v0} × {sin_val})² / 20 = {h_max:g} m. "
                f"Time of flight T = (2u sinθ) / g = (2 × {v0} × {sin_val}) / 10 = {t_flight:g} s."
            )
            questions.append(_make_mcq("PHY101", q_text, corr, dists, exp, rng))

    # 5. Work, Power, Centripetal Force & Springs (30 questions)
    for m in [2, 4, 5, 10, 15, 20]:
        for h in [5, 8, 10, 12, 15]:
            t = 4
            g = 10
            work = m * g * h
            power = work / t
            q_text = (
                f"A crane lifts a load of mass {m} kg vertically through a height of {h} m in {t} s at constant speed "
                f"(take g = 10 m/s²). What is the work done against gravity and the average power developed?"
            )
            corr = f"W = {work:g} J, P = {power:g} W"
            dists = [
                f"W = {m * h:g} J, P = {(m * h) / t:g} W",
                f"W = {work:g} J, P = {work * t:g} W",
                f"W = {work / 2:g} J, P = {power / 2:g} W",
            ]
            exp = f"Work done W = mgh = {m} × 10 × {h} = {work:g} J. Power P = W / t = {work:g} / {t} = {power:g} W."
            questions.append(_make_mcq("PHY101", q_text, corr, dists, exp, rng))

    # 6. Calorimetry & Ohm's Law / Thermal Physics (50 questions)
    for mass_kg in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]:
        for dt in [10, 15, 20, 25, 30, 40, 50]:
            c_water = 4200
            q_joules = mass_kg * c_water * dt
            q_kj = q_joules / 1000.0
            q_text = (
                f"How much thermal energy (in kJ) is required to raise the temperature of {mass_kg} kg of water "
                f"by {dt}°C? (Specific heat capacity of water = 4200 J kg⁻¹ °C⁻¹)"
            )
            corr = f"{q_kj:g} kJ"
            dists = [
                f"{q_kj / 2:g} kJ",
                f"{q_kj * 2:g} kJ",
                f"{round(mass_kg * dt, 2):g} kJ",
            ]
            exp = f"Heat Q = m c ΔT = {mass_kg} × 4200 × {dt} = {q_joules:g} J = {q_kj:g} kJ."
            questions.append(_make_mcq("PHY101", q_text, corr, dists, exp, rng))

    return questions[:200]


def generate_mth101_questions(rng: random.Random) -> list[dict]:
    questions = []

    # 1. Curated MTH 101 conceptual & algebraic questions (40 questions)
    curated = [
        (
            "If A and B are two finite sets, the Principle of Inclusion-Exclusion states that n(A ∪ B) equals:",
            "n(A) + n(B) - n(A ∩ B)",
            ["n(A) + n(B) + n(A ∩ B)", "n(A) × n(B) - n(A ∩ B)", "n(A) - n(B) + n(A ∩ B)"],
            "Elements in the intersection A ∩ B are counted in both n(A) and n(B), so n(A ∪ B) = n(A) + n(B) - n(A ∩ B).",
        ),
        (
            "According to De Morgan's Laws for sets, the complement of the union (A ∪ B)' is equal to:",
            "A' ∩ B'",
            ["A' ∪ B'", "A ∩ B", "(A' ∩ B)'"],
            "De Morgan's Law states that (A ∪ B)' = A' ∩ B' and (A ∩ B)' = A' ∪ B'.",
        ),
        (
            "How many subsets (elements in the power set P(A)) does a finite set A with n = 6 elements have?",
            "64",
            ["36", "12", "32"],
            "A set with n elements has 2^n subsets. For n = 6, 2^6 = 64.",
        ),
        (
            "For a quadratic equation ax² + bx + c = 0 (a ≠ 0) with roots α and β, what are the sum (α + β) and product (αβ) of the roots?",
            "α + β = -b/a and αβ = c/a",
            ["α + β = b/a and αβ = -c/a", "α + β = c/a and αβ = -b/a", "α + β = -a/b and αβ = a/c"],
            "Dividing ax² + bx + c = 0 by a gives x² - (α + β)x + αβ = 0, so α + β = -b/a and αβ = c/a.",
        ),
        (
            "When does a quadratic equation ax² + bx + c = 0 have two equal (repeated) real roots?",
            "When the discriminant b² - 4ac = 0",
            ["When b² - 4ac > 0", "When b² - 4ac < 0", "When b = 0"],
            "The quadratic formula gives equal roots when the discriminant Δ = b² - 4ac equals zero.",
        ),
        (
            "What is the value of i^47, where i = √(-1)?",
            "-i",
            ["i", "-1", "1"],
            "Since i^4 = 1 and 47 = 4(11) + 3, i^47 = (i^4)^11 × i^3 = 1 × (-i) = -i.",
        ),
        (
            "What is the modulus |z| and conjugate z* of the complex number z = 3 - 4i?",
            "|z| = 5, z* = 3 + 4i",
            ["|z| = 7, z* = -3 + 4i", "|z| = 25, z* = 3 + 4i", "|z| = 5, z* = -3 - 4i"],
            "|z| = √(3² + (-4)²) = √(9 + 16) = 5, and the complex conjugate changes the sign of the imaginary part: z* = 3 + 4i.",
        ),
        (
            "In the binomial expansion of (a + b)^n, how many terms are there when n is a positive integer?",
            "n + 1",
            ["n", "2n", "n - 1"],
            "The expansion sums from r = 0 to r = n, giving n + 1 terms in total.",
        ),
        (
            "What is the sum to infinity (S_∞) of a convergent Geometric Progression with first term a = 12 and common ratio r = 1/3?",
            "18",
            ["16", "24", "36"],
            "Using S_∞ = a / (1 - r) for |r| < 1: S_∞ = 12 / (1 - 1/3) = 12 / (2/3) = 18.",
        ),
        (
            "Which trigonometric identity is universally valid for all real angles θ?",
            "sin²θ + cos²θ = 1",
            ["sin²θ - cos²θ = 1", "tan²θ + sec²θ = 1", "1 + cos²θ = sin²θ"],
            "By the Pythagorean theorem on the unit circle, sin²θ + cos²θ = 1 for all θ.",
        ),
        (
            "What is the double-angle formula for sin(2θ)?",
            "2 sinθ cosθ",
            ["cos²θ - sin²θ", "2 sinθ", "sin²θ + cos²θ"],
            "From sin(A + B) = sinA cosB + cosA sinB with A = B = θ, we obtain sin(2θ) = 2 sinθ cosθ.",
        ),
        (
            "Evaluate the standard limit: lim (x → 0) [sin(5x) / x].",
            "5",
            ["1", "0", "1/5"],
            "Rewriting as 5 × lim(x→0) [sin(5x)/(5x)] and using lim(u→0) (sin u)/u = 1 gives 5 × 1 = 5.",
        ),
        (
            "What is the derivative d/dx (ln x) for x > 0?",
            "1 / x",
            ["x ln x", "e^x", "-1 / x²"],
            "The derivative of the natural logarithm ln(x) with respect to x is 1/x.",
        ),
        (
            "What is the derivative d/dx (sin x) and d/dx (cos x) respectively?",
            "cos x and -sin x",
            ["-cos x and sin x", "cos x and sin x", "sec²x and -sin x"],
            "Standard trigonometric derivatives are d/dx(sin x) = cos x and d/dx(cos x) = -sin x.",
        ),
        (
            "A square matrix A is said to be singular (non-invertible) if and only if:",
            "det(A) = 0",
            ["det(A) = 1", "trace(A) = 0", "A is a diagonal matrix"],
            "A square matrix has an inverse A⁻¹ = (1/det(A)) adj(A) if and only if det(A) ≠ 0; when det(A) = 0 it is singular.",
        ),
        (
            "If f(x) = x³ - 6x² + 9x + 2, at what values of x does f(x) have stationary (turning) points?",
            "x = 1 and x = 3",
            ["x = 0 and x = 3", "x = -1 and x = -3", "x = 2 and x = 3"],
            "Setting f'(x) = 3x² - 12x + 9 = 3(x - 1)(x - 3) = 0 gives stationary points at x = 1 and x = 3.",
        ),
        (
            "In how many ways can the letters of the word 'MATHS' (5 distinct letters) be arranged in a row?",
            "120",
            ["60", "24", "25"],
            "The number of permutations of 5 distinct letters is 5! = 5 × 4 × 3 × 2 × 1 = 120.",
        ),
        (
            "Convert the angle 150° into radians.",
            "5π / 6",
            ["3π / 4", "2π / 3", "7π / 6"],
            "150° × (π / 180°) = 15π / 18 = 5π / 6 radians.",
        ),
        (
            "What is the coefficient of x³ in the binomial expansion of (1 + 2x)^5?",
            "80",
            ["40", "10", "160"],
            "The x³ term is 5C3 × 1² × (2x)³ = 10 × 8x³ = 80x³, so the coefficient is 80.",
        ),
        (
            "By the Remainder Theorem, when a polynomial P(x) is divided by (x - a), the remainder is equal to:",
            "P(a)",
            ["P(-a)", "P(0)", "P'(a)"],
            "Writing P(x) = (x - a)Q(x) + R and substituting x = a immediately gives R = P(a).",
        ),
    ]

    for q_text, corr, dists, exp in curated:
        questions.append(_make_mcq("MTH101", q_text, corr, dists, exp, rng))

    # 2. Quadratic equations & roots (35 questions)
    root_pairs = [
        (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (2, 7),
        (3, 4), (3, 5), (3, 7), (4, 5), (4, 6), (5, 6), (-2, 3),
        (-3, 4), (-4, 5), (-1, 6), (-2, 7), (-3, 5), (-5, 6),
        (2, 2), (3, 3), (4, 4), (-2, -5), (-3, -4), (-1, -7),
        (1, 8), (2, 9), (3, 8), (4, 7), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8),
    ]
    for r1, r2 in root_pairs:
        s = r1 + r2
        p = r1 * r2
        b_coef = -s
        c_coef = p
        b_str = f"+ {b_coef}x" if b_coef >= 0 else f"- {abs(b_coef)}x"
        c_str = f"+ {c_coef}" if c_coef >= 0 else f"- {abs(c_coef)}"
        q_text = f"Solve the quadratic equation: x² {b_str} {c_str} = 0."
        if r1 == r2:
            corr = f"x = {r1} (repeated)"
            dists = [f"x = {-r1} (repeated)", f"x = {r1}, x = {-r1}", f"x = {r1 + 1}, x = {r1 - 1}"]
        else:
            corr = f"x = {r1}, x = {r2}"
            dists = [
                f"x = {-r1}, x = {-r2}",
                f"x = {r1 + 1}, x = {r2 - 1}",
                f"x = {r1}, x = {-r2}",
            ]
        exp = f"Factoring gives (x - ({r1}))(x - ({r2})) = 0, so the roots are {corr}."
        questions.append(_make_mcq("MTH101", q_text, corr, dists, exp, rng))

    # 3. Differentiation (Power rule & polynomials) (35 questions)
    for a in [2, 3, 4, 5, 6, 7, 8]:
        for b in [2, 3, 5, 7, 9]:
            x_val = rng.choice([1, 2, 3])
            # f(x) = a x^3 - b x^2 + 4x - 1
            # f'(x) = 3a x^2 - 2b x + 4
            deriv_val = 3 * a * (x_val ** 2) - 2 * b * x_val + 4
            q_text = f"Given f(x) = {a}x³ - {b}x² + 4x - 1, evaluate the derivative f'({x_val})."
            corr = f"{deriv_val}"
            dists = [
                f"{deriv_val + 2 * b}",
                f"{a * (x_val ** 3) - b * (x_val ** 2) + 4 * x_val - 1}",
                f"{deriv_val - 4}",
            ]
            exp = (
                f"Differentiating term-by-term: f'(x) = {3 * a}x² - {2 * b}x + 4. "
                f"At x = {x_val}: f'({x_val}) = {3 * a}({x_val})² - {2 * b}({x_val}) + 4 = {deriv_val}."
            )
            questions.append(_make_mcq("MTH101", q_text, corr, dists, exp, rng))

    # 4. Arithmetic Progression (AP) nth term and sum (30 questions)
    for a1 in [3, 5, 7, 10, 12, 15]:
        for d in [2, 3, 4, 5, 6]:
            n = rng.choice([10, 12, 15, 20])
            tn = a1 + (n - 1) * d
            sn = (n * (2 * a1 + (n - 1) * d)) // 2
            q_text = (
                f"An Arithmetic Progression (A.P.) has first term a = {a1} and common difference d = {d}. "
                f"Find the {n}th term (T_{n}) and the sum of the first {n} terms (S_{n})."
            )
            corr = f"T_{n} = {tn}, S_{n} = {sn}"
            dists = [
                f"T_{n} = {a1 + n * d}, S_{n} = {sn + n}",
                f"T_{n} = {tn}, S_{n} = {n * tn}",
                f"T_{n} = {tn - d}, S_{n} = {sn - a1}",
            ]
            exp = (
                f"T_{n} = a + (n - 1)d = {a1} + ({n - 1})({d}) = {tn}. "
                f"S_{n} = (n/2)(a + T_{n}) = ({n}/2)({a1} + {tn}) = {sn}."
            )
            questions.append(_make_mcq("MTH101", q_text, corr, dists, exp, rng))

    # 5. 2x2 Matrix Determinants (30 questions)
    mat_configs = [
        (3, 2, 1, 4), (5, 3, 2, 4), (6, 1, 3, 2), (4, -2, 3, 5), (7, 3, 2, 3),
        (8, 2, 3, 4), (5, -1, 4, 2), (9, 4, 2, 3), (6, 5, 2, 3), (4, 7, 1, 5),
        (10, 3, 2, 4), (3, -4, 2, 5), (7, -2, 3, 4), (5, 6, 3, 4), (8, 5, 2, 3),
        (2, 9, 1, 6), (4, 3, 5, 2), (7, 4, 5, 3), (6, -3, 2, 4), (5, 2, -3, 4),
        (9, 2, 4, 3), (11, 3, 3, 2), (8, -1, 5, 2), (6, 4, 1, 5), (7, 5, 4, 3),
        (3, 8, 2, 7), (5, 9, 1, 4), (12, 5, 2, 3), (4, -5, 2, 3), (6, 7, 2, 5),
    ]
    for a, b, c, d in mat_configs:
        det = a * d - b * c
        q_text = f"Evaluate the determinant of the 2×2 matrix A = [[{a}, {b}], [{c}, {d}]]."
        corr = f"{det}"
        dists = [
            f"{a * d + b * c}",
            f"{a * b - c * d}",
            f"{-det if det != 0 else 5}",
        ]
        exp = f"For A = [[a, b], [c, d]], det(A) = ad - bc = ({a})({d}) - ({b})({c}) = {a * d} - ({b * c}) = {det}."
        questions.append(_make_mcq("MTH101", q_text, corr, dists, exp, rng))

    # 6. Definite Integrals & Limits (50 questions)
    for k in range(1, 26):
        # Integral from 0 to 2 of (3*k x^2 + 2x) dx = [k x^3 + x^2]_0^2 = 8k + 4
        val1 = 8 * k + 4
        q1 = f"Evaluate the definite integral: ∫₀² ({3 * k}x² + 2x) dx."
        corr1 = f"{val1}"
        dists1 = [f"{4 * k + 2}", f"{8 * k + 2}", f"{6 * k + 4}"]
        exp1 = f"Antiderivative is [{k}x³ + x²] evaluated from 0 to 2: {k}(2³) + 2² - 0 = {8 * k} + 4 = {val1}."
        questions.append(_make_mcq("MTH101", q1, corr1, dists1, exp1, rng))

        # Limit as x -> k of (x^2 - k^2)/(x - k) = 2k
        val2 = 2 * k
        q2 = f"Evaluate the limit: lim (x → {k}) [(x² - {k**2}) / (x - {k})]."
        corr2 = f"{val2}"
        dists2 = [f"{k}", f"{k**2}", "0"]
        exp2 = f"Factor the numerator: (x - {k})(x + {k}) / (x - {k}) = x + {k}. Taking x → {k} gives {k} + {k} = {val2}."
        questions.append(_make_mcq("MTH101", q2, corr2, dists2, exp2, rng))

    return questions[:200]


def generate_bio101_questions(rng: random.Random) -> list[dict]:
    questions = []

    # 1. Comprehensive BIO 101 university bank (Cell Biology, Genetics, Taxonomy, Physiology, Ecology, Biochemistry)
    curated_bio = [
        (
            "Which cellular organelle is the primary site of oxidative phosphorylation and ATP synthesis in eukaryotes?",
            "Mitochondrion",
            ["Golgi apparatus", "Ribosome", "Smooth endoplasmic reticulum"],
            "Mitochondria generate most of the cell's ATP through the Krebs cycle (in the matrix) and oxidative phosphorylation (on the inner cristae membrane).",
        ),
        (
            "Which organelle is responsible for modifying, sorting, and packaging proteins for secretion?",
            "Golgi apparatus",
            ["Lysosome", "Peroxisome", "Nucleolus"],
            "The Golgi apparatus receives proteins from the rough ER, modifies them (e.g., glycosylation), and packages them into vesicles.",
        ),
        (
            "Where are ribosomal RNA (rRNA) molecules synthesized and ribosome subunits assembled within a eukaryotic cell?",
            "Nucleolus",
            ["Centrosome", "Smooth ER", "Peroxisome"],
            "The nucleolus is a dense region inside the nucleus dedicated to rRNA transcription and ribosomal subunit assembly.",
        ),
        (
            "Which organelle contains hydrolytic enzymes for intracellular digestion and autophagy in animal cells?",
            "Lysosome",
            ["Ribosome", "Plastid", "Mesosome"],
            "Lysosomes contain acid hydrolases that break down macromolecules, worn-out organelles, and engulfed pathogens.",
        ),
        (
            "The Fluid Mosaic Model of the plasma membrane was proposed in 1972 by:",
            "Singer and Nicolson",
            ["Watson and Crick", "Schleiden and Schwann", "Davson and Danielli"],
            "S.J. Singer and G.L. Nicolson proposed the Fluid Mosaic Model describing a phospholipid bilayer with embedded integral and peripheral proteins.",
        ),
        (
            "Which of the following structures is present in plant cells but ABSENT in typical animal cells?",
            "Cellulose cell wall, chloroplasts, and a large central vacuole",
            ["Mitochondria and plasma membrane", "80S ribosomes and Golgi bodies", "Nucleus and endoplasmic reticulum"],
            "Plant cells possess a rigid cellulose cell wall, plastids (chloroplasts), plasmodesmata, and a large central vacuole bounded by a tonoplast.",
        ),
        (
            "Prokaryotic cells (such as bacteria) differ from eukaryotic cells because prokaryotes possess:",
            "70S ribosomes and circular DNA in a nucleoid without a nuclear envelope",
            ["80S ribosomes and membrane-bound mitochondria", "Linear chromosomes bound to histone octamers inside a nucleus", "Chloroplasts and endoplasmic reticulum"],
            "Prokaryotes lack a membrane-bound nucleus and membrane-bound organelles, and they have 70S ribosomes in their cytoplasm.",
        ),
        (
            "During which phase of the cell cycle does DNA replication take place?",
            "S (Synthesis) phase of Interphase",
            ["G1 phase of Interphase", "Prophase", "Metaphase"],
            "DNA synthesis (replication) occurs during the S phase of interphase, doubling the DNA content from 2C to 4C before mitosis or meiosis.",
        ),
        (
            "During which stage of mitosis do chromosomes align along the equatorial plane (metaphase plate) of the spindle?",
            "Metaphase",
            ["Prophase", "Anaphase", "Telophase"],
            "In metaphase, spindle fibers attach to kinetochores and align chromosomes along the equatorial metaphase plate.",
        ),
        (
            "Separation of sister chromatids and their movement toward opposite spindle poles occurs during:",
            "Anaphase of mitosis (and Anaphase II of meiosis)",
            ["Prophase I of meiosis", "Metaphase of mitosis", "Telophase I of meiosis"],
            "During anaphase, centromeres split and sister chromatids are pulled apart toward opposite poles.",
        ),
        (
            "Crossing over (exchange of genetic material between non-sister chromatids of homologous chromosomes) occurs during:",
            "Pachytene substage of Prophase I in Meiosis",
            ["Metaphase I of Meiosis", "Anaphase II of Meiosis", "Prophase of Mitosis"],
            "Synapsis occurs in zygotene and genetic crossing over at chiasmata takes place during pachytene of Prophase I in meiosis.",
        ),
        (
            "In a classic Mendelian monohybrid cross between two heterozygous tall pea plants (Tt × Tt), what is the phenotypic ratio in the F2 generation?",
            "3 Tall : 1 Dwarf",
            ["1 Tall : 1 Dwarf", "1 Tall : 2 Intermediate : 1 Dwarf", "All Tall (4 : 0)"],
            "Crossing Tt × Tt gives genotypes 1 TT : 2 Tt : 1 tt. Since T is completely dominant, 3/4 are Tall and 1/4 are Dwarf (3:1 phenotypic ratio).",
        ),
        (
            "In a Mendelian dihybrid cross between two double heterozygotes (RrYy × RrYy), what is the expected F2 phenotypic ratio?",
            "9 : 3 : 3 : 1",
            ["3 : 1", "1 : 1 : 1 : 1", "1 : 2 : 1"],
            "By Mendel's Law of Independent Assortment, two independent 3:1 traits combine to give a 9:3:3:1 phenotypic ratio.",
        ),
        (
            "What is a 'test cross' in genetics?",
            "Crossing an individual of dominant phenotype (unknown genotype) with a homozygous recessive individual",
            ["Crossing two F1 hybrids together", "Crossing two homozygous dominant parents", "Crossing individuals from two different species"],
            "A test cross mates an organism showing a dominant trait with a homozygous recessive tester to determine whether the dominant parent is homozygous or heterozygous.",
        ),
        (
            "In a dihybrid test cross (RrYy × rryy) with unlinked genes, what is the expected phenotypic ratio of the offspring?",
            "1 : 1 : 1 : 1",
            ["9 : 3 : 3 : 1", "3 : 1", "1 : 2 : 1"],
            "The heterozygote RrYy produces 4 gametes (RY, Ry, rY, ry) in equal 1:1:1:1 proportions, and rryy produces only ry.",
        ),
        (
            "The human ABO blood group system illustrates which genetic phenomena?",
            "Multiple alleles (I^A, I^B, i) and codominance (between I^A and I^B)",
            ["Polygenic inheritance and sex-linkage", "Incomplete dominance only", "Cytoplasmic inheritance"],
            "Three alleles (I^A, I^B, i) govern ABO blood type: I^A and I^B are codominant (producing type AB), and both are completely dominant over i (type O).",
        ),
        (
            "Hemophilia and red-green color blindness are more common in human males than females because they are:",
            "X-linked recessive traits (males are hemizygous XY and need only one recessive allele)",
            ["Y-linked dominant traits", "Autosomal dominant traits", "Mitochondrial traits inherited from the father"],
            "Males have only one X chromosome (XY), so a single recessive allele on their X chromosome is expressed phenotypically.",
        ),
        (
            "In DNA, adenine (A) pairs with thymine (T) and guanine (G) pairs with cytosine (C). How many hydrogen bonds form between A-T and G-C respectively?",
            "2 hydrogen bonds between A-T, and 3 hydrogen bonds between G-C",
            ["3 hydrogen bonds between A-T, and 2 hydrogen bonds between G-C", "2 hydrogen bonds in both pairs", "1 covalent bond in each pair"],
            "A=T base pairs are stabilized by 2 hydrogen bonds, whereas G≡C base pairs are stabilized by 3 hydrogen bonds.",
        ),
        (
            "Which nitrogenous base is found in RNA molecules in place of Thymine?",
            "Uracil (U)",
            ["Adenine (A)", "Cytosine (C)", "Xanthine"],
            "RNA contains Adenine, Guanine, Cytosine, and Uracil (U) instead of Thymine (T), as well as ribose sugar instead of deoxyribose.",
        ),
        (
            "How do biological enzymes increase the rate of biochemical reactions?",
            "By lowering the activation energy of the reaction without being consumed",
            ["By making endergonic reactions exergonic (changing ΔG)", "By increasing the temperature of the cytoplasm", "By shifting the equilibrium constant toward products"],
            "Enzymes are biological catalysts that stabilize the transition state and lower activation energy (E_a) without altering ΔG or equilibrium.",
        ),
        (
            "In photosynthesis, the light-dependent reactions take place in the _____, whereas the Calvin cycle (light-independent reactions) occurs in the _____.",
            "Thylakoid membranes (grana); Stroma of the chloroplast",
            ["Stroma; Thylakoid membranes", "Mitochondrial matrix; Cytoplasm", "Outer chloroplast membrane; Vacuole"],
            "Photosystems I and II reside in the thylakoid membranes where ATP and NADPH are generated; carbon fixation (Calvin cycle) occurs in the stroma.",
        ),
        (
            "What is the source of the oxygen gas (O2) released during oxygenic photosynthesis in green plants?",
            "Photolysis (splitting) of water (H2O)",
            ["Splitting of carbon dioxide (CO2)", "Breakdown of glucose", "Reduction of NADP+"],
            "Ruben and Kamen's 18O isotope tracer experiments proved that evolved O2 comes exclusively from the photolysis of water (2H2O → 4H+ + 4e- + O2).",
        ),
        (
            "Where does glycolysis take place in both prokaryotic and eukaryotic cells, and what is its net ATP yield per glucose molecule?",
            "Cytoplasm (cytosol); net gain of 2 ATP and 2 NADH",
            ["Mitochondrial matrix; net gain of 36 ATP", "Inner mitochondrial membrane; net gain of 4 ATP", "Chloroplast stroma; net gain of 18 ATP"],
            "Glycolysis occurs in the cytosol without requiring oxygen, consuming 2 ATP and producing 4 ATP (net 2 ATP), 2 NADH, and 2 pyruvate molecules.",
        ),
        (
            "Who introduced the binomial nomenclature system for naming organisms (Genus + species)?",
            "Carolus Linnaeus",
            ["Charles Darwin", "Robert Whittaker", "Gregor Mendel"],
            "Carolus Linnaeus established binomial nomenclature in Species Plantarum (1753) and Systema Naturae.",
        ),
        (
            "What is the correct hierarchical order of taxonomic categories from broadest (highest) to most specific?",
            "Domain → Kingdom → Phylum → Class → Order → Family → Genus → Species",
            ["Kingdom → Class → Phylum → Order → Family → Genus → Species", "Domain → Phylum → Kingdom → Order → Class → Family → Species", "Kingdom → Phylum → Order → Class → Genus → Family → Species"],
            "The standard taxonomic hierarchy is Domain, Kingdom, Phylum (or Division in plants), Class, Order, Family, Genus, Species.",
        ),
        (
            "In Robert Whittaker's Five-Kingdom classification, unicellular eukaryotic organisms (such as Amoeba, Paramecium, and Euglena) belong to Kingdom:",
            "Protista",
            ["Monera", "Fungi", "Animalia"],
            "Kingdom Monera comprises prokaryotes (bacteria), whereas Kingdom Protista comprises predominantly unicellular eukaryotes.",
        ),
        (
            "Fungi differ fundamentally from green plants because fungi are:",
            "Heterotrophic (absorptive saprophytes/parasites) with cell walls made of chitin and no chlorophyll",
            ["Autotrophic organisms with cellulose cell walls", "Prokaryotic organisms lacking nuclei", "Phagocytic organisms without cell walls"],
            "Fungi lack chlorophyll, obtain nutrients by extracellular digestion and absorption, store glycogen, and have chitinous cell walls.",
        ),
        (
            "Why are Bryophytes (mosses and liverworts) referred to as the 'amphibians of the plant kingdom'?",
            "They live on land but require external liquid water for flagellated sperm to swim to the egg during fertilization",
            ["They possess both xylem and phloem vessels like aquatic ferns", "They spend half their life cycle inside fish gills", "They produce seeds that only germinate underwater"],
            "Bryophytes are non-vascular land plants whose motile antherozoids require a film of water for fertilization, and their dominant phase is the haploid gametophyte.",
        ),
        (
            "In vascular plants, _____ transports water and dissolved mineral salts upward from the roots, while _____ translocates organic sugars (sucrose).",
            "Xylem; Phloem",
            ["Phloem; Xylem", "Cambium; Epidermis", "Cortex; Pith"],
            "Xylem (tracheids and vessels) conducts water and minerals unidirectionally upward; phloem (sieve tubes and companion cells) translocates photosynthates bidirectionally.",
        ),
        (
            "Which plant hormone (phytohormone) is primarily responsible for apical dominance and phototropism (bending of shoots toward light)?",
            "Auxin (Indole-3-acetic acid, IAA)",
            ["Abscisic acid (ABA)", "Ethylene", "Cytokinin"],
            "Auxin accumulates on the shaded side of a coleoptile/shoot, stimulating cell elongation so the shoot bends toward light, and maintains apical dominance.",
        ),
        (
            "Which chamber of the mammalian heart has the thickest muscular wall (myocardium), and why?",
            "Left ventricle, because it pumps oxygenated blood at high pressure to the entire systemic circulation",
            ["Right ventricle, because it pumps blood to the lungs", "Left atrium, because it receives blood from the vena cava", "Right atrium, because it contains the sinoatrial node"],
            "The left ventricle must generate high systolic pressure to propel blood through the aorta to the whole body, whereas the right ventricle only pumps to the nearby lungs.",
        ),
        (
            "What is the functional structural filtering unit of the mammalian kidney?",
            "Nephron",
            ["Neuron", "Alveolus", "Sarcomere"],
            "Each kidney contains ~1 million nephrons (comprising Bowman's capsule, glomerulus, proximal tubule, Loop of Henle, distal tubule, and collecting duct).",
        ),
        (
            "According to Lindeman's 10% Law of energy flow in an ecological food chain:",
            "Only about 10% of the energy at one trophic level is stored as biomass and transferred to the next higher trophic level",
            ["90% of solar energy is captured by primary producers", "Decomposers receive 10% of the sun's total radiation", "Energy is recycled 10 times within a food web"],
            "Roughly 90% of energy is lost as metabolic heat and unassimilated waste at each trophic transfer, leaving ~10% for the next trophic level.",
        ),
        (
            "A mutually beneficial symbiotic association between a fungus and the roots of a vascular plant is called a:",
            "Mycorrhiza",
            ["Lichen", "Rhizobium nodule", "Haustorium"],
            "Mycorrhizae are mutualistic fungus-root associations where the fungus increases water/phosphate uptake and the plant supplies carbohydrates. (Lichens are fungus + alga/cyanobacterium).",
        ),
        (
            "In the nitrogen cycle, the conversion of ammonia (NH3/NH4+) into nitrites (NO2-) and then nitrates (NO3-) by soil bacteria (Nitrosomonas and Nitrobacter) is called:",
            "Nitrification",
            ["Denitrification", "Nitrogen fixation", "Ammonification"],
            "Nitrosomonas oxidizes ammonia to nitrite (NO2-), and Nitrobacter oxidizes nitrite to nitrate (NO3-) in the process of nitrification.",
        ),
        (
            "Structures in different species that share a common evolutionary origin and basic anatomical plan (such as the human arm, bat wing, and whale flipper) are called:",
            "Homologous structures (resulting from divergent evolution)",
            ["Analogous structures (resulting from convergent evolution)", "Vestigial structures", "Atavistic structures"],
            "Homologous organs have the same embryonic origin (pentadactyl limb) adapted to different functions through divergent evolution.",
        ),
        (
            "Which bond links amino acids together in the primary structure of a polypeptide chain?",
            "Peptide bond (formed by condensation between -COOH and -NH2 groups)",
            ["Glycosidic bond", "Phosphodiester bond", "Ester bond"],
            "Amino acids polymerize via condensation reactions removing water to form covalent amide/peptide (-CO-NH-) bonds.",
        ),
        (
            "Which polysaccharide serves as the main carbohydrate energy storage molecule in animal liver and muscle cells?",
            "Glycogen",
            ["Starch (amylose and amylopectin)", "Cellulose", "Chitin"],
            "Animals store glucose as highly branched glycogen in liver and skeletal muscle, whereas plants store starch.",
        ),
        (
            "What happens to a red blood cell (erythrocyte) when placed in a hypertonic salt solution?",
            "Water leaves the cell by osmosis, causing the cell to shrink and crenate",
            ["Water enters the cell by osmosis, causing hemolysis (bursting)", "The cell becomes turgid without changing shape", "No net movement of water occurs"],
            "In a hypertonic external medium (lower water potential), water diffuses out of the red blood cell by exosmosis, leading to shrinkage (crenation).",
        ),
        (
            "What happens to a plant cell when placed in a hypotonic solution (such as pure distilled water)?",
            "Water enters by endosmosis until the cell becomes fully turgid, prevented from bursting by its rigid cell wall",
            ["The cell undergoes plasmolysis and shrinks away from the cell wall", "The cell bursts immediately like an animal cell", "Water leaves the central vacuole"],
            "Endosmosis swells the protoplast against the rigid cellulose cell wall, generating turgor pressure (wall pressure) that prevents lysis.",
        ),
    ]

    for q_text, corr, dists, exp in curated_bio:
        questions.append(_make_mcq("BIO101", q_text, corr, dists, exp, rng))

    # 2. Chargaff's Rule DNA Base Composition problems (25 questions)
    for a_pct in range(12, 37):
        t_pct = a_pct
        rem = 100 - 2 * a_pct
        g_pct = rem / 2.0
        c_pct = g_pct
        g_str = f"{g_pct:g}%"
        q_text = (
            f"Analysis of a double-stranded DNA molecule shows that it contains {a_pct}% Adenine (A). "
            f"According to Chargaff's rules, what are the percentages of Thymine (T), Guanine (G), and Cytosine (C)?"
        )
        corr = f"T = {t_pct}%, G = {g_str}, C = {g_str}"
        dists = [
            f"T = {g_str}, G = {t_pct}%, C = {t_pct}%",
            f"T = {t_pct}%, G = {rem}%, C = {rem}%",
            f"T = {100 - a_pct}%, G = {a_pct}%, C = {a_pct}%",
        ]
        exp = (
            f"In double-stranded DNA, %A = %T = {a_pct}% (total A+T = {2 * a_pct}%). "
            f"The remaining {rem}% is split equally between G and C: %G = %C = {rem}% / 2 = {g_str}."
        )
        questions.append(_make_mcq("BIO101", q_text, corr, dists, exp, rng))

    # 3. Hardy-Weinberg Equilibrium problems (25 questions)
    q_freqs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    traits = [
        ("albinism", "a"),
        ("attached earlobes", "e"),
        ("cystic fibrosis", "c"),
    ]
    for trait_name, allele in traits:
        for q_val in q_freqs:
            p_val = round(1.0 - q_val, 2)
            q2_pct = round((q_val ** 2) * 100, 1)
            het_pct = round(2 * p_val * q_val * 100, 1)
            q_text = (
                f"In a population in Hardy-Weinberg equilibrium, the frequency of the recessive allele ({allele}) "
                f"for {trait_name} is q = {q_val}. What percentage of the population is heterozygous (2pq) and homozygous recessive (q²)?"
            )
            corr = f"Heterozygous (2pq) = {het_pct:g}%, Homozygous recessive (q²) = {q2_pct:g}%"
            dists = [
                f"Heterozygous (2pq) = {round(p_val * q_val * 100, 1):g}%, Homozygous recessive (q²) = {round(q_val * 100, 1):g}%",
                f"Heterozygous (2pq) = {q2_pct:g}%, Homozygous recessive (q²) = {het_pct:g}%",
                f"Heterozygous (2pq) = {round((p_val ** 2) * 100, 1):g}%, Homozygous recessive (q²) = {q2_pct:g}%",
            ]
            exp = (
                f"Since p + q = 1, p = 1 - {q_val} = {p_val}. "
                f"Heterozygote frequency 2pq = 2({p_val})({q_val}) = {het_pct:g}%, and q² = ({q_val})² = {q2_pct:g}%."
            )
            questions.append(_make_mcq("BIO101", q_text, corr, dists, exp, rng))

    # 4. Mitotic & Meiotic Chromosome / Chromatid Counts (30 questions)
    organisms = [
        ("human somatic cell", 46),
        ("pea plant (Pisum sativum)", 14),
        ("fruit fly (Drosophila melanogaster)", 8),
        ("maize plant (Zea mays)", 20),
        ("onion root tip cell (Allium cepa)", 16),
        ("house mouse (Mus musculus)", 40),
        ("domestic dog", 78),
        ("potato plant", 48),
        ("rice plant", 24),
        ("chimpanzee", 48),
    ]
    for org_name, two_n in organisms:
        n_val = two_n // 2
        # Q type 1: Gamete chromosome number
        q1 = f"A diploid {org_name} has 2n = {two_n} chromosomes. How many chromosomes are present in its mature haploid gamete after meiosis?"
        questions.append(
            _make_mcq(
                "BIO101",
                q1,
                f"n = {n_val} chromosomes",
                [f"{two_n} chromosomes", f"{two_n * 2} chromosomes", f"{n_val // 2} chromosomes"],
                f"Meiosis reduces the diploid chromosome number (2n = {two_n}) by half, producing haploid gametes with n = {n_val} chromosomes.",
                rng,
            )
        )
        # Q type 2: Sister chromatids at Metaphase of Mitosis
        q2 = f"A diploid {org_name} has 2n = {two_n} chromosomes. How many sister chromatids are present in the cell at Metaphase of mitosis?"
        questions.append(
            _make_mcq(
                "BIO101",
                q2,
                f"{two_n * 2} chromatids",
                [f"{two_n} chromatids", f"{n_val} chromatids", f"{two_n * 4} chromatids"],
                f"After DNA replication in S phase, each of the {two_n} chromosomes consists of 2 sister chromatids, giving 2 × {two_n} = {two_n * 2} chromatids at Metaphase.",
                rng,
            )
        )
        # Q type 3: Bivalents (tetrads) at Prophase I of Meiosis
        q3 = f"How many homologous pairs (bivalents / tetrads) are formed during Prophase I of meiosis in a {org_name} with 2n = {two_n}?"
        questions.append(
            _make_mcq(
                "BIO101",
                q3,
                f"{n_val} bivalents",
                [f"{two_n} bivalents", f"{two_n * 2} bivalents", f"{max(1, n_val - 2)} bivalents"],
                f"Homologous chromosomes pair up during synapsis in Prophase I to form n = {two_n}/2 = {n_val} bivalents (tetrads).",
                rng,
            )
        )

    # 5. Ecological Trophic Energy Transfer & Bacterial Binary Fission (35 questions)
    producer_energies = [1000, 2500, 5000, 8000, 10000, 15000, 20000, 40000, 50000, 100000]
    for e_prod in producer_energies:
        e_prim = e_prod * 0.1
        e_sec = e_prod * 0.01
        e_tert = e_prod * 0.001
        q1 = (
            f"In a terrestrial food chain (Grass → Grasshopper → Frog → Snake), if the primary producers (Grass) "
            f"capture {e_prod:,} kJ of net energy, how much energy is available to the Secondary Consumers (Frog) according to the 10% law?"
        )
        questions.append(
            _make_mcq(
                "BIO101",
                q1,
                f"{e_sec:g} kJ",
                [f"{e_prim:g} kJ", f"{e_tert:g} kJ", f"{e_prod * 0.5:g} kJ"],
                f"Primary consumers (Grasshopper) receive 10% = {e_prim:g} kJ, and secondary consumers (Frog) receive 10% of that = {e_sec:g} kJ.",
                rng,
            )
        )
        q2 = (
            f"In an aquatic food chain (Phytoplankton → Zooplankton → Small Fish → Shark), if Phytoplankton store "
            f"{e_prod:,} kJ of energy, how much energy reaches the Tertiary Consumers (Shark)?"
        )
        questions.append(
            _make_mcq(
                "BIO101",
                q2,
                f"{e_tert:g} kJ",
                [f"{e_sec:g} kJ", f"{e_prim:g} kJ", f"{e_tert / 10:g} kJ"],
                f"Across 3 trophic transfers (10% each): {e_prod:,} × (0.1)³ = {e_tert:g} kJ reaches the tertiary consumer.",
                rng,
            )
        )

    for init_cells in [1, 2, 3, 5]:
        for gens in [4, 5, 6, 7, 8]:
            final_cells = init_cells * (2 ** gens)
            mins = gens * 20
            q_bact = (
                f"A bacterial culture divides by binary fission once every 20 minutes. Starting with {init_cells} bacterial cell(s), "
                f"how many cells will be present after {mins} minutes under optimal conditions?"
            )
            questions.append(
                _make_mcq(
                    "BIO101",
                    q_bact,
                    f"{final_cells} cells",
                    [f"{init_cells * gens * 2} cells", f"{final_cells // 2} cells", f"{final_cells * 2} cells"],
                    f"Number of generations n = {mins} / 20 = {gens}. Final count N = N0 × 2^n = {init_cells} × 2^{gens} = {final_cells} cells.",
                    rng,
                )
            )

    # 6. Genetic Codons & Polypeptide Length calculations (45 questions)
    for aa_count in range(20, 65):
        bases_coding = aa_count * 3
        bases_with_stop = bases_coding + 3
        q_text = (
            f"A mature mRNA coding region (including its start codon and 1 stop codon) directs the synthesis of a "
            f"polypeptide chain containing {aa_count} amino acids. How many ribonucleotides (bases) are in this coding sequence?"
        )
        corr = f"{bases_with_stop} bases ({aa_count} sense codons + 1 stop codon)"
        dists = [
            f"{bases_coding} bases (stop codon codes for an amino acid)",
            f"{aa_count} bases (1 base per amino acid)",
            f"{aa_count * 2} bases (doublet code)",
        ]
        exp = (
            f"Each amino acid is encoded by a triplet codon (3 bases): {aa_count} × 3 = {bases_coding} bases. "
            f"Adding the 3 bases of the termination (stop) codon gives {bases_coding} + 3 = {bases_with_stop} bases."
        )
        questions.append(_make_mcq("BIO101", q_text, corr, dists, exp, rng))

    return questions[:200]


def seed_all_questions(db: Session, force_reload: bool = False):
    """Ensure the database has 200 questions per course (800 total), loading from data/all_questions.json if present."""
    import json
    from pathlib import Path

    existing_count = db.query(Question).count()
    if existing_count >= 800 and not force_reload:
        return existing_count

    if existing_count > 0:
        db.query(Question).delete()
        db.commit()

    json_bank_path = Path(__file__).resolve().parent / "data" / "all_questions.json"
    letters = ["A", "B", "C", "D"]
    all_q = []

    if json_bank_path.exists():
        raw_items = json.loads(json_bank_path.read_text(encoding="utf-8"))
        for item in raw_items:
            course_code = item["course"].strip().upper().replace(" ", "")
            opts = item["options"]
            ans_idx = int(item["answer_index"])
            corr_letter = letters[ans_idx]
            exp = item.get("explanation") or f"The correct option is {corr_letter} ({opts[ans_idx]})."
            all_q.append(
                {
                    "course_code": course_code,
                    "question_text": item["question"],
                    "option_a": opts[0],
                    "option_b": opts[1],
                    "option_c": opts[2],
                    "option_d": opts[3],
                    "correct_option": corr_letter,
                    "explanation": exp,
                }
            )
    else:
        rng = random.Random(1120)
        all_q.extend(generate_chm101_questions(rng))
        all_q.extend(generate_phy101_questions(rng))
        all_q.extend(generate_mth101_questions(rng))
        all_q.extend(generate_bio101_questions(rng))

    db.bulk_insert_mappings(Question, all_q)
    db.commit()
    return len(all_q)


if __name__ == "__main__":
    from database import SessionLocal, engine, Base

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        total = seed_all_questions(session, force_reload=True)
        print(f"Successfully seeded {total} university 101 questions (200 per course)!")

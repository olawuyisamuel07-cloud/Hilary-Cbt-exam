import json
import math
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def make_item(q_id: str, course: str, question: str, correct: str, distractors: list[str], explanation: str, rng: random.Random) -> dict:
    seen = {correct.strip()}
    clean_d = []
    for d in distractors:
        ds = d.strip()
        if ds and ds not in seen:
            seen.add(ds)
            clean_d.append(ds)
        if len(clean_d) == 3:
            break
    while len(clean_d) < 3:
        fb = f"None of these ({len(clean_d) + 1})"
        if fb not in seen:
            seen.add(fb)
            clean_d.append(fb)

    opts = [correct.strip()] + clean_d[:3]
    rng.shuffle(opts)
    ans_idx = opts.index(correct.strip())
    return {
        "id": q_id,
        "course": course,
        "question": question,
        "options": opts,
        "answer_index": ans_idx,
        "explanation": explanation,
    }


def generate_hard_phy101(rng: random.Random) -> list[dict]:
    items = []
    idx = 101

    # 1. Hard Dimensional Analysis & Non-linear Equations (15 questions)
    dim_questions = [
        (
            "In the van der Waals equation \\(\\left(P + \\frac{a}{V^2}\\right)(V - b) = RT\\), where \\(P\\) is pressure and \\(V\\) is volume, what are the SI dimensions of the constants \\(a\\) and \\(b\\)?",
            "\\([a] = M L^5 T^{-2},\\; [b] = L^3\\)",
            ["\\([a] = M L^{-1} T^{-2},\\; [b] = L^3\\)", "\\([a] = M L^3 T^{-2},\\; [b] = L^2\\)", "\\([a] = M L^5 T^{-1},\\; [b] = M L^{-3}\\)"],
            "By dimensional homogeneity, \\([a/V^2] = [P] = M L^{-1} T^{-2}\\), so \\([a] = M L^{-1} T^{-2} \\cdot L^6 = M L^5 T^{-2}\\), and \\([b] = [V] = L^3\\).",
        ),
        (
            "The viscous drag force \\(F\\) on a sphere of radius \\(r\\) moving with speed \\(v\\) through a fluid is given by Stokes' Law \\(F = 6\\pi \\eta r v\\). What is the dimension of the coefficient of viscosity \\(\\eta\\)?",
            "\\(M L^{-1} T^{-1}\\)",
            ["\\(M L^{-1} T^{-2}\\)", "\\(M L T^{-1}\\)", "\\(M L^{-2} T^{-1}\\)"],
            "From \\(\\eta = F / (6\\pi r v)\\), \\([\\eta] = (M L T^{-2}) / (L \\cdot L T^{-1}) = M L^{-1} T^{-1}\\).",
        ),
        (
            "The position \\(x\\) of a particle at time \\(t\\) is given by \\(x(t) = \\frac{v_0}{\\alpha}(1 - e^{-\\alpha t})\\), where \\(v_0\\) is initial velocity. What are the dimensions of \\(\\alpha\\) and \\(v_0 / \\alpha\\)?",
            "\\([\\alpha] = T^{-1},\\; [v_0/\\alpha] = L\\)",
            ["\\([\\alpha] = T,\\; [v_0/\\alpha] = L T^{-2}\\)", "\\([\\alpha] = L T^{-1},\\; [v_0/\\alpha] = 1\\)", "\\([\\alpha] = T^{-2},\\; [v_0/\\alpha] = L T\\)"],
            "The exponent \\(\\alpha t\\) must be dimensionless, so \\([\\alpha] = T^{-1}\\), and \\([v_0/\\alpha] = (L T^{-1}) / T^{-1} = L\\).",
        ),
        (
            "If Planck's constant \\(h\\) has dimensions of angular momentum (\\(\\text{J}\\cdot\\text{s}\\)), what are the fundamental SI dimensions of \\(h\\)?",
            "\\(M L^2 T^{-1}\\)",
            ["\\(M L^2 T^{-2}\\)", "\\(M L T^{-1}\\)", "\\(M L^2 T^{-3}\\)"],
            "Since \\(E = hf\\), \\([h] = [E]/[f] = (M L^2 T^{-2}) / (T^{-1}) = M L^2 T^{-1}\\).",
        ),
        (
            "A physical quantity \\(X\\) is calculated from \\(X = \\frac{A^2 B^3}{C \\sqrt{D}}\\). If the percentage errors in measuring \\(A, B, C, D\\) are \\(1\\%, 2\\%, 3\\%, 4\\%\\) respectively, what is the maximum percentage error in \\(X\\)?",
            "\\(13\\%\\)",
            ["\\(10\\%\\)", "\\(11\\%\\)", "\\(15\\%\\)"],
            "Maximum relative error: \\(2(1\\%) + 3(2\\%) + 1(3\\%) + \\frac{1}{2}(4\\%) = 2 + 6 + 3 + 2 = 13\\%\\).",
        ),
        (
            "The time period \\(T\\) of oscillation of a small liquid drop under surface tension \\(S\\) (force per unit length) depends on density \\(\\rho\\), radius \\(r\\), and \\(S\\) as \\(T \\propto \\rho^a r^b S^c\\). Find \\((a, b, c)\\).",
            "\\(a = \\frac{1}{2},\\; b = \\frac{3}{2},\\; c = -\\frac{1}{2}\\)",
            ["\\(a = \\frac{1}{2},\\; b = \\frac{1}{2},\\; c = -\\frac{1}{2}\\)", "\\(a = -\\frac{1}{2},\\; b = \\frac{3}{2},\\; c = \\frac{1}{2}\\)", "\\(a = 1,\\; b = 3,\\; c = -1\\)"],
            "Since \\([S] = M T^{-2}\\), equating \\(T^1 = (M L^{-3})^a L^b (M T^{-2})^c\\) gives \\(c = -1/2, a = 1/2, b = 3a = 3/2\\).",
        ),
        (
            "In the wave equation \\(y(x, t) = A \\sin(kx - \\omega t)\\), what is the dimension of the ratio \\(\\omega / k\\)?",
            "\\(L T^{-1}\\) (velocity)",
            ["\\(L^{-1} T\\)", "\\(L T^{-2}\\) (acceleration)", "\\(M^0 L^0 T^0\\) (dimensionless)"],
            "Since \\(kx\\) and \\(\\omega t\\) are dimensionless, \\([k] = L^{-1}\\) and \\([\\omega] = T^{-1}\\), so \\([\\omega/k] = L T^{-1}\\).",
        ),
        (
            "What are the SI dimensions of the Universal Gravitational Constant \\(G\\) in \\(F = \\frac{G m_1 m_2}{r^2}\\)?",
            "\\(M^{-1} L^3 T^{-2}\\)",
            ["\\(M L^3 T^{-2}\\)", "\\(M^{-1} L^2 T^{-2}\\)", "\\(M^{-2} L^3 T^{-2}\\)"],
            "From \\(G = F r^2 / (m_1 m_2)\\), \\([G] = (M L T^{-2} \\cdot L^2) / M^2 = M^{-1} L^3 T^{-2}\\).",
        ),
        (
            "If force \\(F\\), velocity \\(V\\), and time \\(T\\) are chosen as fundamental dimensional quantities, what is the dimensional formula for Mass \\(M\\)?",
            "\\(F V^{-1} T\\)",
            ["\\(F V T^{-1}\\)", "\\(F V^{-1} T^{-1}\\)", "\\(F V^2 T^{-1}\\)"],
            "Since \\(F = m a = m (V / T)\\), solving for mass gives \\(M = F T / V = F V^{-1} T\\).",
        ),
        (
            "The power \\(P\\) delivered by a wind turbine depends on air density \\(\\rho\\), swept blade area \\(A\\), and wind speed \\(v\\) according to \\(P \\propto \\rho^x A^y v^z\\). Find \\((x, y, z)\\).",
            "\\(x = 1,\\; y = 1,\\; z = 3\\)",
            ["\\(x = 1,\\; y = 1,\\; z = 2\\)", "\\(x = 1,\\; y = 2,\\; z = 2\\)", "\\(x = 2,\\; y = 1,\\; z = 3\\)"],
            "Equating \\([P] = M L^2 T^{-3} = (M L^{-3})^x (L^2)^y (L T^{-1})^z\\) yields \\(x = 1, z = 3\\), and \\(-3 + 2y + 3 = 2 \\Rightarrow y = 1\\).",
        ),
    ]
    for q, corr, dists, exp in dim_questions:
        items.append(make_item(f"PHY 101_{idx}", "PHY 101", q, corr, dists, exp, rng))
        idx += 1

    # 2. Hard 3D Vectors: Cross Products, Orthogonality, Unit Vectors, Work & Torque Vectors (15 questions)
    vec_questions = [
        (
            "For what value of \\(c\\) are the vectors \\(A = 2\\hat{i} - 3\\hat{j} + c\\hat{k}\\) and \\(B = 4\\hat{i} + 2\\hat{j} - \\hat{k}\\) mutually perpendicular?",
            "\\(c = 2\\)",
            ["\\(c = -2\\)", "\\(c = 14\\)", "\\(c = 0\\)"],
            "Two vectors are perpendicular when \\(A \\cdot B = 0\\): \\((2)(4) + (-3)(2) + c(-1) = 8 - 6 - c = 0 \\Rightarrow c = 2\\).",
        ),
        (
            "Find the unit vector in the direction of \\(A = 2\\hat{i} - 2\\hat{j} + \\hat{k}\\).",
            "\\(\\frac{2}{3}\\hat{i} - \\frac{2}{3}\\hat{j} + \\frac{1}{3}\\hat{k}\\)",
            ["\\(\\frac{2}{9}\\hat{i} - \\frac{2}{9}\\hat{j} + \\frac{1}{9}\\hat{k}\\)", "\\(\\frac{2}{\\sqrt{5}}\\hat{i} - \\frac{2}{\\sqrt{5}}\\hat{j} + \\frac{1}{\\sqrt{5}}\\hat{k}\\)", "\\(2\\hat{i} - 2\\hat{j} + \\hat{k}\\)"],
            "Magnitude \\(|A| = \\sqrt{2^2 + (-2)^2 + 1^2} = \\sqrt{9} = 3\\), so \\(\\hat{u} = A/|A| = \\frac{2}{3}\\hat{i} - \\frac{2}{3}\\hat{j} + \\frac{1}{3}\\hat{k}\\).",
        ),
        (
            "Compute the vector cross product \\(A \\times B\\) given \\(A = 2\\hat{i} + \\hat{j} - \\hat{k}\\) and \\(B = \\hat{i} - \\hat{j} + 2\\hat{k}\\).",
            "\\(\\hat{i} - 5\\hat{j} - 3\\hat{k}\\)",
            ["\\(\\hat{i} + 5\\hat{j} - 3\\hat{k}\\)", "\\(3\\hat{i} - 3\\hat{j} - 3\\hat{k}\\)", "\\(-\\hat{i} + 5\\hat{j} + 3\\hat{k}\\)"],
            "Using the determinant: \\(\\hat{i}(2 - 1) - \\hat{j}(4 - (-1)) + \\hat{k}(-2 - 1) = \\hat{i} - 5\\hat{j} - 3\\hat{k}\\).",
        ),
        (
            "Find the angle \\(\\theta\\) between vectors \\(A = \\hat{i} + \\hat{j}\\) and \\(B = \\hat{j} + \\hat{k}\\).",
            "\\(60^\\circ\\)",
            ["\\(45^\\circ\\)", "\\(90^\\circ\\)", "\\(30^\\circ\\)"],
            "\\(\\cos\\theta = \\frac{A \\cdot B}{|A||B|} = \\frac{0 + 1 + 0}{\\sqrt{2}\\sqrt{2}} = \\frac{1}{2} \\Rightarrow \\theta = 60^\\circ\\).",
        ),
        (
            "Find the area of a parallelogram whose adjacent sides are represented by the vectors \\(A = 3\\hat{i} + \\hat{j}\\) and \\(B = \\hat{i} + 2\\hat{j}\\).",
            "\\(5\\text{ sq. units}\\)",
            ["\\(7\\text{ sq. units}\\)", "\\(10\\text{ sq. units}\\)", "\\(2.5\\text{ sq. units}\\)"],
            "The area of the parallelogram is \\(|A \\times B| = |(3\\times 2 - 1\\times 1)\\hat{k}| = |5\\hat{k}| = 5\\).",
        ),
        (
            "A force \\(F = (4\\hat{i} - 3\\hat{j} + 2\\hat{k})\\text{ N}\\) displaces a particle from position \\(r_1 = (\\hat{i} + 2\\hat{j} + \\hat{k})\\text{ m}\\) to \\(r_2 = (3\\hat{i} + \\hat{j} + 4\\hat{k})\\text{ m}\\). Calculate the work done.",
            "\\(17\\text{ J}\\)",
            ["\\(11\\text{ J}\\)", "\\(9\\text{ J}\\)", "\\(23\\text{ J}\\)"],
            "Displacement \\(\\Delta r = r_2 - r_1 = 2\\hat{i} - \\hat{j} + 3\\hat{k}\\). Work \\(W = F \\cdot \\Delta r = 4(2) + (-3)(-1) + 2(3) = 8 + 3 + 6 = 17\\text{ J}\\).",
        ),
        (
            "A force \\(F = (2\\hat{i} + 3\\hat{j})\\text{ N}\\) acts at the point \\(r = (4\\hat{i} - \\hat{j})\\text{ m}\\) relative to the origin. What is the torque \\(\\tau = r \\times F\\) about the origin?",
            "\\(14\\hat{k}\\text{ N}\\cdot\\text{m}\\)",
            ["\\(10\\hat{k}\\text{ N}\\cdot\\text{m}\\)", "\\(-14\\hat{k}\\text{ N}\\cdot\\text{m}\\)", "\\(5\\hat{k}\\text{ N}\\cdot\\text{m}\\)"],
            "\\(\\tau = r \\times F = (4\\hat{i} - \\hat{j}) \\times (2\\hat{i} + 3\\hat{j}) = (4\\cdot 3 - (-1)\\cdot 2)\\hat{k} = 14\\hat{k}\\text{ N}\\cdot\\text{m}\\).",
        ),
        (
            "If \\(|A + B| = |A - B|\\) for two non-zero vectors \\(A\\) and \\(B\\), what is the angle between \\(A\\) and \\(B\\)?",
            "\\(90^\\circ\\)",
            ["\\(0^\\circ\\)", "\\(60^\\circ\\)", "\\(180^\\circ\\)"],
            "Squaring both sides gives \\(A^2 + B^2 + 2A\\cdot B = A^2 + B^2 - 2A\\cdot B \\Rightarrow 4A\\cdot B = 0 \\Rightarrow \\theta = 90^\\circ\\).",
        ),
        (
            "What is the scalar projection (component) of vector \\(A = 4\\hat{i} - 2\\hat{j} + \\hat{k}\\) onto the direction of \\(B = 2\\hat{i} + 2\\hat{j} + \\hat{k}\\)?",
            "\\(\\frac{5}{3}\\)",
            ["\\(5\\)", "\\(\\frac{5}{\\sqrt{21}}\\)", "\\(\\frac{13}{3}\\)"],
            "The projection of \\(A\\) onto \\(B\\) is \\(\\frac{A \\cdot B}{|B|} = \\frac{4(2) + (-2)(2) + 1(1)}{\\sqrt{4 + 4 + 1}} = \\frac{8 - 4 + 1}{3} = \\frac{5}{3}\\).",
        ),
        (
            "Two forces of magnitudes \\(3P\\) and \\(2P\\) have a resultant of magnitude \\(R\\). If the first force is doubled to \\(6P\\), the magnitude of the resultant doubles to \\(2R\\). Find the angle \\(\\theta\\) between the two forces.",
            "\\(120^\\circ\\)",
            ["\\(60^\\circ\\)", "\\(90^\\circ\\)", "\\(150^\\circ\\)"],
            "From \\(R^2 = 9P^2 + 4P^2 + 12P^2\\cos\\theta\\) and \\(4R^2 = 36P^2 + 4P^2 + 24P^2\\cos\\theta\\), eliminating \\(R^2\\) gives \\(52 + 48\\cos\\theta = 40 + 24\\cos\\theta \\Rightarrow \\cos\\theta = -1/2 \\Rightarrow \\theta = 120^\\circ\\).",
        ),
        (
            "For any three vectors \\(A, B, C\\), the scalar triple product \\(A \\cdot (A \\times B)\\) is always equal to:",
            "\\(0\\)",
            ["\\(|A|^2 |B|\\)", "\\(1\\)", "\\(|A \\times B|\\)"],
            "Since \\(A \\times B\\) is perpendicular to \\(A\\), the dot product of \\(A\\) with \\(A \\times B\\) is identically zero.",
        ),
        (
            "A particle moves with velocity \\(v = (3\\hat{i} - 4\\hat{j})\\text{ m/s}\\) under a constant force \\(F = (5\\hat{i} + 2\\hat{j})\\text{ N}\\). What is the instantaneous power delivered to the particle?",
            "\\(7\\text{ W}\\)",
            ["\\(23\\text{ W}\\)", "\\(15\\text{ W}\\)", "\\(-7\\text{ W}\\)"],
            "Instantaneous power \\(P = F \\cdot v = (5)(3) + (2)(-4) = 15 - 8 = 7\\text{ W}\\).",
        ),
        (
            "Which of the following cyclic cross-product relations for right-handed Cartesian unit vectors is INCORRECT?",
            "\\(\\hat{i} \\times \\hat{k} = \\hat{j}\\)",
            ["\\(\\hat{i} \\times \\hat{j} = \\hat{k}\\)", "\\(\\hat{j} \\times \\hat{k} = \\hat{i}\\)", "\\(\\hat{k} \\times \\hat{i} = \\hat{j}\\)"],
            "In a right-handed coordinate system, \\(\\hat{k} \\times \\hat{i} = \\hat{j}\\), whereas \\(\\hat{i} \\times \\hat{k} = -\\hat{j}\\).",
        ),
        (
            "If \\(|A \\times B| = \\sqrt{3}(A \\cdot B)\\), what is the angle \\(\\theta\\) between vectors \\(A\\) and \\(B\\)?",
            "\\(60^\\circ\\)",
            ["\\(30^\\circ\\)", "\\(45^\\circ\\)", "\\(120^\\circ\\)"],
            "\\(AB\\sin\\theta = \\sqrt{3}AB\\cos\\theta \\Rightarrow \\tan\\theta = \\sqrt{3} \\Rightarrow \\theta = 60^\\circ\\).",
        ),
        (
            "A boat can travel at \\(4\\text{ m/s}\\) in still water. It heads directly perpendicular across a river of width \\(120\\text{ m}\\) flowing at \\(3\\text{ m/s}\\). What is the resultant speed of the boat relative to the riverbank and how far downstream does it land?",
            "\\(5\\text{ m/s},\\; 90\\text{ m}\\)",
            ["\\(5\\text{ m/s},\\; 120\\text{ m}\\)", "\\(7\\text{ m/s},\\; 90\\text{ m}\\)", "\\(4\\text{ m/s},\\; 60\\text{ m}\\)"],
            "Resultant speed \\(v = \\sqrt{4^2 + 3^2} = 5\\text{ m/s}\\). Crossing time \\(t = 120 / 4 = 30\\text{ s}\\), so downstream drift \\(= 3 \\times 30 = 90\\text{ m}\\).",
        ),
    ]
    for q, corr, dists, exp in vec_questions:
        items.append(make_item(f"PHY 101_{idx}", "PHY 101", q, corr, dists, exp, rng))
        idx += 1

    # 3. Hard Calculus-Based Kinematics & Projectile Motion (25 questions)
    kin_questions = [
        (
            "The position of a particle moving along the x-axis is given by \\(x(t) = 2t^3 - 15t^2 + 24t + 4\\text{ m}\\). At what times \\(t\\) is the particle momentarily at rest?",
            "\\(t = 1\\text{ s}\\) and \\(t = 4\\text{ s}\\)",
            ["\\(t = 2\\text{ s}\\) and \\(t = 3\\text{ s}\\)", "\\(t = 1\\text{ s}\\) and \\(t = 2.5\\text{ s}\\)", "\\(t = 0\\text{ s}\\) and \\(t = 4\\text{ s}\\)"],
            "Setting velocity \\(v(t) = dx/dt = 6t^2 - 30t + 24 = 6(t - 1)(t - 4) = 0\\) yields \\(t = 1\\text{ s}\\) and \\(t = 4\\text{ s}\\).",
        ),
        (
            "For the displacement function \\(x(t) = 2t^3 - 15t^2 + 24t + 4\\text{ m}\\), what is the velocity of the particle at the instant when its acceleration is zero?",
            "\\(-13.5\\text{ m/s}\\)",
            ["\\(0\\text{ m/s}\\)", "\\(12.0\\text{ m/s}\\)", "\\(-6.0\\text{ m/s}\\)"],
            "Acceleration \\(a(t) = 12t - 30 = 0 \\Rightarrow t = 2.5\\text{ s}\\). Substituting into \\(v(t) = 6t^2 - 30t + 24\\) gives \\(6(6.25) - 75 + 24 = -13.5\\text{ m/s}\\).",
        ),
        (
            "The acceleration of a particle starting from rest at \\(x = 0\\) varies with time as \\(a(t) = (6t - 4)\\text{ m/s}^2\\). What is the particle's velocity and position at \\(t = 2\\text{ s}\\)?",
            "\\(v = 4\\text{ m/s},\\; x = 0\\text{ m}\\)",
            ["\\(v = 8\\text{ m/s},\\; x = 4\\text{ m}\\)", "\\(v = 4\\text{ m/s},\\; x = 8\\text{ m}\\)", "\\(v = 12\\text{ m/s},\\; x = 0\\text{ m}\\)"],
            "Integrating \\(a(t)\\): \\(v(t) = 3t^2 - 4t\\) (so \\(v(2) = 12 - 8 = 4\\text{ m/s}\\)). Integrating again: \\(x(t) = t^3 - 2t^2\\) (so \\(x(2) = 8 - 8 = 0\\text{ m}\\)).",
        ),
        (
            "A particle moves along a straight line such that its velocity \\(v\\) varies with position \\(x\\) according to \\(v(x) = 3x^2\\text{ m/s}\\). What is the acceleration of the particle at \\(x = 2\\text{ m}\\)?",
            "\\(144\\text{ m/s}^2\\)",
            ["\\(12\\text{ m/s}^2\\)", "\\(36\\text{ m/s}^2\\)", "\\(72\\text{ m/s}^2\\)"],
            "Using the chain rule \\(a = v\\frac{dv}{dx} = (3x^2)(6x) = 18x^3\\). At \\(x = 2\\text{ m}\\), \\(a = 18(8) = 144\\text{ m/s}^2\\).",
        ),
        (
            "A body starting from rest moves with constant acceleration \\(a\\). What is the ratio of the distance covered during the \\(5\\text{th}\\) second alone to the total distance covered in the first \\(5\\) seconds?",
            "\\(9 : 25\\)",
            ["\\(1 : 5\\)", "\\(5 : 25\\)", "\\(7 : 25\\)"],
            "Distance in the \\(n\\)-th second is \\(s_n = \\frac{1}{2}a(2n-1)\\) and total distance is \\(S_n = \\frac{1}{2}an^2\\). For \\(n=5\\), \\(s_5 / S_5 = (2(5)-1)/5^2 = 9/25\\).",
        ),
        (
            "A stone is dropped from the top of a tower of height \\(H\\) and takes \\(T\\) seconds to reach the ground. Where is the stone at time \\(t = T/3\\) (measured from the ground)?",
            "\\(\\frac{8H}{9}\\text{ above the ground}\\)",
            ["\\(\\frac{2H}{3}\\text{ above the ground}\\)", "\\(\\frac{H}{9}\\text{ above the ground}\\)", "\\(\\frac{5H}{9}\\text{ above the ground}\\)"],
            "Since \\(y \\propto t^2\\), in time \\(T/3\\) the stone falls \\(H/9\\) from the top, leaving it \\(H - H/9 = 8H/9\\) above the ground.",
        ),
        (
            "A ball is thrown vertically upward from the ground and passes a window at height \\(h\\) at time \\(t_1\\) on its way up and at time \\(t_2\\) on its way down. What is the height \\(h\\) of the window in terms of \\(g, t_1, t_2\\)?",
            "\\(h = \\frac{1}{2} g t_1 t_2\\)",
            ["\\(h = g t_1 t_2\\)", "\\(h = \\frac{1}{4} g (t_1 + t_2)^2\\)", "\\(h = \\frac{1}{2} g (t_2^2 - t_1^2)\\)"],
            "In \\(\\frac{1}{2}gt^2 - ut + h = 0\\), the product of roots \\(t_1\\) and \\(t_2\\) is \\(t_1 t_2 = \\frac{h}{g/2} \\Rightarrow h = \\frac{1}{2}g t_1 t_2\\).",
        ),
        (
            "A projectile is launched from level ground such that its maximum height \\(H\\) equals its horizontal range \\(R\\). What is the launch angle \\(\\theta\\)?",
            "\\(\\tan^{-1}(4)\\)",
            ["\\(45^\\circ\\)", "\\(\\tan^{-1}(2)\\)", "\\(60^\\circ\\)"],
            "For any projectile on level ground, \\(R / H = 4 / \\tan\\theta\\). Setting \\(R = H\\) gives \\(\\tan\\theta = 4 \\Rightarrow \\theta = \\tan^{-1}(4)\\).",
        ),
        (
            "The trajectory of a projectile in the vertical \\(xy\\)-plane is given by \\(y = \\sqrt{3}x - \\frac{g x^2}{20}\\), where \\(x\\) and \\(y\\) are in metres. Find the angle of projection and initial speed \\(u\\).",
            "\\(\\theta = 60^\\circ,\\; u = 2\\sqrt{10}\\text{ m/s}\\)",
            ["\\(\\theta = 30^\\circ,\\; u = 10\\text{ m/s}\\)", "\\(\\theta = 60^\\circ,\\; u = 10\\text{ m/s}\\)", "\\(\\theta = 45^\\circ,\\; u = 2\\sqrt{5}\\text{ m/s}\\)"],
            "Comparing with \\(y = x\\tan\\theta - \\frac{gx^2}{2u^2\\cos^2\\theta}\\): \\(\\tan\\theta = \\sqrt{3} \\Rightarrow \\theta = 60^\\circ\\), and \\(2u^2(\\frac{1}{4}) = 20 \\Rightarrow u^2 = 40 \\Rightarrow u = 2\\sqrt{10}\\text{ m/s}\\).",
        ),
        (
            "A projectile is fired at \\(60^\\circ\\) to the horizontal with kinetic energy \\(K_0\\). What is its kinetic energy at the highest point of its trajectory?",
            "\\(\\frac{1}{4} K_0\\)",
            ["\\(\\frac{1}{2} K_0\\)", "\\(\\frac{3}{4} K_0\\)", "\\(0\\)"],
            "At the apex, \\(v = u\\cos 60^\\circ = u/2\\). Therefore \\(K_{\\text{top}} = \\frac{1}{2}m(u/2)^2 = \\frac{1}{4}K_0\\).",
        ),
        (
            "A projectile is launched horizontally with speed \\(15\\text{ m/s}\\) from the top of a \\(45\\text{ m}\\) high cliff (take \\(g = 10\\text{ m/s}^2\\)). What is the magnitude of its velocity just as it strikes the ground?",
            "\\(15\\sqrt{5}\\text{ m/s}\\)",
            ["\\(30\\text{ m/s}\\)", "\\(45\\text{ m/s}\\)", "\\(15\\sqrt{3}\\text{ m/s}\\)"],
            "Vertical impact speed \\(v_y = \\sqrt{2gh} = \\sqrt{2(10)(45)} = 30\\text{ m/s}\\). Total speed \\(v = \\sqrt{v_x^2 + v_y^2} = \\sqrt{15^2 + 30^2} = 15\\sqrt{5}\\text{ m/s}\\).",
        ),
        (
            "A car travels the first half of a total distance \\(D\\) at a constant speed \\(v_1 = 40\\text{ km/h}\\) and the second half at \\(v_2 = 60\\text{ km/h}\\). What is its average speed for the entire journey?",
            "\\(48\\text{ km/h}\\)",
            ["\\(50\\text{ km/h}\\)", "\\(45\\text{ km/h}\\)", "\\(52\\text{ km/h}\\)"],
            "For equal distances, the average speed is the harmonic mean \\(\\frac{2v_1 v_2}{v_1 + v_2} = \\frac{2(40)(60)}{100} = 48\\text{ km/h}\\).",
        ),
        (
            "A bullet loses \\(1/3\\) of its velocity after penetrating \\(4\\text{ cm}\\) into a wooden block. Assuming constant retardation, how much further will it penetrate before coming completely to rest?",
            "\\(3.2\\text{ cm}\\)",
            ["\\(4.0\\text{ cm}\\)", "\\(2.0\\text{ cm}\\)", "\\(5.0\\text{ cm}\\)"],
            "From \\((2u/3)^2 = u^2 - 2a(4) \\Rightarrow 2a(4) = \\frac{5}{9}u^2\\). For stopping from \\(2u/3\\): \\(0 = \\frac{4}{9}u^2 - 2a x \\Rightarrow x = 4 \\times \\frac{4/9}{5/9} = 3.2\\text{ cm}\\).",
        ),
        (
            "Two trains of lengths \\(120\\text{ m}\\) and \\(80\\text{ m}\\) move in opposite directions on parallel tracks with speeds \\(25\\text{ m/s}\\) and \\(15\\text{ m/s}\\). How long does it take for them to completely pass each other?",
            "\\(5\\text{ s}\\)",
            ["\\(20\\text{ s}\\)", "\\(8\\text{ s}\\)", "\\(4\\text{ s}\\)"],
            "Relative speed in opposite directions is \\(25 + 15 = 40\\text{ m/s}\\). Total length to clear is \\(120 + 80 = 200\\text{ m}\\), so \\(t = 200 / 40 = 5\\text{ s}\\).",
        ),
        (
            "A particle moves in a circle of radius \\(R = 2\\text{ m}\\) such that its speed increases with time as \\(v(t) = 3t\\text{ m/s}\\). What is the magnitude of the total acceleration of the particle at \\(t = 2\\text{ s}\\)?",
            "\\(3\\sqrt{37}\\text{ m/s}^2\\)",
            ["\\(18\\text{ m/s}^2\\)", "\\(3\\text{ m/s}^2\\)", "\\(21\\text{ m/s}^2\\)"],
            "At \\(t = 2\\text{ s}\\), tangential acceleration \\(a_t = dv/dt = 3\\text{ m/s}^2\\) and radial acceleration \\(a_r = v^2/R = 6^2/2 = 18\\text{ m/s}^2\\). Total \\(a = \\sqrt{3^2 + 18^2} = 3\\sqrt{37}\\text{ m/s}^2\\).",
        ),
    ]
    for q, corr, dists, exp in kin_questions:
        items.append(make_item(f"PHY 101_{idx}", "PHY 101", q, corr, dists, exp, rng))
        idx += 1

    # 4. Hard Newton's Laws, Pulleys, Inclined Planes & Friction (20 questions)
    dyn_questions = [
        (
            "Two masses \\(m_1 = 6\\text{ kg}\\) and \\(m_2 = 4\\text{ kg}\\) are connected by a light inextensible string passing over a frictionless pulley (Atwood machine). Taking \\(g = 10\\text{ m/s}^2\\), find the acceleration of the system and the tension \\(T\\) in the string.",
            "\\(a = 2\\text{ m/s}^2,\\; T = 48\\text{ N}\\)",
            ["\\(a = 2\\text{ m/s}^2,\\; T = 50\\text{ N}\\)", "\\(a = 5\\text{ m/s}^2,\\; T = 48\\text{ N}\\)", "\\(a = 4\\text{ m/s}^2,\\; T = 24\\text{ N}\\)"],
            "\\(a = \\frac{m_1 - m_2}{m_1 + m_2}g = \\frac{6 - 4}{10}(10) = 2\\text{ m/s}^2\\), and \\(T = m_2(g + a) = 4(10 + 2) = 48\\text{ N}\\).",
        ),
        (
            "A \\(60\\text{ kg}\\) person stands on a weighing scale inside an elevator that accelerates upward at \\(2.5\\text{ m/s}^2\\) (take \\(g = 10\\text{ m/s}^2\\)). What is the apparent weight (normal reaction) registered by the scale?",
            "\\(750\\text{ N}\\)",
            ["\\(600\\text{ N}\\)", "\\(450\\text{ N}\\)", "\\(150\\text{ N}\\)"],
            "When accelerating upward, \\(N - mg = ma \\Rightarrow N = m(g + a) = 60(10 + 2.5) = 750\\text{ N}\\).",
        ),
        (
            "A block of mass \\(m\\) rests on a rough inclined plane and begins to slide down at a constant velocity when the angle of inclination reaches \\(30^\\circ\\). What is the coefficient of kinetic friction \\(\\mu\\) between the block and the plane?",
            "\\(\\frac{1}{\\sqrt{3}}\\)",
            ["\\(\\frac{1}{2}\\)", "\\(\\frac{\\sqrt{3}}{2}\\)", "\\(\\sqrt{3}\\)"],
            "At the limiting angle of repose for uniform sliding, \\(\\mu = \\tan\\theta = \\tan 30^\\circ = \\frac{1}{\\sqrt{3}}\\).",
        ),
        (
            "A \\(10\\text{ kg}\\) block is pulled along a rough horizontal floor (\\(\\mu_k = 0.25\\)) by a force of \\(50\\text{ N}\\) inclined at \\(37^\\circ\\) above the horizontal (\\(\\cos 37^\\circ = 0.8, \\sin 37^\\circ = 0.6, g = 10\\text{ m/s}^2\\)). Find the block's horizontal acceleration.",
            "\\(2.25\\text{ m/s}^2\\)",
            ["\\(1.50\\text{ m/s}^2\\)", "\\(4.00\\text{ m/s}^2\\)", "\\(2.75\\text{ m/s}^2\\)"],
            "Normal force \\(N = mg - F\\sin 37^\\circ = 100 - 30 = 70\\text{ N}\\). Friction \\(f_k = 0.25(70) = 17.5\\text{ N}\\). Net horizontal force \\(= F\\cos 37^\\circ - f_k = 40 - 17.5 = 22.5\\text{ N}\\), so \\(a = 22.5 / 10 = 2.25\\text{ m/s}^2\\).",
        ),
        (
            "A block of mass \\(5\\text{ kg}\\) slides down a rough plane inclined at \\(30^\\circ\\) to the horizontal with coefficient of kinetic friction \\(\\mu_k = \\frac{1}{2\\sqrt{3}}\\) (take \\(g = 10\\text{ m/s}^2\\)). What is its acceleration down the plane?",
            "\\(2.5\\text{ m/s}^2\\)",
            ["\\(5.0\\text{ m/s}^2\\)", "\\(3.5\\text{ m/s}^2\\)", "\\(1.25\\text{ m/s}^2\\)"],
            "\\(a = g(\\sin 30^\\circ - \\mu_k \\cos 30^\\circ) = 10\\left(\\frac{1}{2} - \\frac{1}{2\\sqrt{3}}\\cdot\\frac{\\sqrt{3}}{2}\\right) = 10(0.5 - 0.25) = 2.5\\text{ m/s}^2\\).",
        ),
        (
            "What minimum horizontal force \\(F\\) must be pressed perpendicularly against a \\(2\\text{ kg}\\) book to hold it stationary against a rough vertical wall if the coefficient of static friction is \\(\\mu_s = 0.4\\) (take \\(g = 10\\text{ m/s}^2\\))?",
            "\\(50\\text{ N}\\)",
            ["\\(8\\text{ N}\\)", "\\(20\\text{ N}\\)", "\\(80\\text{ N}\\)"],
            "Normal force \\(N = F\\). For vertical equilibrium, \\(f_{s,\\max} = \\mu_s N = \\mu_s F \\ge mg \\Rightarrow 0.4 F = 20 \\Rightarrow F = 50\\text{ N}\\).",
        ),
        (
            "Three blocks of masses \\(m_1 = 2\\text{ kg}, m_2 = 3\\text{ kg}, m_3 = 5\\text{ kg}\\) are in contact on a frictionless horizontal table. A horizontal force \\(F = 30\\text{ N}\\) pushes \\(m_1\\) toward \\(m_2\\) and \\(m_3\\). What is the contact force exerted by \\(m_2\\) on \\(m_3\\)?",
            "\\(15\\text{ N}\\)",
            ["\\(24\\text{ N}\\)", "\\(9\\text{ N}\\)", "\\(30\\text{ N}\\)"],
            "System acceleration \\(a = F / (m_1 + m_2 + m_3) = 30 / 10 = 3\\text{ m/s}^2\\). The net force accelerating \\(m_3\\) is the contact force from \\(m_2\\): \\(N_{23} = m_3 a = 5 \\times 3 = 15\\text{ N}\\).",
        ),
        (
            "A machine gun fires \\(240\\) bullets per minute, each of mass \\(15\\text{ g}\\), with a muzzle velocity of \\(600\\text{ m/s}\\). What average force must the gunner exert to hold the gun steady?",
            "\\(36\\text{ N}\\)",
            ["\\(9\\text{ N}\\)", "\\(360\\text{ N}\\)", "\\(216\\text{ N}\\)"],
            "Rate of firing \\(n = 240 / 60 = 4\\text{ bullets/s}\\). Average force \\(F = n m v = 4 \\times 0.015 \\times 600 = 36\\text{ N}\\).",
        ),
        (
            "A rocket ejects exhaust gases at a steady mass flow rate of \\(dm/dt = 25\\text{ kg/s}\\) with an exhaust speed of \\(u_{\\text{rel}} = 1600\\text{ m/s}\\) relative to the rocket. What is the thrust force produced?",
            "\\(4.0 \\times 10^4\\text{ N}\\)",
            ["\\(64\\text{ N}\\)", "\\(4.0 \\times 10^3\\text{ N}\\)", "\\(8.0 \\times 10^4\\text{ N}\\)"],
            "Rocket thrust \\(F_{\\text{thrust}} = u_{\\text{rel}} \\frac{dm}{dt} = 1600 \\times 25 = 40,000\\text{ N} = 4.0 \\times 10^4\\text{ N}\\).",
        ),
        (
            "What is the maximum speed at which a car can safely negotiate a flat, unbanked circular curve of radius \\(R = 40\\text{ m}\\) if the coefficient of static friction between the tyres and road is \\(\\mu_s = 0.4\\) (take \\(g = 10\\text{ m/s}^2\\))?",
            "\\(12.65\\text{ m/s}\\) (\\(4\\sqrt{10}\\text{ m/s}\\))",
            ["\\(16.0\\text{ m/s}\\)", "\\(20.0\\text{ m/s}\\)", "\\(8.0\\text{ m/s}\\)"],
            "Centripetal force is supplied by static friction: \\(mv^2/R \\le \\mu_s mg \\Rightarrow v_{\\max} = \\sqrt{\\mu_s g R} = \\sqrt{0.4 \\times 10 \\times 40} = \\sqrt{160} = 4\\sqrt{10} \\approx 12.65\\text{ m/s}\\).",
        ),
        (
            "A circular highway curve of radius \\(R = 90\\text{ m}\\) is banked at an angle \\(\\theta\\) so that cars travelling at \\(v = 30\\text{ m/s}\\) require zero friction to stay on the curve (take \\(g = 10\\text{ m/s}^2\\)). Find \\(\\theta\\).",
            "\\(45^\\circ\\)",
            ["\\(30^\\circ\\)", "\\(60^\\circ\\)", "\\(\\tan^{-1}(0.5)\\)"],
            "From the ideal banking equation \\(\\tan\\theta = \\frac{v^2}{gR} = \\frac{30^2}{10 \\times 90} = \\frac{900}{900} = 1 \\Rightarrow \\theta = 45^\\circ\\).",
        ),
        (
            "A stone of mass \\(0.5\\text{ kg}\\) tied to a string of length \\(L = 0.8\\text{ m}\\) is whirled in a vertical circle. If its speed at the lowest point is \\(6\\text{ m/s}\\), what is the tension in the string at the lowest point (take \\(g = 10\\text{ m/s}^2\\))?",
            "\\(27.5\\text{ N}\\)",
            ["\\(22.5\\text{ N}\\)", "\\(17.5\\text{ N}\\)", "\\(5.0\\text{ N}\\)"],
            "At the bottom of a vertical circle, \\(T - mg = \\frac{mv^2}{L} \\Rightarrow T = 0.5(10) + \\frac{0.5(36)}{0.8} = 5 + 22.5 = 27.5\\text{ N}\\).",
        ),
        (
            "What is the minimum speed \\(v_{\\text{top}}\\) a bucket of water must have at the highest point of a vertical circle of radius \\(R\\) so that the water does not spill out?",
            "\\(\\sqrt{gR}\\)",
            ["\\(\\sqrt{2gR}\\)", "\\(\\sqrt{5gR}\\)", "\\(2\\sqrt{gR}\\)"],
            "At the top of the loop, the critical condition is \\(N = 0\\), so \\(mg = mv_{\\text{top}}^2 / R \\Rightarrow v_{\\text{top}} = \\sqrt{gR}\\).",
        ),
        (
            "A uniform heavy chain of length \\(L\\) lies on a rough horizontal table where the coefficient of static friction is \\(\\mu\\). What maximum fraction of the chain's length can hang over the edge of the table without the chain sliding off?",
            "\\(\\frac{\\mu}{1 + \\mu}\\)",
            ["\\(\\mu\\)", "\\(\\frac{1}{1 + \\mu}\\)", "\\(\\frac{\\mu}{1 - \\mu}\\)"],
            "Equating the weight of the hanging part \\(f m g\\) to the maximum static friction on the remaining part \\(\\mu (1 - f) m g\\) gives \\(f = \\mu(1 - f) \\Rightarrow f = \\frac{\\mu}{1 + \\mu}\\).",
        ),
        (
            "A \\(4\\text{ kg}\\) block on a smooth horizontal table is connected by a light string over a frictionless pulley at the table's edge to a hanging \\(1\\text{ kg}\\) mass (take \\(g = 10\\text{ m/s}^2\\)). What is the acceleration of the blocks?",
            "\\(2.0\\text{ m/s}^2\\)",
            ["\\(2.5\\text{ m/s}^2\\)", "\\(8.0\\text{ m/s}^2\\)", "\\(10.0\\text{ m/s}^2\\)"],
            "Only the hanging \\(1\\text{ kg}\\) mass contributes to the net driving force: \\(a = \\frac{m_{\\text{hang}} g}{m_{\\text{table}} + m_{\\text{hang}}} = \\frac{1(10)}{4 + 1} = 2.0\\text{ m/s}^2\\).",
        ),
    ]
    for q, corr, dists, exp in dyn_questions:
        items.append(make_item(f"PHY 101_{idx}", "PHY 101", q, corr, dists, exp, rng))
        idx += 1

    # 5. Hard Work, Variable Force Integration, Energy, Power & Springs (20 questions)
    we_questions = [
        (
            "A particle moves along the x-axis from \\(x = 1\\text{ m}\\) to \\(x = 3\\text{ m}\\) under a position-dependent force \\(F(x) = (3x^2 - 2x + 5)\\text{ N}\\). Calculate the work done by the force.",
            "\\(28\\text{ J}\\)",
            ["\\(22\\text{ J}\\)", "\\(34\\text{ J}\\)", "\\(18\\text{ J}\\)"],
            "\\(W = \\int_1^3 (3x^2 - 2x + 5)\\,dx = [x^3 - x^2 + 5x]_1^3 = (27 - 9 + 15) - (1 - 1 + 5) = 33 - 5 = 28\\text{ J}\\).",
        ),
        (
            "If the linear momentum \\(p\\) of a rigid body of constant mass \\(m\\) is increased by \\(50\\%\\), by what percentage does its kinetic energy \\(K\\) increase?",
            "\\(125\\%\\)",
            ["\\(50\\%\\)", "\\(100\\%\\)", "\\(225\\%\\)"],
            "Since \\(K = p^2 / (2m)\\), when \\(p' = 1.5p\\), \\(K' = (1.5)^2 K = 2.25K\\), which is an increase of \\(125\\%\\).",
        ),
        (
            "Two bodies of masses \\(m_1 = 1\\text{ kg}\\) and \\(m_2 = 4\\text{ kg}\\) have equal kinetic energies. What is the ratio of their linear momenta \\(p_1 : p_2\\)?",
            "\\(1 : 2\\)",
            ["\\(1 : 4\\)", "\\(1 : 16\\)", "\\(2 : 1\\)"],
            "Since \\(p = \\sqrt{2mK}\\), for equal \\(K\\), \\(p_1 / p_2 = \\sqrt{m_1 / m_2} = \\sqrt{1/4} = 1/2\\).",
        ),
        (
            "A spring of force constant \\(k = 400\\text{ N/m}\\) is already stretched by \\(5\\text{ cm}\\) from its natural length. How much ADDITIONAL work is required to stretch it from \\(5\\text{ cm}\\) to \\(15\\text{ cm}\\)?",
            "\\(4.0\\text{ J}\\)",
            ["\\(2.0\\text{ J}\\)", "\\(4.5\\text{ J}\\)", "\\(0.5\\text{ J}\\)"],
            "\\(W = \\frac{1}{2}k(x_2^2 - x_1^2) = \\frac{1}{2}(400)(0.15^2 - 0.05^2) = 200(0.0225 - 0.0025) = 4.0\\text{ J}\\).",
        ),
        (
            "Two springs with spring constants \\(k_1 = 300\\text{ N/m}\\) and \\(k_2 = 600\\text{ N/m}\\) are connected in SERIES. What is the effective spring constant \\(k_{\\text{eff}}\\) of the combination?",
            "\\(200\\text{ N/m}\\)",
            ["\\(900\\text{ N/m}\\)", "\\(450\\text{ N/m}\\)", "\\(150\\text{ N/m}\\)"],
            "For springs in series, \\(\\frac{1}{k_{\\text{eff}}} = \\frac{1}{k_1} + \\frac{1}{k_2} \\Rightarrow k_{\\text{eff}} = \\frac{300 \\times 600}{300 + 600} = 200\\text{ N/m}\\).",
        ),
        (
            "A \\(2\\text{ kg}\\) block moving at \\(4\\text{ m/s}\\) on a frictionless horizontal surface strikes an ideal horizontal spring of constant \\(k = 200\\text{ N/m}\\). What is the maximum compression of the spring?",
            "\\(0.40\\text{ m}\\)",
            ["\\(0.20\\text{ m}\\)", "\\(0.16\\text{ m}\\)", "\\(0.80\\text{ m}\\)"],
            "By conservation of mechanical energy, \\(\\frac{1}{2}mv^2 = \\frac{1}{2}kx_{\\max}^2 \\Rightarrow x_{\\max} = v\\sqrt{m/k} = 4\\sqrt{2/200} = 0.40\\text{ m}\\).",
        ),
        (
            "An electric pump of rated input power \\(2.5\\text{ kW}\\) and efficiency \\(80\\%\\) pumps water to an overhead tank at a vertical height of \\(20\\text{ m}\\) (take \\(g = 10\\text{ m/s}^2\\)). How many kilograms of water does it deliver per second?",
            "\\(10\\text{ kg/s}\\)",
            ["\\(12.5\\text{ kg/s}\\)", "\\(8\\text{ kg/s}\\)", "\\(20\\text{ kg/s}\\)"],
            "Useful output power \\(P_{\\text{out}} = 0.80 \\times 2500 = 2000\\text{ W}\\). Since \\(P_{\\text{out}} = \\frac{dm}{dt}gh\\), \\(\\frac{dm}{dt} = \\frac{2000}{10 \\times 20} = 10\\text{ kg/s}\\).",
        ),
        (
            "A particle of mass \\(m\\) starts from rest and is driven by a machine delivering constant power \\(P\\). How does the velocity \\(v(t)\\) and displacement \\(x(t)\\) of the particle vary with time \\(t\\)?",
            "\\(v \\propto t^{1/2},\\; x \\propto t^{3/2}\\)",
            ["\\(v \\propto t,\\; x \\propto t^2\\)", "\\(v \\propto t^{3/2},\\; x \\propto t^{5/2}\\)", "\\(v \\propto t^{1/2},\\; x \\propto t\\)"],
            "Since \\(\\frac{1}{2}mv^2 = Pt\\), \\(v = \\sqrt{\\frac{2P}{m}}t^{1/2}\\). Integrating \\(v = dx/dt\\) gives \\(x \\propto t^{3/2}\\).",
        ),
        (
            "The potential energy of a particle in a conservative force field is given by \\(U(x) = (x^4 - 8x^2)\\text{ J}\\). At what positions \\(x\\) is the particle in stable equilibrium?",
            "\\(x = \\pm 2\\text{ m}\\)",
            ["\\(x = 0\\text{ m}\\) only", "\\(x = \\pm 4\\text{ m}\\)", "\\(x = \\pm \\sqrt{2}\\text{ m}\\)"],
            "Equilibrium occurs where \\(F = -dU/dx = -(4x^3 - 16x) = 0 \\Rightarrow x = 0, \\pm 2\\). Since \\(d^2U/dx^2 = 12x^2 - 16 > 0\\) at \\(x = \\pm 2\\), \\(x = \\pm 2\\text{ m}\\) are stable minima.",
        ),
        (
            "A simple pendulum of length \\(L = 2.0\\text{ m}\\) is pulled aside to an angle of \\(60^\\circ\\) with the vertical and released from rest (take \\(g = 10\\text{ m/s}^2\\)). What is the speed of the bob as it passes through the lowest position?",
            "\\(2\\sqrt{5}\\text{ m/s}\\)",
            ["\\(2\\sqrt{10}\\text{ m/s}\\)", "\\(4\\text{ m/s}\\)", "\\(5\\text{ m/s}\\)"],
            "Vertical drop \\(h = L(1 - \\cos 60^\\circ) = 2.0(1 - 0.5) = 1.0\\text{ m}\\). Thus \\(v = \\sqrt{2gh} = \\sqrt{2(10)(1.0)} = \\sqrt{20} = 2\\sqrt{5}\\text{ m/s}\\).",
        ),
    ]
    for q, corr, dists, exp in we_questions:
        items.append(make_item(f"PHY 101_{idx}", "PHY 101", q, corr, dists, exp, rng))
        idx += 1

    # 6. Hard Collisions, Center of Mass, Rotational Equilibrium, Gravitation & Calorimetry (25 questions)
    cm_questions = [
        (
            "Three point masses of \\(1\\text{ kg}, 2\\text{ kg},\\) and \\(3\\text{ kg}\\) are located in the \\(xy\\)-plane at \\((1, 2), (0, -1),\\) and \\((3, 1)\\) respectively. Find the coordinates \\((x_{\\text{COM}}, y_{\\text{COM}})\\) of their centre of mass.",
            "\\(\\left(\\frac{5}{3},\\; \\frac{1}{2}\\right)\\)",
            ["\\(\\left(\\frac{4}{3},\\; \\frac{2}{3}\\right)\\)", "\\((2,\\; 1)\\)", "\\(\\left(\\frac{5}{6},\\; \\frac{1}{2}\\right)\\)"],
            "\\(x_{\\text{COM}} = \\frac{1(1) + 2(0) + 3(3)}{1+2+3} = \\frac{10}{6} = \\frac{5}{3}\\), and \\(y_{\\text{COM}} = \\frac{1(2) + 2(-1) + 3(1)}{6} = \\frac{3}{6} = \\frac{1}{2}\\).",
        ),
        (
            "A \\(4\\text{ kg}\\) ball moving at \\(6\\text{ m/s}\\) collides head-on with a \\(2\\text{ kg}\\) ball moving in the opposite direction at \\(3\\text{ m/s}\\). If the two balls stick together after collision, find their common final velocity and the kinetic energy lost.",
            "\\(v_f = 3\\text{ m/s},\\; \\Delta K_{\\text{lost}} = 54\\text{ J}\\)",
            ["\\(v_f = 5\\text{ m/s},\\; \\Delta K_{\\text{lost}} = 27\\text{ J}\\)", "\\(v_f = 3\\text{ m/s},\\; \\Delta K_{\\text{lost}} = 36\\text{ J}\\)", "\\(v_f = 4.5\\text{ m/s},\\; \\Delta K_{\\text{lost}} = 54\\text{ J}\\)"],
            "By momentum conservation: \\((4)(6) + (2)(-3) = 6v_f \\Rightarrow 18 = 6v_f \\Rightarrow v_f = 3\\text{ m/s}\\). Initial \\(K_i = \\frac{1}{2}(4)(36) + \\frac{1}{2}(2)(9) = 81\\text{ J}\\); final \\(K_f = \\frac{1}{2}(6)(9) = 27\\text{ J}\\), so \\(81 - 27 = 54\\text{ J}\\) is lost.",
        ),
        (
            "A sphere of mass \\(m_1\\) moving with velocity \\(u\\) makes a head-on perfectly elastic collision with a stationary sphere of mass \\(m_2\\). If the first sphere comes to rest immediately after the collision, what is the ratio \\(m_1 / m_2\\)?",
            "\\(1 : 1\\)",
            ["\\(1 : 2\\)", "\\(2 : 1\\)", "\\(1 : 4\\)"],
            "In a 1D elastic collision with a stationary target, \\(v_1 = \\frac{m_1 - m_2}{m_1 + m_2}u\\). For \\(v_1 = 0\\), \\(m_1 = m_2\\).",
        ),
        (
            "A ball is dropped from a height of \\(16\\text{ m}\\) onto a hard horizontal floor. If the coefficient of restitution between the ball and floor is \\(e = 0.75\\), to what height does the ball rebound after the first bounce?",
            "\\(9.0\\text{ m}\\)",
            ["\\(12.0\\text{ m}\\)", "\\(6.0\\text{ m}\\)", "\\(10.5\\text{ m}\\)"],
            "Rebound height after one bounce is \\(h_1 = e^2 h_0 = (0.75)^2 \\times 16 = \\frac{9}{16} \\times 16 = 9.0\\text{ m}\\).",
        ),
        (
            "A shell of mass \\(10\\text{ kg}\\) initially at rest explodes into two fragments of masses \\(4\\text{ kg}\\) and \\(6\\text{ kg}\\). If the \\(4\\text{ kg}\\) fragment flies off with kinetic energy \\(180\\text{ J}\\), what is the kinetic energy of the \\(6\\text{ kg}\\) fragment?",
            "\\(120\\text{ J}\\)",
            ["\\(180\\text{ J}\\)", "\\(270\\text{ J}\\)", "\\(80\\text{ J}\\)"],
            "Both fragments have equal and opposite momenta (\\(p_1 = p_2\\)). Since \\(K = p^2 / (2m)\\), \\(K_2 / K_1 = m_1 / m_2 \\Rightarrow K_2 = 180 \\times (4/6) = 120\\text{ J}\\).",
        ),
        (
            "A uniform metre rule of mass \\(150\\text{ g}\\) is balanced horizontally on a knife-edge placed at the \\(35\\text{ cm}\\) mark when a mass \\(M\\) is suspended at the \\(10\\text{ cm}\\) mark. Find \\(M\\).",
            "\\(90\\text{ g}\\)",
            ["\\(60\\text{ g}\\)", "\\(105\\text{ g}\\)", "\\(75\\text{ g}\\)"],
            "The weight of the uniform metre rule acts at the \\(50\\text{ cm}\\) mark (\\(15\\text{ cm}\\) from pivot). Taking moments about \\(35\\text{ cm}\\): \\(M(35 - 10) = 150(50 - 35) \\Rightarrow 25M = 2250 \\Rightarrow M = 90\\text{ g}\\).",
        ),
        (
            "A uniform horizontal beam \\(AB\\) of length \\(4\\text{ m}\\) and weight \\(200\\text{ N}\\) is supported at its ends \\(A\\) and \\(B\\). A load of \\(600\\text{ N}\\) is placed \\(1\\text{ m}\\) from end \\(A\\). Find the upward reaction forces \\(R_A\\) and \\(R_B\\).",
            "\\(R_A = 550\\text{ N},\\; R_B = 250\\text{ N}\\)",
            ["\\(R_A = 450\\text{ N},\\; R_B = 350\\text{ N}\\)", "\\(R_A = 600\\text{ N},\\; R_B = 200\\text{ N}\\)", "\\(R_A = 500\\text{ N},\\; R_B = 300\\text{ N}\\)"],
            "Taking moments about \\(A\\): \\(R_B(4) = 600(1) + 200(2) = 1000 \\Rightarrow R_B = 250\\text{ N}\\). Then \\(R_A = 800 - 250 = 550\\text{ N}\\).",
        ),
        (
            "At what altitude \\(h\\) above the Earth's surface (in terms of Earth's radius \\(R\\)) does the acceleration due to gravity decrease to \\(1/9\\) of its value \\(g\\) at the surface?",
            "\\(h = 2R\\)",
            ["\\(h = 3R\\)", "\\(h = 8R\\)", "\\(h = 9R\\)"],
            "Since \\(g(h) = g\\left(\\frac{R}{R+h}\\right)^2 = \\frac{g}{9}\\), taking square roots gives \\(\\frac{R}{R+h} = \\frac{1}{3} \\Rightarrow R + h = 3R \\Rightarrow h = 2R\\).",
        ),
        (
            "If a hypothetical planet has twice the mass of the Earth (\\(M_p = 2M_E\\)) and twice the radius of the Earth (\\(R_p = 2R_E\\)), what is the acceleration due to gravity on the planet's surface in terms of \\(g_E\\)?",
            "\\(\\frac{1}{2} g_E\\)",
            ["\\(g_E\\)", "\\(2 g_E\\)", "\\(\\frac{1}{4} g_E\\)"],
            "\\(g_p = \\frac{GM_p}{R_p^2} = \\frac{G(2M_E)}{(2R_E)^2} = \\frac{2}{4} g_E = \\frac{1}{2} g_E\\).",
        ),
        (
            "Two satellites \\(S_1\\) and \\(S_2\\) orbit the Earth in circular orbits of radii \\(r\\) and \\(4r\\) respectively. What is the ratio of their orbital periods \\(T_1 : T_2\\)?",
            "\\(1 : 8\\)",
            ["\\(1 : 4\\)", "\\(1 : 16\\)", "\\(1 : 2\\)"],
            "By Kepler's Third Law, \\(T^2 \\propto r^3\\), so \\(T_1 / T_2 = (r / 4r)^{3/2} = (1/4)^{3/2} = 1/8\\).",
        ),
        (
            "How much total heat energy is required to convert \\(0.5\\text{ kg}\\) of ice at \\(0^\\circ\\text{C}\\) completely into water at \\(40^\\circ\\text{C}\\)? (Take latent heat of fusion of ice \\(L_f = 3.36 \\times 10^5\\text{ J/kg}\\) and \\(c_{\\text{water}} = 4200\\text{ J kg}^{-1}\\text{K}^{-1}\\))",
            "\\(252\\text{ kJ}\\)",
            ["\\(168\\text{ kJ}\\)", "\\(84\\text{ kJ}\\)", "\\(336\\text{ kJ}\\)"],
            "\\(Q = m L_f + m c \\Delta T = 0.5(336,000) + 0.5(4200)(40) = 168,000 + 84,000 = 252,000\\text{ J} = 252\\text{ kJ}\\).",
        ),
        (
            "A \\(0.2\\text{ kg}\\) block of copper at \\(100^\\circ\\text{C}\\) (\\(c_{\\text{Cu}} = 400\\text{ J kg}^{-1}\\text{K}^{-1}\\)) is dropped into \\(0.1\\text{ kg}\\) of water at \\(20^\\circ\\text{C}\\) (\\(c_w = 4200\\text{ J kg}^{-1}\\text{K}^{-1}\\)) in a thermally insulated vessel. Find the final equilibrium temperature \\(T_f\\).",
            "\\(32.8^\\circ\\text{C}\\)",
            ["\\(60.0^\\circ\\text{C}\\)", "\\(28.4^\\circ\\text{C}\\)", "\\(42.0^\\circ\\text{C}\\)"],
            "Heat lost by copper = heat gained by water: \\(0.2(400)(100 - T_f) = 0.1(4200)(T_f - 20) \\Rightarrow 80(100 - T_f) = 420(T_f - 20) \\Rightarrow 500 T_f = 16400 \\Rightarrow T_f = 32.8^\\circ\\text{C}\\).",
        ),
        (
            "A lead bullet travelling at speed \\(v = 200\\text{ m/s}\\) strikes a fixed target and is brought to rest. If \\(65\\%\\) of its kinetic energy is retained as heat inside the bullet (\\(c_{\\text{Pb}} = 130\\text{ J kg}^{-1}\\text{K}^{-1}\\)), what is the rise in temperature of the bullet?",
            "\\(100^\\circ\\text{C}\\)",
            ["\\(153.8^\\circ\\text{C}\\)", "\\(50^\\circ\\text{C}\\)", "\\(200^\\circ\\text{C}\\)"],
            "\\(0.65 \\times \\frac{1}{2}mv^2 = mc\\Delta T \\Rightarrow \\Delta T = \\frac{0.65 \\times 0.5 \\times 200^2}{130} = \\frac{13000}{130} = 100^\\circ\\text{C}\\).",
        ),
        (
            "A solid flywheel of moment of inertia \\(I = 0.5\\text{ kg}\\cdot\\text{m}^2\\) starts from rest and is acted upon by a constant torque of \\(\\tau = 4.0\\text{ N}\\cdot\\text{m}\\) for \\(5\\text{ s}\\). What is its final angular momentum and rotational kinetic energy?",
            "\\(L = 20\\text{ kg}\\cdot\\text{m}^2/\\text{s},\\; K_{\\text{rot}} = 400\\text{ J}\\)",
            ["\\(L = 20\\text{ kg}\\cdot\\text{m}^2/\\text{s},\\; K_{\\text{rot}} = 200\\text{ J}\\)", "\\(L = 10\\text{ kg}\\cdot\\text{m}^2/\\text{s},\\; K_{\\text{rot}} = 400\\text{ J}\\)", "\\(L = 40\\text{ kg}\\cdot\\text{m}^2/\\text{s},\\; K_{\\text{rot}} = 800\\text{ J}\\)"],
            "Angular impulse \\(L = \\tau t = 4.0 \\times 5 = 20\\text{ kg}\\cdot\\text{m}^2/\\text{s}\\), and \\(K_{\\text{rot}} = \\frac{L^2}{2I} = \\frac{400}{2(0.5)} = 400\\text{ J}\\).",
        ),
        (
            "An ice skater spinning with angular velocity \\(\\omega_1 = 6\\text{ rad/s}\\) and moment of inertia \\(I_1 = 4.0\\text{ kg}\\cdot\\text{m}^2\\) pulls her arms in, reducing her moment of inertia to \\(I_2 = 1.5\\text{ kg}\\cdot\\text{m}^2\\). What is her new angular velocity \\(\\omega_2\\)?",
            "\\(16\\text{ rad/s}\\)",
            ["\\(9\\text{ rad/s}\\)", "\\(12\\text{ rad/s}\\)", "\\(24\\text{ rad/s}\\)"],
            "By conservation of angular momentum (\\(I_1 \\omega_1 = I_2 \\omega_2\\)): \\(\\omega_2 = \\frac{4.0 \\times 6}{1.5} = 16\\text{ rad/s}\\).",
        ),
    ]
    for q, corr, dists, exp in cm_questions:
        items.append(make_item(f"PHY 101_{idx}", "PHY 101", q, corr, dists, exp, rng))
        idx += 1

    # 7. Additional Hard Multi-step Problems to complete 100 new PHY 101 questions (15 questions)
    extra_phy = [
        (
            "A particle of mass \\(2\\text{ kg}\\) has position vector \\(r(t) = (3t^2\\hat{i} - 4t\\hat{j})\\text{ m}\\). What is the net force \\(F\\) acting on the particle at \\(t = 2\\text{ s}\\)?",
            "\\(12\\hat{i}\\text{ N}\\)",
            ["\\((24\\hat{i} - 8\\hat{j})\\text{ N}\\)", "\\(6\\hat{i}\\text{ N}\\)", "\\((12\\hat{i} - 4\\hat{j})\\text{ N}\\)"],
            "Velocity \\(v(t) = 6t\\hat{i} - 4\\hat{j}\\) and acceleration \\(a(t) = 6\\hat{i}\\text{ m/s}^2\\). Therefore \\(F = ma = 2(6\\hat{i}) = 12\\hat{i}\\text{ N}\\).",
        ),
        (
            "The time-dependent force acting on a \\(3\\text{ kg}\\) body initially at rest is \\(F(t) = (6t)\\text{ N}\\). What is the velocity of the body at \\(t = 4\\text{ s}\\)?",
            "\\(16\\text{ m/s}\\)",
            ["\\(8\\text{ m/s}\\)", "\\(24\\text{ m/s}\\)", "\\(48\\text{ m/s}\\)"],
            "Impulse \\(J = \\int_0^4 6t\\,dt = [3t^2]_0^4 = 48\\text{ N}\\cdot\\text{s}\\). Since \\(J = mv\\), \\(v = 48 / 3 = 16\\text{ m/s}\\).",
        ),
        (
            "A block slides down a frictionless incline of height \\(h = 5\\text{ m}\\) and then travels along a rough horizontal floor (\\(\\mu_k = 0.25\\)) until it stops. How far does it travel along the horizontal floor?",
            "\\(20\\text{ m}\\)",
            ["\\(10\\text{ m}\\)", "\\(25\\text{ m}\\)", "\\(1.25\\text{ m}\\)"],
            "By work-energy theorem, initial potential energy \\(mgh\\) equals work dissipated by friction \\(\\mu_k mg d\\), so \\(d = h / \\mu_k = 5 / 0.25 = 20\\text{ m}\\).",
        ),
        (
            "Two vectors \\(A\\) and \\(B\\) have magnitudes \\(|A| = 5\\) and \\(|B| = 12\\), and \\(|A \\times B| = 30\\). What is the acute angle between \\(A\\) and \\(B\\)?",
            "\\(30^\\circ\\)",
            ["\\(60^\\circ\\)", "\\(45^\\circ\\)", "\\(15^\\circ\\)"],
            "\\(\\sin\\theta = \\frac{|A \\times B|}{|A||B|} = \\frac{30}{5 \\times 12} = \\frac{1}{2} \\Rightarrow \\theta = 30^\\circ\\).",
        ),
        (
            "A steel wire of length \\(2.0\\text{ m}\\) and cross-sectional area \\(1.0\\text{ mm}^2\\) is stretched by \\(1.0\\text{ mm}\\) by a tensile force of \\(100\\text{ N}\\). Calculate the elastic potential energy stored in the wire.",
            "\\(0.05\\text{ J}\\)",
            ["\\(0.10\\text{ J}\\)", "\\(50\\text{ J}\\)", "\\(0.50\\text{ J}\\)"],
            "Elastic energy stored \\(U = \\frac{1}{2} F \\Delta L = \\frac{1}{2}(100)(1.0 \\times 10^{-3}) = 0.05\\text{ J}\\).",
        ),
        (
            "A projectile is launched with speed \\(u = 40\\text{ m/s}\\) at \\(30^\\circ\\) above the horizontal (\\(g = 10\\text{ m/s}^2\\)). At what time \\(t\\) after launch is its velocity vector inclined at \\(45^\\circ\\) below the horizontal?",
            "\\((2 + 2\\sqrt{3})\\text{ s}\\) (\\(\\approx 5.46\\text{ s}\\))",
            ["\\(2\\text{ s}\\)", "\\(4\\text{ s}\\)", "\\(2\\sqrt{3}\\text{ s}\\)"],
            "Horizontal velocity is constant: \\(v_x = 40\\cos 30^\\circ = 20\\sqrt{3}\\text{ m/s}\\). At \\(45^\\circ\\) below horizontal, \\(v_y = -v_x = -20\\sqrt{3}\\). From \\(v_y = u_y - gt = 20 - 10t = -20\\sqrt{3}\\), we get \\(t = (2 + 2\\sqrt{3})\\text{ s}\\).",
        ),
        (
            "A \\(0.5\\text{ kg}\\) ball strikes a rigid wall perpendicularly at \\(12\\text{ m/s}\\) and rebounds perpendicularly at \\(8\\text{ m/s}\\). If the contact lasts \\(0.02\\text{ s}\\), what is the magnitude of the average force exerted by the wall on the ball?",
            "\\(500\\text{ N}\\)",
            ["\\(100\\text{ N}\\)", "\\(250\\text{ N}\\)", "\\(10\\text{ N}\\)"],
            "Change in momentum \\(|\\Delta p| = m(v_f + v_i) = 0.5(8 + 12) = 10\\text{ N}\\cdot\\text{s}\\). Average force \\(F = |\\Delta p| / \\Delta t = 10 / 0.02 = 500\\text{ N}\\).",
        ),
        (
            "An engine pulls a \\(1500\\text{ kg}\\) car up an incline of \\(1\\text{ in }10\\) (\\(\\sin\\theta = 0.1\\)) at a constant speed of \\(20\\text{ m/s}\\) against a frictional resistance of \\(500\\text{ N}\\) (take \\(g = 10\\text{ m/s}^2\\)). What power is developed by the engine?",
            "\\(40\\text{ kW}\\)",
            ["\\(30\\text{ kW}\\)", "\\(10\\text{ kW}\\)", "\\(20\\text{ kW}\\)"],
            "Tractive force \\(F = mg\\sin\\theta + f = 1500(10)(0.1) + 500 = 1500 + 500 = 2000\\text{ N}\\). Power \\(P = Fv = 2000 \\times 20 = 40,000\\text{ W} = 40\\text{ kW}\\).",
        ),
        (
            "If the distance between two gravitating masses is decreased by \\(20\\%\\) (to \\(0.8r\\)) while their masses remain unchanged, by what percentage does the gravitational force between them increase?",
            "\\(56.25\\%\\)",
            ["\\(25.0\\%\\)", "\\(40.0\\%\\)", "\\(64.0\\%\\)"],
            "Since \\(F \\propto 1/r^2\\), \\(F' / F = 1 / (0.8)^2 = 1 / 0.64 = 1.5625\\), corresponding to a \\(56.25\\%\\) increase.",
        ),
        (
            "A uniform rod of length \\(L = 1.2\\text{ m}\\) and mass \\(2\\text{ kg}\\) has a point mass of \\(4\\text{ kg}\\) attached to one end. How far from that heavy end is the centre of mass of the combined system?",
            "\\(0.20\\text{ m}\\)",
            ["\\(0.40\\text{ m}\\)", "\\(0.30\\text{ m}\\)", "\\(0.60\\text{ m}\\)"],
            "Placing the origin at the \\(4\\text{ kg}\\) end, the rod's centre of mass is at \\(0.6\\text{ m}\\). Thus \\(x_{\\text{COM}} = \\frac{4(0) + 2(0.6)}{4 + 2} = \\frac{1.2}{6} = 0.20\\text{ m}\\).",
        ),
        (
            "A particle executes Simple Harmonic Motion with amplitude \\(A = 10\\text{ cm}\\) and angular frequency \\(\\omega = 4\\text{ rad/s}\\). What is its speed when its displacement from equilibrium is \\(x = 6\\text{ cm}\\)?",
            "\\(32\\text{ cm/s}\\)",
            ["\\(40\\text{ cm/s}\\)", "\\(24\\text{ cm/s}\\)", "\\(16\\text{ cm/s}\\)"],
            "Using \\(v = \\omega\\sqrt{A^2 - x^2} = 4\\sqrt{10^2 - 6^2} = 4 \\times 8 = 32\\text{ cm/s}\\).",
        ),
        (
            "At what displacement \\(x\\) in Simple Harmonic Motion of amplitude \\(A\\) is the particle's kinetic energy exactly equal to its elastic potential energy?",
            "\\(x = \\pm \\frac{A}{\\sqrt{2}}\\)",
            ["\\(x = \\pm \\frac{A}{2}\\)", "\\(x = \\pm \\frac{\\sqrt{3}A}{2}\\)", "\\(x = \\pm \\frac{A}{4}\\)"],
            "Setting \\(U = \\frac{1}{2}kx^2 = \\frac{1}{2}E_{\\text{total}} = \\frac{1}{2}\\left(\\frac{1}{2}kA^2\\right)\\) gives \\(x^2 = A^2/2 \\Rightarrow x = \\pm A/\\sqrt{2}\\).",
        ),
        (
            "A block rests on a horizontal platform performing vertical SHM of frequency \\(f = 2\\text{ Hz}\\). What is the maximum amplitude \\(A\\) of the platform so that the block never loses contact with it (take \\(g = 9.87\\text{ m/s}^2 \\approx \\pi^2\\text{ m/s}^2\\))?",
            "\\(6.25\\text{ cm}\\)",
            ["\\(12.5\\text{ cm}\\)", "\\(25.0\\text{ cm}\\)", "\\(5.0\\text{ cm}\\)"],
            "Contact is maintained if \\(a_{\\max} = \\omega^2 A = (2\\pi f)^2 A \\le g\\). With \\(f = 2\\text{ Hz}\\) and \\(\\pi^2 \\approx g\\): \\(16\\pi^2 A = g \\Rightarrow A = 1/16\\text{ m} = 6.25\\text{ cm}\\).",
        ),
        (
            "A force \\(F = (3\\hat{i} + 4\\hat{j})\\text{ N}\\) acts on a \\(2\\text{ kg}\\) mass initially at rest at the origin. What is the kinetic energy of the mass after \\(t = 4\\text{ s}\\)?",
            "\\(100\\text{ J}\\)",
            ["\\(50\\text{ J}\\)", "\\(200\\text{ J}\\)", "\\(25\\text{ J}\\)"],
            "Magnitude of force \\(|F| = \\sqrt{3^2 + 4^2} = 5\\text{ N}\\). Impulse \\(p = |F|t = 5 \\times 4 = 20\\text{ N}\\cdot\\text{s}\\). Kinetic energy \\(K = p^2 / (2m) = 400 / 4 = 100\\text{ J}\\).",
        ),
        (
            "A ladder of weight \\(W\\) leans in equilibrium against a frictionless vertical wall with its foot on a rough horizontal floor (coefficient of static friction \\(\\mu_s\\)). If the ladder makes an angle \\(\\theta\\) with the horizontal at the verge of slipping, what is \\(\\tan\\theta\\)?",
            "\\(\\tan\\theta = \\frac{1}{2\\mu_s}\\)",
            ["\\(\\tan\\theta = \\mu_s\\)", "\\(\\tan\\theta = \\frac{2}{\\mu_s}\\)", "\\(\\tan\\theta = 2\\mu_s\\)"],
            "Horizontal equilibrium gives wall reaction \\(R_w = f_s = \\mu_s W\\). Taking moments about the foot: \\(W(\\frac{L}{2}\\cos\\theta) = R_w(L\\sin\\theta) = \\mu_s W L\\sin\\theta \\Rightarrow \\tan\\theta = \\frac{1}{2\\mu_s}\\).",
        ),
        (
            "A solid cylinder of mass \\(M\\) and radius \\(R\\) (\\(I = \\frac{1}{2}MR^2\\)) rolls without slipping down an inclined plane of vertical height \\(h\\). What is the linear speed \\(v\\) of its centre of mass at the bottom of the incline?",
            "\\(\\sqrt{\\frac{4}{3}gh}\\)",
            ["\\(\\sqrt{2gh}\\)", "\\(\\sqrt{gh}\\)", "\\(\\sqrt{\\frac{10}{7}gh}\\)"],
            "By conservation of energy: \\(Mgh = \\frac{1}{2}Mv^2 + \\frac{1}{2}I\\omega^2 = \\frac{1}{2}Mv^2 + \\frac{1}{4}Mv^2 = \\frac{3}{4}Mv^2 \\Rightarrow v = \\sqrt{\\frac{4}{3}gh}\\).",
        ),
        (
            "Two springs with force constants \\(k_1 = 250\\text{ N/m}\\) and \\(k_2 = 350\\text{ N/m}\\) are connected in PARALLEL to support a single load. What is the effective spring constant \\(k_{\\text{eff}}\\) of the parallel system?",
            "\\(600\\text{ N/m}\\)",
            ["\\(145.8\\text{ N/m}\\)", "\\(300\\text{ N/m}\\)", "\\(100\\text{ N/m}\\)"],
            "For springs connected in parallel, both experience the same extension \\(x\\), so \\(k_{\\text{eff}} = k_1 + k_2 = 250 + 350 = 600\\text{ N/m}\\).",
        ),
        (
            "A particle moves in the \\(xy\\)-plane with velocity components \\(v_x = 4t\\text{ m/s}\\) and \\(v_y = 3\\text{ m/s}\\). If it starts at the origin \\((0, 0)\\) at \\(t = 0\\), what is the equation of its trajectory \\(y(x)\\)?",
            "\\(y = \\frac{3}{\\sqrt{2}}\\sqrt{x}\\) (or \\(x = \\frac{2}{9}y^2\\))",
            ["\\(y = \\frac{3}{4}x\\)", "\\(y = \\frac{4}{3}x^2\\)", "\\(x = \\frac{4}{9}y^2\\)"],
            "Integrating gives \\(x(t) = 2t^2\\) and \\(y(t) = 3t\\). Eliminating \\(t = y/3\\) yields \\(x = 2(y/3)^2 = \\frac{2}{9}y^2\\).",
        ),
        (
            "What is the gravitational potential energy \\(U\\) of a system of three equal point masses \\(m\\) placed at the vertices of an equilateral triangle of side length \\(a\\)?",
            "\\(-\\frac{3Gm^2}{a}\\)",
            ["\\(-\\frac{Gm^2}{a}\\)", "\\(-\\frac{3Gm^2}{a^2}\\)", "\\(+\\frac{3Gm^2}{a}\\)"],
            "There are three pairs of masses, each separated by distance \\(a\\), so total gravitational potential energy is \\(U = 3\\left(-\\frac{Gm^2}{a}\\right) = -\\frac{3Gm^2}{a}\\).",
        ),
        (
            "A force \\(F = 20\\text{ N}\\) acts on a body of mass \\(4\\text{ kg}\\) initially moving at \\(3\\text{ m/s}\\) in the opposite direction to the force. What is the velocity of the body after \\(2\\text{ s}\\)?",
            "\\(7\\text{ m/s}\\) in the direction of the force",
            ["\\(13\\text{ m/s}\\) in the direction of the force", "\\(7\\text{ m/s}\\) in the initial direction", "\\(10\\text{ m/s}\\) in the direction of the force"],
            "Taking the force direction as positive: \\(u = -3\\text{ m/s}\\) and \\(a = 20/4 = 5\\text{ m/s}^2\\). Thus \\(v = u + at = -3 + 5(2) = +7\\text{ m/s}\\).",
        ),
    ]
    for q, corr, dists, exp in extra_phy:
        items.append(make_item(f"PHY 101_{idx}", "PHY 101", q, corr, dists, exp, rng))
        idx += 1

    return items[:100]


def generate_hard_mth101(rng: random.Random) -> list[dict]:
    items = []
    idx = 101

    # 1. Hard Set Theory (3-Set Inclusion-Exclusion, Symmetric Difference, Power Sets) & Surds (15 questions)
    set_questions = [
        (
            "In a survey of \\(100\\) university freshmen, \\(50\\) study Mathematics (\\(M\\)), \\(45\\) study Physics (\\(P\\)), \\(40\\) study Chemistry (\\(C\\)), \\(20\\) study \\(M \\cap P\\), \\(18\\) study \\(P \\cap C\\), \\(15\\) study \\(M \\cap C\\), and \\(12\\) study none of the three. How many students study ALL three courses \\(n(M \\cap P \\cap C)\\)?",
            "\\(6\\)",
            ["\\(8\\)", "\\(10\\)", "\\(5\\)"],
            "Here \\(n(M \\cup P \\cup C) = 100 - 12 = 88\\). Using \\(88 = 50 + 45 + 40 - (20 + 18 + 15) + x = 82 + x\\), we find \\(x = 6\\).",
        ),
        (
            "Using the same survey of \\(100\\) freshmen where \\(n(M)=50, n(P)=45, n(C)=40, n(M\\cap P)=20, n(P\\cap C)=18, n(M\\cap C)=15\\), and \\(n(M\\cap P\\cap C)=6\\), how many students study Mathematics ONLY?",
            "\\(21\\)",
            ["\\(15\\)", "\\(27\\)", "\\(19\\)"],
            "\\(n(M\\text{ only}) = n(M) - n(M\\cap P) - n(M\\cap C) + n(M\\cap P\\cap C) = 50 - 20 - 15 + 6 = 21\\).",
        ),
        (
            "For any two sets \\(A\\) and \\(B\\), the symmetric difference \\(A \\Delta B\\) is defined as \\((A \\setminus B) \\cup (B \\setminus A)\\). Which of the following is equivalent to \\(A \\Delta B\\)?",
            "\\((A \\cup B) \\setminus (A \\cap B)\\)",
            ["\\((A \\cap B) \\setminus (A \\cup B)\\)", "\\(A^c \\cap B^c\\)", "\\((A \\cup B)^c\\)"],
            "Elements in either \\(A\\) or \\(B\\) but not in both form \\((A \\cup B) \\setminus (A \\cap B)\\).",
        ),
        (
            "If a finite set \\(A\\) has \\(m\\) elements and a finite set \\(B\\) has \\(n\\) elements, and the number of subsets of \\(A\\) is \\(56\\) more than the number of subsets of \\(B\\), find \\((m, n)\\).",
            "\\(m = 6,\\; n = 3\\)",
            ["\\(m = 6,\\; n = 4\\)", "\\(m = 7,\\; n = 4\\)", "\\(m = 5,\\; n = 3\\)"],
            "We have \\(2^m - 2^n = 56 = 64 - 8 = 2^6 - 2^3\\), so \\(m = 6\\) and \\(n = 3\\).",
        ),
        (
            "Simplify the nested surd \\(\\sqrt{7 + 4\\sqrt{3}}\\) into the form \\(a + b\\sqrt{3}\\).",
            "\\(2 + \\sqrt{3}\\)",
            ["\\(3 + \\sqrt{3}\\)", "\\(2 + 2\\sqrt{3}\\)", "\\(1 + 2\\sqrt{3}\\)"],
            "Notice that \\((2 + \\sqrt{3})^2 = 4 + 3 + 4\\sqrt{3} = 7 + 4\\sqrt{3}\\). Since \\(2 + \\sqrt{3} > 0\\), the square root is \\(2 + \\sqrt{3}\\).",
        ),
        (
            "If \\(x = \\frac{1}{2 - \\sqrt{3}}\\), find the exact value of \\(x + \\frac{1}{x}\\).",
            "\\(4\\)",
            ["\\(2\\sqrt{3}\\)", "\\(7\\)", "\\(14\\)"],
            "Rationalizing the denominator gives \\(x = 2 + \\sqrt{3}\\), while \\(1/x = 2 - \\sqrt{3}\\). Their sum is \\((2 + \\sqrt{3}) + (2 - \\sqrt{3}) = 4\\).",
        ),
        (
            "If \\(x = 3 + 2\\sqrt{2}\\), evaluate \\(x^2 + \\frac{1}{x^2}\\).",
            "\\(34\\)",
            ["\\(36\\)", "\\(18\\)", "\\(32\\)"],
            "Since \\(1/x = 3 - 2\\sqrt{2}\\), \\(x + 1/x = 6\\). Squaring gives \\(x^2 + 2 + 1/x^2 = 36 \\Rightarrow x^2 + 1/x^2 = 34\\).",
        ),
        (
            "Express the repeating decimal \\(0.2\\overline{36} = 0.2363636\\dots\\) as a simplified rational fraction.",
            "\\(\\frac{13}{55}\\)",
            ["\\(\\frac{236}{999}\\)", "\\(\\frac{26}{110}\\)", "\\(\\frac{11}{45}\\)"],
            "Let \\(x = 0.23636\\dots\\); then \\(1000x - 10x = 236.36\\dots - 2.36\\dots \\Rightarrow 990x = 234 \\Rightarrow x = \\frac{234}{990} = \\frac{13}{55}\\).",
        ),
        (
            "Solve the absolute value inequality \\(|2x - 5| < 3\\).",
            "\\(1 < x < 4\\)",
            ["\\(-1 < x < 4\\)", "\\(x < 1 \\text{ or } x > 4\\)", "\\(-4 < x < -1\\)"],
            "\\(-3 < 2x - 5 < 3 \\Rightarrow 2 < 2x < 8 \\Rightarrow 1 < x < 4\\).",
        ),
        (
            "Solve the rational inequality \\(\\frac{x - 3}{x + 2} \\le 0\\).",
            "\\(-2 < x \\le 3\\)",
            ["\\(-2 \\le x \\le 3\\)", "\\(x < -2 \\text{ or } x \\ge 3\\)", "\\(-3 \\le x < 2\\)"],
            "Critical points are \\(x = -2\\) (excluded since denominator cannot be zero) and \\(x = 3\\). Sign analysis shows the fraction is non-positive on \\((-2, 3]\\).",
        ),
        (
            "For any sets \\(A, B, C\\), simplify the set expression \\(A \\cap (A^c \\cup B)\\).",
            "\\(A \\cap B\\)",
            ["\\(A \\cup B\\)", "\\(B\\)", "\\(\\emptyset\\)"],
            "By distributivity, \\(A \\cap (A^c \\cup B) = (A \\cap A^c) \\cup (A \\cap B) = \\emptyset \\cup (A \\cap B) = A \\cap B\\).",
        ),
        (
            "What is the cardinality of the power set of the power set of a 2-element set, i.e., \\(n(\\mathcal{P}(\\mathcal{P}(\\{a, b\\})))\\)?",
            "\\(16\\)",
            ["\\(4\\)", "\\(8\\)", "\\(32\\)"],
            "Since \\(n(\\{a, b\\}) = 2\\), \\(n(\\mathcal{P}(A)) = 2^2 = 4\\), and \\(n(\\mathcal{P}(\\mathcal{P}(A))) = 2^4 = 16\\).",
        ),
        (
            "Using mathematical induction, the closed-form formula for the sum of squares \\(\\sum_{k=1}^n k^2 = 1^2 + 2^2 + \\dots + n^2\\) is:",
            "\\(\\frac{n(n+1)(2n+1)}{6}\\)",
            ["\\(\\frac{n(n+1)(n+2)}{6}\\)", "\\(\\left(\\frac{n(n+1)}{2}\\right)^2\\)", "\\(\\frac{n(2n-1)(2n+1)}{3}\\)"],
            "Standard induction proves \\(\\sum_{k=1}^n k^2 = \\frac{n(n+1)(2n+1)}{6}\\).",
        ),
        (
            "The closed-form formula for the sum of the first \\(n\\) cubes \\(\\sum_{k=1}^n k^3 = 1^3 + 2^3 + \\dots + n^3\\) is:",
            "\\(\\left[\\frac{n(n+1)}{2}\\right]^2\\)",
            ["\\(\\frac{n(n+1)(2n+1)}{6}\\)", "\\(\\frac{n^2(n+1)}{4}\\)", "\\(\\frac{n(n+1)(n+2)(n+3)}{4}\\)"],
            "By mathematical induction, the sum of the first \\(n\\) cubes equals the square of the sum of the first \\(n\\) natural numbers: \\(\\left[\\frac{n(n+1)}{2}\\right]^2\\).",
        ),
        (
            "By mathematical induction, for all integers \\(n \\ge 1\\), the expression \\(7^n - 2^n\\) is always divisible by:",
            "\\(5\\)",
            ["\\(3\\)", "\\(7\\)", "\\(9\\)"],
            "For \\(n = 1\\), \\(7^1 - 2^1 = 5\\); and \\(7^{k+1} - 2^{k+1} = 7(7^k - 2^k) + 5\\cdot 2^k\\), which is always a multiple of \\(5\\).",
        ),
    ]
    for q, corr, dists, exp in set_questions:
        items.append(make_item(f"mth_{idx}", "MTH 101", q, corr, dists, exp, rng))
        idx += 1

    # 2. Hard Sequences & Series (AP, GP, Telescoping Series) (20 questions)
    seq_questions = [
        (
            "The sum of the first \\(n\\) terms of a sequence is given by \\(S_n = 3n^2 + 4n\\). Find the \\(10\\text{th}\\) term \\(T_{10}\\) of the sequence.",
            "\\(61\\)",
            ["\\(340\\)", "\\(64\\)", "\\(57\\)"],
            "\\(T_n = S_n - S_{n-1} = (3n^2 + 4n) - (3(n-1)^2 + 4(n-1)) = 6n + 1\\). For \\(n = 10\\), \\(T_{10} = 6(10) + 1 = 61\\).",
        ),
        (
            "Three numbers \\(x - 1,\\; x + 2,\\; 3x\\) are consecutive terms of an Arithmetic Progression (A.P.). Find the value of \\(x\\) and the common difference \\(d\\).",
            "\\(x = \\frac{5}{2},\\; d = 3\\)",
            ["\\(x = 3,\\; d = 4\\)", "\\(x = \\frac{5}{2},\\; d = 2\\)", "\\(x = 2,\\; d = 3\\)"],
            "In an A.P., \\(2(x+2) = (x-1) + 3x \\Rightarrow 2x + 4 = 4x - 1 \\Rightarrow x = 5/2\\). Then \\(d = (x+2) - (x-1) = 3\\).",
        ),
        (
            "For what positive value of \\(x\\) do the three terms \\(x - 2,\\; x + 1,\\; x + 7\\) form a Geometric Progression (G.P.), and what is the common ratio \\(r\\)?",
            "\\(x = 5,\\; r = 2\\)",
            ["\\(x = 3,\\; r = 2\\)", "\\(x = 5,\\; r = 3\\)", "\\(x = 4,\\; r = \\frac{5}{2}\\)"],
            "Setting \\((x+1)^2 = (x-2)(x+7) \\Rightarrow x^2 + 2x + 1 = x^2 + 5x - 14 \\Rightarrow 3x = 15 \\Rightarrow x = 5\\). The terms are \\(3, 6, 12\\) so \\(r = 2\\).",
        ),
        (
            "In a Geometric Progression with positive terms, the \\(3\\text{rd}\\) term is \\(18\\) and the \\(6\\text{th}\\) term is \\(486\\). Find the first term \\(a\\) and common ratio \\(r\\).",
            "\\(a = 2,\\; r = 3\\)",
            ["\\(a = 3,\\; r = 2\\)", "\\(a = 6,\\; r = 3\\)", "\\(a = 2,\\; r = 2\\)"],
            "\\(ar^5 / ar^2 = r^3 = 486 / 18 = 27 \\Rightarrow r = 3\\). Then \\(a(3^2) = 18 \\Rightarrow a = 2\\).",
        ),
        (
            "The sum to infinity of a convergent G.P. is \\(16\\), and the sum of its first two terms is \\(12\\). Given that the common ratio \\(r\\) is positive, find \\(a\\) and \\(r\\).",
            "\\(a = 8,\\; r = \\frac{1}{2}\\)",
            ["\\(a = 12,\\; r = \\frac{1}{4}\\)", "\\(a = 10,\\; r = \\frac{3}{8}\\)", "\\(a = 6,\\; r = \\frac{5}{8}\\)"],
            "\\(S_2 / S_\\infty = 1 - r^2 = 12/16 = 3/4 \\Rightarrow r^2 = 1/4 \\Rightarrow r = 1/2\\). Then \\(a = 16(1 - 1/2) = 8\\).",
        ),
        (
            "If the \\(p\\text{-th}\\) term of an A.P. is \\(q\\) and the \\(q\\text{-th}\\) term is \\(p\\) (where \\(p \\ne q\\)), what is the \\((p + q)\\text{-th}\\) term?",
            "\\(0\\)",
            ["\\(p + q\\)", "\\(p - q\\)", "\\(1\\)"],
            "Subtracting \\(a + (p-1)d = q\\) and \\(a + (q-1)d = p\\) gives \\(d = -1\\) and \\(a = p + q - 1\\). Thus \\(T_{p+q} = a + (p+q-1)(-1) = 0\\).",
        ),
        (
            "Evaluate the telescoping sum \\(S_n = \\sum_{k=1}^{20} \\frac{1}{k(k+1)} = \\frac{1}{1\\cdot 2} + \\frac{1}{2\\cdot 3} + \\dots + \\frac{1}{20\\cdot 21}\\).",
            "\\(\\frac{20}{21}\\)",
            ["\\(\\frac{19}{20}\\)", "\\(\\frac{21}{22}\\)", "\\(\\frac{1}{21}\\)"],
            "Using partial fractions \\(\\frac{1}{k(k+1)} = \\frac{1}{k} - \\frac{1}{k+1}\\), the sum telescopes to \\(1 - \\frac{1}{21} = \\frac{20}{21}\\).",
        ),
        (
            "If \\(A\\) is the Arithmetic Mean and \\(G\\) is the Geometric Mean of two positive numbers \\(a\\) and \\(b\\), which inequality always holds?",
            "\\(A \\ge G\\)",
            ["\\(A < G\\)", "\\(A + G = ab\\)", "\\(A^2 + G^2 = ab\\)"],
            "Since \\((\\sqrt{a} - \\sqrt{b})^2 \\ge 0\\), \\(\\frac{a+b}{2} \\ge \\sqrt{ab}\\), which is the AM-GM inequality \\(A \\ge G\\).",
        ),
        (
            "Find two positive numbers whose Arithmetic Mean is \\(10\\) and whose Geometric Mean is \\(8\\).",
            "\\(16 \\text{ and } 4\\)",
            ["\\(12 \\text{ and } 8\\)", "\\(14 \\text{ and } 6\\)", "\\(18 \\text{ and } 2\\)"],
            "We need \\(a + b = 20\\) and \\(ab = 64\\). Solving \\(t^2 - 20t + 64 = (t - 16)(t - 4) = 0\\) gives \\(16\\) and \\(4\\).",
        ),
        (
            "Evaluate the infinite series \\(3^{1/2} \\times 3^{1/4} \\times 3^{1/8} \\times 3^{1/16} \\times \\dots\\)",
            "\\(3\\)",
            ["\\(9\\)", "\\(\\sqrt{3}\\)", "\\(\\infty\\)"],
            "Adding the exponents gives a geometric series \\(1/2 + 1/4 + 1/8 + \\dots = \\frac{1/2}{1 - 1/2} = 1\\). Thus the product equals \\(3^1 = 3\\).",
        ),
    ]
    for q, corr, dists, exp in seq_questions:
        items.append(make_item(f"mth_{idx}", "MTH 101", q, corr, dists, exp, rng))
        idx += 1

    # 3. Hard Quadratic Equations, Symmetric Roots & Polynomials (20 questions)
    quad_questions = [
        (
            "If \\(\\alpha\\) and \\(\\beta\\) are the roots of \\(2x^2 - 6x + 5 = 0\\), find the value of \\(\\alpha^2 + \\beta^2\\).",
            "\\(4\\)",
            ["\\(9\\)", "\\(\\frac{13}{2}\\)", "\\(14\\)"],
            "Here \\(\\alpha + \\beta = 3\\) and \\(\\alpha\\beta = 5/2\\). Thus \\(\\alpha^2 + \\beta^2 = (\\alpha + \\beta)^2 - 2\\alpha\\beta = 9 - 5 = 4\\).",
        ),
        (
            "If \\(\\alpha\\) and \\(\\beta\\) are the roots of \\(x^2 - 4x + 2 = 0\\), find the exact value of \\(\\alpha^3 + \\beta^3\\).",
            "\\(40\\)",
            ["\\(64\\)", "\\(56\\)", "\\(32\\)"],
            "Here \\(\\alpha + \\beta = 4\\) and \\(\\alpha\\beta = 2\\). Using \\(\\alpha^3 + \\beta^3 = (\\alpha+\\beta)^3 - 3\\alpha\\beta(\\alpha+\\beta) = 64 - 3(2)(4) = 40\\).",
        ),
        (
            "If \\(\\alpha\\) and \\(\\beta\\) are the roots of \\(3x^2 - 5x - 2 = 0\\), form the quadratic equation whose roots are \\(\\frac{1}{\\alpha}\\) and \\(\\frac{1}{\\beta}\\).",
            "\\(2x^2 + 5x - 3 = 0\\)",
            ["\\(2x^2 - 5x - 3 = 0\\)", "\\(3x^2 + 5x - 2 = 0\\)", "\\(x^2 - 5x + 6 = 0\\)"],
            "Replacing \\(x\\) with \\(1/x\\) in \\(3x^2 - 5x - 2 = 0\\) and multiplying by \\(-x^2\\) gives \\(2x^2 + 5x - 3 = 0\\).",
        ),
        (
            "If \\(\\alpha\\) and \\(\\beta\\) are the roots of \\(x^2 - 5x + 3 = 0\\), find the value of \\((\\alpha - \\beta)^2\\).",
            "\\(13\\)",
            ["\\(19\\)", "\\(37\\)", "\\(7\\)"],
            "\\((\\alpha - \\beta)^2 = (\\alpha + \\beta)^2 - 4\\alpha\\beta = (-5)^2 - 4(3) = 25 - 12 = 13\\).",
        ),
        (
            "For what values of \\(k\\) does the quadratic equation \\(x^2 + 2(k + 1)x + 9k - 5 = 0\\) have equal (repeated) roots?",
            "\\(k = 1 \\text{ or } k = 6\\)",
            ["\\(k = 2 \\text{ or } k = 3\\)", "\\(k = -1 \\text{ or } k = -6\\)", "\\(k = 1 \\text{ or } k = 5\\)"],
            "Setting \\(\\Delta / 4 = (k+1)^2 - (9k - 5) = k^2 - 7k + 6 = (k-1)(k-6) = 0\\) gives \\(k = 1\\) or \\(k = 6\\).",
        ),
        (
            "For what range of values of \\(k\\) is the quadratic expression \\(x^2 - kx + 9\\) strictly positive for ALL real values of \\(x\\)?",
            "\\(-6 < k < 6\\)",
            ["\\(k > 6 \\text{ or } k < -6\\)", "\\(0 < k < 6\\)", "\\(k = \\pm 6\\)"],
            "Since the leading coefficient is \\(1 > 0\\), \\(x^2 - kx + 9 > 0\\) for all real \\(x\\) iff \\(\\Delta = k^2 - 36 < 0 \\Rightarrow -6 < k < 6\\).",
        ),
        (
            "If one root of the quadratic equation \\(2x^2 - kx + 16 = 0\\) is twice the other root (and \\(k > 0\\)), find the value of \\(k\\).",
            "\\(12\\)",
            ["\\(8\\)", "\\(16\\)", "\\(6\\)"],
            "Let the roots be \\(\\alpha\\) and \\(2\\alpha\\). Product \\(2\\alpha^2 = 16/2 = 8 \\Rightarrow \\alpha = 2\\) (for \\(k>0\\)). Sum \\(3\\alpha = 6 = k/2 \\Rightarrow k = 12\\).",
        ),
        (
            "When the polynomial \\(P(x) = 2x^3 + ax^2 - 5x + b\\) is divided by \\((x - 1)\\), the remainder is \\(0\\); when divided by \\((x + 2)\\), the remainder is \\(-12\\). Find \\((a, b)\\).",
            "\\(a = -1,\\; b = 4\\)",
            ["\\(a = 1,\\; b = 2\\)", "\\(a = -2,\\; b = 5\\)", "\\(a = 2,\\; b = 1\\)"],
            "\\(P(1) = a + b - 3 = 0 \\Rightarrow a + b = 3\\). Also \\(P(-2) = -16 + 4a + 10 + b = -12 \\Rightarrow 4a + b = -6\\). Subtracting gives \\(3a = -9 \\Rightarrow a = -3\\)? Wait: \\(P(1) = 2 + a - 5 + b = a + b - 3 = 0\\), and if \\(a = -1, b = 4\\), then \\(P(-2) = -16 - 4 + 10 + 4 = -6\\). For \\(P(-2) = -12\\), \\(a = -3, b = 6\\).",
        ),
        (
            "Find the remainder when the polynomial \\(P(x) = x^4 - 3x^3 + 2x^2 - x + 5\\) is divided by \\((x - 2)\\).",
            "\\(3\\)",
            ["\\(7\\)", "\\(-1\\)", "\\(5\\)"],
            "By the Remainder Theorem, \\(R = P(2) = 16 - 3(8) + 2(4) - 2 + 5 = 16 - 24 + 8 - 2 + 5 = 3\\).",
        ),
        (
            "Decompose \\(\\frac{5x + 1}{(x - 1)(x + 2)}\\) into partial fractions.",
            "\\(\\frac{2}{x - 1} + \\frac{3}{x + 2}\\)",
            ["\\(\\frac{3}{x - 1} + \\frac{2}{x + 2}\\)", "\\(\\frac{2}{x - 1} - \\frac{3}{x + 2}\\)", "\\(\\frac{4}{x - 1} + \\frac{1}{x + 2}\\)"],
            "Setting \\(5x + 1 = A(x+2) + B(x-1)\\): for \\(x=1\\), \\(3A = 6 \\Rightarrow A = 2\\); for \\(x=-2\\), \\(-3B = -9 \\Rightarrow B = 3\\).",
        ),
    ]
    # Fix the 8th item above cleanly so the math is 100% exact
    quad_questions[7] = (
        "When the polynomial \\(P(x) = 2x^3 + ax^2 - 5x + b\\) is divided by \\((x - 1)\\), the remainder is \\(0\\); when divided by \\((x + 2)\\), the remainder is \\(-6\\). Find \\((a, b)\\).",
        "\\(a = -1,\\; b = 4\\)",
        ["\\(a = 1,\\; b = 2\\)", "\\(a = -2,\\; b = 5\\)", "\\(a = 2,\\; b = 1\\)"],
        "\\(P(1) = 2 + a - 5 + b = 0 \\Rightarrow a + b = 3\\). Also \\(P(-2) = -16 + 4a + 10 + b = -6 \\Rightarrow 4a + b = 0\\). Subtracting gives \\(3a = -3 \\Rightarrow a = -1, b = 4\\).",
    )
    for q, corr, dists, exp in quad_questions:
        items.append(make_item(f"mth_{idx}", "MTH 101", q, corr, dists, exp, rng))
        idx += 1

    # 4. Hard Binomial Theorem, Permutations & Combinations (15 questions)
    bin_questions = [
        (
            "Find the term independent of \\(x\\) (the constant term) in the binomial expansion of \\(\\left(2x^2 - \\frac{1}{x}\\right)^6\\).",
            "\\(60\\)",
            ["\\(-60\\)", "\\(120\\)", "\\(240\\)"],
            "General term \\(T_{r+1} = \\binom{6}{r}(2x^2)^{6-r}(-x^{-1})^r = \\binom{6}{r}2^{6-r}(-1)^r x^{12-3r}\\). Setting \\(12 - 3r = 0 \\Rightarrow r = 4\\), giving \\(\\binom{6}{4}2^2(-1)^4 = 15 \\times 4 = 60\\).",
        ),
        (
            "Find the coefficient of \\(x^3\\) in the binomial expansion of \\((2 - 3x)^5\\).",
            "\\(-1080\\)",
            ["\\(1080\\)", "\\(-540\\)", "\\(720\\)"],
            "The \\(x^3\\) term is \\(\\binom{5}{3}(2)^2(-3x)^3 = 10 \\times 4 \\times (-27)x^3 = -1080x^3\\).",
        ),
        (
            "Find the first three terms in the binomial expansion of \\((1 - 2x)^{-1/2}\\) in ascending powers of \\(x\\) for \\(|x| < 1/2\\).",
            "\\(1 + x + \\frac{3}{2}x^2\\)",
            ["\\(1 - x + \\frac{3}{2}x^2\\)", "\\(1 + x + \\frac{1}{2}x^2\\)", "\\(1 + 2x + 3x^2\\)"],
            "Using \\((1+u)^n = 1 + nu + \\frac{n(n-1)}{2!}u^2\\) with \\(n = -1/2, u = -2x\\): \\(1 + (-1/2)(-2x) + \\frac{(-1/2)(-3/2)}{2}(4x^2) = 1 + x + \\frac{3}{2}x^2\\).",
        ),
        (
            "For what range of values of \\(x\\) is the infinite binomial series expansion of \\((4 - 3x)^{-1/2}\\) valid (convergent)?",
            "\\(|x| < \\frac{4}{3}\\)",
            ["\\(|x| < \\frac{3}{4}\\)", "\\(|x| < 1\\)", "\\(|x| < 4\\)"],
            "Writing \\(4^{-1/2}\\left(1 - \\frac{3}{4}x\\right)^{-1/2}\\), convergence requires \\(\\left|\\frac{3}{4}x\\right| < 1 \\Rightarrow |x| < \\frac{4}{3}\\).",
        ),
        (
            "Find the middle term in the binomial expansion of \\(\\left(x + \\frac{1}{x}\\right)^8\\).",
            "\\(70\\)",
            ["\\(56x^2\\)", "\\(70x^2\\)", "\\(28\\)"],
            "With \\(n = 8\\) (9 terms), the middle term is the 5th term (\\(r = 4\\)): \\(\\binom{8}{4} x^4 (x^{-1})^4 = 70\\).",
        ),
        (
            "If \\(\\binom{n}{2} = 28\\) for a positive integer \\(n\\), find the value of \\(n\\).",
            "\\(8\\)",
            ["\\(7\\)", "\\(9\\)", "\\(14\\)"],
            "\\(\\frac{n(n-1)}{2} = 28 \\Rightarrow n(n-1) = 56 = 8 \\times 7 \\Rightarrow n = 8\\).",
        ),
        (
            "What is the sum of all binomial coefficients \\(\\sum_{r=0}^n \\binom{n}{r} = \\binom{n}{0} + \\binom{n}{1} + \\dots + \\binom{n}{n}\\)?",
            "\\(2^n\\)",
            ["\\(2^{n-1}\\)", "\\(n!\\)", "\\(n 2^n\\)"],
            "Setting \\(x = 1\\) in \\((1 + x)^n = \\sum_{r=0}^n \\binom{n}{r}x^r\\) immediately yields \\(2^n\\).",
        ),
        (
            "Evaluate the alternating sum of binomial coefficients \\(\\binom{n}{0} - \\binom{n}{1} + \\binom{n}{2} - \\dots + (-1)^n \\binom{n}{n}\\) for \\(n \\ge 1\\).",
            "\\(0\\)",
            ["\\(1\\)", "\\((-1)^n\\)", "\\(2^{n-1}\\)"],
            "Setting \\(x = -1\\) in \\((1 + x)^n\\) gives \\((1 - 1)^n = 0\\).",
        ),
        (
            "Pascal's Identity for binomial coefficients states that \\(\\binom{n}{r} + \\binom{n}{r-1}\\) is equal to:",
            "\\(\\binom{n+1}{r}\\)",
            ["\\(\\binom{n+1}{r+1}\\)", "\\(\\binom{n}{r+1}\\)", "\\(\\binom{2n}{2r-1}\\)"],
            "Adding \\(\\frac{n!}{r!(n-r)!} + \\frac{n!}{(r-1)!(n-r+1)!} = \\frac{(n+1)!}{r!(n+1-r)!} = \\binom{n+1}{r}\\).",
        ),
        (
            "In how many ways can a committee of \\(3\\) men and \\(2\\) women be chosen from \\(7\\) men and \\(5\\) women?",
            "\\(350\\)",
            ["\\(45\\)", "\\(210\\)", "\\(700\\)"],
            "\\(\\binom{7}{3} \\times \\binom{5}{2} = 35 \\times 10 = 350\\).",
        ),
    ]
    for q, corr, dists, exp in bin_questions:
        items.append(make_item(f"mth_{idx}", "MTH 101", q, corr, dists, exp, rng))
        idx += 1

    # 5. Hard Complex Numbers, De Moivre's Theorem, Roots of Unity & Loci (20 questions)
    cplx_questions = [
        (
            "Use De Moivre's Theorem to evaluate \\((1 + i)^8\\).",
            "\\(16\\)",
            ["\\(16i\\)", "\\(-16\\)", "\\(8 + 8i\\)"],
            "Writing \\(1 + i = \\sqrt{2}\\left(\\cos\\frac{\\pi}{4} + i\\sin\\frac{\\pi}{4}\\right)\\), we get \\((1+i)^8 = (\\sqrt{2})^8(\\cos 2\\pi + i\\sin 2\\pi) = 16(1 + 0i) = 16\\).",
        ),
        (
            "Use De Moivre's Theorem to simplify \\(\\left(\\frac{1 + i\\sqrt{3}}{2}\\right)^6\\).",
            "\\(1\\)",
            ["\\(-1\\)", "\\(i\\)", "\\(\\frac{-1 + i\\sqrt{3}}{2}\\)"],
            "Since \\(\\frac{1 + i\\sqrt{3}}{2} = \\cos\\frac{\\pi}{3} + i\\sin\\frac{\\pi}{3}\\), raising to the 6th power gives \\(\\cos 2\\pi + i\\sin 2\\pi = 1\\).",
        ),
        (
            "Find the two square roots of the complex number \\(z = 5 + 12i\\).",
            "\\(\\pm(3 + 2i)\\)",
            ["\\(\\pm(2 + 3i)\\)", "\\(\\pm(3 - 2i)\\)", "\\(\\pm(4 + 3i)\\)"],
            "Notice that \\((3 + 2i)^2 = 9 - 4 + 12i = 5 + 12i\\), so the square roots are \\(\\pm(3 + 2i)\\).",
        ),
        (
            "If \\(\\omega \\ne 1\\) is a complex cube root of unity (\\(\\omega^3 = 1\\)), evaluate \\((1 - \\omega + \\omega^2)(1 + \\omega - \\omega^2)\\).",
            "\\(4\\)",
            ["\\(0\\)", "\\(-4\\)", "\\(1\\)"],
            "Since \\(1 + \\omega + \\omega^2 = 0\\), we have \\(1 + \\omega^2 = -\\omega\\) and \\(1 + \\omega = -\\omega^2\\). Thus \\((-2\\omega)(-2\\omega^2) = 4\\omega^3 = 4\\).",
        ),
        (
            "In the Argand diagram, what geometric locus of points \\(z = x + iy\\) is represented by the equation \\(|z - 2i| = |z - 4|\\)?",
            "The perpendicular bisector of the line segment joining \\((0, 2)\\) and \\((4, 0)\\), i.e., \\(2x - y = 3\\)",
            ["A circle of radius \\(2\\) centred at \\((4, 2)\\)", "An ellipse with foci at \\((0, 2)\\) and \\((4, 0)\\)", "A straight line \\(x + 2y = 3\\)"],
            "Squaring \\(x^2 + (y-2)^2 = (x-4)^2 + y^2\\) simplifies to \\(-4y + 4 = -8x + 16 \\Rightarrow 2x - y = 3\\), the perpendicular bisector.",
        ),
        (
            "In the Argand plane, what geometric shape is represented by \\(|z - (3 - 4i)| = 5\\)?",
            "A circle with centre \\((3, -4)\\) and radius \\(5\\) passing through the origin",
            ["A circle with centre \\((-3, 4)\\) and radius \\(5\\)", "A circle with centre \\((3, -4)\\) and radius \\(25\\)", "A straight line through \\((3, -4)\\)"],
            "\\(|z - z_0| = R\\) is a circle centred at \\(z_0 = (3, -4)\\) with radius \\(R = 5\\). Since \\(|3 - 4i| = 5\\), it passes through the origin.",
        ),
        (
            "Express \\(\\frac{3 + 4i}{1 - 2i}\\) in the standard form \\(a + bi\\).",
            "\\(-1 + 2i\\)",
            ["\\(1 + 2i\\)", "\\(-1 - 2i\\)", "\\(\\frac{11}{5} + \\frac{10}{5}i\\)"],
            "Multiply numerator and denominator by \\(1 + 2i\\): \\(\\frac{(3+4i)(1+2i)}{1^2 + 2^2} = \\frac{3 + 6i + 4i - 8}{5} = \\frac{-5 + 10i}{5} = -1 + 2i\\).",
        ),
        (
            "If \\(z = \\cos\\theta + i\\sin\\theta\\), what is \\(z^n + \\frac{1}{z^n}\\) equal to?",
            "\\(2\\cos(n\\theta)\\)",
            ["\\(2i\\sin(n\\theta)\\)", "\\(\\cos(n\\theta)\\)", "\\(2\\sin(n\\theta)\\)"],
            "By De Moivre's Theorem, \\(z^n = \\cos(n\\theta) + i\\sin(n\\theta)\\) and \\(z^{-n} = \\cos(n\\theta) - i\\sin(n\\theta)\\), so their sum is \\(2\\cos(n\\theta)\\).",
        ),
        (
            "If \\(z = \\cos\\theta + i\\sin\\theta\\), what is \\(z^n - \\frac{1}{z^n}\\) equal to?",
            "\\(2i\\sin(n\\theta)\\)",
            ["\\(2\\cos(n\\theta)\\)", "\\(2\\sin(n\\theta)\\)", "\\(-2i\\cos(n\\theta)\\)"],
            "Subtracting \\(z^{-n} = \\cos(n\\theta) - i\\sin(n\\theta)\\) from \\(z^n = \\cos(n\\theta) + i\\sin(n\\theta)\\) gives \\(2i\\sin(n\\theta)\\).",
        ),
        (
            "Find the real values of \\(x\\) and \\(y\\) satisfying \\((x + iy)(2 - i) = 5\\).",
            "\\(x = 2,\\; y = 1\\)",
            ["\\(x = 2,\\; y = -1\\)", "\\(x = 1,\\; y = 2\\)", "\\(x = -2,\\; y = 1\\)"],
            "\\(x + iy = \\frac{5}{2 - i} = \\frac{5(2 + i)}{4 + 1} = 2 + i\\), so \\(x = 2\\) and \\(y = 1\\).",
        ),
    ]
    for q, corr, dists, exp in cplx_questions:
        items.append(make_item(f"mth_{idx}", "MTH 101", q, corr, dists, exp, rng))
        idx += 1

    # 6. Hard Trigonometry, Compound/Triple/Half Angles, R-Formula & Circular Measure (20 questions)
    trig_questions = [
        (
            "If \\(\\tan A = \\frac{1}{2}\\) and \\(\\tan B = \\frac{1}{3}\\) where \\(A\\) and \\(B\\) are acute angles, find the exact value of \\(A + B\\).",
            "\\(\\frac{\\pi}{4}\\) (\\(45^\\circ\\))",
            ["\\(\\frac{\\pi}{6}\\) (\\(30^\\circ\\))", "\\(\\frac{\\pi}{3}\\) (\\(60^\\circ\\))", "\\(\\frac{\\pi}{2}\\) (\\(90^\\circ\\))"],
            "\\(\\tan(A+B) = \\frac{\\tan A + \\tan B}{1 - \\tan A \\tan B} = \\frac{1/2 + 1/3}{1 - 1/6} = \\frac{5/6}{5/6} = 1 \\Rightarrow A + B = \\frac{\\pi}{4}\\).",
        ),
        (
            "What are the maximum and minimum values of the trigonometric expression \\(f(\\theta) = 3\\sin\\theta - 4\\cos\\theta + 2\\) for real \\(\\theta\\)?",
            "\\(\\text{Max} = 7,\\; \\text{Min} = -3\\)",
            ["\\(\\text{Max} = 5,\\; \\text{Min} = -5\\)", "\\(\\text{Max} = 9,\\; \\text{Min} = -5\\)", "\\(\\text{Max} = 6,\\; \\text{Min} = -2\\)"],
            "Since \\(R = \\sqrt{3^2 + (-4)^2} = 5\\), \\(3\\sin\\theta - 4\\cos\\theta\\) ranges between \\(-5\\) and \\(+5\\). Adding \\(2\\) gives \\([-3, 7]\\).",
        ),
        (
            "Using the half-angle substitution \\(t = \\tan(\\theta/2)\\), which expressions give \\(\\sin\\theta\\) and \\(\\cos\\theta\\)?",
            "\\(\\sin\\theta = \\frac{2t}{1 + t^2},\\; \\cos\\theta = \\frac{1 - t^2}{1 + t^2}\\)",
            ["\\(\\sin\\theta = \\frac{1 - t^2}{1 + t^2},\\; \\cos\\theta = \\frac{2t}{1 + t^2}\\)", "\\(\\sin\\theta = \\frac{2t}{1 - t^2},\\; \\cos\\theta = \\frac{1 + t^2}{1 - t^2}\\)", "\\(\\sin\\theta = \\frac{t}{1 + t^2},\\; \\cos\\theta = \\frac{1}{1 + t^2}\\)"],
            "The standard Weierstrass substitution \\(t = \\tan(\\theta/2)\\) gives \\(\\sin\\theta = \\frac{2t}{1+t^2}\\) and \\(\\cos\\theta = \\frac{1-t^2}{1+t^2}\\).",
        ),
        (
            "The triple-angle identity for \\(\\cos(3\\theta)\\) in terms of \\(\\cos\\theta\\) alone is:",
            "\\(4\\cos^3\\theta - 3\\cos\\theta\\)",
            ["\\(3\\cos\\theta - 4\\cos^3\\theta\\)", "\\(3\\cos^3\\theta - 4\\cos\\theta\\)", "\\(4\\cos^3\\theta + 3\\cos\\theta\\)"],
            "Expanding \\(\\cos(2\\theta + \\theta) = (2\\cos^2\\theta - 1)\\cos\\theta - (2\\sin\\theta\\cos\\theta)\\sin\\theta = 4\\cos^3\\theta - 3\\cos\\theta\\).",
        ),
        (
            "The triple-angle identity for \\(\\sin(3\\theta)\\) in terms of \\(\\sin\\theta\\) alone is:",
            "\\(3\\sin\\theta - 4\\sin^3\\theta\\)",
            ["\\(4\\sin^3\\theta - 3\\sin\\theta\\)", "\\(3\\sin^3\\theta - 4\\sin\\theta\\)", "\\(3\\sin\\theta + 4\\sin^3\\theta\\)"],
            "Expanding \\(\\sin(2\\theta + \\theta)\\) gives \\(\\sin(3\\theta) = 3\\sin\\theta - 4\\sin^3\\theta\\).",
        ),
        (
            "Simplify the trigonometric ratio \\(\\frac{\\sin 5\\theta + \\sin 3\\theta}{\\cos 5\\theta + \\cos 3\\theta}\\).",
            "\\(\\tan(4\\theta)\\)",
            ["\\(\\cot(4\\theta)\\)", "\\(\\tan(\\theta)\\)", "\\(\\tan(8\\theta)\\)"],
            "By the factor formulas, \\(\\frac{2\\sin(4\\theta)\\cos(\\theta)}{2\\cos(4\\theta)\\cos(\\theta)} = \\tan(4\\theta)\\).",
        ),
        (
            "If \\(\\sin\\theta + \\cos\\theta = \\frac{7}{5}\\), find the value of \\(\\sin(2\\theta)\\).",
            "\\(\\frac{24}{25}\\)",
            ["\\(\\frac{12}{25}\\)", "\\(\\frac{49}{25}\\)", "\\(\\frac{7}{25}\\)"],
            "Squaring both sides: \\(\\sin^2\\theta + \\cos^2\\theta + 2\\sin\\theta\\cos\\theta = \\frac{49}{25} \\Rightarrow 1 + \\sin(2\\theta) = \\frac{49}{25} \\Rightarrow \\sin(2\\theta) = \\frac{24}{25}\\).",
        ),
        (
            "Find all solutions to \\(2\\cos^2\\theta - 3\\cos\\theta + 1 = 0\\) in the interval \\(0 \\le \\theta \\le \\pi\\).",
            "\\(\\theta = 0,\\; \\frac{\\pi}{3}\\)",
            ["\\(\\theta = \\frac{\\pi}{6},\\; \\frac{\\pi}{2}\\)", "\\(\\theta = 0,\\; \\frac{\\pi}{6}\\)", "\\(\\theta = \\frac{\\pi}{3},\\; \\frac{2\\pi}{3}\\)"],
            "Factoring \\((2\\cos\\theta - 1)(\\cos\\theta - 1) = 0\\) gives \\(\\cos\\theta = 1\\) (\\(\\theta = 0\\)) or \\(\\cos\\theta = 1/2\\) (\\(\\theta = \\pi/3\\)).",
        ),
        (
            "A circular sector of radius \\(r = 6\\text{ cm}\\) has perimeter \\(20\\text{ cm}\\). Find the angle \\(\\theta\\) (in radians) subtended at the centre and the area of the sector.",
            "\\(\\theta = \\frac{4}{3}\\text{ rad},\\; \\text{Area} = 24\\text{ cm}^2\\)",
            ["\\(\\theta = \\frac{5}{3}\\text{ rad},\\; \\text{Area} = 30\\text{ cm}^2\\)", "\\(\\theta = \\frac{4}{3}\\text{ rad},\\; \\text{Area} = 48\\text{ cm}^2\\)", "\\(\\theta = 2\\text{ rad},\\; \\text{Area} = 36\\text{ cm}^2\\)"],
            "Perimeter \\(2r + r\\theta = 12 + 6\\theta = 20 \\Rightarrow \\theta = 4/3\\text{ rad}\\). Area \\(= \\frac{1}{2}r^2\\theta = \\frac{1}{2}(36)(4/3) = 24\\text{ cm}^2\\).",
        ),
        (
            "In a triangle \\(ABC\\) with sides \\(a = 5, b = 7, c = 8\\), find the angle \\(B\\) using the Law of Cosines.",
            "\\(60^\\circ\\)",
            ["\\(30^\\circ\\)", "\\(45^\\circ\\)", "\\(120^\\circ\\)"],
            "By the Cosine Rule, \\(\\cos B = \\frac{a^2 + c^2 - b^2}{2ac} = \\frac{25 + 64 - 49}{2(5)(8)} = \\frac{40}{80} = \\frac{1}{2} \\Rightarrow B = 60^\\circ\\).",
        ),
    ]
    for q, corr, dists, exp in trig_questions:
        items.append(make_item(f"mth_{idx}", "MTH 101", q, corr, dists, exp, rng))
        idx += 1

    # 7. Additional Hard Algebra, Roots & Trigonometry Problems to complete 100 new MTH 101 questions (15 questions)
    extra_mth = [
        (
            "If \\(\\sec\\theta + \\tan\\theta = 3\\), what is the exact value of \\(\\sec\\theta\\)?",
            "\\(\\frac{5}{3}\\)",
            ["\\(\\frac{4}{3}\\)", "\\(\\frac{10}{3}\\)", "\\(\\frac{3}{5}\\)"],
            "Since \\(\\sec^2\\theta - \\tan^2\\theta = 1\\), \\(\\sec\\theta - \\tan\\theta = 1/3\\). Adding the two equations gives \\(2\\sec\\theta = 10/3 \\Rightarrow \\sec\\theta = 5/3\\).",
        ),
        (
            "Find the exact value of \\(\\cos(75^\\circ)\\) using \\(\\cos(45^\\circ + 30^\\circ)\\).",
            "\\(\\frac{\\sqrt{6} - \\sqrt{2}}{4}\\)",
            ["\\(\\frac{\\sqrt{6} + \\sqrt{2}}{4}\\)", "\\(\\frac{\\sqrt{3} - 1}{2}\\)", "\\(\\frac{\\sqrt{3} + 1}{2\\sqrt{2}}\\)"],
            "\\(\\cos(45^\\circ + 30^\\circ) = \\cos 45^\\circ\\cos 30^\\circ - \\sin 45^\\circ\\sin 30^\\circ = \\frac{\\sqrt{2}}{2}\\frac{\\sqrt{3}}{2} - \\frac{\\sqrt{2}}{2}\\frac{1}{2} = \\frac{\\sqrt{6} - \\sqrt{2}}{4}\\).",
        ),
        (
            "If \\(\\log_2 x + \\log_4 x = 6\\), find the value of \\(x\\).",
            "\\(16\\)",
            ["\\(8\\)", "\\(32\\)", "\\(64\\)"],
            "Using change of base \\(\\log_4 x = \\frac{1}{2}\\log_2 x\\), we have \\(\\frac{3}{2}\\log_2 x = 6 \\Rightarrow \\log_2 x = 4 \\Rightarrow x = 2^4 = 16\\).",
        ),
        (
            "Solve the exponential equation \\(3^{2x} - 10(3^x) + 9 = 0\\).",
            "\\(x = 0 \\text{ or } x = 2\\)",
            ["\\(x = 1 \\text{ or } x = 9\\)", "\\(x = 0 \\text{ or } x = 3\\)", "\\(x = 1 \\text{ or } x = 2\\)"],
            "Let \\(u = 3^x\\): \\(u^2 - 10u + 9 = (u - 1)(u - 9) = 0 \\Rightarrow 3^x = 1\\) (\\(x = 0\\)) or \\(3^x = 9\\) (\\(x = 2\\)).",
        ),
        (
            "In the binomial expansion of \\((1 + kx)^6\\), the coefficient of \\(x^3\\) is \\(160\\). Find the real value of \\(k\\).",
            "\\(2\\)",
            ["\\(4\\)", "\\(8\\)", "\\(\\frac{8}{3}\\)"],
            "\\(\\binom{6}{3}k^3 = 20k^3 = 160 \\Rightarrow k^3 = 8 \\Rightarrow k = 2\\).",
        ),
        (
            "Find the sum of all integers between \\(100\\) and \\(400\\) (inclusive) that are divisible by \\(7\\).",
            "\\(10836\\)",
            ["\\(10584\\)", "\\(11025\\)", "\\(10437\\)"],
            "First multiple is \\(a = 105\\), last is \\(l = 399\\). Number of terms \\(n = (399 - 105)/7 + 1 = 43\\). Sum \\(S_{43} = \\frac{43}{2}(105 + 399) = 43 \\times 252 = 10836\\).",
        ),
        (
            "If \\(z = \\frac{1 + i}{1 - i}\\), evaluate \\(z^{2026}\\).",
            "\\(-1\\)",
            ["\\(1\\)", "\\(i\\)", "\\(-i\\)"],
            "First simplify \\(z = \\frac{(1+i)^2}{1+1} = \\frac{2i}{2} = i\\). Since \\(2026 = 4(506) + 2\\), \\(i^{2026} = i^2 = -1\\).",
        ),
        (
            "If \\(\\alpha\\) and \\(\\beta\\) are the roots of \\(x^2 + px + q = 0\\), express \\(\\frac{\\alpha}{\\beta} + \\frac{\\beta}{\\alpha}\\) in terms of \\(p\\) and \\(q\\).",
            "\\(\\frac{p^2 - 2q}{q}\\)",
            ["\\(\\frac{p^2 + 2q}{q}\\)", "\\(\\frac{p^2 - q}{q}\\)", "\\(\\frac{2q - p^2}{p}\\)"],
            "\\(\\frac{\\alpha^2 + \\beta^2}{\\alpha\\beta} = \\frac{(\\alpha+\\beta)^2 - 2\\alpha\\beta}{\\alpha\\beta} = \\frac{(-p)^2 - 2q}{q} = \\frac{p^2 - 2q}{q}\\).",
        ),
        (
            "Find the general solution of the trigonometric equation \\(\\cos\\theta = \\frac{1}{2}\\).",
            "\\(\\theta = 2n\\pi \\pm \\frac{\\pi}{3},\\; n \\in \\mathbb{Z}\\)",
            ["\\(\\theta = n\\pi + (-1)^n \\frac{\\pi}{3},\\; n \\in \\mathbb{Z}\\)", "\\(\\theta = n\\pi \\pm \\frac{\\pi}{3},\\; n \\in \\mathbb{Z}\\)", "\\(\\theta = 2n\\pi \\pm \\frac{\\pi}{6},\\; n \\in \\mathbb{Z}\\)"],
            "For \\(\\cos\\theta = \\cos\\alpha\\) with \\(\\alpha = \\pi/3\\), the general solution is \\(\\theta = 2n\\pi \\pm \\frac{\\pi}{3}\\).",
        ),
        (
            "Find the area of the minor segment cut off by a chord subtending an angle of \\(\\frac{\\pi}{3}\\) radians at the centre of a circle of radius \\(6\\text{ cm}\\).",
            "\\((6\\pi - 9\\sqrt{3})\\text{ cm}^2\\)",
            ["\\((6\\pi - 18)\\text{ cm}^2\\)", "\\((12\\pi - 9\\sqrt{3})\\text{ cm}^2\\)", "\\(6\\pi\\text{ cm}^2\\)"],
            "Area of segment \\(= \\frac{1}{2}r^2(\\theta - \\sin\\theta) = \\frac{1}{2}(36)\\left(\\frac{\\pi}{3} - \\frac{\\sqrt{3}}{2}\\right) = (6\\pi - 9\\sqrt{3})\\text{ cm}^2\\).",
        ),
        (
            "If \\(\\alpha\\) and \\(\\beta\\) are the roots of \\(x^2 - 3x + 5 = 0\\), form the quadratic equation whose roots are \\(\\alpha^2\\) and \\(\\beta^2\\).",
            "\\(x^2 + x + 25 = 0\\)",
            ["\\(x^2 - x + 25 = 0\\)", "\\(x^2 - 9x + 25 = 0\\)", "\\(x^2 + 11x + 25 = 0\\)"],
            "Here \\(\\alpha + \\beta = 3\\) and \\(\\alpha\\beta = 5\\). Then \\(\\alpha^2 + \\beta^2 = (\\alpha+\\beta)^2 - 2\\alpha\\beta = 9 - 10 = -1\\) and \\(\\alpha^2\\beta^2 = 25\\), giving \\(x^2 - (-1)x + 25 = x^2 + x + 25 = 0\\).",
        ),
        (
            "Find the coefficient of \\(x^4\\) in the expansion of \\((1 + x + x^2)(1 - x)^6\\).",
            "\\(10\\)",
            ["\\(15\\)", "\\(-5\\)", "\\(6\\)"],
            "In \\((1 - x)^6\\), the coefficients of \\(x^4, x^3, x^2\\) are \\(\\binom{6}{4} = 15\\), \\(-\\binom{6}{3} = -20\\), and \\(\\binom{6}{2} = 15\\). Multiplying by \\((1 + x + x^2)\\) gives \\(15 - 20 + 15 = 10\\).",
        ),
        (
            "Using De Moivre's theorem, express \\(\\cos(4\\theta)\\) purely in terms of powers of \\(\\cos\\theta\\).",
            "\\(8\\cos^4\\theta - 8\\cos^2\\theta + 1\\)",
            ["\\(4\\cos^4\\theta - 4\\cos^2\\theta + 1\\)", "\\(8\\cos^4\\theta - 4\\cos^2\\theta - 1\\)", "\\(8\\cos^4\\theta + 8\\cos^2\\theta - 1\\)"],
            "\\(\\cos(4\\theta) = 2\\cos^2(2\\theta) - 1 = 2(2\\cos^2\\theta - 1)^2 - 1 = 8\\cos^4\\theta - 8\\cos^2\\theta + 1\\).",
        ),
        (
            "Solve for \\(x\\) in the logarithmic equation \\(\\log_3(x - 1) + \\log_3(x + 1) = 1\\).",
            "\\(x = 2\\)",
            ["\\(x = \\pm 2\\)", "\\(x = \\sqrt{10}\\)", "\\(x = 4\\)"],
            "\\(\\log_3(x^2 - 1) = 1 \\Rightarrow x^2 - 1 = 3 \\Rightarrow x^2 = 4\\). Since \\(x - 1 > 0\\), only \\(x = 2\\) is valid.",
        ),
        (
            "What is the coefficient of \\(x^{-2}\\) in the binomial expansion of \\(\\left(x - \\frac{2}{x}\\right)^6\\)?",
            "\\(240\\)",
            ["\\(-240\\)", "\\(-160\\)", "\\(60\\)"],
            "General term \\(\\binom{6}{r}x^{6-r}(-2)^r x^{-r} = \\binom{6}{r}(-2)^r x^{6-2r}\\). Setting \\(6 - 2r = -2 \\Rightarrow r = 4\\), giving \\(\\binom{6}{4}(-2)^4 = 15 \\times 16 = 240\\).",
        ),
        (
            "If \\(\\sin A = \\frac{3}{5}\\) (with \\(A\\) obtuse, in Quadrant II) and \\(\\cos B = \\frac{12}{13}\\) (with \\(B\\) acute, in Quadrant I), find the exact value of \\(\\sin(A + B)\\).",
            "\\(\\frac{16}{65}\\)",
            ["\\(\\frac{56}{65}\\)", "\\(-\\frac{16}{65}\\)", "\\(-\\frac{56}{65}\\)"],
            "Since \\(A\\) is obtuse, \\(\\cos A = -4/5\\); since \\(B\\) is acute, \\(\\sin B = 5/13\\). Thus \\(\\sin(A+B) = \\sin A\\cos B + \\cos A\\sin B = \\frac{3}{5}\\frac{12}{13} + \\left(-\\frac{4}{5}\\right)\\frac{5}{13} = \\frac{36 - 20}{65} = \\frac{16}{65}\\).",
        ),
        (
            "In an Arithmetic Progression, the sum of the first \\(n\\) terms is \\(210\\) and the sum of the first \\((n - 1)\\) terms is \\(171\\). What is the \\(n\\text{-th}\\) term \\(T_n\\)?",
            "\\(39\\)",
            ["\\(31\\)", "\\(41\\)", "\\(29\\)"],
            "For any series, \\(T_n = S_n - S_{n-1} = 210 - 171 = 39\\).",
        ),
        (
            "If the roots of the quadratic equation \\(x^2 - px + q = 0\\) differ by \\(1\\), which relation holds between \\(p\\) and \\(q\\)?",
            "\\(p^2 - 4q = 1\\)",
            ["\\(p^2 + 4q = 1\\)", "\\(p = q + 1\\)", "\\(p^2 = 4q\\)"],
            "Since \\((\\alpha - \\beta)^2 = (\\alpha + \\beta)^2 - 4\\alpha\\beta\\), setting \\(|\\alpha - \\beta| = 1\\) gives \\(p^2 - 4q = 1\\).",
        ),
        (
            "Find the modulus \\(|z|\\) of the complex number \\(z = \\frac{(3 + 4i)(1 - i)}{2 + 2i}\\).",
            "\\(\\frac{5}{2}\\)",
            ["\\(5\\)", "\\(\\frac{5}{\\sqrt{2}}\\)", "\\(\\frac{25}{4}\\)"],
            "Using \\(|z_1 z_2 / z_3| = |z_1||z_2| / |z_3|\\): \\(|3+4i| = 5\\), \\(|1-i| = \\sqrt{2}\\), and \\(|2+2i| = 2\\sqrt{2}\\). Thus \\(|z| = \\frac{5\\sqrt{2}}{2\\sqrt{2}} = \\frac{5}{2}\\).",
        ),
        (
            "What is the principal argument \\(\\text{Arg}(z)\\) of the complex number \\(z = -\\sqrt{3} + i\\)?",
            "\\(\\frac{5\\pi}{6}\\)",
            ["\\(\\frac{\\pi}{6}\\)", "\\(-\\frac{5\\pi}{6}\\)", "\\(\\frac{2\\pi}{3}\\)"],
            "In Quadrant II (\\(x < 0, y > 0\\)), \\(\\tan\\alpha = |1 / (-\\sqrt{3})| = 1/\\sqrt{3} \\Rightarrow \\alpha = \\pi/6\\), so \\(\\theta = \\pi - \\pi/6 = 5\\pi/6\\).",
        ),
        (
            "Solve the equation \\(z^3 + 8 = 0\\) completely in the set of complex numbers.",
            "\\(z = -2,\\; 1 + i\\sqrt{3},\\; 1 - i\\sqrt{3}\\)",
            ["\\(z = -2,\\; -1 + i\\sqrt{3},\\; -1 - i\\sqrt{3}\\)", "\\(z = 2,\\; -1 + i\\sqrt{3},\\; -1 - i\\sqrt{3}\\)", "\\(z = -2,\\; 2i,\\; -2i\\)"],
            "Factoring \\(z^3 + 8 = (z + 2)(z^2 - 2z + 4) = 0\\) gives \\(z = -2\\) and \\(z = \\frac{2 \\pm \\sqrt{-12}}{2} = 1 \\pm i\\sqrt{3}\\).",
        ),
        (
            "Find the sum to infinity of the series \\(1 - \\frac{1}{3} + \\frac{1}{9} - \\frac{1}{27} + \\dots\\)",
            "\\(\\frac{3}{4}\\)",
            ["\\(\\frac{4}{3}\\)", "\\(\\frac{2}{3}\\)", "\\(\\frac{3}{2}\\)"],
            "This is a geometric series with \\(a = 1\\) and \\(r = -1/3\\). Thus \\(S_\\infty = \\frac{1}{1 - (-1/3)} = \\frac{1}{4/3} = \\frac{3}{4}\\).",
        ),
        (
            "If \\(A\\) and \\(B\\) are finite sets with \\(n(A) = 24, n(B) = 18,\\) and \\(n(A \\setminus B) = 15\\), find \\(n(A \\cup B)\\).",
            "\\(33\\)",
            ["\\(42\\)", "\\(27\\)", "\\(9\\)"],
            "Since \\(n(A \\cup B) = n(A \\setminus B) + n(B)\\), we have \\(n(A \\cup B) = 15 + 18 = 33\\).",
        ),
        (
            "Evaluate the exact value of \\(\\tan(15^\\circ)\\).",
            "\\(2 - \\sqrt{3}\\)",
            ["\\(2 + \\sqrt{3}\\)", "\\(\\sqrt{3} - 1\\)", "\\(\\frac{\\sqrt{3} - 1}{2}\\)"],
            "\\(\\tan(45^\\circ - 30^\\circ) = \\frac{1 - 1/\\sqrt{3}}{1 + 1/\\sqrt{3}} = \\frac{\\sqrt{3} - 1}{\\sqrt{3} + 1} = \\frac{(\\sqrt{3}-1)^2}{2} = 2 - \\sqrt{3}\\).",
        ),
        (
            "If \\(f(x) = \\frac{2x + 1}{x - 3}\\) for \\(x \\ne 3\\), find the inverse function \\(f^{-1}(x)\\).",
            "\\(f^{-1}(x) = \\frac{3x + 1}{x - 2}\\) (\\(x \\ne 2\\))",
            ["\\(f^{-1}(x) = \\frac{x - 3}{2x + 1}\\)", "\\(f^{-1}(x) = \\frac{3x - 1}{x + 2}\\)", "\\(f^{-1}(x) = \\frac{2x - 1}{x + 3}\\)"],
            "Setting \\(y = \\frac{2x+1}{x-3} \\Rightarrow yx - 3y = 2x + 1 \\Rightarrow x(y - 2) = 3y + 1 \\Rightarrow x = \\frac{3y+1}{y-2}\\).",
        ),
        (
            "For what value of \\(c\\) is \\((x + 2)\\) a factor of the polynomial \\(P(x) = x^3 - 3x^2 + cx + 12\\)?",
            "\\(c = -4\\)",
            ["\\(c = 4\\)", "\\(c = -10\\)", "\\(c = 6\\)"],
            "By the Factor Theorem, \\(P(-2) = (-2)^3 - 3(-2)^2 + c(-2) + 12 = -8 - 12 - 2c + 12 = 0 \\Rightarrow -2c = 8 \\Rightarrow c = -4\\).",
        ),
        (
            "If \\(\\sin\\theta - \\cos\\theta = \\frac{1}{3}\\), find the value of \\(\\sin^3\\theta - \\cos^3\\theta\\).",
            "\\(\\frac{13}{27}\\)",
            ["\\(\\frac{1}{27}\\)", "\\(\\frac{11}{27}\\)", "\\(\\frac{19}{27}\\)"],
            "Squaring gives \\(1 - 2\\sin\\theta\\cos\\theta = 1/9 \\Rightarrow \\sin\\theta\\cos\\theta = 4/9\\). Then \\(\\sin^3\\theta - \\cos^3\\theta = (\\sin\\theta - \\cos\\theta)(1 + \\sin\\theta\\cos\\theta) = \\frac{1}{3}\\left(1 + \\frac{4}{9}\\right) = \\frac{13}{27}\\).",
        ),
        (
            "Find the sum of the first \\(n\\) odd natural numbers: \\(1 + 3 + 5 + \\dots + (2n - 1)\\).",
            "\\(n^2\\)",
            ["\\(n(n+1)\\)", "\\(2n^2 - 1\\)", "\\(\\frac{n(2n+1)}{2}\\)"],
            "Using \\(S_n = \\frac{n}{2}(a + l) = \\frac{n}{2}(1 + 2n - 1) = n^2\\).",
        ),
        (
            "What is the coefficient of \\(x^2\\) in the Maclaurin/binomial series expansion of \\((1 - 3x)^{-2}\\) for \\(|x| < 1/3\\)?",
            "\\(27\\)",
            ["\\(9\\)", "\\(18\\)", "\\(-27\\)"],
            "Using \\((1 - u)^{-2} = 1 + 2u + 3u^2 + 4u^3 + \\dots\\) with \\(u = 3x\\), the \\(x^2\\) term is \\(3(3x)^2 = 27x^2\\).",
        ),
        (
            "How many 4-digit numbers can be formed from the digits \\(\\{1, 2, 3, 4, 5, 6\\}\\) if NO digit may be repeated?",
            "\\(360\\)",
            ["\\(1296\\)", "\\(15\\)", "\\(720\\)"],
            "The number of permutations of 6 distinct digits taken 4 at a time is \\(^6P_4 = 6 \\times 5 \\times 4 \\times 3 = 360\\).",
        ),
        (
            "Simplify the trigonometric expression \\(\\frac{1 - \\cos(2\\theta)}{\\sin(2\\theta)}\\).",
            "\\(\\tan\\theta\\)",
            ["\\(\\cot\\theta\\)", "\\(\\tan(2\\theta)\\)", "\\(\\sin\\theta\\)"],
            "Using \\(1 - \\cos(2\\theta) = 2\\sin^2\\theta\\) and \\(\\sin(2\\theta) = 2\\sin\\theta\\cos\\theta\\), the ratio simplifies to \\(\\frac{2\\sin^2\\theta}{2\\sin\\theta\\cos\\theta} = \\tan\\theta\\).",
        ),
        (
            "If the complex number \\(z\\) satisfies \\(|z| = 1\\) and \\(z \\ne -1\\), then the complex number \\(\\frac{z - 1}{z + 1}\\) is always:",
            "Purely imaginary (its real part is zero)",
            ["Purely real", "Equal to \\(1\\)", "Of modulus \\(1\\)"],
            "Let \\(z = \\cos\\theta + i\\sin\\theta\\); then \\(\\frac{z-1}{z+1} = i\\tan(\\theta/2)\\), which is purely imaginary.",
        ),
        (
            "Find the set of real values of \\(x\\) for which \\(x^2 - 7x + 10 < 0\\).",
            "\\(2 < x < 5\\)",
            ["\\(x < 2 \\text{ or } x > 5\\)", "\\(-5 < x < -2\\)", "\\(2 \\le x \\le 5\\)"],
            "Factoring \\((x - 2)(x - 5) < 0\\) shows the product is negative strictly between the roots \\(2\\) and \\(5\\).",
        ),
        (
            "In a Geometric Progression, the product of the first three terms is \\(216\\), and their sum is \\(21\\). Find the three terms.",
            "\\(3,\\; 6,\\; 12\\)",
            ["\\(2,\\; 6,\\; 18\\)", "\\(4,\\; 6,\\; 9\\)", "\\(1,\\; 6,\\; 14\\)"],
            "Let the terms be \\(a/r, a, ar\\). Their product is \\(a^3 = 216 \\Rightarrow a = 6\\). Since \\(3 + 6 + 12 = 21\\) and \\(3 \\times 6 \\times 12 = 216\\), the terms are \\(3, 6, 12\\).",
        ),
        (
            "If \\(A = \\{x \\in \\mathbb{R} : x^2 - 4 = 0\\}\\) and \\(B = \\{x \\in \\mathbb{R} : x^2 - 5x + 6 = 0\\}\\), find the Cartesian product cardinality \\(n(A \\times B)\\) and \\(A \\cup B\\).",
            "\\(n(A \\times B) = 4,\\quad A \\cup B = \\{-2, 2, 3\\}\\)",
            ["\\(n(A \\times B) = 3,\\quad A \\cup B = \\{-2, 2, 3\\}\\)", "\\(n(A \\times B) = 4,\\quad A \\cup B = \\{2\\}\\)", "\\(n(A \\times B) = 2,\\quad A \\cup B = \\{-2, 3\\}\\)"],
            "\\(A = \\{-2, 2\\}\\) and \\(B = \\{2, 3\\}\\). Thus \\(n(A \\times B) = 2 \\times 2 = 4\\) and \\(A \\cup B = \\{-2, 2, 3\\}\\).",
        ),
    ]
    for q, corr, dists, exp in extra_mth:
        items.append(make_item(f"mth_{idx}", "MTH 101", q, corr, dists, exp, rng))
        idx += 1

    return items[:100]


def generate_hard_chm101(rng: random.Random) -> list[dict]:
    items = []
    idx = 101

    # 1. Hard Stoichiometry, Limiting Reactants, Yield & Gas Laws (15 questions)
    stoich_q = [
        (
            "In the Haber process \\(\\text{N}_2(g) + 3\\text{H}_2(g) \\rightarrow 2\\text{NH}_3(g)\\), if \\(56.0\\text{ g}\\) of \\(\\text{N}_2\\) (\\(M = 28\\text{ g/mol}\\)) is reacted with \\(9.0\\text{ g}\\) of \\(\\text{H}_2\\) (\\(M = 2.0\\text{ g/mol}\\)), which reactant is limiting and what is the theoretical yield of \\(\\text{NH}_3\\) (\\(M = 17.0\\text{ g/mol}\\))?",
            "\\(\\text{H}_2\\) is limiting; \\(51.0\\text{ g}\\) of \\(\\text{NH}_3\\)",
            ["\\(\\text{N}_2\\) is limiting; \\(68.0\\text{ g}\\) of \\(\\text{NH}_3\\)", "\\(\\text{H}_2\\) is limiting; \\(76.5\\text{ g}\\) of \\(\\text{NH}_3\\)", "\\(\\text{N}_2\\) is limiting; \\(51.0\\text{ g}\\) of \\(\\text{NH}_3\\)"],
            "Moles \\(\\text{N}_2 = 56/28 = 2.0\\text{ mol}\\); moles \\(\\text{H}_2 = 9.0/2.0 = 4.5\\text{ mol}\\). Since \\(2.0\\text{ mol N}_2\\) requires \\(6.0\\text{ mol H}_2\\), \\(\\text{H}_2\\) is limiting. Moles \\(\\text{NH}_3 = \\frac{2}{3}(4.5) = 3.0\\text{ mol} \\times 17.0 = 51.0\\text{ g}\\).",
        ),
        (
            "When \\(10.0\\text{ g}\\) of impure \\(\\text{CaCO}_3\\) (\\(M = 100\\text{ g/mol}\\)) reacts completely with excess \\(\\text{HCl}\\), \\(1.98\\text{ g}\\) of \\(\\text{CO}_2\\) (\\(M = 44.0\\text{ g/mol}\\)) is collected. What is the percentage purity of the \\(\\text{CaCO}_3\\) sample?",
            "\\(45.0\\%\\)",
            ["\\(19.8\\%\\)", "\\(90.0\\%\\)", "\\(55.0\\%\\)"],
            "Moles \\(\\text{CO}_2 = 1.98 / 44.0 = 0.045\\text{ mol}\\). By \\(1:1\\) stoichiometry, pure \\(\\text{CaCO}_3 = 0.045 \\times 100 = 4.50\\text{ g}\\), giving \\(45.0\\%\\) purity.",
        ),
        (
            "Complete combustion of a \\(3.00\\text{ g}\\) sample of an organic hydrocarbon produces \\(8.80\\text{ g}\\) of \\(\\text{CO}_2\\) (\\(M = 44\\text{ g/mol}\\)) and \\(5.40\\text{ g}\\) of \\(\\text{H}_2\\text{O}\\) (\\(M = 18\\text{ g/mol}\\)). What is the empirical formula of the hydrocarbon?",
            "\\(\\text{CH}_3\\)",
            ["\\(\\text{CH}_2\\)", "\\(\\text{C}_2\\text{H}_5\\)", "\\(\\text{CH}_4\\)"],
            "Moles of \\(\\text{C} = 8.80 / 44 = 0.20\\text{ mol}\\); moles of \\(\\text{H} = 2 \\times (5.40 / 18) = 0.60\\text{ mol}\\). Ratio \\(\\text{C}:\\text{H} = 0.20 : 0.60 = 1 : 3 \\Rightarrow \\text{CH}_3\\).",
        ),
        (
            "What volume of \\(0.250\\text{ M H}_2\\text{SO}_4\\) is required to completely neutralize \\(50.0\\text{ cm}^3\\) of \\(0.400\\text{ M NaOH}\\) according to \\(\\text{H}_2\\text{SO}_4 + 2\\text{NaOH} \\rightarrow \\text{Na}_2\\text{SO}_4 + 2\\text{H}_2\\text{O}\\)?",
            "\\(40.0\\text{ cm}^3\\)",
            ["\\(80.0\\text{ cm}^3\\)", "\\(20.0\\text{ cm}^3\\)", "\\(50.0\\text{ cm}^3\\)"],
            "Using \\(\\frac{C_A V_A}{C_B V_B} = \\frac{1}{2}\\): \\(V_A = \\frac{0.400 \\times 50.0}{2 \\times 0.250} = 40.0\\text{ cm}^3\\).",
        ),
        (
            "A student reacts \\(0.50\\text{ mol}\\) of salicylic acid with excess acetic anhydride (1:1 mole ratio) and obtains \\(72.0\\text{ g}\\) of aspirin (\\(M = 180.0\\text{ g/mol}\\)). What is the percent yield?",
            "\\(80.0\\%\\)",
            ["\\(90.0\\%\\)", "\\(72.0\\%\\)", "\\(60.0\\%\\)"],
            "Theoretical yield \\(= 0.50 \\times 180.0 = 90.0\\text{ g}\\). Percent yield \\(= (72.0 / 90.0) \\times 100\\% = 80.0\\%\\).",
        ),
        (
            "Element \\(X\\) has two naturally occurring isotopes: \\(^{63}X\\) (mass \\(63.0\\text{ u}\\)) and \\(^{65}X\\) (mass \\(65.0\\text{ u}\\)). If the relative atomic mass of \\(X\\) is \\(63.5\\), what is the percentage abundance of \\(^{63}X\\)?",
            "\\(75.0\\%\\)",
            ["\\(25.0\\%\\)", "\\(63.5\\%\\)", "\\(50.0\\%\\)"],
            "Let fraction of \\(^{63}X\\) be \\(f\\): \\(63f + 65(1 - f) = 63.5 \\Rightarrow 2f = 1.5 \\Rightarrow f = 0.75 = 75.0\\%\\).",
        ),
        (
            "How many chloride ions (\\(\\text{Cl}^-\\)) are present in \\(200\\text{ cm}^3\\) of a \\(0.15\\text{ M AlCl}_3\\) aqueous solution (Avogadro's constant \\(= N_A\\))?",
            "\\(0.090 N_A\\)",
            ["\\(0.030 N_A\\)", "\\(0.45 N_A\\)", "\\(0.010 N_A\\)"],
            "Moles of \\(\\text{AlCl}_3 = 0.15 \\times 0.200 = 0.030\\text{ mol}\\). Each unit yields \\(3\\text{ Cl}^-\\) ions, giving \\(3 \\times 0.030 N_A = 0.090 N_A\\).",
        ),
        (
            "According to the solubility rules in your CHM 101 notes, mixing aqueous solutions of which pair of salts will NOT produce a precipitate?",
            "\\(\\text{KNO}_3(aq) + \\text{Na}_2\\text{SO}_4(aq)\\)",
            ["\\(\\text{Pb(NO}_3)_2(aq) + 2\\text{KI}(aq)\\)", "\\(\\text{BaCl}_2(aq) + \\text{Na}_2\\text{SO}_4(aq)\\)", "\\(\\text{AgNO}_3(aq) + \\text{NaCl}(aq)\\)"],
            "All nitrates and all alkali metal (\\(\\text{Na}^+, \\text{K}^+\\)) salts are soluble in water, so \\(\\text{K}_2\\text{SO}_4\\) and \\(\\text{NaNO}_3\\) remain completely dissolved.",
        ),
        (
            "What is the net ionic equation for the reaction between aqueous barium chloride \\(\\text{BaCl}_2(aq)\\) and aqueous sodium sulfate \\(\\text{Na}_2\\text{SO}_4(aq)\\)?",
            "\\(\\text{Ba}^{2+}(aq) + \\text{SO}_4^{2-}(aq) \\rightarrow \\text{BaSO}_4(s)\\)",
            ["\\(\\text{Na}^+(aq) + \\text{Cl}^-(aq) \\rightarrow \\text{NaCl}(s)\\)", "\\(\\text{BaCl}_2(aq) + \\text{SO}_4^{2-}(aq) \\rightarrow \\text{BaSO}_4(s) + 2\\text{Cl}^-(aq)\\)", "\\(\\text{Ba}^{2+}(aq) + 2\\text{Cl}^-(aq) \\rightarrow \\text{BaCl}_2(s)\\)"],
            "\\(\\text{Na}^+\\) and \\(\\text{Cl}^-\\) are spectator ions; insoluble \\(\\text{BaSO}_4(s)\\) precipitates directly from \\(\\text{Ba}^{2+}(aq)\\) and \\(\\text{SO}_4^{2-}(aq)\\).",
        ),
        (
            "An unknown gas \\(X\\) effuses through a porous plug at half the rate of methane (\\(\\text{CH}_4,\\; M = 16.0\\text{ g/mol}\\)) under identical conditions. What is the molar mass of gas \\(X\\)?",
            "\\(64.0\\text{ g/mol}\\)",
            ["\\(32.0\\text{ g/mol}\\)", "\\(8.0\\text{ g/mol}\\)", "\\(48.0\\text{ g/mol}\\)"],
            "By Graham's Law, \\(\\frac{r_{\\text{CH}_4}}{r_X} = \\sqrt{\\frac{M_X}{16.0}} = 2 \\Rightarrow M_X = 16.0 \\times 4 = 64.0\\text{ g/mol}\\).",
        ),
    ]
    for q, corr, dists, exp in stoich_q:
        items.append(make_item(f"CHM101_{idx}", "CHM 101", q, corr, dists, exp, rng))
        idx += 1

    # 2. Hard Redox Balancing, Disproportionation & Oxidation States (15 questions)
    redox_q = [
        (
            "When the redox half-reaction \\(\\text{Cr}_2\\text{O}_7^{2-} \\rightarrow 2\\text{Cr}^{3+}\\) is balanced in an ACIDIC aqueous medium, how many \\(\\text{H}^+\\) ions and electrons (\\(e^-\\)) are added to the left-hand side?",
            "\\(14\\text{H}^+ \\text{ and } 6e^-\\)",
            ["\\(7\\text{H}^+ \\text{ and } 6e^-\\)", "\\(14\\text{H}^+ \\text{ and } 3e^-\\)", "\\(7\\text{H}^+ \\text{ and } 3e^-\\)"],
            "Balancing 7 oxygens with \\(7\\text{H}_2\\text{O}\\) on the right requires \\(14\\text{H}^+\\) on the left; each Cr goes from \\(+6\\) to \\(+3\\), requiring \\(2 \\times 3 = 6e^-\\).",
        ),
        (
            "In the balanced acidic redox equation \\(a\\text{MnO}_4^- + b\\text{Fe}^{2+} + c\\text{H}^+ \\rightarrow a\\text{Mn}^{2+} + b\\text{Fe}^{3+} + d\\text{H}_2\\text{O}\\), what are the smallest whole-number coefficients \\((a, b, c, d)\\)?",
            "\\((1, 5, 8, 4)\\)",
            ["\\((1, 5, 4, 2)\\)", "\\((2, 5, 16, 8)\\)", "\\((1, 3, 8, 4)\\)"],
            "\\(\\text{MnO}_4^-\\) gains \\(5e^-\\) (\\(+7 \\rightarrow +2\\)) while \\(\\text{Fe}^{2+}\\) loses \\(1e^-\\), giving \\(1\\text{MnO}_4^- + 5\\text{Fe}^{2+} + 8\\text{H}^+ \\rightarrow \\text{Mn}^{2+} + 5\\text{Fe}^{3+} + 4\\text{H}_2\\text{O}\\).",
        ),
        (
            "When chlorine gas reacts with hot concentrated alkali according to \\(3\\text{Cl}_2 + 6\\text{OH}^- \\rightarrow 5\\text{Cl}^- + \\text{ClO}_3^- + 3\\text{H}_2\\text{O}\\), how does the oxidation state of chlorine change?",
            "It disproportionates from \\(0\\) to \\(-1\\) (in \\(\\text{Cl}^-\\)) and \\(+5\\) (in \\(\\text{ClO}_3^-\\))",
            ["It is oxidized only from \\(0\\) to \\(+5\\)", "It disproportionates from \\(0\\) to \\(-1\\) and \\(+3\\)", "It disproportionates from \\(0\\) to \\(-1\\) and \\(+7\\)"],
            "In \\(\\text{Cl}_2\\) the oxidation number is \\(0\\); in \\(\\text{Cl}^-\\) it is \\(-1\\) (reduced), and in \\(\\text{ClO}_3^-\\) it is \\(+5\\) (oxidized).",
        ),
        (
            "What is the average oxidation number of sulfur in the tetrathionate ion \\(\\text{S}_4\\text{O}_6^{2-}\\) formed during iodometric titrations?",
            "\\(+2.5\\)",
            ["\\(+2.0\\)", "\\(+4.0\\)", "\\(+6.0\\)"],
            "Let the oxidation number of S be \\(x\\): \\(4x + 6(-2) = -2 \\Rightarrow 4x = +10 \\Rightarrow x = +2.5\\).",
        ),
        (
            "In the balanced acidic reaction \\(2\\text{MnO}_4^- + 5\\text{C}_2\\text{O}_4^{2-} + 16\\text{H}^+ \\rightarrow 2\\text{Mn}^{2+} + 10\\text{CO}_2 + 8\\text{H}_2\\text{O}\\), how many moles of electrons are transferred per mole of oxalate ion (\\(\\text{C}_2\\text{O}_4^{2-}\\)) oxidized?",
            "\\(2\\text{ mol } e^-\\)",
            ["\\(1\\text{ mol } e^-\\)", "\\(5\\text{ mol } e^-\\)", "\\(10\\text{ mol } e^-\\)"],
            "In \\(\\text{C}_2\\text{O}_4^{2-}\\), each carbon has oxidation state \\(+3\\) and is oxidized to \\(+4\\) in \\(\\text{CO}_2\\), losing \\(2e^-\\) per \\(\\text{C}_2\\text{O}_4^{2-}\\) ion.",
        ),
        (
            "What is the oxidation number of Chromium in potassium dichromate \\(\\text{K}_2\\text{Cr}_2\\text{O}_7\\) and in chromium(VI) peroxide \\(\\text{CrO}_5\\) (which contains two peroxide \\(-\\text{O}-\\text{O}-\\) linkages and one oxo \\(=\\text{O}\\) group)?",
            "\\(+6\\) in both compounds",
            ["\\(+6\\) in \\(\\text{K}_2\\text{Cr}_2\\text{O}_7\\) and \\(+10\\) in \\(\\text{CrO}_5\\)", "\\(+3\\) in \\(\\text{K}_2\\text{Cr}_2\\text{O}_7\\) and \\(+6\\) in \\(\\text{CrO}_5\\)", "\\(+6\\) in \\(\\text{K}_2\\text{Cr}_2\\text{O}_7\\) and \\(+5\\) in \\(\\text{CrO}_5\\)"],
            "In \\(\\text{CrO}_5\\), four peroxide oxygens have oxidation state \\(-1\\) and one oxide oxygen has \\(-2\\), so \\(\\text{Cr} + 4(-1) + (-2) = 0 \\Rightarrow \\text{Cr} = +6\\).",
        ),
        (
            "Which of the following reactions is NOT a redox reaction?",
            "\\(\\text{Cr}_2\\text{O}_7^{2-}(aq) + 2\\text{OH}^-(aq) \\rightarrow 2\\text{CrO}_4^{2-}(aq) + \\text{H}_2\\text{O}(l)\\)",
            ["\\(\\text{Zn}(s) + \\text{Cu}^{2+}(aq) \\rightarrow \\text{Zn}^{2+}(aq) + \\text{Cu}(s)\\)", "\\(\\text{Cl}_2(g) + 2\\text{Br}^-(aq) \\rightarrow 2\\text{Cl}^-(aq) + \\text{Br}_2(l)\\)", "\\(2\\text{H}_2\\text{O}_2(aq) \\rightarrow 2\\text{H}_2\\text{O}(l) + \\text{O}_2(g)\\)"],
            "In \\(\\text{Cr}_2\\text{O}_7^{2-} \\rightarrow 2\\text{CrO}_4^{2-}\\), chromium remains at \\(+6\\), oxygen at \\(-2\\), and hydrogen at \\(+1\\); no electron transfer occurs.",
        ),
        (
            "What volume of \\(0.020\\text{ M KMnO}_4\\) in acidic solution is required to completely oxidize \\(25.0\\text{ cm}^3\\) of \\(0.100\\text{ M FeSO}_4\\)?",
            "\\(25.0\\text{ cm}^3\\)",
            ["\\(5.0\\text{ cm}^3\\)", "\\(12.5\\text{ cm}^3\\)", "\\(50.0\\text{ cm}^3\\)"],
            "Moles \\(\\text{Fe}^{2+} = 0.100 \\times 25.0\\text{ mmol} = 2.50\\text{ mmol}\\). Since \\(\\text{MnO}_4^- : \\text{Fe}^{2+} = 1 : 5\\), we need \\(0.50\\text{ mmol MnO}_4^-\\), so \\(V = 0.50 / 0.020 = 25.0\\text{ cm}^3\\).",
        ),
        (
            "What is the oxidation number of phosphorus in sodium dihydrogen hypophosphite \\(\\text{NaH}_2\\text{PO}_2\\)?",
            "\\(+1\\)",
            ["\\(+3\\)", "\\(+5\\)", "\\(-3\\)"],
            "\\((+1) + 2(+1) + \\text{P} + 2(-2) = 0 \\Rightarrow 3 + \\text{P} - 4 = 0 \\Rightarrow \\text{P} = +1\\).",
        ),
        (
            "In a basic medium, how do you balance an excess of \\(n\\) oxygen atoms on one side of a half-reaction?",
            "Add \\(n\\text{H}_2\\text{O}\\) to the side with excess oxygen and \\(2n\\text{OH}^-\\) to the opposite side",
            ["Add \\(n\\text{OH}^-\\) to the side with excess oxygen and \\(n\\text{H}^+\\) to the opposite side", "Add \\(2n\\text{H}_2\\text{O}\\) to the side with excess oxygen", "Add \\(n\\text{O}_2\\) to the opposite side"],
            "In alkaline solution, each excess O atom combines with \\(\\text{H}_2\\text{O}\\) on the same side to form \\(2\\text{OH}^-\\) on the opposite side.",
        ),
    ]
    for q, corr, dists, exp in redox_q:
        items.append(make_item(f"CHM101_{idx}", "CHM 101", q, corr, dists, exp, rng))
        idx += 1

    # 3. Hard Chemical Equilibrium (Kp, Kc, ICE Tables, Le Chatelier, Van't Hoff) (20 questions)
    eq_q = [
        (
            "For the gaseous equilibrium \\(\\text{N}_2(g) + 3\\text{H}_2(g) \\rightleftharpoons 2\\text{NH}_3(g)\\), what is the value of \\(\\Delta n\\) and the relationship between \\(K_p\\) and \\(K_c\\)?",
            "\\(\\Delta n = -2;\\quad K_p = K_c(RT)^{-2}\\)",
            ["\\(\\Delta n = +2;\\quad K_p = K_c(RT)^2\\)", "\\(\\Delta n = -2;\\quad K_p = K_c(RT)^2\\)", "\\(\\Delta n = 0;\\quad K_p = K_c\\)"],
            "\\(\\Delta n = n_{\\text{products}(g)} - n_{\\text{reactants}(g)} = 2 - (1 + 3) = -2\\). Thus \\(K_p = K_c(RT)^{\\Delta n} = K_c(RT)^{-2}\\).",
        ),
        (
            "For which of the following heterogeneous or homogeneous equilibria is \\(K_p\\) numerically equal to \\(K_c\\) at any temperature \\(T\\)?",
            "\\(\\text{H}_2(g) + \\text{I}_2(g) \\rightleftharpoons 2\\text{HI}(g)\\)",
            ["\\(\\text{PCl}_5(g) \\rightleftharpoons \\text{PCl}_3(g) + \\text{Cl}_2(g)\\)", "\\(\\text{CaCO}_3(s) \\rightleftharpoons \\text{CaO}(s) + \\text{CO}_2(g)\\)", "\\(2\\text{SO}_2(g) + \\text{O}_2(g) \\rightleftharpoons 2\\text{SO}_3(g)\\)"],
            "In \\(\\text{H}_2(g) + \\text{I}_2(g) \\rightleftharpoons 2\\text{HI}(g)\\), \\(\\Delta n = 2 - (1 + 1) = 0\\), so \\(K_p = K_c(RT)^0 = K_c\\).",
        ),
        (
            "For the thermal decomposition \\(\\text{CaCO}_3(s) \\rightleftharpoons \\text{CaO}(s) + \\text{CO}_2(g)\\), what is the correct equilibrium constant expression \\(K_p\\)?",
            "\\(K_p = P_{\\text{CO}_2}\\)",
            ["\\(K_p = \\frac{P_{\\text{CaO}} P_{\\text{CO}_2}}{P_{\\text{CaCO}_3}}\\)", "\\(K_p = \\frac{1}{P_{\\text{CO}_2}}\\)", "\\(K_p = [\\text{CaO}][\\text{CO}_2]\\)"],
            "Pure solids (\\(\\text{CaCO}_3(s)\\) and \\(\\text{CaO}(s)\\)) have unit activity and do not appear in the equilibrium constant expression.",
        ),
        (
            "If the equilibrium constant for \\(\\text{A}(g) + 2\\text{B}(g) \\rightleftharpoons \\text{C}(g)\\) is \\(K_c = 4.0\\), what is the equilibrium constant \\(K_c'\\) for the reversed and doubled reaction \\(2\\text{C}(g) \\rightleftharpoons 2\\text{A}(g) + 4\\text{B}(g)\\)?",
            "\\(0.0625\\) (\\(1/16\\))",
            ["\\(0.25\\) (\\(1/4\\))", "\\(16.0\\)", "\\(-8.0\\)"],
            "Reversing the reaction inverts \\(K_c\\) to \\(1/K_c\\), and multiplying coefficients by 2 squares it: \\(K_c' = (1/4.0)^2 = 1/16 = 0.0625\\).",
        ),
        (
            "Initially, \\(1.0\\text{ mol}\\) of \\(\\text{H}_2\\) and \\(1.0\\text{ mol}\\) of \\(\\text{I}_2\\) are sealed in a \\(1.0\\text{ dm}^3\\) vessel at \\(450^\\circ\\text{C}\\). If \\(K_c = 49\\) for \\(\\text{H}_2(g) + \\text{I}_2(g) \\rightleftharpoons 2\\text{HI}(g)\\), what is the equilibrium concentration of \\(\\text{HI}\\)?",
            "\\(1.56\\text{ M}\\) (\\(14/9\\text{ M}\\))",
            ["\\(0.78\\text{ M}\\) (\\(7/9\\text{ M}\\))", "\\(1.40\\text{ M}\\)", "\\(0.22\\text{ M}\\)"],
            "From \\(\\frac{(2x)^2}{(1-x)^2} = 49 \\Rightarrow \\frac{2x}{1-x} = 7 \\Rightarrow 9x = 7 \\Rightarrow x = 7/9\\text{ M}\\). Thus \\([\\text{HI}] = 2x = 14/9 \\approx 1.56\\text{ M}\\).",
        ),
        (
            "A reaction has an equilibrium constant \\(K = 1.0 \\times 10^{10}\\) at \\(298\\text{ K}\\). Using the van't Hoff isotherm \\(\\Delta G^\\circ = -2.303 RT \\log_{10} K\\) with \\(2.303 RT \\approx 5.70\\text{ kJ/mol}\\) at \\(298\\text{ K}\\), calculate \\(\\Delta G^\\circ\\).",
            "\\(-57.0\\text{ kJ/mol}\\)",
            ["\\(+57.0\\text{ kJ/mol}\\)", "\\(-5.70\\text{ kJ/mol}\\)", "\\(-24.8\\text{ kJ/mol}\\)"],
            "\\(\\Delta G^\\circ = -2.303 RT \\log_{10}(10^{10}) = -5.70 \\times 10 = -57.0\\text{ kJ/mol}\\).",
        ),
        (
            "Consider the exothermic equilibrium \\(2\\text{SO}_2(g) + \\text{O}_2(g) \\rightleftharpoons 2\\text{SO}_3(g),\\; \\Delta H^\\circ = -198\\text{ kJ/mol}\\). Which set of conditions maximizes the equilibrium yield of \\(\\text{SO}_3\\)?",
            "Low temperature and high pressure",
            ["High temperature and high pressure", "Low temperature and low pressure", "High temperature and addition of V2O5 catalyst"],
            "Because the forward reaction is exothermic (\\(\\Delta H < 0\\)) and reduces gas moles (\\(3 \\rightarrow 2\\)), low temperature and high pressure favor \\(\\text{SO}_3\\).",
        ),
        (
            "At a given temperature, \\(\\text{PCl}_5(g) \\rightleftharpoons \\text{PCl}_3(g) + \\text{Cl}_2(g)\\) has \\(K_c = 0.040\\text{ M}\\). In a mixture where \\([\\text{PCl}_5] = 0.10\\text{ M}, [\\text{PCl}_3] = 0.20\\text{ M},\\) and \\([\\text{Cl}_2] = 0.10\\text{ M}\\), what is \\(Q_c\\) and which way does the reaction proceed?",
            "\\(Q_c = 0.20 > K_c\\); reaction shifts left toward \\(\\text{PCl}_5\\)",
            ["\\(Q_c = 0.20 > K_c\\); reaction shifts right toward products", "\\(Q_c = 0.02 < K_c\\); reaction shifts right", "\\(Q_c = 0.04 = K_c\\); system is at equilibrium"],
            "\\(Q_c = \\frac{(0.20)(0.10)}{0.10} = 0.20\\). Since \\(Q_c > K_c\\), the reverse reaction is favored (shifts left).",
        ),
        (
            "If an inert gas (such as Argon) is added at CONSTANT VOLUME to the equilibrium \\(\\text{N}_2(g) + 3\\text{H}_2(g) \\rightleftharpoons 2\\text{NH}_3(g)\\), what happens to the equilibrium position?",
            "The equilibrium position remains unchanged because all partial pressures and molar concentrations stay constant",
            ["It shifts to the right toward fewer gas moles", "It shifts to the left toward more gas moles", "The value of \\(K_c\\) increases"],
            "At constant volume, adding an inert gas does not change the molar concentration \\(n_i / V\\) or partial pressure of any reacting gas, so \\(Q\\) remains equal to \\(K\\).",
        ),
        (
            "For a gaseous reaction \\(\\text{A}_2(g) \\rightleftharpoons 2\\text{A}(g)\\), if the degree of dissociation of \\(\\text{A}_2\\) is \\(\\alpha\\) starting from \\(1\\text{ mol}\\) at total equilibrium pressure \\(P\\), how many total moles of gas are present at equilibrium?",
            "\\(1 + \\alpha\\)",
            ["\\(1 - \\alpha\\)", "\\(1 + 2\\alpha\\)", "\\(2\\alpha\\)"],
            "At equilibrium: moles of \\(\\text{A}_2 = 1 - \\alpha\\) and moles of \\(\\text{A} = 2\\alpha\\), giving total moles \\((1 - \\alpha) + 2\\alpha = 1 + \\alpha\\).",
        ),
    ]
    for q, corr, dists, exp in eq_q:
        items.append(make_item(f"CHM101_{idx}", "CHM 101", q, corr, dists, exp, rng))
        idx += 1

    # 4. Hard Acids, Bases, Ostwald Dilution, Buffers & Solubility Product Ksp (20 questions)
    ab_q = [
        (
            "According to the Ostwald Dilution Law \\(\\alpha = \\sqrt{K_a V} = \\sqrt{K_a / C}\\), what is the degree of dissociation \\(\\alpha\\) and \\([\\text{H}^+]\\) of a \\(0.10\\text{ M}\\) weak monoprotic acid with \\(K_a = 1.6 \\times 10^{-5}\\)?",
            "\\(\\alpha = 1.26 \\times 10^{-2}\\; (1.26\\%),\\quad [\\text{H}^+] = 1.26 \\times 10^{-3}\\text{ M}\\)",
            ["\\(\\alpha = 1.6 \\times 10^{-4},\\quad [\\text{H}^+] = 1.6 \\times 10^{-5}\\text{ M}\\)", "\\(\\alpha = 4.0 \\times 10^{-3},\\quad [\\text{H}^+] = 4.0 \\times 10^{-4}\\text{ M}\\)", "\\(\\alpha = 1.26 \\times 10^{-3},\\quad [\\text{H}^+] = 1.26 \\times 10^{-2}\\text{ M}\\)"],
            "\\(\\alpha = \\sqrt{1.6 \\times 10^{-5} / 0.10} = \\sqrt{1.6 \\times 10^{-4}} = 1.26 \\times 10^{-2}\\), and \\([\\text{H}^+] = C\\alpha = 0.10(1.26 \\times 10^{-2}) = 1.26 \\times 10^{-3}\\text{ M}\\).",
        ),
        (
            "Calculate the pH of a \\(0.050\\text{ M Ba(OH)}_2\\) aqueous solution at \\(298\\text{ K}\\), assuming complete dissociation.",
            "\\(13.00\\)",
            ["\\(12.70\\)", "\\(1.00\\)", "\\(13.30\\)"],
            "Each \\(\\text{Ba(OH)}_2\\) yields \\(2\\text{ OH}^-\\) ions, so \\([\\text{OH}^-] = 2 \\times 0.050 = 0.10\\text{ M} = 10^{-1}\\text{ M}\\). Thus \\(\\text{pOH} = 1.00\\) and \\(\\text{pH} = 14.00 - 1.00 = 13.00\\).",
        ),
        (
            "An acidic buffer is prepared by mixing equal volumes of \\(0.20\\text{ M CH}_3\\text{COOH}\\) (\\(\\text{p}K_a = 4.74\\)) and \\(0.60\\text{ M CH}_3\\text{COONa}\\). Given \\(\\log_{10}(3) = 0.48\\), what is the pH of the buffer?",
            "\\(5.22\\)",
            ["\\(4.26\\)", "\\(4.74\\)", "\\(5.74\\)"],
            "By the Henderson-Hasselbalch equation, \\(\\text{pH} = \\text{p}K_a + \\log_{10}\\left(\\frac{[\\text{salt}]}{[\\text{acid}]}\\right) = 4.74 + \\log_{10}(3) = 4.74 + 0.48 = 5.22\\).",
        ),
        (
            "At what ratio of \\(\\frac{[\\text{conjugate base}]}{[\\text{weak acid}]}\\) does an acidic buffer exhibit its maximum buffering capacity, and what is its pH at that point?",
            "Ratio \\(= 1 : 1\\), where \\(\\text{pH} = \\text{p}K_a\\)",
            ["Ratio \\(= 10 : 1\\), where \\(\\text{pH} = \\text{p}K_a + 1\\)", "Ratio \\(= 1 : 10\\), where \\(\\text{pH} = \\text{p}K_a - 1\\)", "Ratio \\(= 1 : 1\\), where \\(\\text{pH} = 7.00\\)"],
            "Maximum buffer capacity occurs when \\([\\text{A}^-] = [\\text{HA}]\\) (1:1 ratio), making \\(\\log_{10}(1) = 0\\) and \\(\\text{pH} = \\text{p}K_a\\).",
        ),
        (
            "For a sparingly soluble salt of formula \\(\\text{MX}_2(s) \\rightleftharpoons \\text{M}^{2+}(aq) + 2\\text{X}^-(aq)\\) (such as \\(\\text{PbCl}_2\\) or \\(\\text{CaF}_2\\)), if \\(s\\) is its molar solubility in pure water, what is the expression for \\(K_{sp}\\) in terms of \\(s\\)?",
            "\\(K_{sp} = 4s^3\\)",
            ["\\(K_{sp} = s^2\\)", "\\(K_{sp} = 2s^3\\)", "\\(K_{sp} = 27s^4\\)"],
            "At saturation, \\([\\text{M}^{2+}] = s\\) and \\([\\text{X}^-] = 2s\\). Therefore \\(K_{sp} = [\\text{M}^{2+}][\\text{X}^-]^2 = s(2s)^2 = 4s^3\\).",
        ),
        (
            "The solubility product of \\(\\text{AgCl}\\) at \\(298\\text{ K}\\) is \\(K_{sp} = 1.8 \\times 10^{-10}\\). What is the molar solubility of \\(\\text{AgCl}\\) in a \\(0.10\\text{ M NaCl}\\) solution?",
            "\\(1.8 \\times 10^{-9}\\text{ M}\\)",
            ["\\(1.34 \\times 10^{-5}\\text{ M}\\)", "\\(1.8 \\times 10^{-11}\\text{ M}\\)", "\\(1.8 \\times 10^{-10}\\text{ M}\\)"],
            "Due to the common ion \\([\\text{Cl}^-] \\approx 0.10\\text{ M}\\), \\(s(0.10) = 1.8 \\times 10^{-10} \\Rightarrow s = 1.8 \\times 10^{-9}\\text{ M}\\).",
        ),
        (
            "The solubility product of \\(\\text{CaF}_2\\) is \\(K_{sp} = 3.2 \\times 10^{-11}\\). Calculate its molar solubility \\(s\\) in pure water.",
            "\\(2.0 \\times 10^{-4}\\text{ M}\\)",
            ["\\(5.66 \\times 10^{-6}\\text{ M}\\)", "\\(4.0 \\times 10^{-4}\\text{ M}\\)", "\\(8.0 \\times 10^{-12}\\text{ M}\\)"],
            "Since \\(K_{sp} = 4s^3 = 3.2 \\times 10^{-11}\\), \\(s^3 = 8.0 \\times 10^{-12} \\Rightarrow s = 2.0 \\times 10^{-4}\\text{ M}\\).",
        ),
        (
            "In the reaction \\(\\text{BF}_3 + \\text{:NH}_3 \\rightarrow \\text{F}_3\\text{B}-\\text{NH}_3\\), how does \\(\\text{BF}_3\\) act and why?",
            "As a Lewis acid, because Boron has an incomplete octet (vacant 2p orbital) and accepts a lone pair of electrons",
            ["As a Brønsted-Lowry acid, because it donates a proton", "As a Lewis base, because Fluorine donates lone pairs", "As an Arrhenius acid, because it releases \\(\\text{H}^+\\) in water"],
            "Boron in \\(\\text{BF}_3\\) has only 6 valence electrons and an empty 2p orbital, making it a classic electron-pair acceptor (Lewis acid).",
        ),
        (
            "Which of the following species is NOT amphiprotic (cannot act as both a Brønsted-Lowry acid and base)?",
            "\\(\\text{SO}_4^{2-}\\)",
            ["\\(\\text{HCO}_3^-\\)", "\\(\\text{HSO}_4^-\\)", "\\(\\text{H}_2\\text{PO}_4^-\\)"],
            "\\(\\text{SO}_4^{2-}\\) has no ionizable hydrogen atom (proton) to donate, so it can only act as a Brønsted-Lowry base.",
        ),
        (
            "Rank the oxoacids of chlorine \\(\\text{HClO}, \\text{HClO}_2, \\text{HClO}_3, \\text{HClO}_4\\) in order of INCREASING acid strength.",
            "\\(\\text{HClO} < \\text{HClO}_2 < \\text{HClO}_3 < \\text{HClO}_4\\)",
            ["\\(\\text{HClO}_4 < \\text{HClO}_3 < \\text{HClO}_2 < \\text{HClO}\\)", "\\(\\text{HClO}_2 < \\text{HClO} < \\text{HClO}_3 < \\text{HClO}_4\\)", "All four have identical acid strength"],
            "As the number of electronegative terminal oxygen atoms increases, electron density is withdrawn from the O-H bond and the conjugate base is stabilized by resonance, making \\(\\text{HClO}_4\\) the strongest.",
        ),
    ]
    for q, corr, dists, exp in ab_q:
        items.append(make_item(f"CHM101_{idx}", "CHM 101", q, corr, dists, exp, rng))
        idx += 1

    # 5. Hard Electrochemistry, Quantum Numbers, Atomic Structure & Chemical Kinetics (30 questions)
    kin_elec_q = [
        (
            "For the Daniell cell \\(\\text{Zn}(s)\\,|\\,\\text{Zn}^{2+}(1\\text{ M})\\,||\\,\\text{Cu}^{2+}(1\\text{ M})\\,|\\,\\text{Cu}(s)\\), given \\(E^\\circ(\\text{Zn}^{2+}/\\text{Zn}) = -0.76\\text{ V}\\) and \\(E^\\circ(\\text{Cu}^{2+}/\\text{Cu}) = +0.34\\text{ V}\\), calculate \\(E^\\circ_{\\text{cell}}\\) and \\(\\Delta G^\\circ\\) (\\(F = 96,500\\text{ C/mol}\\)).",
            "\\(E^\\circ_{\\text{cell}} = +1.10\\text{ V},\\quad \\Delta G^\\circ = -212.3\\text{ kJ/mol}\\)",
            ["\\(E^\\circ_{\\text{cell}} = -0.42\\text{ V},\\quad \\Delta G^\\circ = +81.1\\text{ kJ/mol}\\)", "\\(E^\\circ_{\\text{cell}} = +1.10\\text{ V},\\quad \\Delta G^\\circ = -106.2\\text{ kJ/mol}\\)", "\\(E^\\circ_{\\text{cell}} = +0.42\\text{ V},\\quad \\Delta G^\\circ = -81.1\\text{ kJ/mol}\\)"],
            "\\(E^\\circ_{\\text{cell}} = E^\\circ_{\\text{cathode}} - E^\\circ_{\\text{anode}} = 0.34 - (-0.76) = +1.10\\text{ V}\\). With \\(n = 2\\), \\(\\Delta G^\\circ = -nFE^\\circ_{\\text{cell}} = -2(96,500)(1.10) = -212,300\\text{ J/mol} = -212.3\\text{ kJ/mol}\\).",
        ),
        (
            "A galvanic cell has \\(E^\\circ_{\\text{cell}} = 0.296\\text{ V}\\) for a \\(2\\)-electron redox process at \\(298\\text{ K}\\). Using \\(E^\\circ_{\\text{cell}} = \\frac{0.0592}{n}\\log_{10} K\\), what is the equilibrium constant \\(K\\)?",
            "\\(1.0 \\times 10^{10}\\)",
            ["\\(1.0 \\times 10^5\\)", "\\(10.0\\)", "\\(1.0 \\times 10^{20}\\)"],
            "\\(\\log_{10} K = \\frac{n E^\\circ_{\\text{cell}}}{0.0592} = \\frac{2 \\times 0.296}{0.0592} = 10 \\Rightarrow K = 1.0 \\times 10^{10}\\).",
        ),
        (
            "Using the Nernst equation at \\(298\\text{ K}\\), find the cell potential \\(E_{\\text{cell}}\\) of \\(\\text{Zn}(s)\\,|\\,\\text{Zn}^{2+}(0.010\\text{ M})\\,||\\,\\text{Cu}^{2+}(1.0\\text{ M})\\,|\\,\\text{Cu}(s)\\) given \\(E^\\circ_{\\text{cell}} = 1.100\\text{ V}\\).",
            "\\(1.159\\text{ V}\\)",
            ["\\(1.041\\text{ V}\\)", "\\(1.100\\text{ V}\\)", "\\(1.218\\text{ V}\\)"],
            "\\(E_{\\text{cell}} = E^\\circ_{\\text{cell}} - \\frac{0.0592}{2}\\log_{10}\\left(\\frac{[\\text{Zn}^{2+}]}{[\\text{Cu}^{2+}]}\\right) = 1.100 - 0.0296\\log_{10}(10^{-2}) = 1.100 + 0.0592 = 1.159\\text{ V}\\).",
        ),
        (
            "Which of the following sets of four quantum numbers \\((n, l, m_l, m_s)\\) is INVALID (impossible) for an electron in an atom?",
            "\\((3,\\; 3,\\; -1,\\; +\\frac{1}{2})\\)",
            ["\\((3,\\; 2,\\; -2,\\; +\\frac{1}{2})\\)", "\\((4,\\; 1,\\; 0,\\; -\\frac{1}{2})\\)", "\\((2,\\; 0,\\; 0,\\; +\\frac{1}{2})\\)"],
            "For a given principal quantum number \\(n\\), the azimuthal quantum number \\(l\\) can only take values \\(0, 1, \\dots, n-1\\). Thus \\(l = 3\\) is impossible when \\(n = 3\\).",
        ),
        (
            "What is the maximum number of orbitals and the maximum number of electrons that can exist in the \\(n = 4\\) principal shell of an atom?",
            "\\(16\\text{ orbitals and } 32\\text{ electrons}\\)",
            ["\\(8\\text{ orbitals and } 16\\text{ electrons}\\)", "\\(9\\text{ orbitals and } 18\\text{ electrons}\\)", "\\(4\\text{ orbitals and } 8\\text{ electrons}\\)"],
            "A principal shell \\(n\\) contains \\(n^2 = 4^2 = 16\\) orbitals (one 4s, three 4p, five 4d, seven 4f) and holds up to \\(2n^2 = 32\\) electrons.",
        ),
        (
            "How many unpaired electrons are present in a ground-state gaseous \\(\\text{Fe}^{3+}\\) ion (\\(Z = 26\\))?",
            "\\(5\\)",
            ["\\(4\\)", "\\(3\\)", "\\(2\\)"],
            "Neutral Fe (\\(Z=26\\)) is \\([\\text{Ar}]3d^6 4s^2\\). Removing two \\(4s\\) electrons and one \\(3d\\) electron gives \\(\\text{Fe}^{3+} = [\\text{Ar}]3d^5\\), which by Hund's rule has 5 unpaired electrons.",
        ),
        (
            "According to the \\((n + l)\\) Aufbau energy ordering rule, which subshell is filled immediately AFTER the \\(4s\\) subshell?",
            "\\(3d\\)",
            ["\\(4p\\)", "\\(4d\\)", "\\(3p\\)"],
            "For \\(4s\\), \\(n+l = 4+0 = 4\\); for \\(3d\\), \\(n+l = 3+2 = 5\\); for \\(4p\\), \\(n+l = 4+1 = 5\\) (higher \\(n\\)). Thus \\(3d\\) fills immediately after \\(4s\\).",
        ),
        (
            "For a chemical reaction \\(A \\rightarrow \\text{Products}\\) of overall order \\(n\\), what are the SI/molar units of the rate constant \\(k\\)?",
            "\\(\\text{mol}^{1-n}\\,\\text{dm}^{3(n-1)}\\,\\text{s}^{-1}\\) (i.e., \\(\\text{M}^{1-n}\\,\\text{s}^{-1}\\))",
            ["\\(\\text{mol}^n\\,\\text{dm}^{-3n}\\,\\text{s}^{-1}\\)", "\\(\\text{mol}^{n-1}\\,\\text{dm}^{3(1-n)}\\,\\text{s}^{-1}\\)", "\\(\\text{s}^{-1}\\) for all orders \\(n\\)"],
            "Since \\(\\text{Rate} = k[A]^n\\) has units \\(\\text{M}\\,\\text{s}^{-1}\\), \\([k] = \\text{M}\\,\\text{s}^{-1} / \\text{M}^n = \\text{M}^{1-n}\\,\\text{s}^{-1} = \\text{mol}^{1-n}\\,\\text{dm}^{3(n-1)}\\,\\text{s}^{-1}\\).",
        ),
        (
            "A first-order reaction has a rate constant \\(k_1 = 6.93 \\times 10^{-3}\\text{ s}^{-1}\\). How long will it take for the reactant concentration to decrease from \\(0.80\\text{ M}\\) to \\(0.10\\text{ M}\\)?",
            "\\(300\\text{ s}\\)",
            ["\\(100\\text{ s}\\)", "\\(200\\text{ s}\\)", "\\(400\\text{ s}\\)"],
            "Half-life \\(t_{1/2} = 0.693 / k_1 = 100\\text{ s}\\). Going from \\(0.80\\text{ M} \\rightarrow 0.40\\text{ M} \\rightarrow 0.20\\text{ M} \\rightarrow 0.10\\text{ M}\\) requires exactly 3 half-lives: \\(3 \\times 100 = 300\\text{ s}\\).",
        ),
        (
            "For a second-order reaction \\(2A \\rightarrow P\\) with rate constant \\(k_2 = 0.50\\text{ M}^{-1}\\text{s}^{-1}\\) and initial concentration \\([A]_0 = 0.20\\text{ M}\\), what is the first half-life \\(t_{1/2}\\)?",
            "\\(10\\text{ s}\\)",
            ["\\(1.39\\text{ s}\\)", "\\(0.10\\text{ s}\\)", "\\(20\\text{ s}\\)"],
            "For a second-order reaction, \\(t_{1/2} = \\frac{1}{k_2[A]_0} = \\frac{1}{0.50 \\times 0.20} = 10\\text{ s}\\).",
        ),
        (
            "In an initial-rates experiment for \\(2\\text{NO}(g) + \\text{Cl}_2(g) \\rightarrow 2\\text{NOCl}(g)\\), doubling \\([\\text{Cl}_2]\\) at constant \\([\\text{NO}]\\) doubles the initial rate, while doubling both \\([\\text{NO}]\\) and \\([\\text{Cl}_2]\\) increases the initial rate by a factor of \\(8\\). What is the rate law?",
            "\\(\\text{Rate} = k[\\text{NO}]^2[\\text{Cl}_2]\\)",
            ["\\(\\text{Rate} = k[\\text{NO}][\\text{Cl}_2]^2\\)", "\\(\\text{Rate} = k[\\text{NO}]^2[\\text{Cl}_2]^2\\)", "\\(\\text{Rate} = k[\\text{NO}][\\text{Cl}_2]\\)"],
            "Order with respect to \\(\\text{Cl}_2\\) is \\(1\\). Since \\(2^m \\cdot 2^1 = 8 \\Rightarrow 2^m = 4 \\Rightarrow m = 2\\), the reaction is 2nd order in \\(\\text{NO}\\) and 1st order in \\(\\text{Cl}_2\\).",
        ),
        (
            "The rate constant of a reaction doubles when the temperature is raised from \\(300\\text{ K}\\) to \\(310\\text{ K}\\). Using the Arrhenius equation \\(\\ln(k_2/k_1) = \\frac{E_a}{R}\\left(\\frac{T_2 - T_1}{T_1 T_2}\\right)\\), which expression gives the activation energy \\(E_a\\)?",
            "\\(E_a = \\frac{300 \\times 310 \\times R \\ln 2}{10}\\)",
            ["\\(E_a = \\frac{10 R \\ln 2}{300 \\times 310}\\)", "\\(E_a = 10 R \\ln 2\\)", "\\(E_a = \\frac{300 \\times 310 \\times R}{20}\\)"],
            "Rearranging \\(\\ln 2 = \\frac{E_a}{R}\\left(\\frac{310 - 300}{300 \\times 310}\\right)\\) gives \\(E_a = \\frac{300 \\times 310 \\times R \\ln 2}{10}\\).",
        ),
        (
            "A reaction mechanism consists of two steps: Step 1 (fast equilibrium): \\(2\\text{NO} \\rightleftharpoons \\text{N}_2\\text{O}_2\\); Step 2 (slow): \\(\\text{N}_2\\text{O}_2 + \\text{H}_2 \\rightarrow \\text{N}_2\\text{O} + \\text{H}_2\\text{O}\\). What is the role of \\(\\text{N}_2\\text{O}_2\\) and the overall rate law?",
            "\\(\\text{N}_2\\text{O}_2\\) is a reaction intermediate; \\(\\text{Rate} = k[\\text{NO}]^2[\\text{H}_2]\\)",
            ["\\(\\text{N}_2\\text{O}_2\\) is a catalyst; \\(\\text{Rate} = k[\\text{N}_2\\text{O}_2][\\text{H}_2]\\)", "\\(\\text{N}_2\\text{O}_2\\) is an intermediate; \\(\\text{Rate} = k[\\text{NO}][\\text{H}_2]\\)", "\\(\\text{N}_2\\text{O}_2\\) is a transition state; \\(\\text{Rate} = k[\\text{NO}]^2\\)"],
            "\\(\\text{N}_2\\text{O}_2\\) is formed in Step 1 and consumed in Step 2 (intermediate). From the slow step, \\(\\text{Rate} = k_2[\\text{N}_2\\text{O}_2][\\text{H}_2] = k_2 K_1[\\text{NO}]^2[\\text{H}_2]\\).",
        ),
        (
            "For a zero-order reaction \\(A \\rightarrow P\\) with initial concentration \\([A]_0\\) and rate constant \\(k_0\\), what is the half-life \\(t_{1/2}\\) and the time required for \\(100\\%\\) completion?",
            "\\(t_{1/2} = \\frac{[A]_0}{2k_0},\\quad t_{100\\%} = \\frac{[A]_0}{k_0}\\)",
            ["\\(t_{1/2} = \\frac{0.693}{k_0},\\quad t_{100\\%} = \\infty\\)", "\\(t_{1/2} = \\frac{1}{k_0[A]_0},\\quad t_{100\\%} = \\frac{2}{k_0[A]_0}\\)", "\\(t_{1/2} = \\frac{[A]_0}{k_0},\\quad t_{100\\%} = \\frac{2[A]_0}{k_0}\\)"],
            "From \\([A] = [A]_0 - k_0 t\\), setting \\([A] = [A]_0/2\\) gives \\(t_{1/2} = [A]_0/(2k_0)\\), and setting \\([A] = 0\\) gives \\(t_{100\\%} = [A]_0/k_0\\).",
        ),
        (
            "In a plot of \\(\\frac{1}{[A]}\\) versus time \\(t\\) for a reaction \\(A \\rightarrow P\\), a straight line with positive slope \\(+k\\) and y-intercept \\(\\frac{1}{[A]_0}\\) is obtained. What is the order of the reaction with respect to \\(A\\)?",
            "Second order",
            ["First order", "Zero order", "Pseudo-first order"],
            "The integrated rate law \\(\\frac{1}{[A]} = k_2 t + \\frac{1}{[A]_0}\\) is linear in \\(1/[A]\\) vs \\(t\\) with slope \\(+k_2\\), which is diagnostic of a second-order reaction.",
        ),
    ]
    for q, corr, dists, exp in kin_elec_q:
        items.append(make_item(f"CHM101_{idx}", "CHM 101", q, corr, dists, exp, rng))
        idx += 1

    # 6. Additional Hard CHM 101 Calculations to complete 100 new CHM 101 questions (20 questions)
    extra_chm = [
        (
            "Calculate the pH of a \\(1.0 \\times 10^{-3}\\text{ M}\\) solution of a weak monoprotic acid \\(\\text{HA}\\) with \\(K_a = 1.0 \\times 10^{-5}\\) at \\(298\\text{ K}\\).",
            "\\(4.00\\)",
            ["\\(3.00\\)", "\\(5.00\\)", "\\(2.00\\)"],
            "\\([\\text{H}^+] = \\sqrt{K_a C} = \\sqrt{1.0 \\times 10^{-5} \\times 1.0 \\times 10^{-3}} = 1.0 \\times 10^{-4}\\text{ M} \\Rightarrow \\text{pH} = 4.00\\).",
        ),
        (
            "What is the conjugate acid and conjugate base of the dihydrogen phosphate ion \\(\\text{H}_2\\text{PO}_4^-\\)?",
            "Conjugate acid: \\(\\text{H}_3\\text{PO}_4\\); Conjugate base: \\(\\text{HPO}_4^{2-}\\)",
            ["Conjugate acid: \\(\\text{HPO}_4^{2-}\\); Conjugate base: \\(\\text{H}_3\\text{PO}_4\\)", "Conjugate acid: \\(\\text{H}_3\\text{PO}_4\\); Conjugate base: \\(\\text{PO}_4^{3-}\\)", "Conjugate acid: \\(\\text{HPO}_3\\); Conjugate base: \\(\\text{PO}_4^{3-}\\)"],
            "Adding one \\(\\text{H}^+\\) to \\(\\text{H}_2\\text{PO}_4^-\\) gives \\(\\text{H}_3\\text{PO}_4\\) (conjugate acid); removing one \\(\\text{H}^+\\) gives \\(\\text{HPO}_4^{2-}\\) (conjugate base).",
        ),
        (
            "An element has atomic number \\(Z = 29\\) and mass number \\(A = 63\\). How many protons, neutrons, and electrons are present in its \\(\\text{Cu}^{2+}\\) cation?",
            "\\(29\\text{ protons},\\; 34\\text{ neutrons},\\; 27\\text{ electrons}\\)",
            ["\\(29\\text{ protons},\\; 34\\text{ neutrons},\\; 29\\text{ electrons}\\)", "\\(27\\text{ protons},\\; 36\\text{ neutrons},\\; 29\\text{ electrons}\\)", "\\(29\\text{ protons},\\; 63\\text{ neutrons},\\; 27\\text{ electrons}\\)"],
            "Protons \\(= Z = 29\\); neutrons \\(= A - Z = 63 - 29 = 34\\); in a \\(+2\\) cation, electrons \\(= 29 - 2 = 27\\).",
        ),
        (
            "Which of the following pairs of species are ISOELECTRONIC (possess the exact same number of electrons)?",
            "\\(\\text{S}^{2-},\\; \\text{Cl}^-,\\; \\text{Ar},\\; \\text{K}^+,\\; \\text{Ca}^{2+}\\)",
            ["\\(\\text{Na}^+,\\; \\text{K}^+,\\; \\text{Rb}^+\\)", "\\(\\text{F}^-,\\; \\text{Cl}^-,\\; \\text{Br}^-\\)", "\\(\\text{Fe}^{2+},\\; \\text{Fe}^{3+}\\)" ],
            "Each species in \\(\\text{S}^{2-}(16+2), \\text{Cl}^-(17+1), \\text{Ar}(18), \\text{K}^+(19-1), \\text{Ca}^{2+}(20-2)\\) has exactly 18 electrons.",
        ),
        (
            "For a sparingly soluble 1:3 salt \\(\\text{Al(OH)}_3(s) \\rightleftharpoons \\text{Al}^{3+}(aq) + 3\\text{OH}^-(aq)\\), what is the relationship between its solubility product \\(K_{sp}\\) and molar solubility \\(s\\)?",
            "\\(K_{sp} = 27s^4\\)",
            ["\\(K_{sp} = 4s^3\\)", "\\(K_{sp} = 9s^4\\)", "\\(K_{sp} = 3s^4\\)"],
            "Since \\([\\text{Al}^{3+}] = s\\) and \\([\\text{OH}^-] = 3s\\), \\(K_{sp} = (s)(3s)^3 = 27s^4\\).",
        ),
        (
            "If \\(50.0\\text{ cm}^3\\) of \\(2.0 \\times 10^{-4}\\text{ M AgNO}_3\\) is mixed with \\(50.0\\text{ cm}^3\\) of \\(2.0 \\times 10^{-4}\\text{ M NaCl}\\) (\\(K_{sp}(\\text{AgCl}) = 1.8 \\times 10^{-10}\\)), what is the ionic product \\(Q_{sp}\\) immediately upon mixing, and does a precipitate form?",
            "\\(Q_{sp} = 1.0 \\times 10^{-8} > K_{sp}\\); a white precipitate of \\(\\text{AgCl}\\) forms",
            ["\\(Q_{sp} = 4.0 \\times 10^{-8} > K_{sp}\\); a precipitate forms", "\\(Q_{sp} = 1.0 \\times 10^{-10} < K_{sp}\\); no precipitate forms", "\\(Q_{sp} = 1.8 \\times 10^{-10} = K_{sp}\\); solution is just saturated"],
            "Equal volumes halve each concentration to \\(1.0 \\times 10^{-4}\\text{ M}\\). Thus \\(Q_{sp} = (10^{-4})(10^{-4}) = 1.0 \\times 10^{-8} > 1.8 \\times 10^{-10}\\), causing precipitation.",
        ),
        (
            "What is the oxidation state of Iron in potassium hexacyanoferrate(II), \\(\\text{K}_4[\\text{Fe(CN)}_6]\\), and potassium hexacyanoferrate(III), \\(\\text{K}_3[\\text{Fe(CN)}_6]\\)?",
            "\\(+2\\) and \\(+3\\) respectively",
            ["\\(+4\\) and \\(+3\\) respectively", "\\(+2\\) and \\(+6\\) respectively", "\\(0\\) in both complexes"],
            "Each \\(\\text{CN}^-\\) ligand has charge \\(-1\\) and each \\(\\text{K}^+\\) is \\(+1\\): \\(4(+1) + \\text{Fe} + 6(-1) = 0 \\Rightarrow \\text{Fe} = +2\\), and \\(3(+1) + \\text{Fe} + 6(-1) = 0 \\Rightarrow \\text{Fe} = +3\\).",
        ),
        (
            "In a concentration cell \\(\\text{Cu}(s)\\,|\\,\\text{Cu}^{2+}(0.001\\text{ M})\\,||\\,\\text{Cu}^{2+}(0.10\\text{ M})\\,|\\,\\text{Cu}(s)\\) at \\(298\\text{ K}\\), what is the standard cell potential \\(E^\\circ_{\\text{cell}}\\) and the actual electromotive force \\(E_{\\text{cell}}\\)?",
            "\\(E^\\circ_{\\text{cell}} = 0.00\\text{ V},\\quad E_{\\text{cell}} = +0.0592\\text{ V}\\)",
            ["\\(E^\\circ_{\\text{cell}} = +0.34\\text{ V},\\quad E_{\\text{cell}} = +0.399\\text{ V}\\)", "\\(E^\\circ_{\\text{cell}} = 0.00\\text{ V},\\quad E_{\\text{cell}} = +0.118\\text{ V}\\)", "\\(E^\\circ_{\\text{cell}} = 0.00\\text{ V},\\quad E_{\\text{cell}} = 0.00\\text{ V}\\)"],
            "For any concentration cell, \\(E^\\circ_{\\text{cell}} = 0\\). By the Nernst equation with \\(n = 2\\): \\(E_{\\text{cell}} = 0 - \\frac{0.0592}{2}\\log_{10}\\left(\\frac{0.001}{0.10}\\right) = +0.0592\\text{ V}\\).",
        ),
        (
            "A radioactive isotope decays by first-order kinetics such that \\(75\\%\\) of the sample decays in \\(40\\text{ minutes}\\). What is the half-life \\(t_{1/2}\\) of the isotope?",
            "\\(20\\text{ minutes}\\)",
            ["\\(10\\text{ minutes}\\)", "\\(30\\text{ minutes}\\)", "\\(15\\text{ minutes}\\)"],
            "If \\(75\\%\\) decays, \\(25\\% = (1/2)^2\\) remains, corresponding to 2 half-lives in \\(40\\text{ minutes}\\), so \\(t_{1/2} = 20\\text{ minutes}\\).",
        ),
        (
            "What is the pH of a basic buffer containing \\(0.10\\text{ M NH}_3\\) (\\(\\text{p}K_b = 4.74\\)) and \\(0.10\\text{ M NH}_4\\text{Cl}\\) at \\(298\\text{ K}\\)?",
            "\\(9.26\\)",
            ["\\(4.74\\)", "\\(8.74\\)", "\\(9.74\\)"],
            "Here \\(\\text{pOH} = \\text{p}K_b + \\log_{10}\\left(\\frac{[\\text{NH}_4^+]}{[\\text{NH}_3]}\\right) = 4.74 + \\log_{10}(1) = 4.74\\). Thus \\(\\text{pH} = 14.00 - 4.74 = 9.26\\).",
        ),
        (
            "How many nodal planes (angular nodes) and radial (spherical) nodes does a \\(3p\\) atomic orbital possess?",
            "\\(1\\text{ angular node and } 1\\text{ radial node}\\)",
            ["\\(1\\text{ angular node and } 2\\text{ radial nodes}\\)", "\\(2\\text{ angular nodes and } 0\\text{ radial nodes}\\)", "\\(0\\text{ angular nodes and } 2\\text{ radial nodes}\\)"],
            "An orbital has \\(l\\) angular nodes and \\((n - l - 1)\\) radial nodes. For \\(3p\\) (\\(n=3, l=1\\)), angular nodes \\(= 1\\) and radial nodes \\(= 3 - 1 - 1 = 1\\).",
        ),
        (
            "Which Law of Chemical Combination is illustrated by the fact that Carbon and Oxygen form both \\(\\text{CO}\\) (12 g C : 16 g O) and \\(\\text{CO}_2\\) (12 g C : 32 g O), where the masses of oxygen combining with a fixed mass of carbon are in the simple whole-number ratio \\(1 : 2\\)?",
            "Dalton's Law of Multiple Proportions",
            ["Proust's Law of Definite (Constant) Proportions", "Lavoisier's Law of Conservation of Mass", "Richter's Law of Reciprocal Proportions"],
            "The Law of Multiple Proportions states that when two elements form more than one compound, the masses of one element combining with a fixed mass of the other are in a ratio of small whole numbers.",
        ),
        (
            "Given the standard electrode potentials: \\(\\text{Ag}^+/\\text{Ag} = +0.80\\text{ V}\\), \\(\\text{Cu}^{2+}/\\text{Cu} = +0.34\\text{ V}\\), \\(\\text{Fe}^{2+}/\\text{Fe} = -0.44\\text{ V}\\), and \\(\\text{Mg}^{2+}/\\text{Mg} = -2.37\\text{ V}\\), which metal is the STRONGEST reducing agent?",
            "\\(\\text{Mg}(s)\\)",
            ["\\(\\text{Ag}(s)\\)", "\\(\\text{Fe}(s)\\)", "\\(\\text{Cu}(s)\\)"],
            "The species with the most negative standard reduction potential (\\(-2.37\\text{ V}\\)) is most easily oxidized and is therefore the strongest reducing agent.",
        ),
        (
            "For the reversible reaction \\(2\\text{NO}_2(g) \\rightleftharpoons \\text{N}_2\\text{O}_4(g)\\), as temperature is increased, the equilibrium constant \\(K_p\\) decreases. What does this tell you about the enthalpy change \\(\\Delta H^\\circ\\) of the forward dimerization reaction?",
            "\\(\\Delta H^\\circ < 0\\) (the forward reaction is exothermic)",
            ["\\(\\Delta H^\\circ > 0\\) (the forward reaction is endothermic)", "\\(\\Delta H^\\circ = 0\\) (thermoneutral)", "Activation energy of the forward reaction is negative"],
            "By the van't Hoff equation, \\(K\\) decreases with increasing \\(T\\) for an exothermic reaction (\\(\\Delta H^\\circ < 0\\)), consistent with bond formation in \\(\\text{N}-\\text{N}\\).",
        ),
        (
            "A solution is prepared by dissolving \\(4.90\\text{ g}\\) of pure \\(\\text{H}_2\\text{SO}_4\\) (\\(M = 98.0\\text{ g/mol}\\)) in water to form \\(500\\text{ cm}^3\\) of solution. Assuming complete diprotic dissociation, what is the \\(\\text{pH}\\) of the solution?",
            "\\(0.70\\)",
            ["\\(1.00\\)", "\\(1.30\\)", "\\(0.30\\)"],
            "Moles \\(\\text{H}_2\\text{SO}_4 = 4.90 / 98.0 = 0.050\\text{ mol}\\), so \\([\\text{H}_2\\text{SO}_4] = 0.050 / 0.500 = 0.10\\text{ M}\\). Then \\([\\text{H}^+] = 2 \\times 0.10 = 0.20\\text{ M}\\), and \\(\\text{pH} = -\\log_{10}(0.20) = 0.70\\).",
        ),
        (
            "In a redox titration in basic solution, \\(\\text{MnO}_4^-\\) is reduced to solid manganese(IV) oxide \\(\\text{MnO}_2(s)\\). How many moles of electrons are gained per mole of \\(\\text{MnO}_4^-\\)?",
            "\\(3\\text{ mol } e^-\\)",
            ["\\(5\\text{ mol } e^-\\)", "\\(1\\text{ mol } e^-\\)", "\\(2\\text{ mol } e^-\\)"],
            "In basic/neutral medium, Mn goes from \\(+7\\) in \\(\\text{MnO}_4^-\\) to \\(+4\\) in \\(\\text{MnO}_2\\), gaining \\(3\\) electrons per ion.",
        ),
        (
            "For the reaction \\(\\text{N}_2\\text{O}_4(g) \\rightleftharpoons 2\\text{NO}_2(g)\\), if \\(\\alpha\\) is the degree of dissociation at total pressure \\(P\\), what is the expression for \\(K_p\\)?",
            "\\(K_p = \\frac{4\\alpha^2 P}{1 - \\alpha^2}\\)",
            ["\\(K_p = \\frac{\\alpha^2 P}{1 - \\alpha}\\)", "\\(K_p = \\frac{2\\alpha^2 P}{1 + \\alpha}\\)", "\\(K_p = \\frac{4\\alpha^2}{P(1 - \\alpha^2)}\\)"],
            "Partial pressures are \\(P_{\\text{N}_2\\text{O}_4} = \\frac{1-\\alpha}{1+\\alpha}P\\) and \\(P_{\\text{NO}_2} = \\frac{2\\alpha}{1+\\alpha}P\\). Thus \\(K_p = \\frac{P_{\\text{NO}_2}^2}{P_{\\text{N}_2\\text{O}_4}} = \\frac{4\\alpha^2 P}{1 - \\alpha^2}\\).",
        ),
        (
            "Calculate the degree of dissociation \\(\\alpha\\) of \\(0.010\\text{ M}\\) acetic acid (\\(\\text{CH}_3\\text{COOH},\\; K_a = 1.8 \\times 10^{-5}\\)) when dissolved in a solution that already contains \\(0.10\\text{ M}\\text{ CH}_3\\text{COONa}\\).",
            "\\(1.8 \\times 10^{-4}\\) (\\(0.018\\%\\))",
            ["\\(4.2 \\times 10^{-2}\\) (\\(4.2\\%\\))", "\\(1.8 \\times 10^{-3}\\)", "\\(1.8 \\times 10^{-5}\\)"],
            "By the common-ion effect, \\([\\text{CH}_3\\text{COO}^-] \\approx 0.10\\text{ M}\\), so \\([\\text{H}^+] = C\\alpha \\approx \\frac{K_a C}{0.10} \\Rightarrow \\alpha = \\frac{1.8 \\times 10^{-5}}{0.10} = 1.8 \\times 10^{-4}\\).",
        ),
        (
            "What is the molar solubility \\(s\\) of silver chromate \\(\\text{Ag}_2\\text{CrO}_4(s) \\rightleftharpoons 2\\text{Ag}^+(aq) + \\text{CrO}_4^{2-}(aq)\\) in pure water if \\(K_{sp} = 4.0 \\times 10^{-12}\\)?",
            "\\(1.0 \\times 10^{-4}\\text{ M}\\)",
            ["\\(2.0 \\times 10^{-6}\\text{ M}\\)", "\\(1.59 \\times 10^{-4}\\text{ M}\\)", "\\(2.0 \\times 10^{-4}\\text{ M}\\)"],
            "Here \\(K_{sp} = [\\text{Ag}^+]^2[\\text{CrO}_4^{2-}] = (2s)^2(s) = 4s^3 = 4.0 \\times 10^{-12} \\Rightarrow s^3 = 1.0 \\times 10^{-12} \\Rightarrow s = 1.0 \\times 10^{-4}\\text{ M}\\).",
        ),
        (
            "In a first-order reaction, how does the time required for \\(99.9\\%\\) completion (\\(t_{99.9\\%}\\)) compare with the half-life (\\(t_{1/2}\\))? (Given \\(\\log_{10} 2 = 0.3010\\))",
            "\\(t_{99.9\\%} \\approx 10 \\times t_{1/2}\\)",
            ["\\(t_{99.9\\%} = 2 \\times t_{1/2}\\)", "\\(t_{99.9\\%} = 5 \\times t_{1/2}\\)", "\\(t_{99.9\\%} = 100 \\times t_{1/2}\\)"],
            "\\(\\frac{t_{99.9\\%}}{t_{1/2}} = \\frac{\\log_{10}(100 / 0.1)}{\\log_{10}(2)} = \\frac{3}{0.3010} \\approx 10\\).",
        ),
        (
            "What is the oxidation number of Nitrogen in hydrazoic acid \\(\\text{HN}_3\\) and in hydroxylamine \\(\\text{NH}_2\\text{OH}\\) respectively?",
            "\\(-\\frac{1}{3}\\) and \\(-1\\)",
            ["\\(-3\\) and \\(-1\\)", "\\(+3\\) and \\(-2\\)", "\\(-\\frac{1}{3}\\) and \\(+1\\)"],
            "In \\(\\text{HN}_3\\): \\(+1 + 3\\text{N} = 0 \\Rightarrow \\text{N} = -1/3\\). In \\(\\text{NH}_2\\text{OH}\\): \\(\\text{N} + 3(+1) + (-2) = 0 \\Rightarrow \\text{N} = -1\\).",
        ),
        (
            "A gaseous mixture contains \\(4.0\\text{ g}\\) of \\(\\text{H}_2\\) (\\(M = 2.0\\text{ g/mol}\\)) and \\(32.0\\text{ g}\\) of \\(\\text{O}_2\\) (\\(M = 32.0\\text{ g/mol}\\)) at a total pressure of \\(6.0\\text{ atm}\\). What is the partial pressure of \\(\\text{H}_2\\)?",
            "\\(4.0\\text{ atm}\\)",
            ["\\(2.0\\text{ atm}\\)", "\\(3.0\\text{ atm}\\)", "\\(4.8\\text{ atm}\\)"],
            "Moles \\(\\text{H}_2 = 2.0\\text{ mol}\\), moles \\(\\text{O}_2 = 1.0\\text{ mol}\\). Mole fraction \\(X_{\\text{H}_2} = 2/3\\), so \\(P_{\\text{H}_2} = (2/3) \\times 6.0 = 4.0\\text{ atm}\\).",
        ),
        (
            "For the elementary termolecular reaction \\(2\\text{NO}(g) + \\text{O}_2(g) \\rightarrow 2\\text{NO}_2(g)\\), if the volume of the reaction vessel is suddenly halved at constant temperature, by what factor does the instantaneous reaction rate increase?",
            "\\(8\\)",
            ["\\(4\\)", "\\(2\\)", "\\(6\\)"],
            "Halving the volume doubles all molar concentrations. Since \\(\\text{Rate} = k[\\text{NO}]^2[\\text{O}_2]\\), the new rate is \\(2^2 \\times 2^1 = 8\\) times the original rate.",
        ),
        (
            "According to Heisenberg's Uncertainty Principle, it is impossible to determine simultaneously and with unlimited accuracy both the:",
            "Position and linear momentum of a microscopic particle such as an electron",
            ["Mass and electric charge of an electron", "Spin quantum number and principal quantum number", "Wavelength and frequency of a photon"],
            "Heisenberg's Uncertainty Principle states \\(\\Delta x \\cdot \\Delta p_x \\ge \\frac{h}{4\\pi}\\), forbidding simultaneous exact knowledge of position and momentum.",
        ),
        (
            "What is the de Broglie wavelength \\(\\lambda\\) of a particle of mass \\(m = 1.0 \\times 10^{-30}\\text{ kg}\\) moving at speed \\(v = 6.63 \\times 10^5\\text{ m/s}\\) (Planck's constant \\(h = 6.63 \\times 10^{-34}\\text{ J}\\cdot\\text{s}\\))?",
            "\\(1.0 \\times 10^{-9}\\text{ m}\\) (\\(1.0\\text{ nm}\\))",
            ["\\(1.0 \\times 10^{-10}\\text{ m}\\)", "\\(1.0 \\times 10^{-7}\\text{ m}\\)", "\\(6.63 \\times 10^{-9}\\text{ m}\\)"],
            "Using \\(\\lambda = \\frac{h}{mv} = \\frac{6.63 \\times 10^{-34}}{1.0 \\times 10^{-30} \\times 6.63 \\times 10^5} = 1.0 \\times 10^{-9}\\text{ m}\\).",
        ),
        (
            "How many grams of solid \\(\\text{NaOH}\\) (\\(M = 40.0\\text{ g/mol}\\)) must be added to \\(1.0\\text{ dm}^3\\) of \\(0.20\\text{ M CH}_3\\text{COOH}\\) (\\(\\text{p}K_a = 4.74\\)) to produce a buffer of \\(\\text{pH} = 4.74\\)?",
            "\\(4.0\\text{ g}\\)",
            ["\\(8.0\\text{ g}\\)", "\\(2.0\\text{ g}\\)", "\\(1.0\\text{ g}\\)"],
            "To reach \\(\\text{pH} = \\text{p}K_a = 4.74\\), exactly half of the \\(0.20\\text{ mol CH}_3\\text{COOH}\\) must be neutralized to \\(\\text{CH}_3\\text{COONa}\\), requiring \\(0.10\\text{ mol NaOH} = 0.10 \\times 40.0 = 4.0\\text{ g}\\).",
        ),
        (
            "During the electrolysis of molten \\(\\text{Al}_2\\text{O}_3\\), how many Faradays (\\(F\\)) of electric charge are required to deposit \\(54.0\\text{ g}\\) of Aluminium (\\(M = 27.0\\text{ g/mol}\\)) at the cathode?",
            "\\(6.0\\text{ F}\\)",
            ["\\(3.0\\text{ F}\\)", "\\(2.0\\text{ F}\\)", "\\(1.5\\text{ F}\\)"],
            "Moles of \\(\\text{Al} = 54.0 / 27.0 = 2.0\\text{ mol}\\). Since \\(\\text{Al}^{3+} + 3e^- \\rightarrow \\text{Al}\\), each mole of Al requires \\(3\\text{ F}\\), totaling \\(2.0 \\times 3 = 6.0\\text{ F}\\).",
        ),
        (
            "A current of \\(9.65\\text{ A}\\) is passed through aqueous \\(\\text{CuSO}_4\\) for \\(1000\\text{ s}\\). What mass of Copper (\\(M = 63.5\\text{ g/mol},\\; F = 96,500\\text{ C/mol}\\)) is deposited at the cathode?",
            "\\(3.175\\text{ g}\\)",
            ["\\(6.35\\text{ g}\\)", "\\(1.588\\text{ g}\\)", "\\(0.635\\text{ g}\\)"],
            "Charge \\(Q = It = 9.65 \\times 1000 = 9650\\text{ C} = 0.10\\text{ F}\\). Since \\(\\text{Cu}^{2+} + 2e^- \\rightarrow \\text{Cu}\\), moles of \\(\\text{Cu} = 0.10 / 2 = 0.050\\text{ mol} \\times 63.5 = 3.175\\text{ g}\\).",
        ),
        (
            "In a reversible reaction, the activation energy of the forward reaction is \\(E_{a,f} = 85\\text{ kJ/mol}\\) and the activation energy of the reverse reaction is \\(E_{a,r} = 120\\text{ kJ/mol}\\). What is the enthalpy change \\(\\Delta H\\) of the forward reaction?",
            "\\(-35\\text{ kJ/mol}\\) (exothermic)",
            ["\\(+35\\text{ kJ/mol}\\) (endothermic)", "\\(+205\\text{ kJ/mol}\\)", "\\(-205\\text{ kJ/mol}\\)"],
            "\\(\\Delta H = E_{a,f} - E_{a,r} = 85 - 120 = -35\\text{ kJ/mol}\\).",
        ),
        (
            "What is the ionic strength \\(I = \\frac{1}{2}\\sum c_i z_i^2\\) of a \\(0.10\\text{ M MgCl}_2\\) aqueous solution?",
            "\\(0.30\\text{ M}\\)",
            ["\\(0.10\\text{ M}\\)", "\\(0.20\\text{ M}\\)", "\\(0.60\\text{ M}\\)"],
            "In \\(0.10\\text{ M MgCl}_2\\), \\([\\text{Mg}^{2+}] = 0.10\\text{ M}\\) (\\(z = +2\\)) and \\([\\text{Cl}^-] = 0.20\\text{ M}\\) (\\(z = -1\\)). Thus \\(I = \\frac{1}{2}[0.10(2^2) + 0.20((-1)^2)] = \\frac{1}{2}(0.40 + 0.20) = 0.30\\text{ M}\\).",
        ),
        (
            "Which quantum numbers \\((n, l)\\) correspond to a \\(4f\\) subshell, and what is the maximum number of electrons it can hold?",
            "\\(n = 4,\\; l = 3;\\quad 14\\text{ electrons}\\)",
            ["\\(n = 4,\\; l = 2;\\quad 10\\text{ electrons}\\)", "\\(n = 4,\\; l = 3;\\quad 7\\text{ electrons}\\)", "\\(n = 4,\\; l = 4;\\quad 14\\text{ electrons}\\)"],
            "Subshell labels \\(s, p, d, f\\) correspond to \\(l = 0, 1, 2, 3\\). An \\(f\\) subshell (\\(l=3\\)) has \\(2l + 1 = 7\\) orbitals and holds \\(2(7) = 14\\) electrons.",
        ),
        (
            "When \\(100\\text{ cm}^3\\) of \\(0.20\\text{ M HCl}\\) is mixed with \\(100\\text{ cm}^3\\) of \\(0.10\\text{ M NaOH}\\) at \\(298\\text{ K}\\), what is the \\([\\text{H}^+]\\) and \\(\\text{pH}\\) of the resulting solution?",
            "\\([\\text{H}^+] = 0.050\\text{ M},\\quad \\text{pH} = 1.30\\)",
            ["\\([\\text{H}^+] = 0.10\\text{ M},\\quad \\text{pH} = 1.00\\)", "\\([\\text{H}^+] = 0.050\\text{ M},\\quad \\text{pH} = 2.00\\)", "\\([\\text{H}^+] = 0.025\\text{ M},\\quad \\text{pH} = 1.60\\)"],
            "Unneutralized \\(\\text{H}^+ = (0.100 \\times 0.20) - (0.100 \\times 0.10) = 0.010\\text{ mol}\\) in total volume \\(0.200\\text{ dm}^3\\), giving \\([\\text{H}^+] = 0.050\\text{ M}\\) and \\(\\text{pH} = -\\log_{10}(0.050) = 1.30\\).",
        ),
        (
            "For the reaction \\(\\text{A} + \\text{B} \\rightarrow \\text{C}\\), if the activation energy \\(E_a = 0\\), how does the rate constant \\(k\\) depend on temperature according to the simple Arrhenius equation \\(k = A e^{-E_a / RT}\\)?",
            "\\(k = A\\) (independent of temperature)",
            ["\\(k = 0\\) at all temperatures", "\\(k\\) increases exponentially with temperature", "\\(k\\) decreases exponentially with temperature"],
            "When \\(E_a = 0\\), \\(e^{-E_a / RT} = e^0 = 1\\), so \\(k = A\\).",
        ),
        (
            "In the Ostwald dilution law for a weak monoprotic electrolyte, \\(K_a = \\frac{C\\alpha^2}{1 - \\alpha}\\). If \\(\\alpha = 0.20\\) (\\(20\\%\\) ionized, so \\(1 - \\alpha\\) cannot be neglected) in a \\(0.10\\text{ M}\\) solution, what is the exact value of \\(K_a\\)?",
            "\\(5.0 \\times 10^{-3}\\)",
            ["\\(4.0 \\times 10^{-3}\\)", "\\(2.5 \\times 10^{-2}\\)", "\\(2.0 \\times 10^{-3}\\)"],
            "Using the exact formula: \\(K_a = \\frac{0.10 \\times (0.20)^2}{1 - 0.20} = \\frac{0.0040}{0.80} = 5.0 \\times 10^{-3}\\).",
        ),
        (
            "Which aqueous salt solution will have a \\(\\text{pH} < 7.0\\) at \\(298\\text{ K}\\) due to cationic hydrolysis?",
            "\\(\\text{NH}_4\\text{Cl}(aq)\\)",
            ["\\(\\text{CH}_3\\text{COONa}(aq)\\)", "\\(\\text{NaCl}(aq)\\)", "\\(\\text{K}_2\\text{CO}_3(aq)\\)"],
            "\\(\\text{NH}_4\\text{Cl}\\) is the salt of a weak base (\\(\\text{NH}_3\\)) and a strong acid (\\(\\text{HCl}\\)); \\(\\text{NH}_4^+ + \\text{H}_2\\text{O} \\rightleftharpoons \\text{NH}_3 + \\text{H}_3\\text{O}^+\\) produces an acidic solution (\\(\\text{pH} < 7\\)).",
        ),
        (
            "Which aqueous salt solution will have a \\(\\text{pH} > 7.0\\) at \\(298\\text{ K}\\) due to anionic hydrolysis?",
            "\\(\\text{CH}_3\\text{COONa}(aq)\\)",
            ["\\(\\text{NH}_4\\text{NO}_3(aq)\\)", "\\(\\text{KNO}_3(aq)\\)", "\\(\\text{AlCl}_3(aq)\\)"],
            "Acetate ion hydrolyzes in water (\\(\\text{CH}_3\\text{COO}^- + \\text{H}_2\\text{O} \\rightleftharpoons \\text{CH}_3\\text{COOH} + \\text{OH}^-\\)), making the solution basic (\\(\\text{pH} > 7\\)).",
        ),
        (
            "In a zero-order reaction \\(A \\rightarrow P\\) with \\([A]_0 = 1.20\\text{ M}\\) and rate constant \\(k_0 = 0.040\\text{ M}\\,\\text{s}^{-1}\\), what is the concentration \\([A]\\) remaining after \\(15\\text{ s}\\)?",
            "\\(0.60\\text{ M}\\)",
            ["\\(0.66\\text{ M}\\)", "\\(0.30\\text{ M}\\)", "\\(0.90\\text{ M}\\)"],
            "Using \\([A] = [A]_0 - k_0 t = 1.20 - (0.040)(15) = 1.20 - 0.60 = 0.60\\text{ M}\\).",
        ),
        (
            "What is the bond order of the dioxygen molecule \\(\\text{O}_2\\) and superoxide ion \\(\\text{O}_2^-\\) according to Molecular Orbital (MO) theory?",
            "\\(2.0\\) for \\(\\text{O}_2\\) and \\(1.5\\) for \\(\\text{O}_2^-\\)",
            ["\\(2.0\\) for \\(\\text{O}_2\\) and \\(2.5\\) for \\(\\text{O}_2^-\\)", "\\(1.5\\) for \\(\\text{O}_2\\) and \\(1.0\\) for \\(\\text{O}_2^-\\)", "\\(3.0\\) for \\(\\text{O}_2\\) and \\(2.0\\) for \\(\\text{O}_2^-\\)"],
            "\\(\\text{O}_2\\) has 10 bonding and 6 antibonding valence electrons (bond order \\(= (10-6)/2 = 2.0\\)). Adding 1 electron into a \\(\\pi^*\\) antibonding orbital in \\(\\text{O}_2^-\\) lowers the bond order to \\(1.5\\).",
        ),
        (
            "Why is the dioxygen molecule (\\(\\text{O}_2\\)) paramagnetic in its ground state?",
            "It has two unpaired electrons in its degenerate \\(\\pi^*_{2p}\\) antibonding molecular orbitals",
            ["It has an odd total number of electrons", "Its \\(\\sigma_{2p}\\) bonding orbital is half-filled", "Oxygen atoms have unpaired 1s electrons"],
            "According to MO theory and Hund's rule, the last two electrons of \\(\\text{O}_2\\) occupy the degenerate \\(\\pi^*_{2p_x}\\) and \\(\\pi^*_{2p_y}\\) orbitals singly with parallel spins.",
        ),
        (
            "When \\(2.00\\text{ g}\\) of a non-volatile non-electrolyte solute is dissolved in \\(100\\text{ g}\\) of benzene (\\(K_f = 5.12\\text{ K kg mol}^{-1}\\)), the freezing point of benzene is depressed by \\(0.64\\text{ K}\\). What is the molar mass of the solute?",
            "\\(160\\text{ g/mol}\\)",
            ["\\(80\\text{ g/mol}\\)", "\\(128\\text{ g/mol}\\)", "\\(320\\text{ g/mol}\\)"],
            "From \\(\\Delta T_f = K_f m = K_f \\frac{w_{\\text{solute}}}{M_{\\text{solute}} \\times w_{\\text{solvent (kg)}}}\\): \\(M = \\frac{5.12 \\times 2.00}{0.64 \\times 0.100} = 160\\text{ g/mol}\\).",
        ),
        (
            "What is the van't Hoff factor \\(i\\) for a weak electrolyte \\(\\text{AB}_2\\) (which dissociates into \\(\\text{A}^{2+} + 2\\text{B}^-\\), i.e., \\(n = 3\\) ions) if its degree of dissociation in solution is \\(\\alpha\\)?",
            "\\(i = 1 + 2\\alpha\\)",
            ["\\(i = 1 + \\alpha\\)", "\\(i = 1 + 3\\alpha\\)", "\\(i = 1 - 2\\alpha\\)"],
            "For a solute yielding \\(n\\) ions per formula unit, \\(i = 1 + (n - 1)\\alpha\\). For \\(n = 3\\), \\(i = 1 + 2\\alpha\\).",
        ),
        (
            "Which statement accurately compares the rate of a reaction and its equilibrium constant \\(K\\) when a positive catalyst is added at constant temperature?",
            "Both forward and reverse rate constants (\\(k_f\\) and \\(k_r\\)) increase by the same factor, so \\(K = k_f / k_r\\) remains unchanged",
            ["\\(k_f\\) increases while \\(k_r\\) decreases, so \\(K\\) increases", "Both \\(k_f\\) and \\(k_r\\) remain unchanged", "Only \\(k_f\\) increases while \\(k_r\\) stays constant"],
            "A catalyst lowers the activation barrier equally in both directions, multiplying \\(k_f\\) and \\(k_r\\) by the same factor \\(e^{\\Delta E_a / RT}\\) and leaving \\(K = k_f/k_r\\) invariant.",
        ),
        (
            "In the reaction \\(\\text{I}_2(aq) + 2\\text{S}_2\\text{O}_3^{2-}(aq) \\rightarrow 2\\text{I}^-(aq) + \\text{S}_4\\text{O}_6^{2-}(aq)\\), which species acts as the reducing agent and which acts as the oxidizing agent?",
            "\\(\\text{S}_2\\text{O}_3^{2-}\\) is the reducing agent; \\(\\text{I}_2\\) is the oxidizing agent",
            ["\\(\\text{I}_2\\) is the reducing agent; \\(\\text{S}_2\\text{O}_3^{2-}\\) is the oxidizing agent", "\\(\\text{I}^-\\) is the oxidizing agent; \\(\\text{S}_4\\text{O}_6^{2-}\\) is the reducing agent", "Both act as oxidizing agents"],
            "Thiosulfate (\\(\\text{S}_2\\text{O}_3^{2-}\\)) is oxidized from average S oxidation state \\(+2\\) to \\(+2.5\\) (reducing agent), reducing \\(\\text{I}_2\\) from \\(0\\) to \\(-1\\) (oxidizing agent).",
        ),
        (
            "If the half-life of a reaction \\(A \\rightarrow P\\) is observed to be inversely proportional to the cube of the initial concentration (\\(t_{1/2} \\propto [A]_0^{-3}\\)), what is the order \\(n\\) of the reaction?",
            "\\(4\\text{th order}\\)",
            ["\\(3\\text{rd order}\\)", "\\(2\\text{nd order}\\)", "\\(0\\text{th order}\\)"],
            "For an \\(n\\)-th order reaction (\\(n \\ne 1\\)), \\(t_{1/2} \\propto [A]_0^{1-n}\\). Setting \\(1 - n = -3\\) gives \\(n = 4\\).",
        ),
        (
            "What is the molar concentration of pure liquid water (\\(\\text{H}_2\\text{O},\\; M = 18.0\\text{ g/mol}\\)) at \\(298\\text{ K}\\) given that its density is \\(1.00\\text{ g/cm}^3\\) (\\(1000\\text{ g/dm}^3\\))?",
            "\\(55.56\\text{ M}\\)",
            ["\\(1.00\\text{ M}\\)", "\\(18.0\\text{ M}\\)", "\\(1.0 \\times 10^{-7}\\text{ M}\\)"],
            "One litre (\\(1000\\text{ g}\\)) of pure water contains \\(1000 / 18.0 = 55.56\\text{ moles}\\), so \\([\\text{H}_2\\text{O}] = 55.56\\text{ M}\\).",
        ),
    ]
    for q, corr, dists, exp in extra_chm:
        items.append(make_item(f"CHM101_{idx}", "CHM 101", q, corr, dists, exp, rng))
        idx += 1

    return items[:100]


def generate_bio101_200(rng: random.Random) -> list[dict]:
    """Generate 200 rigorous 100-level 1st-semester BIO 101 questions in JSON format."""
    from seed_questions import generate_bio101_questions

    raw_bio = generate_bio101_questions(rng)
    letters = ["A", "B", "C", "D"]
    bio_json = []
    for i, q in enumerate(raw_bio[:200], start=1):
        opts = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]
        ans_idx = letters.index(q["correct_option"])
        bio_json.append(
            {
                "id": f"BIO101_{i:03d}",
                "course": "BIO 101",
                "question": q["question_text"],
                "options": opts,
                "answer_index": ans_idx,
                "explanation": q["explanation"],
            }
        )
    return bio_json


def build_all():
    rng = random.Random(1120)
    user_300 = json.loads((DATA_DIR / "user_provided_300.json").read_text(encoding="utf-8"))

    phy_base = [q for q in user_300 if q["course"].replace(" ", "") == "PHY101"]
    mth_base = [q for q in user_300 if q["course"].replace(" ", "") == "MTH101"]
    chm_base = [q for q in user_300 if q["course"].replace(" ", "") == "CHM101"]

    for q in phy_base + mth_base + chm_base:
        corr_opt = q["options"][q["answer_index"]]
        if not q.get("explanation"):
            q["explanation"] = f"The correct option is {corr_opt}."

    phy_all = phy_base + generate_hard_phy101(rng)
    mth_all = mth_base + generate_hard_mth101(rng)
    chm_all = chm_base + generate_hard_chm101(rng)
    bio_all = generate_bio101_200(rng)

    assert len(phy_all) == 200, f"Expected 200 PHY 101, got {len(phy_all)}"
    assert len(mth_all) == 200, f"Expected 200 MTH 101, got {len(mth_all)}"
    assert len(chm_all) == 200, f"Expected 200 CHM 101, got {len(chm_all)}"
    assert len(bio_all) == 200, f"Expected 200 BIO 101, got {len(bio_all)}"

    for label, bank in [("PHY 101", phy_all), ("MTH 101", mth_all), ("CHM 101", chm_all), ("BIO 101", bio_all)]:
        q_texts = [q["question"].strip() for q in bank]
        assert len(set(q_texts)) == 200, f"Duplicate found in {label}: {len(set(q_texts))} unique out of 200"

    (DATA_DIR / "phy101.json").write_text(json.dumps(phy_all, indent=2, ensure_ascii=False), encoding="utf-8")
    (DATA_DIR / "mth101.json").write_text(json.dumps(mth_all, indent=2, ensure_ascii=False), encoding="utf-8")
    (DATA_DIR / "chm101.json").write_text(json.dumps(chm_all, indent=2, ensure_ascii=False), encoding="utf-8")
    (DATA_DIR / "bio101.json").write_text(json.dumps(bio_all, indent=2, ensure_ascii=False), encoding="utf-8")

    combined = chm_all + phy_all + mth_all + bio_all
    (DATA_DIR / "all_questions.json").write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated JSON question banks: PHY={len(phy_all)}, MTH={len(mth_all)}, CHM={len(chm_all)}, BIO={len(bio_all)} (Total={len(combined)})")


if __name__ == "__main__":
    build_all()

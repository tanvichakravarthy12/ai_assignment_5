# prior of difficulty
def get_p_difficulty(diff):
    return 0.4 if diff else 0.6

# prior of intelligence
def get_p_intelligence(intel):
    return 0.3 if intel else 0.7

# grade cpt
def get_p_grade(grade, diff, intel):
    if intel:
        if diff:
            # high intel, high difficulty
            probs = {'A': 0.30, 'B': 0.40, 'C': 0.30}
        else:
            # high intel, low difficulty
            probs = {'A': 0.90, 'B': 0.08, 'C': 0.02}
    else:
        if diff:
            # low intel, high difficulty
            probs = {'A': 0.01, 'B': 0.12, 'C': 0.87}
        else:
            # low intel, low difficulty
            probs = {'A': 0.05, 'B': 0.25, 'C': 0.70}
    return probs.get(grade, 0.0)

# sat cpt
def get_p_sat(sat, intel):
    if intel:
        return 0.80 if sat else 0.20
    else:
        return 0.05 if sat else 0.95

# letter cpt
def get_p_letter(letter_strong, grade):
    if grade == 'A':
        return 0.90 if letter_strong else 0.10
    elif grade == 'B':
        return 0.60 if letter_strong else 0.40
    else:
        return 0.01 if letter_strong else 0.99

# joint probability calculation
def get_joint_prob(diff, intel, grade, sat, letter_strong):
    p_d = get_p_difficulty(diff)
    p_i = get_p_intelligence(intel)
    p_g = get_p_grade(grade, diff, intel)
    p_s = get_p_sat(sat, intel)
    p_l = get_p_letter(letter_strong, grade)
    return p_d * p_i * p_g * p_s * p_l

if __name__ == "__main__":
    # P(Intelligence=High | Letter=Weak, Difficulty=High)
    
    # sum over G and S for high intel
    p_high_intel_and_evidence = 0.0
    for grade in ['A', 'B', 'C']:
        for sat in [True, False]:
            p_high_intel_and_evidence += get_joint_prob(True, True, grade, sat, False)
            
    # sum over G and S for low intel
    p_low_intel_and_evidence = 0.0
    for grade in ['A', 'B', 'C']:
        for sat in [True, False]:
            p_low_intel_and_evidence += get_joint_prob(True, False, grade, sat, False)
            
    # total probability of evidence
    p_evidence = p_high_intel_and_evidence + p_low_intel_and_evidence
    
    # posterior probability
    p_result = p_high_intel_and_evidence / p_evidence
    
    print("Query: P(Intelligence=High | Letter=Weak, Difficulty=High)\n")
    print("Joint Probability (High Intelligence & Evidence):", round(p_high_intel_and_evidence, 6))
    print("\nTotal Evidence Probability (Weak Letter in Hard Class):", round(p_evidence, 6))
    print("\nPosterior Probability (High Intelligence given Evidence):", round(p_result, 6))
    print(f"\nInterpretation: There is a {round(p_result * 100, 2)}% chance the student has High Intelligence.")

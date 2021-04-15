'''
You've caught two of your fellow minions passing coded notes back and forth -- while they're on duty, no less! Worse, you're pretty sure it's not job-related --
they're both huge fans of the space soap opera ""Lance & Janice"". You know how much Commander Lambda hates waste,
so if you can prove that these minions are wasting time passing non-job-related notes, it'll put you that much closer to a promotion.
Fortunately for you, the minions aren't exactly advanced cryptographers. In their code, every lowercase letter [a..z] is replaced with the corresponding one in [z..a],
while every other character (including uppercase letters and punctuation) is left untouched.
That is, 'a' becomes 'z', 'b' becomes 'y', 'c' becomes 'x', etc.  For instance, the word ""vmxibkgrlm"", when decoded, would become ""encryption"".
Write a function called solution(s) which takes in a string and returns the deciphered string so you can show the commander proof that these minions
are talking about ""Lance & Janice"" instead of doing their jobs.
'''

'''
Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution("wrw blf hvv ozhg mrtsg'h vkrhlwv?")
Output:
    did you see last night's episode?

Input:
solution.solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!")
Output:
    Yeah! I can't believe Lance lost his job at the colony!!
'''
# a = 97, z = 122

def solution(x):
    letters_reversed = [chr(i+97) for i in range(25, -1, -1)]
    out = ""
    for letter in x:
        code = ord(letter)
        if code in range(97,123):
            reversed = letters_reversed[code-97]
            out+=reversed
        else:
            out+=letter
    return out

if __name__ == '__main__':
    print(solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!"))
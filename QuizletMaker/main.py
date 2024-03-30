import math

def inp(ques, ans=None, int_only=False, yn=False, rep_msg=None, rep=False, no_ans=False):
    if ans:
        ans = [an.lower() for an in ans]
    if rep:
        print(rep_msg)
    res = input(ques).lower()
    if no_ans and not res:
        return False
    if int_only:
        try:
            return str(int(res))
        except:
            inp(ques, int_only=True, rep_msg=rep_msg, rep=True)
    return res if not yn and not ans or yn and res in ['yes', 'no'] or ans and res in ans else inp(ques, ans=ans, yn=yn,
                                                                                                   rep_msg=rep_msg,
                                                                                                   rep=True,
                                                                                                   no_ans=no_ans)

def prompt_generator(notes, num, focus, r_type, sctn_len): 
    # IF NOTES ARE OUTLINE OR BULLET, CONVERT BULLET POINTS TO TABS

    prompt = f"""<PROMPT START> 
    You will be given the notes that a student is using in preparation for a test.
    Your job is to write {num} flashcards, including question and answer, to help the student prepare for the
    test. 
    
    Your response should be formatted in one paragraph, with a slash between each flashcard and a semicolon
    between the question and answer. Here is an example:
    'What year was the Declaration of Independence signed?; 1776'
    For clarity, please do not use slashes or semicolons for any other purpose.

    Here is what the student has said about what areas deserve the most focus (this student's response is between
    brackets, ignore this if they did not say anything): 
    [{focus}]
    Please note that you should still try to include as much of the notes as possible in the flashcards, and ensure 
    that there is a healthy balance of open ended and basic questions.
    
    You will now be given the student's notes. They may exceed the maximum amount of characters I can input, so
    please DO NOT start creating flashcards until you are explicitly told that the prompt has ended. If it does not
    say "<PROMPT END>" at the end of the notes, simply say "continue" and you will continue to be given the notes until
    the end has been reached: \n{notes} 
    <PROMPT END>
    """

    if len(prompt) <= sctn_len: return prompt

    sections = []
    for i in range(0, len(prompt), sctn_len):
        if len(prompt) - i <= sctn_len: sections.append(prompt[i : len(prompt) - 1])
        else: sections.append(prompt[i : i + sctn_len])
        if r_type == str: sections.append("\n\n\n\n\n")

    if r_type == str: return "".join(sections)
    return sections

notes = """
The French Revolution was a period of political and societal change in France that began with the Estates General of 1789 and ended with the coup of 18 Brumaire on November 1799 and the formation of the French Consulate 1. The revolution was a result of a combination of social, political, and economic factors that the Ancien Régime proved unable to manage 1. The revolution is widely recognized as one of the most significant events in modern European history, and its ideas are considered fundamental principles of liberal democracy 1.

The French Revolution was characterized by several key events, including the Storming of the Bastille on July 14, 1789, which marked the beginning of the revolution 1. The National Assembly was formed on June 17, 1789, and it abolished feudalism and established a constitutional monarchy 1. The Reign of Terror, which lasted from September 1793 to July 1794, was a period of extreme violence and political repression 1. The revolution also led to the rise of Napoleon Bonaparte, who became the first consul of France in 1799 1.

The French Revolution had a profound impact on France and the world. It abolished the Ancien Régime and created a constitutional monarchy 1. It also led to the proclamation of the French First Republic in September 1792 1. The revolution resulted in the Reign of Terror and the execution of Louis XVI 1. The French Revolutionary Wars, which lasted from 1792 to 1802, were a series of conflicts between France and other European powers 1. The revolution also led to the establishment of the French Consulate in November 1799 1.

The French Revolution was a complex and multifaceted event that has been the subject of much historical analysis and debate. It is widely recognized as a turning point in modern European history and a significant event in the development of liberal democracy 1. The revolution’s legacy can be seen in the values and institutions that remain central to modern French political discourse 1.
"""

prompt = prompt_generator(notes, 10, "", "", 1900)
if type(prompt)==str: print(prompt)
else: 
    for i in prompt:
        print(i)
        print('\n\n\n\n\n')

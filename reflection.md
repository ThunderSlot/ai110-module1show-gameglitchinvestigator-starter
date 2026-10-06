# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
Easy, normal and hard mode specifications were unrelated in accordance with the trial numbers and range set.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
    1. the hints were backwards
    2. new game button not working
    3. Attempts number def and actual trial unmatched
    4. val from input box not inserting right way into list and have to clicked twice and added in redundantly

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 21    | go lower as shown in hint|  go higher shown as the opposite of as it should be |app.py: 37|
|click on new button | game resets | nothing nappen |  app.py : 134|
|Input the guess | increase the trials as it is | trial stuck and has to input twice | app.py 114 |
| Input the guess | shown the num of trial as the input is added | -2 of the real num of input trial | appy.py96|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude code from terminal

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
AI suggested to check the validity of input that should be within the integer rate set by the difficulity


- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
1. checking the flow of code
2. try running the app and see if it is correct
3. writing the test script

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  >> test_too_low_guess_says_go_higher -> check that if the input is lower than the secrete, try to output go higher


- Did AI help you design or understand any tests? How?
NO

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit takes whole Python script from top to bottom every time someone interacts with the app, whether they click a button, type in a box, or move a slider. That's a "rerun." It's like a whiteboard that gets erased and redrawn from scratch after every click. That makes Streamlit simple to write, because you just write a normal script, but it means ordinary variables don't survive. Anything that was set gets reset on the next rerun.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Look for the AI sugesstion that can advice sometimes out of the box thoughts that u never thought before while managing the direction of crafting by it

- What is one thing you would do differently next time you work with AI on a coding task?
 I would do the same workflow from prompt, to logic to refactor to test.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI gen code could unlock the thoughts out of the box from its suggestion, but sometimes it can also make mistake on generating the code from the prompt but that can be easily overcome with clearly prompt instruction.

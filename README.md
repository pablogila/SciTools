# New Tools for Scientific Research

## Benefits and Risks of AI Tools for Academics

---

**Last update: 2023/05/15**  

This is a quick overview of the benefits, risks, and how-to's of AI tools for scientific research, and in particular for _Large Language Models_ (LLMs). It is intended for scientists who have been living under a rock (or in a lab) for the last few months and want to learn the basics of AI stuff. It also contains some tools that may not be powered by LLMs, but are still useful for scientific research.  

---

## The first problem: there is too much noise ❌

Too many AI tools have spawned in the last months, but only a few seem useful for our academic duties. Here we will focus only on the most useful ones.  

![](pictures/too_much_info.jpg)  

---

## The rest of the problems ❌

**AI tools are not magic:**  
* **Can't do math**.  

* **Will always answer**... But will not always know the _correct_ answer.

* **Limited memory** - this will change in a few months though.  

* **Biased training data**.  

* **Lack of moral and ethical decisions**.  

* **Lower quality** of _everything_ in the long term.  

**AI tools should be considered as a complementary tool rather than a replacement for your intelligence.**  

---

## What can we use LLMs for? ✅

The most interesting use cases for scientific research are:  

* **Learning** and **summarizing** complex concepts. You can simply ask for a topic, but also to explain several paragraphs in simpler terms.  

* Help with **literature review**, finding new related papers and summarizing key points.  

* Overcome the **Blank Page Syndrome**.  

* **Translate** and **correct** texts.  

* Seek **inspiration**.

* Speed up the **writing** of proposals and papers by suggesting a **structure** or even paragraph **drafts**.  

* Write **computer code** faster and more efficiently, fix bugs, ask for specific features, write documentation...  

---

## How to use LLMs, for Scientists Living Under a Rock 📚

* **Be Specific**. These tools rely on the given context to generate the next word. It can not read your mind. You need to be very specific with your questions, and give it as much context as possible.  

* **Train the inputs**. It will rarely give you what you want at first. It particularly excells if you ask it to review its previous output, checking for any possible mistakes, and then ask it to continue from there. It will often give you a more coherent response.  

* **Create a prompt library**. Save the prompts that work best for you, so that you can reuse them later in the future.  

* And again, **be critical**. AI should not replace your intelligence.  

---

# Summary of The Cool Tools 😎  

## Main LLMs tools  
* [Bing Chat](https://www.bing.com/chat). The best general tool available to date. It does give you real references, and is really useful to search for any kind of info. It uses a more powerful model (GPT-4) than the free version of ChatGPT (GPT-3.5). Only works on _Microsoft Edge_, but you can install a plugin called _Bing Chat for All Browsers_ to use it on [Chrome](https://chrome.google.com/webstore/detail/bing-chat-for-all-browser/jofbglonpbndadajbafmmaklbfbkggpo) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/bing-chat-for-all-browsers/).  
* [ChatGPT](https://chat.openai.com/). The famous one. It is useful, for coding and text correction in particular, but it is NOT connected to the internet _yet_, so do NOT trust references from him, he might be lying.  
* [Github Copilot](https://github.com/features/copilot). A VSCode plugin that helps you write code, the best code completion tool currently available, free with the university account.  
* [HuggingChat](https://huggingface.co/chat/). New open source LLMs will probably appear here. Still under development, but expect major improvements in the coming months.  
* [Google Bard](https://bard.google.com/). Not yet available in Europe, but kind of like _Bing Chat_. More stuff [soon](https://g.co/Labs)  

## Finding related literature
* [Inciteful](https://inciteful.xyz/). Paste a DOI and find related papers, using cross citations.  
* [Connected Papers](https://www.connectedpapers.com/). Paste a DOI and find related papers, not by cross citations but using AI to find similarities.  
* [Research Rabbit](https://researchrabbitapp.com/). Upload a BibTeX or connect to your Zotero account, and find papers related to your collection.  

## Literature review
* [Elicit](https://elicit.org/). Ask a Question, get summarized results from papers.
* [Consensus](https://consensus.app/search/). Ask a yes or no question, and will try to answer according to the scientific literature.  

## Useful tools for other tasks
* [Pix2Tex](https://p2t.behye.com/). Write $\LaTeX$ equations by uploading a screenshot.     
* [Deepl Write](https://www.deepl.com/write). Check your grammar or translate, really useful even for scientific texts.  
* [Google Reverse Image Search](https://images.google.com/). It is not new at all, but it is really useful to find the source of that graph that you don't know where it came from.  

## Miscellaneous LLM tools
These tools can be easily replicated by more general LLMs with a bit of prompting, but may be useful if you want to skip that part.  
* [Explain Paper](https://www.explainpaper.com/). Upload a paper and mark sections of text that you do not understand, it will try to explain them in a simpler way.  
* [Ora.AI](https://ora.ai). You can tune the model to answer very specific questions.  

---

# Prompt Examples ✍

* Help with the outline of a talk  
`I am a physicist, performing my master thesis on a scientific research group. The group leader asked me to give a small talk of around 15 minutes to the group members, about ChatGPT and other new AI tools that are currently emerging, such as bing chat, deepl, etc. I want to talk about the benefits of AI use in academic research: how can it be used for learning and understanding new concepts, to write proposals faster, to code faster, etc. Also about the risks: sometimes, results such as citations or mathematical calculations may be invented, and the scientist should learn when can a result be trusted. I want you to give me a possible outline of the talk. It should be very brief, remember that the talk can't be longer than 15 minutes. Think about the thematics that I proposed you, and add any other topics that may be relevant.`  

* Break the blank page syndrome  
`I am currently writing a paper about solar panels. I want to start introducing the climate challenges, to link it with the importance of solar energy. Please write the first paragraph of the paper.`

* Asking complex questions  
`In the context of DFT, what is the monkhorst-pack grid?`

* Simplify explanations  
`Explain it again, but at the level of an undergraduate student.`

* Programming  
`Write a python function that returns the fibonacci sequence up to the number given as an argument`  

* Fixing the previous code, cause it probably doesn't work  
`The python code that you provided before does not work. I get the following error: [ERROR]`  

* Finding bugs  
`I have the following python function. It should return the fibonacci sequence up to the number given as an argument, but it does not work. Can you find the bug? [CODE]`  

* Writing documentation  
`I have the following python function. How does it work? Write the documentation on how to use this function. [CODE]`  

---



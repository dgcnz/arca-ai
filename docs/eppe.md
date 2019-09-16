# [Eppe]

## Preliminaries and related work

### What makes natural language understanding hard

Under a finite domain, one can constrain the focus on the following specific solvable issues:

**a) Compositionality and the combinatorial explosion of form and meaning**

If enough data and not immense language subset: learning based approaches.

Else:

To understand a large language subset including novel and previously unheard expressions, while also being robust to misinterpretation, one requires a mores sophistiucated and modular way to compose grammatical primitives. This is exatly what *construction grammars* do.

**b) Reference resolution and ambiguity**

In general, reference resolution consists of two steps.
1. *Anaphora resolution* identifies the noun to which a pronoun refers within a sentence. 
2. *Grounding* identifies the object in the real world to which the noun in the sentence refers

In cases where grounding can not disambiguate the references, clarification dialogs are required.

**c) Conditionals**

If-then-else pattern for verbal articulation

**d) Erroneous input and ungrammatical sloppy language**

Spelling and grammar errors + jargon

**e) Disfluency analysis and repair**

Humans often abandon sentences and words midway during the speaking, switching to other conversation segments or correcting sentences on the fly.

**f) Indirect assertions through relative clauses and appositions**
Relative clauses are often used for indirect assertions of world properties.

"The noodles, which are still in the pot on the stove, must be wasted by now; bring them to the trash!"

**g) Modalities**

Modalities are used to express ability, knowledge, temporality and other mental attitutes.

**h) Indirect speech acts**
Often used for politeness and sociality.
Open the window -> Can you open the window?

This is literally a modality question about the hearer's abilities, a robot should instead treat it as a command. It is an issue to decide when a robot should interpret a modality literally or as indirect speech.

**i) Interlocutor feedback**

+ okay, aight, etc.

**j) Metaphor**

It hasn't been applied to human robot interaction but it's said that it plays a central role in abstract thought, so it's crucial to understand language.

**k) Integration of Robots with NLU systems**

Connecting a NLU system to a robotic platform is not trivial. Problem solving unit connected with NLU system and motion system.

### Embodied Construction Grammar and Compositionality 

> In mathematics, semantics, and philosophy of language, the principle of compositionality is the principle that the meaning of a complex expression is determined by the meanings of its constituent expressions and the rules used to combine them.

Embodied Construction Grammar not only provides a way to compose constructions, but also concepts. These concepts are neurologically and cognitively motivated in accordance with the established theory about *image schemas*.


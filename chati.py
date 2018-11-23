import nltk
import random



GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]

def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)




if __name__ == "__main__" :
  sentence = raw_input("type")
  reply = check_for_greeting(sentence)
  print(reply)

def respond(sentence):

    """Parse the user's inbound sentence and find candidate terms that make up a best-fit response"""

    cleaned = preprocess_text(sentence)

    parsed = TextBlob(cleaned)

​

    # Loop through all the sentences, if more than one. This will help extract the most relevant

    # response text even across multiple sentences (for example if there was no obvious direct noun

    # in one sentence

    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

​

    # If we said something about the bot and used some kind of direct noun, construct the

    # sentence around that, discarding the other candidates

    resp = check_for_comment_about_bot(pronoun, noun, adjective)

​

    # If we just greeted the bot, we'll use a return greeting

    if not resp:

        resp = check_for_greeting(parsed)

​

    if not resp:

        # If we didn't override the final sentence, try to construct a new one:

        if not pronoun:

            resp = random.choice(NONE_RESPONSES)

        elif pronoun == 'I' and not verb:

            resp = random.choice(COMMENTS_ABOUT_SELF)

        else:

            resp = construct_response(pronoun, noun, verb)

​

    # If we got through all that with nothing, use a random response

    if not resp:

        resp = random.choice(NONE_RESPONSES)

​

    logger.info("Returning phrase '%s'", resp)

    # Check that we're not going to say anything obviously offensive

    filter_response(resp)

​

    return resp

​

def find_candidate_parts_of_speech(parsed):

    """Given a parsed input, find the best pronoun, direct noun, adjective, and verb to match their input.

    Returns a tuple of pronoun, noun, adjective, verb any of which may be None if there was no good match"""

    pronoun = None

    noun = None

    adjective = None

    verb = None

    for sent in parsed.sentences:

        pronoun = find_pronoun(sent)

        noun = find_noun(sent)

        adjective = find_adjective(sent)

        verb = find_verb(sent)

    logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)

    return pronoun, noun, adjective, verb



def check_for_comment_about_bot(pronoun, noun, adjective):

    """Check if the user's input was about the bot itself, in which case try to fashion a response

    that feels right based on their input. Returns the new best sentence, or None."""

    resp = None

    if pronoun == 'I' and (noun or adjective):

        if noun:

            if random.choice((True, False)):

                resp = random.choice(SELF_VERBS_WITH_NOUN_CAPS_PLURAL).format(**{'noun': noun.pluralize().capitalize()})

            else:

                resp = random.choice(SELF_VERBS_WITH_NOUN_LOWER).format(**{'noun': noun})

        else:

            resp = random.choice(SELF_VERBS_WITH_ADJECTIVE).format(**{'adjective': adjective})

    return resp

​

# Template for responses that include a direct noun which is indefinite/uncountable

SELF_VERBS_WITH_NOUN_CAPS_PLURAL = [

    "My last startup totally crushed the {noun} vertical",

    "Were you aware I was a serial entrepreneur in the {noun} sector?",

    "My startup is Uber for {noun}",

    "I really consider myself an expert on {noun}",

]

​

SELF_VERBS_WITH_NOUN_LOWER = [

    "Yeah but I know a lot about {noun}",

    "My bros always ask me about {noun}",

]

​

SELF_VERBS_WITH_ADJECTIVE = [

    "I'm personally building the {adjective} Economy",

    "I consider myself to be a {adjective}preneur",

]






def construct_response(pronoun, noun, verb):

    """No special cases matched, so we're going to try to construct a full sentence that uses as much

    of the user's input as possible"""

    resp = []

​

    if pronoun:

        resp.append(pronoun)

​

    # We always respond in the present tense, and the pronoun will always either be a passthrough

    # from the user, or 'you' or 'I', in which case we might need to change the tense for some

    # irregular verbs.

    if verb:

        verb_word = verb[0]

        if verb_word in ('be', 'am', 'is', "'m"):  # This would be an excellent place to use lemmas!

            if pronoun.lower() == 'you':

                # The bot will always tell the person they aren't whatever they said they were

                resp.append("aren't really")

            else:

                resp.append(verb_word)

    if noun:

        pronoun = "an" if starts_with_vowel(noun) else "a"

        resp.append(pronoun + " " + noun)

​

    resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "")))

​

    return " ".join(resp)

​

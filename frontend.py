import streamlit as st
from backend import get_response, custom_css
import time

st.set_page_config(
    page_title="LLM Powered FlashCard Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(custom_css(), unsafe_allow_html=True)

if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'flipped_cards' not in st.session_state:
    st.session_state.flipped_cards = set()

st.markdown("""
<div class="navbar">
    <h1>LLM Powered FlashCard Generator</h1>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    **How to use:**
    1. Enter your text content in the main area
    2. Customize the options
    3. Click "Generate Flashcards"
    4. Study by clicking cards to flip them!
    """)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Enter Your Text Content")
    text_input = st.text_area(
        "",
        placeholder="Paste your book excerpt, chapter, or any educational content here...",
        height=300,
        help="Enter the text you want to convert into flashcards"
    )

with col2:
    st.subheader("Customization Options")
    
    difficulty = st.selectbox(
        "Difficulty Level:",
        options=["Easy", "Medium", "Hard"],
        index=1,
        help="Choose the complexity level of questions"
    )
    
    # answer_length = st.selectbox(
    #     "Answer Length:",
    #     options=["short", "long"],
    #     index = 0,
    #     help="Specify the desired length of answers"
    # )
    
    num_flashcards = st.slider(
        "Number of Flashcards:",
        min_value=10,
        max_value=30,
        value=10,
        help="Select how many flashcards to generate",
        
    )

    subject = st.selectbox(
        "Related subject",
        options=["General", "Science", "History", "Finance", "AI/ML/Data Science", "Legal", "Health & Fitness", "Geography", "Computer Science", "Natural Language", "Mathematics"],
        index = 0,
        help="Enter the relevant subject (if any)"
    )



st.markdown("<br>", unsafe_allow_html=True)
generate_button = st.button("🚀 Generate Flashcards", use_container_width=True)

def generate_flashcards(text_input, difficulty, subject, num_flashcards):
    
    sample_flashcards = get_response(text_input, difficulty, subject, num_flashcards)
    
    return sample_flashcards[:num_flashcards]

if generate_button:
    if not text_input.strip():
        st.error("Please enter some text content to generate flashcards.")
    else:
        with st.spinner("Generating flashcards..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            flashcards = generate_flashcards(text_input, difficulty, subject, num_flashcards)
            
            if flashcards:
                st.session_state.flashcards = flashcards
                st.session_state.flipped_cards = set()
                st.success(f"✅Successfully generated {len(flashcards)} flashcards!")
            else:
                st.error("Failed to generate flashcards. Please try again.")

if st.session_state.flashcards:
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.subheader(f"Generated Flashcards ({len(st.session_state.flashcards)} cards)")
    
    # flashcards in rows of 2
    for i in range(0, len(st.session_state.flashcards), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            if i + j < len(st.session_state.flashcards):
                card_index = i + j
                flashcard = st.session_state.flashcards[card_index]
                
                with col:
                    if card_index in st.session_state.flipped_cards:
                        
                        card_html = f"""
                        <div class="flashcard flashcard-back">
                            <div class="flashcard-label">Answer</div>
                            <div class="flashcard-content">
                                {flashcard['answer']}
                            </div>
                        </div>
                        """
                        button_text = "🔄 Show Question"
                    else:
                        
                        card_html = f"""
                        <div class="flashcard flashcard-front">
                            <div class="flashcard-label">Question</div>
                            <div class="flashcard-content">
                                {flashcard['question']}
                            </div>
                        </div>
                        """
                        button_text = "💡 Show Answer"
                    
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Flip button
                    if st.button(button_text, key=f"flip_{card_index}", use_container_width=True):
                        if card_index in st.session_state.flipped_cards:
                            st.session_state.flipped_cards.discard(card_index)
                        else:
                            st.session_state.flipped_cards.add(card_index)
                        st.rerun()
    
    # Action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔄 Flip All Cards", use_container_width=True):
            if len(st.session_state.flipped_cards) == len(st.session_state.flashcards):
                st.session_state.flipped_cards = set()
            else:
                st.session_state.flipped_cards = set(range(len(st.session_state.flashcards)))
            st.rerun()
    
    with col2:
        if st.button("🎲 Shuffle Cards", use_container_width=True):
            import random
            random.shuffle(st.session_state.flashcards)
            st.session_state.flipped_cards = set()
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.flashcards = []
            st.session_state.flipped_cards = set()
            st.rerun()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
---
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>LLM Powered FlashCard Generator by AP | Built with ❤️ using Gemini 2.0 Flash Lite</p>
</div>
""", unsafe_allow_html=True)

# sample1 = """Cryptography, or cryptology (from Ancient Greek: κρυπτός, romanized: kryptós "hidden, secret"; and γράφειν graphein, "to write", or -λογία -logia, "study", respectively), is the practice and study of techniques for secure communication in the presence of adversarial behavior. More generally, cryptography is about constructing and analyzing protocols that prevent third parties or the public from reading private messages. Modern cryptography exists at the intersection of the disciplines of mathematics, computer science, information security, electrical engineering, digital signal processing, physics, and others. Core concepts related to information security (data confidentiality, data integrity, authentication, and non-repudiation) are also central to cryptography. Practical applications of cryptography include electronic commerce, chip-based payment cards, digital currencies, computer passwords, and military communications. Cryptography prior to the modern age was effectively synonymous with encryption, converting readable information (plaintext) to unintelligible nonsense text (ciphertext), which can only be read by reversing the process (decryption). The sender of an encrypted (coded) message shares the decryption (decoding) technique only with the intended recipients to preclude access from adversaries. The cryptography literature often uses the names "Alice" (or "A") for the sender, "Bob" (or "B") for the intended recipient, and "Eve" (or "E") for the eavesdropping adversary. Since the development of rotor cipher machines in World War I and the advent of computers in World War II, cryptography methods have become increasingly complex and their applications more varied. Modern cryptography is heavily based on mathematical theory and computer science practice; cryptographic algorithms are designed around computational hardness assumptions, making such algorithms hard to break in actual practice by any adversary. While it is theoretically possible to break into a well-designed system, it is infeasible in actual practice to do so. Such schemes, if well designed, are therefore termed "computationally secure". Theoretical advances (e.g., improvements in integer factorization algorithms) and faster computing technology require these designs to be continually reevaluated and, if necessary, adapted. Information-theoretically secure schemes that provably cannot be broken even with unlimited computing power, such as the one-time pad, are much more difficult to use in practice than the best theoretically breakable but computationally secure schemes. The growth of cryptographic technology has raised a number of legal issues in the Information Age. Cryptography's potential for use as a tool for espionage and sedition has led many governments to classify it as a weapon and to limit or even prohibit its use and export. In some jurisdictions where the use of cryptography is legal, laws permit investigators to compel the disclosure of encryption keys for documents relevant to an investigation. Cryptography also plays a major role in digital rights management and copyright infringement disputes with regard to digital media. Terminology diagram showing shift three alphabetic cypher D becomes A and E becomes B Alphabet shift ciphers are believed to have been used by Julius Caesar over 2,000 years ago. This is an example with k = 3. In other words, the letters in the alphabet are shifted three in one direction to encrypt and three in the other direction to decrypt. The first use of the term "cryptograph" (as opposed to "cryptogram") dates back to the 19th century—originating from "The Gold-Bug", a story by Edgar Allan Poe. Until modern times, cryptography referred almost exclusively to "encryption", which is the process of converting ordinary information (called plaintext) into an unintelligible form (called ciphertext). Decryption is the reverse, in other words, moving from the unintelligible ciphertext back to plaintext. A cipher (or cypher) is a pair of algorithms that carry out the encryption and the reversing decryption. The detailed operation of a cipher is controlled both by the algorithm and, in each instance, by a "key". The key is a secret (ideally known only to the communicants), usually a string of characters (ideally short so it can be remembered by the user), which is needed to decrypt the ciphertext. In formal mathematical terms, a "cryptosystem" is the ordered list of elements of finite possible plaintexts, finite possible cyphertexts, finite possible keys, and the encryption and decryption algorithms that correspond to each key. Keys are important both formally and in actual practice, as ciphers without variable keys can be trivially broken with only the knowledge of the cipher used and are therefore useless (or even counter-productive) for most purposes. Historically, ciphers were often used directly for encryption or decryption without additional procedures such as authentication or integrity checks. There are two main types of cryptosystems: symmetric and asymmetric. In symmetric systems, the only ones known until the 1970s, the same secret key encrypts and decrypts a message. Data manipulation in symmetric systems is significantly faster than in asymmetric systems. Asymmetric systems use a "public key" to encrypt a message and a related "private key" to decrypt it. The advantage of asymmetric systems is that the public key can be freely published, allowing parties to establish secure communication without having a shared secret key. In practice, asymmetric systems are used to first exchange a secret key, and then secure communication proceeds via a more efficient symmetric system using that key. Examples of asymmetric systems include Diffie–Hellman key exchange, RSA (Rivest–Shamir–Adleman), ECC (Elliptic Curve Cryptography), and Post-quantum cryptography. Secure symmetric algorithms include the commonly used AES (Advanced Encryption Standard) which replaced the older DES (Data Encryption Standard). Insecure symmetric algorithms include children's language tangling schemes such as Pig Latin or other cant, and all historical cryptographic schemes, however seriously intended, prior to the invention of the one-time pad early in the 20th century. In colloquial use, the term "code" is often used to mean any method of encryption or concealment of meaning. However, in cryptography, code has a more specific meaning: the replacement of a unit of plaintext (i.e., a meaningful word or phrase) with a code word (for example, "wallaby" replaces "attack at dawn"). A cypher, in contrast, is a scheme for changing or substituting an element below such a level (a letter, a syllable, or a pair of letters, etc.) to produce a cyphertext. Cryptanalysis is the term used for the study of methods for obtaining the meaning of encrypted information without access to the key normally required to do so; i.e., it is the study of how to "crack" encryption algorithms or their implementations. Some use the terms "cryptography" and "cryptology" interchangeably in English, while others (including US military practice generally) use "cryptography" to refer specifically to the use and practice of cryptographic techniques and "cryptology" to refer to the combined study of cryptography and cryptanalysis. English is more flexible than several other languages in which "cryptology" (done by cryptologists) is always used in the second sense above. RFC 2828 advises that steganography is sometimes included in cryptology. The study of characteristics of languages that have some application in cryptography or cryptology (e.g. frequency data, letter combinations, universal patterns, etc.) is called cryptolinguistics. Cryptolinguistics is especially used in military intelligence applications for deciphering foreign communications.

# """

import streamlit as st
import hashlib

def generate_primes(n):
    primes = []
    i = 2
    while len(primes) < n:
        if all(i % p != 0 for p in primes):
            primes.append(i)
        i += 1
    return primes

def derive_key(salt, length):
    hash_obj = hashlib.sha256(salt.encode())
    key = hash_obj.digest()
    while len(key) < length:
        hash_obj.update(key)
        key += hash_obj.digest()
    return list(key[:length])

def encrypt(phrase, salt):
    primes = generate_primes(len(phrase))
    key = derive_key(salt, len(phrase))
    
    encrypted = []
    cumul = 0

    for i, char in enumerate(phrase):
        p = primes[i]
        k = key[i]
        decalage = (ord(char) + p + k + cumul) % 256
        encrypted.append(decalage)
        cumul = (cumul + decalage) % 256 

    return encrypted

def decrypt(encrypted, salt):
    primes = generate_primes(len(encrypted))
    key = derive_key(salt, len(encrypted))

    decrypted = ''
    cumul = 0

    for i, val in enumerate(encrypted):
        p = primes[i]
        k = key[i]
        orig = (val - p - k - cumul) % 256
        decrypted += chr(orig)
        cumul = (cumul + val) % 256

    return decrypted


st.title("Outil de cryptage et décryptage par Raphael et Corentin")

mode = st.radio("Que veux-tu faire ?", ("Crypter", "Décrypter"))

salt = st.text_input("Entrez votre salt", value="AjvfklvjklbBFIEHZOI54564")

if mode == "Crypter":
    phrase = st.text_area("Entrez la phrase à crypter")
    
    if st.button("Crypter"):
        if phrase and salt:
            encrypted = encrypt(phrase, salt)
            st.success("Phrase cryptée avec succès !")
            st.code(encrypted)
        else:
            st.error("Merci d'entrer une phrase et un salt.")

elif mode == "Décrypter":
    encrypted_input = st.text_area("Entrez la liste de nombres cryptés (ex: 12, 34, 56)")
    
    if st.button("Décrypter"):
        if encrypted_input and salt:
            try:
                encrypted_list = [int(x.strip()) for x in encrypted_input.split(",")]
                decrypted = decrypt(encrypted_list, salt)
                st.success("Phrase décryptée avec succès !")
                st.code(decrypted)
            except Exception as e:
                st.error(f"Erreur dans le format de la liste : {e}")
        else:
            st.error("Merci d'entrer une liste de nombres cryptés et un salt.")

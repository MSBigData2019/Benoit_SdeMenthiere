# Written with <3 by Julien Romero

import hashlib
from sys import argv
import sys
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode


class Crack:
    """Crack The general method used to crack the passwords"""

    def __init__(self, filename, name):
        """__init__
        Initialize the cracking session
        :param filename: The file with the encrypted passwords
        :param name: Your name
        :return: Nothing
        """
        self.name = name.lower()
        self.passwords = get_passwords(filename)

    def check_password(self, password):
        """check_password
        Checks if the password is correct
        !! This method should not be modified !!
        :param password: A string representing the password
        :return: Whether the password is correct or not
        """
        password = str(password)
        cond = False
        if (sys.version_info > (3, 0)):
            cond = hashlib.md5(bytes(password, "utf-8")).hexdigest() in \
                self.passwords
        else:
            cond = hashlib.md5(bytearray(password)).hexdigest() in \
                self.passwords
        if cond:
            args = {"name": self.name,
                    "password": password}
            args = urlencode(args, "utf-8")
            page = urlopen('http://137.194.211.71:5000/' +
                                          'submit?' + args)
            if b'True' in page.read():
                print("You found the password: " + password)
                return True
        return False

    def evaluate(self):
        """evaluate
        Retrieve the grade from the server,
        !! This method MUST not be modified !!
        """
        args = {"name": self.name }
        args = urlencode(args, "utf-8")
        page = urlopen('http://137.194.211.71:5000/' +
                                          'evaluate?' + args)
        print("Grade :=>> " + page.read().decode('ascii').strip())

    def crack(self):
        """crack
        Cracks the passwords. YOUR CODE GOES BELOW.

        We suggest you use one function per question. Once a password is found,
        it is memorized by the server, thus you can comment the call to the
        corresponding function once you find all the corresponding passwords.
        """
        self.bruteforce_digits()
        self.bruteforce_letters()
        self.dictionnary_passwords()
        self.dictionnary_passwords_and_digits()
        self.dictionnary_nouns_cat()
        self.dictionnary_nouns_diceware()
        self.dictionnary_words()
        self.dictionnary_words_leet()
        self.social_google()
        self.social_jdoe()

    def bruteforce_digits(self):
        pass

    def bruteforce_letters(self):
        pass

    def dictionnary_passwords(self):
        pass

    def dictionnary_passwords_and_digits(self):
        pass

    def dictionnary_nouns_cat(self):
        pass

    def dictionnary_nouns_diceware(self):
        pass

    def dictionnary_words(self):
        pass

    def dictionnary_words_leet(self):
        pass

    def social_google(self):
        pass

    def social_jdoe(self):
        pass


def get_passwords(filename):
    """get_passwords
    Get the passwords from a file
    :param filename: The name of the file which stores the passwords
    :return: The set of passwords
    """
    passwords = set()
    with open(filename, "r") as f:
        for line in f:
            passwords.add(line.strip())
    return passwords


if __name__ == "__main__":
    name = "Sarrauste".lower()
    # This is the correct location on the moodle
    encfile = "../passwords/" + name + ".enc"

    # If you run the script on your computer: uncomment and fill the following
    # line. Do not forget to comment this line again when you submit your code
    # on the moodle.
    # encfile = "PATH TO YOUR ENC FILE"

    # First argument is the password file, the second your name
    crack = Crack(encfile, name)
    crack.crack()
    if "--eval" in sys.argv: crack.evaluate()

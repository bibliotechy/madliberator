#!/usr/bin/env python3

filename = __file__

import argparse
from jinja2 import Environment,BaseLoader

from madliberator.madliberator import Mabliberator


parser = argparse.ArgumentParser()
parser.add_argument(
    '--infile', 
    nargs="?", 
    type=argparse.FileType('rb'),
)

parser.add_argument(
    '--stop-words',
    nargs='?',
    type=argparse.FileType('rb'),
    default=None
)

args = parser.parse_args()


if __name__ == "__main__":
    stop_words = []
    if args.stop_words is not None:
        stop_words += args.stop_words.read().decode('utf-8').splitlines()

    text = args.infile.read()
    lines = text.decode("utf-8").splitlines()
    liberated_lines = [
        Mabliberator(line,noun_pct=.25, verb_pct=.25,      addl_stop_words=stop_words).madliberate() for line in lines
    ]


    env = Environment(loader=BaseLoader,trim_blocks=True, lstrip_blocks=True)
    print(""" 
<html>
    <head>
        <style>
            body {
            font-size: 1.2rem;
            }

            input[type="text"] {
            border-top: transparent;
            border-left: transparent;
            border-right: transparent;
            margin-left: 1.1rem;
            margin-right: 1.1rem;
            width: 101px;
            margin-left: .5rem;
            margin-right: .5rem;
            text-align: center;
            outline-width: 0;
            }

            input:focus {
            outline: none;

            }

            input::placeholder {
            text-align: center;
            }
            input:focus::placeholder {
            color: transparent;
            }

            p {
            line-height: 1.5rem;
            }

            @media (min-width: 600px) {
            div {
                width: 80%;
                margin: 0 auto;
            }
            }
        </style>
    <head>
    <body>
        <div class="main-wrapper">
          <p>
    """)
    for i,line in enumerate(liberated_lines):
        
        print(env.from_string(line).render(
            VERB="<input type='text' placeholder='Verb' class='verb'>", 
            NOUN="<input type='text' placeholder='Noun' class='noun'>",
            ADJ="<input type='text' placeholder='Adjective' class='adj'>",
            ADV="<input type='text' placeholder='Adverb' class='adv'>", 
            PLURAL_NOUN="<input type='text' placeholder='Plural Noun' class='plural-noun'>"
        ))
        print("</p><p>")
    print(
        """
                </p>
            </div>
        </body>
        </html>
        """)

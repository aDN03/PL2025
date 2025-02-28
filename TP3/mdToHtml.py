import re
import sys 

def mdToHTML(md):

    # Headers

    md = re.sub(r'###\s+(.*)', r'<h3>\1</h3>', md)
    md = re.sub(r'##\s+(.*)', r'<h2>\1</h2>', md)
    md = re.sub(r'#\s+(.*)', r'<h1>\1</h1>', md)

    # Bold

    md = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', md)

    # Italic

    md = re.sub(r'\*(.*?)\*', r'<i>\1</i>', md)

    # List

    md = re.sub(r'(\d+\.\s+.*\n?)+', r'<ol>\g<0></ol>', md)
    md = re.sub(r'\d+\.\s+(.*)', r'<li>\1</li>\n', md)

    # Image

    md = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', md)

    # Link

    md = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', md)

    return md

def main():
    md = sys.stdin.read()
    html = mdToHTML(md)
    with open('output.html', 'w') as file:
        file.write(html)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup
import argparse

# Parse input arguments
parser = argparse.ArgumentParser(description='obp-image-manipulation')
parser.add_argument('input_file',
                    help = 'Input file to process')
parser.add_argument('output_file',
                    help = 'Output file')

args = parser.parse_args()

css = '''figure {
             display: table;
             width: 100%;
         }
         p.caption-centered {
             display: table-caption;
             caption-side: bottom;
         }
      '''

caption_classes = {'class' : ['caption-left-aligned',
                              'caption-centered',
                              'caption-right-aligned']}

def run():
    input_filename = os.path.join(os.path.dirname(__file__),
                                  args.input_file)
    output_filename = os.path.join(os.path.dirname(__file__),
                                   args.output_file)

    with open(input_filename, 'r') as f:
        # Create the soup object
        soup = BeautifulSoup(f, features='html.parser') 

        # Create a <stile> tag and append it in <head>
        style = soup.new_tag('style')
        style.append(css)
        head = soup.find('head')
        head.append(style)

        for image_group in get_image_groups(soup):
            caption, images = image_group
            manipulate(soup, caption, images)

        write_output(soup, output_filename)
        
def get_image_groups(soup):
        # Harvast all the captions
        captions = [x for x in soup.find_all('p', caption_classes)]

        for caption in captions:
            relevant_siblings = []
            for sibling in caption.previous_siblings:
                if sibling.name is None:
                    continue
                if sibling.name != "div":
                    break
                if sibling['class'][0] != "_idGenObjectLayout-2":
                    raise ValueError("WRONG CLASS")
                relevant_siblings.append(sibling)

            yield (caption, relevant_siblings)

def manipulate(soup, caption, images):
        # Create the <figure> tag
        figure = soup.new_tag('figure')
        
        for image in images:
                # Store the id of the first child div element for later use
                div = image.find('div')
                img_id = div['id']
                
                # Extract the <img> tag and insert the img_id attribute
                img = image.find('img')
                img['id'] = img_id
                del img['class']
                img['alt'] = caption.text
                img['title'] = caption.text

                # Place the <img> element inside <figure>
                figure.append(img)

                # Get rid of the old <div> which contained the image
                image.decompose()

        # Change the class of the caption
        # and then wrap it around the new <figure>
        caption['class'] = 'caption-centered'
        caption.wrap(figure)
        
def write_output(soup, output_filename):
        with open(output_filename, 'wb') as output:
            raw_soup = soup.encode('utf-16')
            output.write(raw_soup)

if __name__ == '__main__':
    run()

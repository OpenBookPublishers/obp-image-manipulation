#!/usr/bin/env python3
import os
from bs4 import BeautifulSoup

css = '''
          figure {
              display: table;
              border:3px dotted red;
              float:right;
              padding: 1.5em 0 1.5em 1.5em;
          }
          p.caption-centered {
              display: table-caption;
              caption-side: bottom;
              border:3px dotted red;
          }
          /*img {display: block !important}*/
        '''

caption_classes = {'class' : ['caption-left-aligned',
                              'caption-centered',
                              'caption-right-aligned']}

def run():
    input_filename = os.path.join(os.path.dirname(__file__),
                                  'ch1.xhtml')
    output_filename = os.path.join(os.path.dirname(__file__),
                                   'output.html')

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

                # Place the <img> element inside <figure>
                figure.append(img)

                # Get rid of the whole <div> contained in image
                image.decompose()

        # Change the class of the caption
        # and then wrap it around the new <figure>
        caption['class'] = 'caption-centered'
        caption.wrap(figure)
        
def write_output(soup, output_filename):
        output = open(output_filename, 'w')
        output.write(soup.prettify())

if __name__ == '__main__':
    run()

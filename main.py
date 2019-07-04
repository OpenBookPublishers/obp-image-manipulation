#!/usr/bin/env python3

import os

from bs4 import BeautifulSoup, Tag

css = '''
          figure {
              display: table;
              border:3px dotted red;
              /*float:right;*/
          }
          p.caption {
              display: table-caption;
              caption-side: bottom;
              border:3px dotted red;
          }
        '''

caption_classes = {'class' : ['caption-left-aligned',
                              'caption-centered', 
                              'caption-right-aligned']}


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
            print(caption, images)


def write_output():
    pass
    #    output = open(output_filename, 'w')
    #    output.write(soup.prettify())

def manipulate():        
        # Rename the parent div figure and delete attributes
        image.name = 'figure'
        del image['id']
        del image['class']
        
        # Store the id of the first child div element for later use 
        div = image.find('div')
        img_id = div['id']
        
        # Extract the <img> tag and insert the img_id attribute    
        img = image.find('img')
        img['id'] = img_id
        del img['class']
        
        # Delete the uncessesary tags and place the <img> element
        image.clear()
        image.append(img)


if __name__ == '__main__':
    run()


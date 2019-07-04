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

input_filename = os.path.join(os.path.dirname(__file__),
                              'ch1.xhtml')

with open(input_filename, 'r') as file:
    
    # Create the soup object    
    soup = BeautifulSoup(file, features='html.parser')
    
    # Create a <stile> tag and append it in <head>
    style = soup.new_tag('style')
    style.append(css)
    head = soup.find('head')
    head.append(style)

    # Harvast all the captions
    captions = [x for x in soup.find_all('p', {'class' : ['caption-left-aligned',
                                                          'caption-centered',
                                                          'caption-right-aligned']})]
    
    for n, image in enumerate(soup.find_all('div', {'class' : '_idGenObjectLayout-2'})):
        
        #~ print('')
        #~ print(image)
        #~ print(captions[n-1])
        #~ print('')
        
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
        
        # Append the caption (stored at n-1)
        image.append(captions[n-1])
        
        print('')
        print(image)
        #~ print(captions[n-1])
        print('')
        
    output = open('/home/luca/rudy/OEBPS/output.html', 'w')
    output.write(soup.prettify())

        
        
        
        
                    

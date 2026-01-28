#coding:utf-8
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase, as_text
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import splitname, getnames
import datetime
from bs4 import BeautifulSoup 
import re

from pylatexenc.latex2text import LatexNodes2Text

# load bib file 
parser = BibTexParser(ignore_nonstandard_types = False)
github_href_root = 'https://raw.githubusercontent.com/toyamaailab/toyamaailab.github.io/main/resource/'
test_bib_path = './config/AI_SCIPapers_SCI.bib'
test_bib_file = open(test_bib_path, 'r')

bib_database = bibtexparser.load(test_bib_file, parser)

journal_list = [x for x in bib_database.entries if x['ENTRYTYPE'] == 'article']
conference_list = [x for x in bib_database.entries if x['ENTRYTYPE'] == 'inproceedings']
inpress_list = [x for x in bib_database.entries if x['ENTRYTYPE'] == 'inpress']

# read demo html file 
publications_demo_html = BeautifulSoup(open('./config/publications_demo.html', 'r'), from_encoding='utf-8')
highlights_demo_html = BeautifulSoup(open('./config/highlights_demo.html', 'r'), from_encoding='utf-8')
data_demo_html = BeautifulSoup(open('./config/sourcedata_demo.html', 'r'), from_encoding='utf-8')

index_html = BeautifulSoup(open('index.html', 'r'), from_encoding='utf-8')
#index_html = BeautifulSoup(open('index.html', 'r', encoding='utf-8'), 'html.parser')


# update date to html
publication_date = publications_demo_html.find(id="update_date")
publication_date.string = 'Update: ' + str(datetime.date.today())

data_date = data_demo_html.find(id="update_date")
data_date.string = 'Update: ' + str(datetime.date.today())

highlights_date = highlights_demo_html.find(id="update_date")
highlights_date.string = 'Update: ' + str(datetime.date.today())


index_date = index_html.find(id="update_date")
index_date.string = 'Update: ' + str(datetime.date.today())
print(index_html)
with open("index.html", "w", encoding='utf-8') as file:
    file.write(str(index_html))


# utils functions

journal_list = sorted(journal_list, key=lambda x: datetime.datetime.strptime('{} {}'.format(x['month'], x['year']), '%B %Y'))[::-1]

def generate_person(bib_person, demo_html):
    person_string_list = []
    author_list = bib_person.split(' and ')
    
    author_tag = demo_html.new_tag('span', attrs={'class': 'author'})
    
    author_num = len(author_list)
    
    for author_index, x in enumerate(author_list):
        single_name = splitname(x)
        
        name_string = ''
        
        if single_name['first'] != []:
            name_string += single_name['first'][0] + ' '
        if single_name['von'] != []:
            name_string += single_name['von'][0] + ' '
        if single_name['last'] != []:
            name_string += single_name['last'][0]
        
        # print(LatexNodes2Text().latex_to_text(name_string))
        name_string = LatexNodes2Text().latex_to_text(name_string)
        
        # if author_index != author_num - 2:
        #     connect_symbol = ','
        # else:
        #     connect_symbol = ''
        
        if 'Shangce Gao' in name_string or 'S Gao' in name_string:
            bold_tag = demo_html.new_tag('b')
            bold_tag.append(name_string + ',')
            author_tag.append(bold_tag)
        else:
            text_tag = demo_html.new_tag('span')
            text_tag.append(name_string + ',')
            author_tag.append(text_tag)
        
        if author_index == author_num - 2:
            author_tag.append('and')
        
        # if author_index == author_num - 2:
        #     author_tag.append(', and')
        # if author_index < author_num - 2:
        #     author_tag.append(',')
        
        person_string_list.append(LatexNodes2Text().latex_to_text(name_string))
    if len(person_string_list) == 1:
        person_string = person_string_list[0]
    else:
        person_string = ', '.join(person_string_list[:-1])
        person_string += ', and ' + person_string_list[-1]
    
    return author_tag

def generate_title(bib_title, demo_html):
    title_tag = publications_demo_html.new_tag('span', attrs={'class': 'title'})
    title_tag.append('"{},"'.format(LatexNodes2Text().latex_to_text(bib_title)))
    return title_tag

def generate_journal(bib_journal, demo_html):
    journal_tag = demo_html.new_tag('span', attrs={'class': 'journal'})
    journal_tag.append(LatexNodes2Text().latex_to_text(bib_journal) + ',')
    return journal_tag
    
def generate_conference(bib_booktitle, demo_html):
    conference_tag = demo_html.new_tag('span', attrs={'class': 'conference'})
    conference_tag.append(LatexNodes2Text().latex_to_text(bib_booktitle) + ',')
    return conference_tag

def generate_vol_no_page(bib, demo_html):
    vol_tag = demo_html.new_tag('span', attrs={'class': 'vol'})
    return_string = ''
    data_list = []
    if 'volume' in bib:
        data_list.append('vol.' + bib['volume'])
        vol_tag.append('vol. ' + bib['volume'] + ',')
    if 'number' in bib:
        data_list.append('no.' + bib['number'])
        vol_tag.append('no. ' + bib['number'] + ',')
    if 'pages' in bib:
        data_list.append('pp.' + bib['pages'].replace('--', '-'))
        vol_tag.append('pp. ' + bib['pages'].replace('--', '-') + ',')
        # return_string += ', pp.' + bib['pages']
    return vol_tag

def generate_date(bib, demo_html):
    date_tag = demo_html.new_tag('span', attrs={'class': 'date'})
    date_string = ''
    if 'month' in bib:
        date_string += bib['month']
    if 'year' in bib:
        date_string += ' ' + bib['year']
    date_tag.append(date_string + '.')
    return date_tag

def generate_note(bib, demo_html):
    note_tag = demo_html.new_tag('span', attrs={'class': 'note'})
    if 'note' in bib:
        note_tag.append(' {} '.format(bib['note']))
    return note_tag
    
def is_highlight(bib, demo_html):
    if 'highlight' in bib:
        if bib['highlight'].casefold() == 'true'.casefold():
            return True
    return False
  
def generate_doi_pdf(bib, demo_html):
    doi_pdf_tag = demo_html.new_tag('span', attrs={'class': 'doi'})
    return_string = ''
    if 'doi' in bib:
        return_string += 'DOI: ' + bib['doi']
        if 'url' in bib:
            doi_pdf_tag.append('DOI: ' + bib['doi'] + ',')
        else:
            doi_pdf_tag.append('DOI: ' + bib['doi'] + '.')
    
    other_resource = False
    
    if 'url' in bib:
        return_string += '[PDF]'
        other_resource = True
        
        pdf_tag = demo_html.new_tag('a', attrs={'href': bib['url'], 'target': '_blank'})
        pdf_tag.string = '[PDF].'
        doi_pdf_tag.append(pdf_tag)
    
    
    return doi_pdf_tag

def generate_other_resource(bib, demo_html):
    resource_tag = demo_html.new_tag('span', attrs={'class': 'resource'})
    return_string = ''
    other_resource = False
    
    if 'resource' in bib:
        return_string += ', [Experimental Results DATA]'
        other_resource = True
        # resource_tag.append(', ')
        data_tag = demo_html.new_tag('a', attrs={'href': github_href_root + bib['resource'], 'target': '_blank'})
        data_tag.string = '[Experimental Results DATA]'
        resource_tag.append(data_tag)
    if 'code' in bib:
        return_string += ', [Code]'
        other_resource = True
        # resource_tag.append(', ')
        if re.match(r'^https?:/{2}\w.+$', bib['code']):
            code_tag = demo_html.new_tag('a', attrs={'href': bib['code'], 'class': 'code', 'target': '_blank'})
        else:
            code_tag =  demo_html.new_tag('a', attrs={'href': github_href_root + bib['code'], 'class': 'code', 'target': '_blank'})
        code_tag.string = '[Code]'
        resource_tag.append(code_tag)
    if 'resourcebaidu' in bib:
        other_resource = True
        # resource_tag.append(', ')
        data_baidu_tag = demo_html.new_tag('a', attrs={'href': bib['resourcebaidu'], 'target': '_blank'})
        data_baidu_tag.string = '[Experimental Results DATA in Baidu Cloud]'
        resource_tag.append(data_baidu_tag)
    if 'codebaidu' in bib:
        other_resource = True
        # resource_tag.append(', ')
        code_baidu_tag = demo_html.new_tag('a', attrs={'href': bib['codebaidu'], 'class': 'code', 'target': '_blank'})
        code_baidu_tag.string = '[Code in Baidu Cloud]'
        resource_tag.append(code_baidu_tag)
    if 'extraction' in bib:
        other_resource = True
        # resource_tag.append(', ')
        ext_tag = demo_html.new_tag('span')
        ext_tag.string = 'Ext Code: ' + bib['extraction']
        resource_tag.append(ext_tag)
    if not other_resource:
        return False
    
    
    return resource_tag

# write conference paper to publications html
pub_conference_node = publications_demo_html.find(id="pub_conference")
for x in conference_list:
    print(x['ID'])
    list_tag = publications_demo_html.new_tag('li')
    author = generate_person(x['author'], publications_demo_html)
    title = generate_title(x['title'], publications_demo_html)
    conference = generate_journal(x['booktitle'], publications_demo_html)
    vol_no_pages = generate_vol_no_page(x, publications_demo_html)
    date = generate_date(x, publications_demo_html)
    note = generate_note(x, publications_demo_html)
    doi_pdf = generate_doi_pdf(x, publications_demo_html)
    list_tag.append(author)
    list_tag.append(title)
    list_tag.append(' in ')
    list_tag.append(conference)
    # list_tag.append(', ')
    list_tag.append(vol_no_pages)
    # list_tag.append(', ')
    list_tag.append(date)
    # list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    
    pub_conference_node.append(list_tag)
    br_tag = publications_demo_html.new_tag('br')
    pub_conference_node.append(br_tag)

# write press paper to publications html
pub_journal_node = publications_demo_html.find(id="pub_journal") 
pub_journal_node['start'] = str(len(journal_list + conference_list)) 
for x in journal_list:
    print(x['ID'])
    list_tag = publications_demo_html.new_tag('li')
    author = generate_person(x['author'], publications_demo_html)
    title = generate_title(x['title'], publications_demo_html)
    journal = generate_journal(x['journal'], publications_demo_html)
    vol_no_pages = generate_vol_no_page(x, publications_demo_html)
    date = generate_date(x, publications_demo_html)
    note = generate_note(x, publications_demo_html)
    doi_pdf = generate_doi_pdf(x, publications_demo_html)
    list_tag.append(author)
    # list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    # list_tag.append(', ')
    list_tag.append(vol_no_pages)
    # list_tag.append(', ')
    list_tag.append(date)
    # list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    
    pub_journal_node.append(list_tag)
    br_tag = publications_demo_html.new_tag('br')
    pub_journal_node.append(br_tag)

# write inpress paper to publications html
inpress_node = publications_demo_html.find(id="inpress")
inpress_node['start'] = str(len(journal_list + inpress_list + conference_list)) 
for x in inpress_list:
    print(x['ID'])
    list_tag = publications_demo_html.new_tag('li')
    author = generate_person(x['author'], publications_demo_html)
    title = generate_title(x['title'], publications_demo_html)
    journal = generate_journal(x['journal'], publications_demo_html)
    vol_no_pages = generate_vol_no_page(x, publications_demo_html)
    date = generate_date(x, publications_demo_html)
    note = generate_note(x, publications_demo_html)
    doi_pdf = generate_doi_pdf(x, publications_demo_html)
    list_tag.append(author)
    # list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    # list_tag.append(', ')
    # list_tag.append(vol_no_pages)
    # list_tag.append(', ')
    list_tag.append(date)
    # list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    
    inpress_node.append(list_tag)
    br_tag = publications_demo_html.new_tag('br')
    inpress_node.append(br_tag)



# generate publication html
with open("publications.html", "w", encoding='utf-8') as file:
    file.write(str(publications_demo_html))

# write the paper with data to sourcedata html
data_node = data_demo_html.find(id="data")
for x in inpress_list + journal_list:
    print(x['ID'])
    list_tag = data_demo_html.new_tag('li')
    author = generate_person(x['author'], data_demo_html)
    title = generate_title(x['title'], data_demo_html)
    journal = generate_journal(x['journal'], data_demo_html)
    vol_no_pages = generate_vol_no_page(x, data_demo_html)
    date = generate_date(x, data_demo_html)
    doi_pdf = generate_doi_pdf(x, data_demo_html)
    other_resource = generate_other_resource(x, data_demo_html)
    if not other_resource:
        continue
    
    list_tag.append(author)
    # list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    # list_tag.append(', ')
    if x['ENTRYTYPE'] != 'inpress':
        list_tag.append(vol_no_pages)
        # list_tag.append(', ')
    list_tag.append(date)
    # list_tag.append('. ')
    list_tag.append(doi_pdf)
    list_tag.append(other_resource)
    
    data_node.append(list_tag)
    br_tag = data_demo_html.new_tag('br')
    data_node.append(br_tag)
    
# generate sourcedata html
with open("sourcedata.html", "w", encoding='utf-8') as file:
    file.write(str(data_demo_html))
    
# write conference paper to highlight html
pub_conference_node = highlights_demo_html.find(id="pub_conference")
for x in conference_list:
    print(x['ID'])
    list_tag = highlights_demo_html.new_tag('li')
    author = generate_person(x['author'], highlights_demo_html)
    title = generate_title(x['title'], highlights_demo_html)
    conference = generate_journal(x['booktitle'], highlights_demo_html)
    vol_no_pages = generate_vol_no_page(x, highlights_demo_html)
    date = generate_date(x, highlights_demo_html)
    note = generate_note(x, highlights_demo_html)
    doi_pdf = generate_doi_pdf(x, highlights_demo_html)
    list_tag.append(author)
    list_tag.append(title)
    list_tag.append(' in ')
    list_tag.append(conference)
    # list_tag.append(', ')
    list_tag.append(vol_no_pages)
    # list_tag.append(', ')
    list_tag.append(date)
    # list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    
    pub_conference_node.append(list_tag)
    br_tag = highlights_demo_html.new_tag('br')
    pub_conference_node.append(br_tag)

# write journal paper to highlight html
pub_journal_node = highlights_demo_html.find(id="pub_journal") 
highlight_num = len(conference_list)
for x in inpress_list + journal_list:
    print(x['ID'])
    list_tag = highlights_demo_html.new_tag('li')
    author = generate_person(x['author'], highlights_demo_html)
    title = generate_title(x['title'], highlights_demo_html)
    journal = generate_journal(x['journal'], highlights_demo_html)
    vol_no_pages = generate_vol_no_page(x, highlights_demo_html)
    date = generate_date(x, highlights_demo_html)
    note = generate_note(x, highlights_demo_html)
    doi_pdf = generate_doi_pdf(x, highlights_demo_html)
    list_tag.append(author)
    # list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    # list_tag.append(', ')
    list_tag.append(vol_no_pages)
    # list_tag.append(', ')
    list_tag.append(date)
    # list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    if not is_highlight(x, highlights_demo_html):  
        continue
    else:
        highlight_num += 1
    
    pub_journal_node.append(list_tag)
    br_tag = highlights_demo_html.new_tag('br')
    pub_journal_node.append(br_tag)
pub_journal_node['start'] = str(highlight_num) 

'''
# write the highlight journal to highlights html
highlight_node =  highlights_demo_html.find(id="pub_journal")
for x in inpress_list + journal_list:
    print(x['ID'])
    list_tag = highlights_demo_html.new_tag('li')
    author = generate_person(x['author'], highlights_demo_html)
    title = generate_title(x['title'], highlights_demo_html)
    journal = generate_journal(x['journal'], highlights_demo_html)
    vol_no_pages = generate_vol_no_page(x, highlights_demo_html)
    date = generate_date(x, highlights_demo_html)
    note = generate_note(x, highlights_demo_html)
    doi_pdf = generate_doi_pdf(x, highlights_demo_html)
    if not is_highlight(x, highlights_demo_html):  
        continue    

    list_tag.append(author)
    # list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    # list_tag.append(', ')
    list_tag.append(vol_no_pages)
    # list_tag.append(', ')
    list_tag.append(date)
    # list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    
    highlight_node.append(list_tag)
    br_tag = highlights_demo_html.new_tag('br')
    highlight_node.append(br_tag)
'''
# generate highlights html
with open("highlights.html", "w", encoding='utf-8') as file:
    file.write(str(highlights_demo_html))
    
    
# soup = BeautifulSoup(open('../publications.html', 'r'))
# inpress_node = soup.find(id="inpress")
# append_tag = soup.new_tag('li')
# append_tag.append('<b>abc</b>')
# inpress_node.append(append_tag)
# print(press_node)

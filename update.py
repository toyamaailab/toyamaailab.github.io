import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase, as_text
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import splitname, getnames
import datetime
from bs4 import BeautifulSoup 

from pylatexenc.latex2text import LatexNodes2Text

parser = BibTexParser(ignore_nonstandard_types = False)
github_href_root = 'https://raw.githubusercontent.com/toyamaailab/toyamaailab.github.io/main/resource/'
test_bib_path = './config/AI_SCIPapers_SCI.bib'
test_bib_file = open(test_bib_path, 'r')

bib_database = bibtexparser.load(test_bib_file, parser)

press_list = [x for x in bib_database.entries if x['ENTRYTYPE'] != 'inpress' ]
inpress_list = [x for x in bib_database.entries if x['ENTRYTYPE'] == 'inpress']

publications_demo_html = BeautifulSoup(open('./config/publications_demo.html', 'r'))
data_demo_html = BeautifulSoup(open('./config/sourcedata_demo.html', 'r'))
index_html = BeautifulSoup(open('index.html', 'r'))

publication_date = publications_demo_html.find(id="update_date")
publication_date.string = 'Update: ' + str(datetime.date.today())

data_date = data_demo_html.find(id="update_date")
data_date.string = 'Update: ' + str(datetime.date.today())

index_date = index_html.find(id="update_date")
index_date.string = 'Update: ' + str(datetime.date.today())
with open("index.html", "w") as file:
    file.write(str(index_html))


press_list = sorted(press_list, key=lambda x: datetime.datetime.strptime('{} {}'.format(x['month'], x['year']), '%B %Y'))[::-1]

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
        if 'Shangce Gao' in name_string or 'S Gao' in name_string:
            bold_tag = demo_html.new_tag('b')
            bold_tag.append(name_string)
            author_tag.append(bold_tag)
        else:
            author_tag.append(name_string)
        
        if author_index == author_num - 2:
            author_tag.append(', and ')
        if author_index < author_num - 2:
            author_tag.append(', ')
        
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
    journal_tag.append(LatexNodes2Text().latex_to_text(bib_journal))
    return journal_tag

def generate_vol_no_page(bib, demo_html):
    vol_tag = demo_html.new_tag('span', attrs={'class': 'vol'})
    return_string = ''
    data_list = []
    if 'volume' in bib:
        data_list.append('vol.' + bib['volume'])
        vol_tag.append('vol.' + bib['volume'])
        # return_string += 'vol.' + bib['volume']
    if 'number' in bib:
        data_list.append('no.' + bib['number'])
        vol_tag.append(', no.' + bib['number'])
        # return_string += ', no.' + bib['number']
    if 'pages' in bib:
        data_list.append('pp.' + bib['pages'].replace('--', '-'))
        vol_tag.append(', pp.' + bib['pages'].replace('--', '-'))
        # return_string += ', pp.' + bib['pages']
    return vol_tag

def generate_date(bib, demo_html):
    date_tag = demo_html.new_tag('span', attrs={'class': 'date'})
    date_string = ''
    if 'month' in bib:
        date_string += bib['month']
    if 'year' in bib:
        date_string += ' ' + bib['year']
    date_tag.append(date_string)
    return date_tag

def generate_note(bib, demo_html):
    note_tag = demo_html.new_tag('span', attrs={'class': 'note'})
    if 'note' in bib:
        note_tag.append(' {} '.format(bib['note']))
    return note_tag
  
def generate_doi_pdf(bib, demo_html):
    doi_pdf_tag = demo_html.new_tag('span', attrs={'class': 'doi'})
    return_string = ''
    if 'doi' in bib:
        return_string += 'DOI: ' + bib['doi']
        doi_pdf_tag.append('DOI: ' + bib['doi'])
    
    other_resource = False
    
    if 'url' in bib:
        return_string += ', [PDF]'
        other_resource = True
        doi_pdf_tag.append(', ')
        pdf_tag = demo_html.new_tag('a', attrs={'href': bib['url'], 'target': '_blank'})
        pdf_tag.string = '[PDF]'
        doi_pdf_tag.append(pdf_tag)
   
    if not other_resource:
        return_string += '.'
        # resource_tag.append('.')
    
    
    return doi_pdf_tag

def generate_other_resource(bib, demo_html):
    resource_tag = demo_html.new_tag('span', attrs={'class': 'resource'})
    return_string = ''
    other_resource = False
    
    if 'resource' in bib:
        return_string += ', [Experimental Results DATA]'
        other_resource = True
        resource_tag.append(', ')
        data_tag = demo_html.new_tag('a', attrs={'href': github_href_root + bib['resource'], 'target': '_blank'})
        data_tag.string = '[Experimental Results DATA]'
        resource_tag.append(data_tag)
    if 'code' in bib:
        return_string += ', [Code]'
        other_resource = True
        resource_tag.append(', ')
        code_tag =  demo_html.new_tag('a', attrs={'href': github_href_root + bib['code'], 'class': 'code', 'target': '_blank'})
        code_tag.string = '[Code]'
        resource_tag.append(code_tag)
    if 'resourcebaidu' in bib:
        other_resource = True
        resource_tag.append(', ')
        data_baidu_tag = demo_html.new_tag('a', attrs={'href': bib['resourcebaidu'], 'target': '_blank'})
        data_baidu_tag.string = '[Experimental Results DATA in Baidu Cloud]'
        resource_tag.append(data_baidu_tag)
    if 'codebaidu' in bib:
        other_resource = True
        resource_tag.append(', ')
        code_baidu_tag = demo_html.new_tag('a', attrs={'href': bib['codebaidu'], 'class': 'code', 'target': '_blank'})
        code_baidu_tag.string = '[Code in Baidu Cloud]'
        resource_tag.append(code_baidu_tag)
    if 'extraction' in bib:
        other_resource = True
        resource_tag.append(', ')
        ext_tag = demo_html.new_tag('span')
        ext_tag.string = 'Ext Code: ' + bib['extraction']
        resource_tag.append(ext_tag)
    if not other_resource:
        return False
    
    
    return resource_tag


inpress_node = publications_demo_html.find(id="inpress") 
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
    list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    list_tag.append(', ')
    # list_tag.append(vol_no_pages)
    # list_tag.append(', ')
    list_tag.append(date)
    list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    
    inpress_node.append(list_tag)
    br_tag = publications_demo_html.new_tag('br')
    inpress_node.append(br_tag)

    
press_node = publications_demo_html.find(id="published") 
for x in press_list:
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
    list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    list_tag.append(', ')
    list_tag.append(vol_no_pages)
    list_tag.append(', ')
    list_tag.append(date)
    list_tag.append('. ')
    list_tag.append(note)
    list_tag.append(doi_pdf)
    
    press_node.append(list_tag)
    br_tag = publications_demo_html.new_tag('br')
    press_node.append(br_tag)

with open("publications.html", "w") as file:
    file.write(str(publications_demo_html))


data_node = data_demo_html.find(id="data")
for x in inpress_list + press_list:
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
    list_tag.append(', ')
    list_tag.append(title)
    list_tag.append(' ')
    list_tag.append(journal)
    list_tag.append(', ')
    if x['ENTRYTYPE'] != 'inpress':
        list_tag.append(vol_no_pages)
        list_tag.append(', ')
    list_tag.append(date)
    list_tag.append('. ')
    list_tag.append(doi_pdf)
    list_tag.append(other_resource)
    
    data_node.append(list_tag)
    br_tag = data_demo_html.new_tag('br')
    data_node.append(br_tag)
with open("sourcedata.html", "w") as file:
    file.write(str(data_demo_html))
    
# soup = BeautifulSoup(open('../publications.html', 'r'))
# inpress_node = soup.find(id="inpress")
# append_tag = soup.new_tag('li')
# append_tag.append('<b>abc</b>')
# inpress_node.append(append_tag)
# print(press_node)
